"""Separate editorial acceptance, bound to evidence, report and finding disposition."""
from __future__ import annotations
import json
from pathlib import Path
from bs4 import BeautifulSoup
from flwu import history as h
from flwu.evidence_binding import AcquisitionIndex
from flwu.research import validate_person_identity
from flwu import publication_pending


def report_row(conn, capture_id):
    row = conn.execute('SELECT c.*,s.mode FROM captures c JOIN streams s USING(stream) WHERE capture_id=?', (capture_id,)).fetchone()
    if row is None or row['mode'] != 'manual_research':
        raise ValueError('Publication acceptance requires a live report capture')
    return row


def requirements(conn, row):
    expected = {}
    for capture in conn.execute('SELECT seq,payload FROM captures WHERE stream=? AND seq<=? ORDER BY seq', (row['stream'], row['seq'])):
        payload = json.loads(capture['payload'])
        review = payload.get('opinion_review')
        if review:
            key = 'opinion:'+review['id']
            if review['relevance'] == 'relevant':
                expected[key] = {'version':review['receipt_sha256'], 'summary':review['summary'],
                                 'sha256':review['pdf_sha256'], 'capture_seq':capture['seq']}
            else:
                expected.pop(key, None)
        source = payload.get('source_gate_review')
        if source and source.get('acceptance_version') == 3:
            for finding in payload.get('findings', []):
                expected['source:'+finding['key']] = {'version':h.sha(finding),
                    'summary':None, 'sha256':source['sha256'], 'capture_seq':capture['seq'],
                    'kind':finding['kind'], 'facts':finding['facts']}
    if any(x['capture_seq'] > row['seq'] for x in expected.values()):
        raise ValueError('Reviewed findings changed after report capture; rebuild the report')
    return expected


def acquisition_snapshot(conn, row):
    """Pin the last standard-update result preceding this report, in its stream."""
    from flwu.opinion_discovery import stream_for
    contract = json.loads(row['payload'])['contract']
    stream = stream_for(row['stream'])[0]
    for capture in conn.execute('SELECT capture_id,payload FROM captures WHERE stream=? AND seq<=? ORDER BY seq DESC',
                                (stream, row['seq'])):
        event = json.loads(capture['payload']).get('opinion_discovery', {})
        if event.get('kind') != 'update-result':
            continue
        bounds = event.get('bounds', {})
        if (bounds.get('start'), bounds.get('end')) != (contract.get('window_start'), contract.get('window_end')):
            continue
        digest = event.get('queue_sha256')
        artifact = conn.execute('SELECT bytes FROM artifacts WHERE sha256=?', (digest,)).fetchone()
        if artifact is None or h.sha(artifact[0]) != digest:
            raise ValueError('Standard update queue artifact missing or changed')
        queue = json.loads(artifact[0])
        if queue.get('run_id') != event.get('run_id') or queue.get('bounds') != bounds:
            raise ValueError('Standard update queue does not match saved run identity/bounds')
        return {'capture_id':capture['capture_id'], 'run_id':event['run_id'], 'queue_sha256':digest}
    raise ValueError('Report requires a saved standard update result for its stream and reporting dates')


def acquisition_queue(conn, row):
    binding = acquisition_snapshot(conn, row)
    return json.loads(conn.execute('SELECT bytes FROM artifacts WHERE sha256=?',
                                  (binding['queue_sha256'],)).fetchone()[0])


def prior_rosters(conn, row):
    """Compare only with a finalized predecessor, never an unfinished capture."""
    prior = conn.execute(
        'SELECT c.payload FROM finalized_reports f JOIN captures c ON c.seq=f.capture_seq '
        'WHERE f.stream=? AND c.seq<? ORDER BY c.seq DESC,f.seq DESC LIMIT 1',
        (row['stream'], row['seq'])).fetchone()
    if prior is None:
        return {}
    return {f['key']: f['facts']['entities'] for f in json.loads(prior['payload'])['findings']
            if f['kind'] == 'source_inventory' and f['facts'].get('entities')}


def roster_template(conn, row):
    current = {f['key']: f['facts']['entities'] for f in json.loads(row['payload'])['findings']
               if f['kind'] == 'source_inventory' and f['facts'].get('entities')}
    prior = prior_rosters(conn, row)
    return [{'inventory_key': key, 'people': current.get(key, []), 'reason': '',
             'removals': [{'id': p['id'], 'name': p['name'], 'reason': '', 'citations': []}
                          for p in prior.get(key, [])
                          if p['id'] not in {x['id'] for x in current.get(key, [])}]}
            for key in sorted(set(current) | set(prior))]


def template(conn, capture_id, report):
    row = report_row(conn, capture_id)
    return {'schema_version':1, 'capture_id':capture_id,
            'report_sha256':h.sha(Path(report).read_bytes()), 'acquisition':acquisition_snapshot(conn,row), 'reviewer':'',
            'legal_review':'', 'visual_review':'',
            'dispositions':[{'finding_id':key, 'version':value['version'], 'decision':'',
                             'candidate_key':None, 'reason':'', 'citations':[]}
                            for key,value in requirements(conn,row).items()],
            'rosters':roster_template(conn, row),
            'pending':publication_pending.template(acquisition_queue(conn, row))}


def validate(conn, manifest, report_bytes, *, require_latest=True):
    fields = {'schema_version','capture_id','report_sha256','reviewer','legal_review','visual_review','dispositions','rosters','acquisition','pending'}
    if not isinstance(manifest,dict) or set(manifest)!=fields or manifest['schema_version']!=1:
        raise ValueError('Use the exact publication acceptance template')
    if any(not isinstance(manifest[k],str) or not manifest[k].strip() for k in ('reviewer','legal_review','visual_review')):
        raise ValueError('Separate actual legal and visual publication review is required')
    if h.sha(report_bytes)!=manifest['report_sha256']:
        raise ValueError('Acceptance report bytes changed')
    row=report_row(conn,manifest['capture_id']);payload=json.loads(row['payload'])
    if payload['status']!='ready_for_review' or any(c['status']!='verified' for c in payload['checks']):
        raise ValueError('Incomplete research cannot receive publication acceptance')
    if require_latest and conn.execute('SELECT max(seq) FROM captures WHERE stream=?',(row['stream'],)).fetchone()[0]!=row['seq']:
        raise ValueError('Accept the latest report capture')
    if manifest['acquisition'] != acquisition_snapshot(conn,row):
        raise ValueError('Publication acquisition binding differs from the saved standard update snapshot')
    index=AcquisitionIndex(conn,row['stream'],through_seq=row['seq'])
    publication_pending.validate(acquisition_queue(conn, row), manifest['pending'], index)
    for finding in payload['findings']:
        for ref in finding['citations']:
            index.validate(ref)
    expected=requirements(conn,row)
    decisions=manifest['dispositions']
    if not isinstance(decisions,list) or any(not isinstance(d,dict) for d in decisions):
        raise ValueError('Dispositions must be explicit records')
    ids=[d.get('finding_id') for d in decisions]
    if any(not isinstance(key, str) for key in ids) or len(ids)!=len(set(ids)) or set(ids)!=set(expected):
        raise ValueError('Every relevant finding requires exactly one publication disposition')
    candidates={f['key']:f for f in payload['findings'] if f['kind']=='candidate' and f['facts'].get('decision')=='include'}
    mapped=set()
    report_text=' '.join(BeautifulSoup(report_bytes,'html.parser').get_text(' ',strip=True).split())
    for decision in decisions:
        if set(decision)!={'finding_id','version','decision','candidate_key','reason','citations'}:
            raise ValueError('Invalid publication disposition fields')
        if (not isinstance(decision['citations'], list)
                or any(not isinstance(cite, dict) for cite in decision['citations'])
                or (decision['candidate_key'] is not None and not isinstance(decision['candidate_key'], str))):
            raise ValueError('Disposition citations must be records and candidate key must be a string or null')
        requirement=expected[decision['finding_id']]
        if decision['version']!=requirement['version']:
            raise ValueError('Stale reviewed-finding version')
        if not isinstance(decision['reason'],str) or not decision['reason'].strip():
            raise ValueError('Publication disposition requires substantive reason')
        if decision['decision']=='include':
            candidate=candidates.get(decision['candidate_key'])
            if not candidate or not any(c['sha256']==requirement['sha256'] for c in candidate['citations']):
                raise ValueError('Included finding must map to an actual candidate citing its acquired source')
            facts=candidate['facts']
            summary=facts.get('summary') or '\n\n'.join(c['statement'] for c in facts.get('claims',[]) if c.get('review')=='supported')
            if not facts.get('title') or not summary or facts.get('section') not in ('case_law','statutes','procedural_rules','local_rules'):
                raise ValueError('Included candidate needs title, summary and explicit section')
            if requirement['summary'] and requirement['summary'] not in summary:
                raise ValueError('Published opinion summary must retain the accepted reviewed summary')
            if any(' '.join(value.split()) not in report_text for value in (facts['title'],summary)):
                raise ValueError('Included candidate missing from reviewed report text')
            mapped.add(candidate['key'])
        elif decision['decision']=='include_directory':
            person = next((f for f in payload['findings'] if f['key'] == decision['candidate_key']), None)
            if (requirement.get('kind') not in ('judge', 'clerk') or not person
                    or person['kind'] != requirement['kind']
                    or person['facts'] != requirement['facts']
                    or not any(c['sha256'] == requirement['sha256'] for c in person['citations'])):
                raise ValueError('Directory inclusion must retain the reviewed personnel facts and acquired source')
            if not person['facts'].get('name') or ' '.join(person['facts']['name'].split()) not in report_text:
                raise ValueError('Directory inclusion missing from reviewed report')
        elif decision['decision']=='exclude':
            if decision['candidate_key'] is not None or not decision['citations']:
                raise ValueError('Exclusion needs cited support and no included candidate')
            for cite in decision['citations']:
                index.validate(cite)
                if not cite.get('quote'):
                    raise ValueError('Exclusion needs a source quotation')
            if not any(c['sha256']==requirement['sha256'] for c in decision['citations']):
                raise ValueError('Exclusion must cite the reviewed finding source')
        else:
            raise ValueError('Publication decision must be include, include_directory or exclude')
    # Other acquired findings may enter a report, but never without explicit claims.
    for key,candidate in candidates.items():
        if key not in mapped:
            raise ValueError('Included candidate lacks a reviewed-finding mapping')
    inventories={f['key']:f for f in payload['findings'] if f['kind']=='source_inventory' and f['facts'].get('entities')}
    prior = prior_rosters(conn, row)
    rosters=manifest['rosters']
    if not isinstance(rosters,list) or any(not isinstance(r,dict) for r in rosters):
        raise ValueError('Roster reconciliation must be explicit')
    keys=[r.get('inventory_key') for r in rosters]
    if any(not isinstance(key, str) for key in keys) or len(keys)!=len(set(keys)) or set(keys)!=(set(inventories) | set(prior)):
        raise ValueError('Every personnel inventory needs an official named-roster reconciliation')
    expected_people = {}
    for roster in rosters:
        if set(roster) not in ({'inventory_key','people','reason'}, {'inventory_key','people','reason','removals'}) or not roster.get('reason'):
            raise ValueError('Roster reconciliation requires inventory, people and reason')
        actual=inventories.get(roster['inventory_key'], {}).get('facts', {}).get('entities', [])
        removed = {p['id']: p for p in prior.get(roster['inventory_key'], [])
                   if p['id'] not in {x['id'] for x in actual}}
        removals = roster.get('removals', [])
        if (not isinstance(removals, list) or any(not isinstance(r, dict) or
                set(r) != {'id', 'name', 'reason', 'citations'} or not isinstance(r['id'], str)
                for r in removals)):
            raise ValueError('Roster removals require explicit identity, reason and citations')
        if len(removals) != len(removed) or {r['id'] for r in removals} != set(removed):
            raise ValueError('Every removed roster identity requires an explicit supported disposition')
        for removal in removals:
            if (removal['name'] != removed[removal['id']]['name']
                    or not isinstance(removal['reason'], str) or not removal['reason'].strip()
                    or not isinstance(removal['citations'], list) or not removal['citations']):
                raise ValueError('Roster removal requires original name and cited substantive explanation')
            for cite in removal['citations']:
                index.validate(cite)
                if not cite.get('quote'):
                    raise ValueError('Roster removal requires quoted source support')
        for person in actual:
            identity = (person['name'], person.get('type'))
            if identity[1] not in ('judge', 'clerk'):
                raise ValueError('Roster person requires a supported judge/clerk role')
            key = 'person-' + person['id']
            if key in expected_people and expected_people[key] != identity:
                raise ValueError('Conflicting roster identities share a person ID')
            expected_people[key] = identity
        people=roster['people']
        if not isinstance(people,list):
            raise ValueError('Expected roster people must be a list')
        for person in people:
            if (not isinstance(person, dict) or not isinstance(person.get('id'), str)
                    or not person['id'].strip() or not isinstance(person.get('citation'), dict)):
                raise ValueError('Roster people require stable identities and cited evidence')
            validate_person_identity(person);index.validate(person['citation'])
        if len({p['id'] for p in people})!=len(people) or {(p['id'],p['name']) for p in people}!={(p['id'],p['name']) for p in actual}:
            raise ValueError('Report roster differs from the explicitly cited official people')
    personnel = {f['key']: f for f in payload['findings'] if f['kind'] in ('judge', 'clerk')}
    if set(personnel) != set(expected_people):
        raise ValueError('Every roster person requires exactly one matching personnel record; unrostered people are forbidden')
    for key, (name, role) in expected_people.items():
        person = personnel[key]
        if person['kind'] != role or person['facts'].get('name') != name:
            raise ValueError('Personnel record differs from its reconciled roster identity')
    return row


def accept(conn, manifest, report):
    raw=Path(report).read_bytes()
    digest=h.sha(manifest)
    with h.publication_transaction(conn):
        validate(conn,manifest,raw)
        conn.execute('CREATE TABLE IF NOT EXISTS publication_acceptances(capture_id TEXT NOT NULL, report_sha256 TEXT NOT NULL, manifest_sha256 TEXT PRIMARY KEY, manifest TEXT NOT NULL, accepted_at TEXT NOT NULL)')
        conn.execute('INSERT OR IGNORE INTO publication_acceptances VALUES(?,?,?,?,?)',
                     (manifest['capture_id'],h.sha(raw),digest,h.canonical(manifest),h.now()))
    return {'acceptance_sha256':digest,'capture_id':manifest['capture_id'],'publication_performed':False}


def require(conn, capture_id, report_bytes, *, require_latest=True):
    if not conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='publication_acceptances'").fetchone():
        raise ValueError('Separate publication acceptance is required before finalization/export')
    saved=conn.execute('SELECT * FROM publication_acceptances WHERE capture_id=? AND report_sha256=? ORDER BY accepted_at DESC LIMIT 1',
                       (capture_id,h.sha(report_bytes))).fetchone()
    if saved is None:
        raise ValueError('Separate publication acceptance missing for this report/capture')
    manifest=json.loads(saved['manifest'])
    if h.sha(manifest)!=saved['manifest_sha256']:
        raise ValueError('Publication acceptance checksum mismatch')
    validate(conn,manifest,report_bytes,require_latest=require_latest)

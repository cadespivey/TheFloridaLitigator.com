"""Separate report/roster acceptance and review-site building."""
from __future__ import annotations
import json
from functools import lru_cache
from pathlib import Path
import shutil

from flwu import workflow as w, history as h, publication_acceptance as pa, publication as pub
from flwu.evidence_binding import AcquisitionIndex
from flwu.research import validate_person_identity


def built(conn,config,prepared,directories):
    identity=h.sha([prepared,directories])
    return next((e for e in reversed(w.events(conn,config)) if e['kind']=='site_built' and e['identity']==identity),None)


VERIFIER_POLICY = 'flwu-final-items-v1'
MAX_BATCH_ITEMS = 6
MAX_BATCH_CHARACTERS = 25000


@lru_cache(maxsize=1)
def verification_policy():
    root = Path(__file__).resolve().parents[2]
    inputs = [root/'src/flwu'/name for name in ('workflow_release.py', 'publication_driver.py', 'publication_acceptance.py')]
    inputs += [root/'skills/florida-update/references'/name for name in ('release-and-recovery.md', 'review-rules.md')]
    return h.sha([VERIFIER_POLICY, {str(path.relative_to(root)): h.sha(path.read_bytes()) for path in inputs}])


def verification_items(conn, config, prepared, directories, manifest):
    """Freeze content and supporting evidence independently of batch order and build ID."""
    row = conn.execute('SELECT payload FROM captures WHERE capture_id=?', (prepared['capture_id'],)).fetchone()
    findings = {f['key']: f for f in json.loads(row[0])['findings']}
    issue = w.read(prepared['public_preview'])
    public = {item['id']: item for section in issue['sections'].values() for item in section['items']}
    items = []
    for disposition in manifest['dispositions']:
        if disposition['decision'] != 'include':
            continue
        key = disposition['candidate_key']
        finding = findings[key]
        article = dict(kind='news', key=key, public=public[key], facts=finding['facts'],
                       evidence=finding['citations'], version=disposition['version'])
        if disposition['finding_id'].startswith('opinion:'):
            from flwu import source_gate
            hashes = dict.fromkeys(c['text_sha256'] for c in finding['citations'])
            article['readings'] = [source_gate.blob(conn, digest).decode('utf-8') for digest in hashes]
        items.append(article)
    decisions = {h.sha(e['receipt']): e for e in w.accepted(conn, config).values()
                 if e['task']['kind'] in ('directory_review', 'directory_removal')}
    represented = set()
    public_people = {person['id']: person for person in issue['directory']}
    for change in w.read(directories['audit']):
        if change['before'] == change['after']:
            continue
        decision = decisions[change['decision_sha256']]
        task = decision['task']
        finding = findings.get(task['identity'], {})
        represented.add(task['identity'])
        # The assembly's own observation stamp is rebound by aggregate acceptance.
        # Preserve all source, contact and identity evidence in the item binding.
        if (change.get('after') or {}).get('source_observation', {}).get('capture_id') == prepared['capture_id']:
            change = dict(change, after={k: v for k,v in change['after'].items() if k != 'source_observation'})
        items.append(dict(kind='directory', key=[change['path'], task['identity']],
                          change=change, public=public_people.get(task['identity']), evidence=finding.get('citations', []) +
                          decision['receipt'].get('identity_citations', []),
                          source=task['inputs'].get('source_assignment'),
                          matches=task['inputs'].get('possible_matches', [])))
    for disposition in manifest['dispositions']:
        key = disposition['candidate_key']
        if disposition['decision'] != 'include_directory' or key in represented:
            continue
        items.append(dict(kind='directory', key=key, public=public_people[key],
                          change=dict(after=public_people[key]), evidence=findings[key]['citations'],
                          source=None, matches=[]))
    return items


def item_digest(item):
    return h.sha([verification_policy(), item])


def checked_batch(task, receipt):
    if set(receipt) != {'reviewer', 'results'} or not isinstance(receipt['reviewer'], str) or not receipt['reviewer'].strip():
        raise ValueError('Verification needs the reviewer and the exact item results')
    expected = [item_digest(item) for item in task['inputs']['items']]
    results = receipt['results']
    if not isinstance(results, list) or len(results) != len(expected):
        raise ValueError('Every item in this batch requires its own result')
    for digest, result in zip(expected, results):
        if (not isinstance(result, dict) or set(result) != {'binding', 'decision', 'reason'}
                or result['binding'] != digest or result['decision'] != 'verified'
                or not isinstance(result['reason'], str) or not result['reason'].strip()):
            raise ValueError('Unresolved, stale or unsupported verification result')
    return expected


def campaign(conn, config, prepared, directories, build, manifest, decisions):
    items = verification_items(conn, config, prepared, directories, manifest)
    saved = {}
    reviewed_here = set()
    prior = config.get('baseline_capture')
    if prior and not h.invalidation(conn, prior):
        owner = conn.execute(
            "SELECT json_extract(payload,'$.workflow_report.contract_sha256') FROM captures WHERE capture_id=?",
            (prior,)).fetchone()
        previous = owner and owner[0] and conn.execute(
            "SELECT json_extract(payload,'$.workflow.task.inputs.campaign') FROM captures "
            "WHERE stream=? AND json_extract(payload,'$.workflow.kind')='decision' "
            "AND json_extract(payload,'$.workflow.task.kind')='publication_acceptance' "
            "AND json_extract(payload,'$.workflow.task.inputs.capture_id')=? ORDER BY seq DESC LIMIT 1",
            ('workflow:'+owner[0], prior)).fetchone()
        if previous and previous[0]:
            proof = json.loads(previous[0])
            if proof['policy'] == verification_policy():
                saved.update(proof['results'])
    for event in w.events(conn, config, kinds=('verified_batch_items',)):
        if event['policy'] == verification_policy():
            saved.update(event['results'])
            if event.get('capture_id') == prepared['capture_id']:
                reviewed_here.update(event['results'])
    for entry in decisions.values():
        task = entry['task']
        if task['kind'] == 'publication_verification' and task['inputs']['policy'] == verification_policy():
            for digest, result in zip(checked_batch(task, entry['receipt']), entry['receipt']['results']):
                saved[digest] = h.sha([entry['receipt']['reviewer'], result])
                if task['inputs']['capture_id'] == prepared['capture_id']:reviewed_here.add(digest)
    batch = []
    size = 0
    for item in items:
        if item_digest(item) in saved:
            continue
        length = len(h.canonical(item))
        if batch and (len(batch) == MAX_BATCH_ITEMS or size + length > MAX_BATCH_CHARACTERS):
            break
        batch.append(item)
        size += length
    if batch:
        data = dict(items=batch, policy=verification_policy(), build_identity=build['identity'],
                    capture_id=prepared['capture_id'], site=build['site'])
        return w.packet(config, 'publication_verification', prepared['capture_id'], data,
                        dict(reviewer='', results=[]),
                        'Verify each final item against its evidence. Report a named defect or unresolved evidence before acceptance.')
    from flwu import derived_cache
    digests = [item_digest(i) for i in items]
    if len(digests) != len(set(digests)):
        raise ValueError('Duplicate final item binding requires reconciliation')
    audit = w.read(directories['audit'])
    proof = dict(policy=verification_policy(),
                 verification_status={key: 'individually_verified' if key in reviewed_here else 'reused' for key in digests},
                 exclusions={d['finding_id']:d['reason'] for d in manifest['dispositions'] if d['decision']=='exclude'},
                 identity_waivers=[r['identity_waiver_sha256'] for r in audit if r.get('identity_verification')=='waived_by_user'],
                 implementation=derived_cache.policy(), contract_sha256=h.sha(config),
                 directory_operations=len(audit),
                 distinct_directory_ids=len({(r.get('after') or r['before'])['id'] for r in audit}),
                 results={item_digest(i): saved[item_digest(i)] for i in items},
                 dispositions=h.sha(manifest['dispositions']), coverage=h.sha(manifest['pending']),
                 audit=h.sha(w.read(directories['audit'])),
                 reviewed_bytes=dict(issue=prepared['public_preview_sha256'],
                                     directories={path: h.sha(Path(path).read_bytes())
                                                  for path in directories['directory_paths']}))
    return proof


def tasks(conn,config,prepared,directories):
    build=built(conn,config,prepared,directories)
    if build is None:return
    verify_build(build)
    manifest=w.read(prepared['acceptance_template']);done=w.accepted(conn,config)
    for roster in manifest['rosters']:
        task=w.packet(config,'roster_review',roster['inventory_key'],
                      dict(capture_id=prepared['capture_id'],inventory=roster),roster,
                      'Check named membership and explicit removals against the supplied citations. '
                      'A missing person on a partial page is not evidence of departure.',
                      checks=('Explicit cited roster and supported removal decisions',))
        yield task
        if task['packet_sha256'] not in done:return
        manifest['rosters'][manifest['rosters'].index(roster)]=done[task['packet_sha256']]['receipt']
    proof = None
    if w.review_protocol(conn, config) >= 2:
        proof = campaign(conn, config, prepared, directories, build, manifest, done)
        if proof.get('kind') == 'publication_verification':
            yield proof
            return
    # Do not infer legal/visual acceptance from screening or a successful build.
    try:
        pa.require(conn,prepared['capture_id'],Path(prepared['report']).read_bytes())
        if any(e['task']['kind']=='publication_acceptance' and
               e['task']['inputs'].get('build_identity')==build['identity']
               and e['task']['inputs'].get('campaign') == proof
               for e in done.values()):return
    except ValueError:
        pass
    yield w.packet(config,'publication_acceptance',prepared['capture_id'],
                   dict(report=prepared['report'],site=build['site'],capture_id=prepared['capture_id'],
                        directory_audit=directories['audit'],manifest_sha256=h.sha(manifest),build_identity=build['identity'],
                        **({'campaign': proof} if proof is not None else {})),
                   manifest,
                   'Inspect the report and built website, including current directory changes. '
                   'Record the actual reviewer and legal/visual review. Do not claim independent human review. '
                   'All finding dispositions and roster decisions are already reconciled; changes require '
                   'a new mapping task/report rather than editing generated claims.',
                   checks=('Existing publication acceptance validator must pass',))


def validate_decision(conn,config,task,receipt):
    if task['kind'] == 'publication_verification':
        return dict(verified=checked_batch(task, receipt))
    if task['kind']=='publication_acceptance':
        expected=task['receipt_template']
        if any(receipt.get(k)!=v for k,v in expected.items() if k not in ('reviewer','legal_review','visual_review')):
            raise ValueError('Acceptance mappings changed; update their task decisions and rebuild')
        if 'campaign' in task['inputs']:
            from flwu.publication_driver import artifact_checks
            proof = artifact_checks(conn, config, task)
            w.record(conn, config, dict(kind='publication_artifact_checked', **proof))
        return pa.accept(conn,receipt,Path(task['inputs']['report']))
    if task['kind']!='roster_review':raise ValueError('Unsupported release review')
    expected=task['receipt_template']
    if set(receipt)!=set(expected) or receipt['inventory_key']!=expected['inventory_key'] or not receipt['reason'].strip():
        raise ValueError('Complete the exact roster review template')
    if {(p['id'],p['name']) for p in receipt['people']}!={(p['id'],p['name']) for p in expected['people']} or len(receipt['people'])!=len(expected['people']):
        raise ValueError('Roster review cannot change prepared membership')
    index=AcquisitionIndex(conn,config['registry']['stream'])
    for person in receipt['people']:
        validate_person_identity(person);index.validate(person['citation'])
    if {(p['id'],p['name']) for p in receipt['removals']}!={(p['id'],p['name']) for p in expected['removals']} or len(receipt['removals'])!=len(expected['removals']):
        raise ValueError('Every prepared roster removal requires a decision')
    for removal in receipt['removals']:
        if not removal['reason'].strip() or not removal['citations']:raise ValueError('Removal requires cited substantive support')
        for cite in removal['citations']:index.validate(cite)
    return {'validated':'roster_review'}


def build(run_dir, *, repair=False):
    config=w.load(run_dir)
    with w.locked(config),h.database(config['database']) as conn:
        from flwu.workflow_report import assemble
        queue=w.latest_queue(conn,config,refresh=True)
        _,_,_,fingerprint=assemble(conn,config,queue)
        prepared=next((e for e in reversed(w.events(conn,config)) if e['kind']=='report_prepared' and e['fingerprint']==fingerprint),None)
        if prepared is None:raise ValueError('Prepare the current report first')
        from flwu.workflow_directory import current
        directories=current(conn,config,prepared)
        if directories is None:raise ValueError('Review and refresh current directories first')
        existing=built(conn,config,prepared,directories)
        if existing and not repair:
            verify_build(existing)
            return {k:v for k,v in existing.items() if k!='hashes'}
        identity=h.sha([prepared,directories]);folder=Path(config['run_dir'])/'workflow'/'builds'/identity
        archive=folder/'archive';archive.mkdir(parents=True,exist_ok=True)
        # The isolated review preview intentionally includes only this report.
        shutil.copy2(prepared['public_preview'],archive/Path(prepared['public_preview']).name)
        from flwu.site import build_site
        site=folder/'site'
        if site.exists():
            # An interrupted build is not success. Preserve partial output and
            # rebuild under a fresh attempt path without deleting evidence.
            n=1
            while (folder/('site-attempt-'+str(n))).exists():n+=1
            site=folder/('site-attempt-'+str(n))
        build_site(archive,site,preview=True,county_directories=directories['directory_paths'],partial_directory_preview=True)
        hashes={str(p.relative_to(site)):h.sha(p.read_bytes()) for p in site.rglob('*') if p.is_file()}
        if existing and hashes != existing['hashes']:
            raise ValueError('Rebuilt output differs from the accepted build inputs; preserved attempt requires investigation')
        result=dict(kind='site_built',identity=identity,site=str(site),hashes=hashes,capture_id=prepared['capture_id'],production=False)
        w.record(conn,config,result);w.write(folder/'validation.json',result)
        return {k:v for k,v in result.items() if k!='hashes'}


def verify_build(build):
    root=Path(build['site'])
    for name,digest in build['hashes'].items():
        p=root/name
        if not p.is_file() or h.sha(p.read_bytes())!=digest:
            raise ValueError('Built artifact missing or changed; run workflow build --repair --run-dir <original-run-directory>')
    if {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()} != set(build['hashes']):
        raise ValueError('Built artifact missing or changed: unexpected files; run workflow build --repair')


def require_build_acceptance(conn,config,build):
    for entry in w.accepted(conn, config).values():
        task = entry['task']
        if task['kind'] != 'publication_acceptance' or task['inputs'].get('build_identity') != build['identity']:
            continue
        proof = task['inputs'].get('campaign')
        if w.review_protocol(conn, config) >= 2 and (not proof or proof['policy'] != verification_policy()):
            continue
        return proof
    raise ValueError('Current directory and report build requires publication acceptance')


def state(conn,config,prepared,directories,*,emit=False):
    build=built(conn,config,prepared,directories)
    if build is None:
        return dict(phase='build_review_site',complete=False,command=w.command(config,'workflow','build','--run-dir',config['run_dir']))
    verify_build(build)
    # Task generation deals with the actual acceptance record; this check also
    # catches later source reviews or modified report bytes after approval.
    pa.require(conn,prepared['capture_id'],Path(prepared['report']).read_bytes())
    require_build_acceptance(conn,config,build)
    if config['mode']=='preview':
        return dict(phase='preview_complete',complete=True,publication_performed=False,
                    capture_id=prepared['capture_id'],report=prepared['report'],site=build['site'],
                    directory_paths=directories['directory_paths'])
    finalized=conn.execute('SELECT 1 FROM finalized_reports WHERE capture_seq=? AND report_sha256=?',
                           (prepared['capture_seq'],h.sha(Path(prepared['report']).read_bytes()))).fetchone()
    if finalized:
        exported=next((e for e in reversed(w.events(conn,config)) if e['kind']=='publication_bundle'
                       and e['identity']==build['identity']),None)
        if exported:
            verify_build(dict(site=exported['folder'],hashes=exported['hashes']))
            integrated=next((e for e in reversed(w.events(conn,config)) if e['kind']=='publication_integrated' and e['identity']==build['identity']),None)
            if integrated:
                for item in integrated['files']:
                    target=Path(item['destination'])
                    if not target.is_file() or h.sha(target.read_bytes())!=item['sha256']:
                        raise ValueError('Integrated publication file changed; reconcile before release')
                deployed=next((e for e in reversed(w.events(conn,config)) if e['kind']=='deployment_verified' and e['identity']==build['identity']),None)
                if deployed:
                    return dict(build_identity=build['identity'],phase='publication_complete',complete=True,publication_performed=True,
                                commit=deployed['commit'],site=deployed['site'],run_url=deployed['run_url'],verified_at=deployed['verified_at'])
                observed=next((e for e in reversed(w.events(conn,config)) if e['kind']=='release_observed' and e['identity']==build['identity']),None)
                if observed:
                    return dict(build_identity=build['identity'],phase='deployment_verification' if observed['state']=='MERGED' else 'merge_required',
                                complete=False,publication_performed=False,pr=observed['url'],
                                next_instruction='Resume this recorded PR; after merge verify the successful Pages run with workflow verify-deployment.')
                return dict(build_identity=build['identity'],phase='release_required',complete=False,publication_performed=False,
                            files=integrated['files'],manifest=exported['manifest'],
                            command=w.command(config,'workflow','release-plan','--run-dir',config['run_dir']),
                            next_instruction='Release the integrated files through Git/PR and verify the deployed issue and directories.')
            return dict(phase='publication_handoff',complete=False,publication_performed=False,
                        manifest=exported['manifest'],
                        command=w.command(config,'workflow','integrate','--run-dir',config['run_dir']),
                        next_instruction='Integrate the pinned publication bundle, then release and verify deployment.')
        return dict(phase='export_publication',complete=False,publication_performed=False,
                    command=w.command(config,'workflow','export','--run-dir',config['run_dir']))
    return dict(phase='ready_for_publication',complete=False,publication_performed=False,
                capture_id=prepared['capture_id'],directory_paths=directories['directory_paths'],
                command=w.command(config,'history','finalize','--database',config['database'],
                                  '--capture-id',prepared['capture_id'],'--report',prepared['report'],
                                  '--review','Separately accepted through the workflow publication-acceptance task'),
                next_instruction='Use the existing export/build/release commands after finalization; a review build is not deployment.')


def export(run_dir):
    """Create a bounded release handoff; do not deploy or overwrite current files."""
    import shlex
    config=w.load(run_dir)
    if config['mode']!='publish' or config.get('trial'):
        raise ValueError('Only an explicitly initialized publish workflow can export a release bundle')
    if not config['archive']:raise ValueError('Publish workflow requires an explicit --archive destination at init')
    with w.locked(config),h.database(config['database']) as conn:
        from flwu.workflow_report import assemble
        from flwu.workflow_directory import current
        queue=w.latest_queue(conn,config,refresh=True)
        _,_,_,fingerprint=assemble(conn,config,queue)
        prepared=next((e for e in reversed(w.events(conn,config)) if e['kind']=='report_prepared' and e['fingerprint']==fingerprint),None)
        if prepared is None:raise ValueError('Prepare the current report first')
        directories=current(conn,config,prepared)
        if directories is None:raise ValueError('Refresh current directories first')
        build=built(conn,config,prepared,directories)
        if build is None:raise ValueError('Build and review the current site first')
        verify_build(build)
        pa.require(conn,prepared['capture_id'],Path(prepared['report']).read_bytes())
        approval = require_build_acceptance(conn,config,build)
        existing=next((e for e in reversed(w.events(conn,config)) if e['kind']=='publication_bundle' and e['identity']==build['identity']),None)
        if existing:
            verify_build(dict(site=existing['folder'],hashes=existing['hashes']))
            return dict(phase='publication_handoff',complete=False,publication_performed=False,manifest=existing['manifest'])
        folder=Path(config['run_dir'])/'workflow'/'release'/build['identity']
        output=pub.export_capture(config['database'],prepared['capture_id'],folder/'archive')
        if approval:
            reviewed = approval['reviewed_bytes']
            w.verify_projections(dict(projection_hashes={prepared['public_preview']: reviewed['issue'],
                                                         **reviewed['directories']}))
            frozen = w.read(prepared['public_preview'])
            final = w.read(output)
            finalized = conn.execute('SELECT finalized_at,report_sha256 FROM finalized_reports WHERE capture_seq=? ORDER BY seq DESC LIMIT 1',
                                     (prepared['capture_seq'],)).fetchone()
            frozen['published_at'] = finalized['finalized_at']
            frozen['provenance'].update(review_status='finalized', report_sha256=finalized['report_sha256'])
            del frozen['content_sha256']
            frozen['content_sha256'] = pub.digest(frozen)
            if final != frozen:
                raise ValueError('Export differs from the reviewed issue outside finalized provenance')
        copies=[dict(source=str(output),destination=str(Path(config['archive'])/Path(output).name),expected_previous_sha256=None)]
        for source,target in zip(directories['directory_paths'],config['directories']):
            if approval:
                pinned = folder/'directories'/Path(source).name
                w.write_bytes(pinned, Path(source).read_bytes(), immutable=True)
                if h.sha(pinned.read_bytes()) != approval['reviewed_bytes']['directories'][source]:
                    raise ValueError('Released directory bytes differ from verified data')
                source = str(pinned)
            copies.append(dict(source=source,destination=target,expected_previous_sha256=h.sha(Path(target).read_bytes())))
        manifest=dict(capture_id=prepared['capture_id'],publication_performed=False,
                      review_site=build['site'],files=copies,
                      commands=[shlex.join(['cp',item['source'],item['destination']]) for item in copies],
                      release_instructions=str(w.ROOT/'docs/workflow/WEB_PUBLICATION.md'),
                      completion_checks=['Recheck destination hashes before copying; do not overwrite concurrent edits.',
                                         'Review and stage only these publication files, scan credentials, commit/push under existing authorization.',
                                         'Verify GitHub Pages deployment and live current issue/directory; handoff is not publication.'])
        w.write(folder/'handoff.json',manifest,immutable=True)
        result=dict(kind='publication_bundle',identity=build['identity'],folder=str(folder),manifest=str(folder/'handoff.json'),
                    hashes={str(p.relative_to(folder)):h.sha(p.read_bytes()) for p in folder.rglob('*') if p.is_file()})
        result['projection_hashes']=w.projection_hashes([folder/name for name in result['hashes']])
        w.record(conn,config,result)
        return dict(phase='publication_handoff',complete=False,publication_performed=False,manifest=result['manifest'])


def integrate(run_dir):
    """Install exactly the accepted bundle with a durable, resumable intent."""
    import os
    import tempfile
    export(run_dir)  # Revalidates current acceptance and generated output.
    config=w.load(run_dir)
    with w.locked(config),h.database(config['database']) as conn:
        bundle=next(e for e in reversed(w.events(conn,config)) if e['kind']=='publication_bundle')
        manifest=w.read(bundle['manifest']);files=[]
        for item in manifest['files']:
            source=Path(item['source']);target=Path(item['destination'])
            if target.is_symlink():raise ValueError('Publication destination must not be a symlink')
            raw=source.read_bytes();digest=h.sha(raw)
            actual=h.sha(target.read_bytes()) if target.exists() else None
            if actual not in (item['expected_previous_sha256'],digest):
                raise ValueError('Concurrent publication edit; destination does not match the pinned prior bytes: '+str(target))
            files.append(dict(**item,sha256=digest))
        previous_intent=next((e for e in reversed(w.events(conn,config)) if e['kind']=='integration_intent' and e['identity']==bundle['identity']),None)
        directory_inputs=previous_intent['directory_inputs'] if previous_intent else {
            item['destination']:w.read(item['destination']) for item in files
            if item['destination'] in config['directories']}
        intent=dict(kind='integration_intent',identity=bundle['identity'],files=files,directory_inputs=directory_inputs)
        w.record(conn,config,intent)
        # Validate every destination before the first write. Retry accepts only
        # the pinned before/after states, so a crash midway can safely resume.
        for item in files:
            target=Path(item['destination']);raw=Path(item['source']).read_bytes()
            if h.sha(raw)!=item['sha256']:raise ValueError('Publication source changed during integration')
            actual=h.sha(target.read_bytes()) if target.exists() else None
            if actual==item['sha256']:continue
            if actual!=item['expected_previous_sha256']:raise ValueError('Concurrent publication edit during integration')
            target.parent.mkdir(parents=True,exist_ok=True)
            fd,temp=tempfile.mkstemp(prefix='.flwu-integrate-',dir=target.parent)
            try:
                with os.fdopen(fd,'wb') as handle:
                    handle.write(raw);handle.flush();os.fsync(handle.fileno())
                os.replace(temp,target)
            finally:
                if os.path.exists(temp):os.unlink(temp)
        result=dict(kind='publication_integrated',identity=bundle['identity'],files=files)
        w.record(conn,config,result)
        return dict(phase='release_required',complete=False,publication_performed=False,
                    command=w.command(config,'workflow','release-plan','--run-dir',config['run_dir']),
                    files=files,next_instruction='Commit only these integrated files, push the release branch, and open or reuse its pull request. Deployment verification remains required.')

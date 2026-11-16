"""Bound reuse of reviewed directory identities; no name-only or inferred scope."""
from __future__ import annotations

import copy
from pathlib import Path

from flwu import county_directory as cd, history as h, workflow as w
from flwu.county_directory import name_key


def supplements(conn, config):
    values={path:w.read(path) for path in config.get('directories',[])}
    intents=w.events(conn,config,kinds=('integration_intent',))
    if intents:
        intent=intents[-1]
        for item in intent['files']:
            path=item['destination']
            if path in values and path in intent.get('directory_inputs',{}):
                if h.sha(Path(path).read_bytes())==item['sha256']:
                    values[path]=copy.deepcopy(intent['directory_inputs'][path])
    for value in values.values():cd.validate_supplement(value,preview=True)
    return values


def _field(facts, key):
    field=facts.get('fields',{}).get(key,{})
    return field.get('value') if field.get('status')=='verified' else None


def _urls(finding):
    facts=finding['facts']
    values=[c.get('url') for c in finding['citations']]
    for key in ('profile_url','procedure_url'):
        values.extend((facts.get(key),_field(facts,key)))
    return {value.rstrip('/') for value in values if isinstance(value,str) and value}


def _compatible(finding, person, courts):
    kind=finding['kind'];facts=finding['facts']
    if kind=='clerk':
        if person['kind']!='Clerk':return False
    elif kind=='judge':
        if person['kind'] not in {'Judge','Senior judge','General magistrate','Hearing officer','Special master','Judicial officer'}:
            return False
    else:return False
    roles=[value for value in (facts.get('role'),_field(facts,'role')) if value]
    display_roles={role.casefold():role for role in cd.ROLES}
    display_roles.update(cd.PERSON_ROLES)
    for role in roles:
        if not isinstance(role,str):return False
        normalized=role.strip().casefold()
        if display_roles.get(normalized)!=person['kind']:return False
        categories={court['category'] for court in courts if court['group_id'] in person['court_ids']}
        if normalized in ('county judge','county court judge') and categories!={'County Courts'}:return False
        if normalized in ('circuit judge','circuit court judge','circuit judge (chief judge)') and categories!={'Circuit Courts'}:return False
    return True


def basis(finding, values):
    """Return inspectable proof only for one unambiguous reviewed identity."""
    facts=finding['facts'];name=facts.get('name');urls=_urls(finding);matches=[]
    for path,value in sorted(values.items()):
        if value['review_status']!='reviewed':continue
        named=[person for person in value['people'] if name_key(person['name'])==name_key(name)]
        # A shared name within a directory is a semantic identity question.
        if len(named)>1:return None
        for person in named:
            stable=finding['key'] in (person['id'],person.get('legacy_person_id'))
            matched=sorted(urls & {(person.get(key) or '').rstrip('/') for key in ('profile_url','procedure_url')})
            if not stable and not matched:continue
            if person['contact_status']!='source_recorded' or not _compatible(finding,person,value['courts']):return None
            keys=('id','name','kind','counties','court_ids','profile_url','procedure_url','source_observation','sources')
            saved={key:copy.deepcopy(person[key]) for key in keys}
            if person.get('legacy_person_id'):saved['legacy_person_id']=person['legacy_person_id']
            matches.append(dict(path=path,directory_sha256=h.sha(value),
                                content_sha256=value['content_sha256'],review=copy.deepcopy(value['review']),
                                through_capture=copy.deepcopy(value['through_capture']),person=saved,
                                match=('stable_id' if stable else 'exact_name_and_official_url' if person['name']==name
                                       else 'full_name_case_whitespace_and_official_url'),matched_urls=matched))
    if not matches:return None
    # Multiple county copies of one stable ID are supported. Different stable
    # identities are left for review, even when their names and URLs agree.
    if len({match['person']['id'] for match in matches})>1 and not all(match['match']=='stable_id' for match in matches):return None
    scope=dict(counties=sorted({c for match in matches for c in match['person']['counties']}),
               court_ids=sorted({c for match in matches for c in match['person']['court_ids']}))
    if not scope['counties'] and not scope['court_ids']:return None
    for key,scope_key in (('county','counties'),('counties','counties'),('court_ids','court_ids')):
        for explicit in (facts.get(key),_field(facts,key)):
            if explicit is None:continue
            items=[explicit] if isinstance(explicit,str) else explicit
            if not isinstance(items,list) or any(not isinstance(item,str) for item in items):return None
            if set(items)-set(scope[scope_key]):return None
    return dict(policy='reviewed_directory_identity_scope_v1',scope=scope,matches=matches)


def bind(config, task, done, proof):
    """Leave existing accepted packet identities untouched."""
    if proof is None or task['packet_sha256'] in done:return task
    return w.packet(config,task['kind'],task['identity'],
                    dict(task['inputs'],directory_reuse=copy.deepcopy(proof)),
                    task['receipt_template'],task['instructions'],checks=task['completion_checks'])


def identity_basis(finding, values):
    proof=basis(finding,values)
    if proof is not None:proof['citations']=copy.deepcopy(finding['citations'])
    return proof


def verify(conn, config, task):
    proof=task['inputs'].get('directory_reuse')
    if proof is None:return None
    values=supplements(conn,config)
    if task['kind']=='directory_review':
        row=conn.execute('SELECT payload FROM captures WHERE capture_id=?',(task['inputs']['capture_id'],)).fetchone()
        import json
        finding=next(f for f in json.loads(row[0])['findings'] if f['key']==task['identity'])
        expected=identity_basis(finding,{path:value for path,value in values.items() if path in task['inputs']['scopes']})
    else:
        expected=basis(task['inputs']['finding'],values)
    if expected!=proof:
        raise ValueError('Reviewed directory reuse evidence changed; regenerate the publication task')
    return proof

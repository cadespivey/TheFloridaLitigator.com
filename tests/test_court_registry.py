"""Reviewed directories extend future registries without changing pinned runs."""
import copy
import json

import pytest

from flwu import court_registry as r, source_gate as gate, history as h
from flwu.cli import main
from tests.test_county_directory import supplement,seal


def directories(root,supplement,count=67):
    root.mkdir();paths=[]
    for n in range(count):
        data=copy.deepcopy(supplement);county='County '+str(n);ordinal=r.ORDINALS[n%20]
        data['county']=county;group='circuit_'+ordinal
        data['courts']=[dict(group_id=group,category='Circuit Courts',label=ordinal+' Circuit',url='https://court.flcourts.gov/'+ordinal)]
        data.update(review_status='reviewed',review=dict(reviewed_by='Fixture',reviewed_at='2026-11-04T12:00:00Z',attestation='Reviewed fixture'))
        for person in data['people']:
            person['counties']=[county];person['court_ids']=[group]
            person['profile_url']='https://court.flcourts.gov/'+person['id']
            person['procedure_url']='https://court.flcourts.gov/shared-procedure.pdf#schedule'
            person['sources']=[dict(url='https://court.flcourts.gov/supporting.pdf',sha256='b'*64,retrieved_at='2026-10-20T12:00:00Z')]
        seal(data);path=root/(str(n)+'.json');path.write_text(json.dumps(data));paths.append(path)
    return paths


def registry():
    url='https://court.flcourts.gov/ExistingCaseSensitivePath'
    return dict(schema_version=1,stream='weekly',review_protocol=gate.PROTOCOL,sources=[dict(id=gate.source_id(url),url=url)])


def test_reconciles_all_circuits_deduplicates_and_parks_unclassified_support(tmp_path,supplement):
    paths=directories(tmp_path/'dirs',supplement);old=registry();before=copy.deepcopy(old)
    merged,audit=r.reconcile(old,paths)
    assert old==before and merged['sources'][0]==old['sources'][0]
    assert audit['missing_circuits']==[] and [v['number'] for v in audit['circuits']]==list(range(1,21))
    urls=[s['url'] for s in merged['sources']]
    assert len(urls)==len(set(urls)) and urls.count('https://court.flcourts.gov/shared-procedure.pdf')==1
    assert 'https://court.flcourts.gov/supporting.pdf' not in urls
    assert audit['supporting_candidates'][0]['status']=='scope_review_required'
    assert not audit['acquisition_performed'] and audit['database_writes']==0
    assert all(s['id']==gate.source_id(s['url']) for s in merged['sources'])
    url='https://court.flcourts.gov/shared-procedure.pdf'
    page=r.context(merged,audit,url,limit=2)
    assert page['registered'] and page['registry_matches_snapshot'] and len(page['references'])==2
    assert page['next_offset']==2 and page['total_references']>2
    assert r.context(merged,audit,'https://court.flcourts.gov/supporting.pdf')['status']=='scope_review_required'
    with pytest.raises(ValueError,match='stream/protocol'):
        r.context(dict(merged,stream='other'),audit,url)
    with pytest.raises(ValueError,match='between 1 and 50'):r.context(merged,audit,url,limit=500)
    with pytest.raises(ValueError,match='no addition'):r.context(merged,audit,'https://court.flcourts.gov/unknown')


def test_cli_never_opens_database_and_retries_identical_outputs(tmp_path,supplement,monkeypatch,capsys):
    directories(tmp_path/'dirs',supplement);source=tmp_path/'input.json';source.write_text(json.dumps(registry()));original=source.read_bytes()
    monkeypatch.setattr(h,'database',lambda *a,**k:pytest.fail('Registry reconciliation must not open a database'))
    args=['source-gate','reconcile','--registry',str(source),'--directories',str(tmp_path/'dirs'),
          '--output',str(tmp_path/'next.json'),'--manifest',str(tmp_path/'audit.json')]
    assert main(args)==0 and main(args)==0
    assert source.read_bytes()==original
    assert gate.load_registry(tmp_path/'next.json')['stream']=='weekly'
    (tmp_path/'next.json').write_text('{}')
    assert main(args)==1 and 'different data' in capsys.readouterr().err


def test_refuses_input_overwrite_partial_scope_and_unreviewed_directory(tmp_path,supplement):
    paths=directories(tmp_path/'dirs',supplement,count=1);source=tmp_path/'input.json';source.write_text(json.dumps(registry()))
    with pytest.raises(ValueError,match='distinct'):r.run(source,tmp_path/'dirs',source,tmp_path/'audit.json')
    with pytest.raises(ValueError,match='67 reviewed'):r.run(source,tmp_path/'dirs',tmp_path/'next.json',tmp_path/'audit.json')
    assert not (tmp_path/'next.json').exists()
    data=json.loads(paths[0].read_text());data['review_status']='pending';seal(data);paths[0].write_text(json.dumps(data))
    with pytest.raises(ValueError):r.reconcile(registry(),paths)


def test_invalid_checksum_duplicate_county_and_secret_url_are_not_promoted(tmp_path,supplement):
    paths=directories(tmp_path/'dirs',supplement,count=2)
    data=json.loads(paths[0].read_text());data['county']='Tampered';paths[0].write_text(json.dumps(data))
    with pytest.raises(ValueError,match='checksum'):r.reconcile(registry(),paths)
    data['county']='County 1'
    for person in data['people']:person['counties']=['County 1']
    seal(data);paths[0].write_text(json.dumps(data))
    with pytest.raises(ValueError,match='Duplicate county'):r.reconcile(registry(),paths)
    data['county']='County 0'
    for person in data['people']:person['counties']=['County 0']
    data['people'][0]['profile_url']='https://court.flcourts.gov/?api_key=private';seal(data);paths[0].write_text(json.dumps(data))
    with pytest.raises(ValueError):r.reconcile(registry(),paths)

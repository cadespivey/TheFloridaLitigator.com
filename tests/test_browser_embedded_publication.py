"""Synthetic byte fixtures test provenance binding, not legal correctness."""
import base64
import copy
import json

import pytest

from flwu import history as h
from flwu.evidence_binding import AcquisitionIndex


def acquire(conn, *, wrapper_change=None, observation_change=None, save_wrapper=True):
    raw=b'%PDF-1.4\nSynthetic PDF fixture'
    text=b'Synthetic order fixture.'
    url='https://court.example/order'
    stamp='2026-11-16T14:06:26.008Z'
    wrapper=dict(url=url,retrieved_at=stamp,pdf='data:application/pdf;base64,'+base64.b64encode(raw).decode())
    wrapper.update(wrapper_change or {})
    saved=json.dumps(wrapper).encode()
    observed=dict(url=url,retrieved_at=stamp,sha256=h.sha(raw),text_sha256=h.sha(text),success=True,
                  acquisition_method='browser-embedded-pdf-data-uri-v1',browser_snapshot_sha256=h.sha(saved))
    observed.update(observation_change or {})
    artifacts={h.sha(raw):raw,h.sha(text):text}
    if save_wrapper:artifacts[h.sha(saved)]=saved
    capture=h.record(conn,stream='browser-acquisition',mode='manual_research',scope={'target_stream':'report'},
                     run_id='fixture',payload=dict(status='incomplete',contract={},checks=[],findings=[],drafts=[],source_gate=observed),
                     artifacts=artifacts)
    ref={key:observed[key] for key in ('url','retrieved_at','sha256','text_sha256')}
    ref.update(acquisition_capture_id=capture['capture_id'],quote=text.decode(),locator='Fixture paragraph')
    return ref,observed,capture


def test_embedded_pdf_binds_without_inventing_http_status(tmp_path):
    with h.database(tmp_path/'history.sqlite') as conn:
        ref,observed,capture=acquire(conn)
        index=AcquisitionIndex(conn,'report')
        assert index.validate(ref)['browser_snapshot_sha256']==observed['browser_snapshot_sha256']
        assert 'http_status' not in ref
        index.validate_tree({'support':{'citation':ref}})
        with pytest.raises(ValueError,match='does not match'):
            index.validate(dict(ref,http_status=200))
        with pytest.raises(ValueError,match='does not match'):
            AcquisitionIndex(conn,'other-report').validate(ref)
        with pytest.raises(ValueError,match='does not match'):
            AcquisitionIndex(conn,'report',through_seq=capture['seq']-1).validate(ref)


@pytest.mark.parametrize('change',[
    {'acquisition_method':'unverified-browser-label'},
    {'acquisition_method':None},
    {'browser_snapshot_sha256':'0'*64},
])
def test_observation_label_alone_cannot_replace_http_provenance(tmp_path,change):
    with h.database(tmp_path/'history.sqlite') as conn:
        ref,_,_=acquire(conn,observation_change=change)
        with pytest.raises(ValueError):AcquisitionIndex(conn,'report').validate(ref)


@pytest.mark.parametrize('change',[
    {'url':'https://court.example/other-order'},
    {'retrieved_at':'2026-11-17T14:06:26.008Z'},
    {'pdf':'data:application/pdf;base64,'+base64.b64encode(b'%PDF-1.4\nDifferent document').decode()},
    {'pdf':'data:application/pdf;base64,not valid base64!'},
    {'pdf':'data:text/plain;base64,'+base64.b64encode(b'%PDF-1.4\nSynthetic PDF fixture').decode()},
])
def test_browser_wrapper_must_identify_the_same_acquired_pdf(tmp_path,change):
    with h.database(tmp_path/'history.sqlite') as conn:
        ref,_,_=acquire(conn,wrapper_change=change)
        with pytest.raises(ValueError):AcquisitionIndex(conn,'report').validate(ref)


def test_missing_or_changed_wrapper_is_not_accepted(tmp_path):
    with h.database(tmp_path/'missing.sqlite') as conn:
        ref,_,_=acquire(conn,save_wrapper=False)
        with pytest.raises(ValueError,match='snapshot artifact missing'):
            AcquisitionIndex(conn,'report').validate(ref)
    with h.database(tmp_path/'changed.sqlite') as conn:
        ref,observed,_=acquire(conn)
        index=AcquisitionIndex(conn,'report')
        index.validate(ref)
        conn.execute('UPDATE artifacts SET bytes=? WHERE sha256=?',(b'changed',observed['browser_snapshot_sha256']))
        with pytest.raises(ValueError,match='snapshot artifact missing or changed'):
            index.validate(ref)


@pytest.mark.parametrize('field,value',[
    ('url','https://court.example/other-order'),
    ('retrieved_at','2026-11-17T14:06:26.008Z'),
    ('text_sha256','0'*64),
    ('acquisition_capture_id','0'*64),
    ('quote','A different order.'),
])
def test_browser_reference_cannot_change_source_extraction_or_quote(tmp_path,field,value):
    with h.database(tmp_path/'history.sqlite') as conn:
        ref,_,_=acquire(conn)
        ref=copy.deepcopy(ref);ref[field]=value
        with pytest.raises(ValueError):AcquisitionIndex(conn,'report').validate(ref)

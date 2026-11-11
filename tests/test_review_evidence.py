"""Lossless bounded packets and exact quote selection, with no production writes."""
import copy
import json
from pathlib import Path

import pytest

from flwu import history as h, review_evidence as e, workflow as w
from tests.test_source_gate import env


def checked(ref):
    raw = Path(ref['path']).read_bytes()
    assert h.sha(raw) == ref['sha256']
    assert len(raw) == ref['bytes'] <= e.MAX_FILE_BYTES
    return raw


def entries(index):
    result = []
    ref = index['first']
    seen = set()
    while ref:
        assert ref['path'] not in seen
        seen.add(ref['path'])
        page = json.loads(checked(ref))
        result.extend(page['entries'])
        ref = page['next']
    assert len(result) == index['count']
    return result


def value(ref):
    if ref['format'] == 'json': return json.loads(checked(ref))
    parts = entries(ref['parts'])
    cursor = 0
    text = ''
    for part in parts:
        fragment = checked(part).decode()
        assert part['start_char'] == cursor
        cursor += len(fragment)
        assert part['end_char'] == cursor
        text += fragment
    assert cursor == ref['characters']
    assert h.sha(text.encode()) == ref['serialized_sha256']
    return json.loads(text)


def test_large_alignment_lossless_bounded_fields_pages_and_unicode(tmp_path):
    script = 'try { new URL(window.parent.location) } catch { fallback(); }\n'
    groups = [dict(id=str(n), kind='replace', before=[script+'a'*20000],
                   after=[script+'🙂\u00a0é'*13000], context_before=[{'open':'body'}],
                   context_after=[{'close':'body'}], decoded_fields=[{'link':'/Case.PDF'}],
                   decoding_limit_paths=[['unknown', n]]) for n in range(15)]
    alignment = dict(groups=groups, before_sha256='old', after_sha256='new')
    original = copy.deepcopy(alignment)
    ref = e.project(tmp_path, alignment)
    manifest = json.loads(checked(ref))
    recovered = []
    for entry in entries(manifest['groups']):
        card = json.loads(checked(entry))
        recovered.append(dict(id=card['id'], kind=card['kind'],
                              **{field['field']: value(field['value']) for field in entries(card['fields'])}))
    assert recovered == groups  # Script logic, decoded fields and limits all survive.
    assert manifest['alignment_sha256'] == h.sha(alignment)
    assert alignment == original
    assert all(p.stat().st_size <= e.MAX_FILE_BYTES for p in tmp_path.iterdir())
    assert e.project(tmp_path, alignment) == ref  # Repeat/recovery is deterministic.


def test_serialization_obligation_and_no_alignment_text_changes(tmp_path):
    alignment = {'groups':[{'id':'serialization','kind':'original_serialization',
                            'before_sha256':'old','after_sha256':'new'}]}
    manifest = json.loads(checked(e.project(tmp_path, alignment)))
    entry = entries(manifest['groups'])[0]
    assert entry['format'] == 'complete_group'
    assert json.loads(checked(entry)) == alignment['groups'][0]
    changes = {'current':['Changed operative rule '*2000], 'previous':['Old rule']}
    plain = json.loads(checked(e.project(tmp_path/'plain', changed_text=changes)))
    assert plain['groups']['count'] == 0
    assert {s:value(v) for s,v in plain['changed_text'].items()} == changes


def guide_with_text(tmp_path, text):
    path = tmp_path/'source.txt'; path.write_bytes(text.encode())
    binding = dict(path=str(path), sha256='rawhash', text_sha256=h.sha(text.encode()),
                   url='https://court.gov/clerk', retrieved_at='2026-11-09T01:00:00+00:00', http_status=200)
    guide = tmp_path/'guide.json'
    guide.write_text(json.dumps({'quote_bindings':{'current':binding}}))
    return guide, binding


def test_quote_preserves_whitespace_unicode_timestamps_and_exact_offsets(tmp_path):
    text = 'Heading\r\nKristopher\u00a0Warburton selected October 30.\r\nPrior role ended.\n'
    guide, binding = guide_with_text(tmp_path, text)
    result = e.quote(tmp_path, guide, 'current', start_line=2, end_line=2)
    assert result['support']['quote'] == text.splitlines(keepends=True)[1]
    assert result['citation']['retrieved_at'] == binding['retrieved_at']
    assert result['citation']['url'] == binding['url']
    assert set(result['support']) == {'sha256','text_sha256','quote','locator'}
    quoted = e.quote(tmp_path, guide, 'current', start_char=9, end_char=30)
    assert quoted['support']['quote'] == text[9:30]
    assert Path(binding['path']).read_bytes() == text.encode()


@pytest.mark.parametrize('arguments',[
    {}, {'start_line':1}, {'start_line':0,'end_line':1},
    {'start_line':1,'end_line':999}, {'start_char':1,'end_char':1},
    {'start_char':-1,'end_char':2}, {'start_char':0,'end_char':999},
    {'start_line':1,'end_line':1,'start_char':0,'end_char':2},
])
def test_invalid_quote_ranges_fail(tmp_path, arguments):
    guide, _ = guide_with_text(tmp_path, 'Only one line')
    with pytest.raises(ValueError): e.quote(tmp_path, guide, 'current', **arguments)


def test_quote_rejects_tampered_extraction_missing_side_escape_and_oversize(tmp_path):
    guide, binding = guide_with_text(tmp_path, 'x'*9000)
    with pytest.raises(ValueError, match='8 KiB'):
        e.quote(tmp_path, guide, 'current', start_line=1, end_line=1)
    with pytest.raises(ValueError, match='No acquired'):
        e.quote(tmp_path, guide, 'previous', start_line=1, end_line=1)
    Path(binding['path']).write_text('tampered')
    with pytest.raises(ValueError, match='hash mismatch'):
        e.quote(tmp_path, guide, 'current', start_line=1, end_line=1)
    with pytest.raises(ValueError, match='inside the run'):
        e.quote(tmp_path/'subdir', guide, 'current', start_line=1, end_line=1)
    with pytest.raises(ValueError, match='hash mismatch'):
        e.project(tmp_path/'projection', texts={'current':binding})


def test_bounded_files_tamper_detected_not_overwritten(tmp_path):
    ref = e.project(tmp_path, {'groups':[{'id':'g','kind':'replace','after':'x'*10000}]})
    fragment = next(tmp_path.glob('*.txt'))
    fragment.write_text('altered')
    with pytest.raises(ValueError, match='Immutable review fragment'):
        e.project(tmp_path, {'groups':[{'id':'g','kind':'replace','after':'x'*10000}]})
    assert fragment.read_text() == 'altered'
    assert Path(ref['path']).is_file()


def test_v7_small_index_templates_and_exact_quote_command_do_not_modify_task(tmp_path, capsys):
    from flwu.cli import main
    guide, binding = guide_with_text(tmp_path, 'Name\nContact: 555-0100\n')
    inputs = {'observation':{k:v for k,v in binding.items() if k!='path'},
              'current-text_path':binding['path'], 'prior_findings':[
                  dict(key='person-existing',kind='clerk',facts={'name':'Previous Clerk','nested':{'retained':'yes'}},
                       expected_version='version1',citations=[{'old':'binding'}]) ]}
    task = w.packet({'run_dir':str(tmp_path)},'source_review','example',inputs,{'outcome':''},'Original')
    before = copy.deepcopy(task)
    returned = w.materialize({'run_dir':str(tmp_path)}, task)
    current = w.read(returned['review_guide'])
    assert current['guide_version'] == 7
    assert w.read(current['personnel_templates']['new']['clerk'])['kind'] == 'clerk'
    existing = entries(current['personnel_templates']['existing'])[0]
    saved = w.read(existing['path'])
    assert saved['facts'] == inputs['prior_findings'][0]['facts']
    assert saved['expected_version'] == 'version1' and saved['citations'] == []
    assert task == before == w.read(returned['packet'])
    assert main(['workflow','quote','--run-dir',str(tmp_path),'--guide',returned['review_guide'],
                 '--start-line','2','--end-line','2']) == 0
    selected = json.loads(capsys.readouterr().out)
    assert selected['support']['quote'] == 'Contact: 555-0100\n'
    assert not (tmp_path/'workflow'/'contract.json').exists()  # No DB/init needed or created.
    assert w.materialize({'run_dir':str(tmp_path)},task) == returned


def test_source_gate_rejects_nonprojectable_person_then_persists_typed_clerk(env):
    from tests.test_source_gate import acquire, receipt
    from flwu import source_gate as g
    conn, registry, _ = env
    first, _ = acquire(env, 'typed-person', page=b'Kristopher Warburton, Clerk. Office phone 555-0100.')
    task = first['tasks'][0]
    draft = receipt(task, registry, conn)
    observation = task['observation']
    citation = {k:observation[k] for k in ('url','sha256','text_sha256','retrieved_at')}
    citation.update(quote='Kristopher Warburton, Clerk. Office phone 555-0100.', locator='Office text')
    finding = dict(key='person-clerk-warburton',kind='personnel_change',expected_version=None,
                   facts={'name':'Kristopher Warburton'},citations=[citation])
    draft.update(outcome='updated_findings',findings=[finding])
    count = conn.execute('SELECT count(*) FROM captures').fetchone()[0]
    with pytest.raises(ValueError, match='judge|clerk'):
        g.accept(conn, registry, draft)
    assert conn.execute('SELECT count(*) FROM captures').fetchone()[0] == count
    finding['kind'] = 'clerk'
    finding['facts']['fields'] = {'office_phone':dict(value='555-0100',status='verified',citation=citation)}
    acknowledgement = g.accept(conn, registry, draft)
    stored = conn.execute('SELECT kind,facts FROM finding_versions WHERE entity_key=?', (finding['key'],)).fetchone()
    assert stored['kind'] == 'clerk'  # This is a directory-projectable record, not an event alias.
    assert json.loads(stored['facts']) == finding['facts']
    assert g.accept(conn, registry, draft)['capture_id'] == acknowledgement['capture_id']

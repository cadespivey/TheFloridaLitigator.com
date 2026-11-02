"""Valid Word procedure evidence must not become a PDF-format coverage failure."""
import io
import zipfile

import httpx
import pytest

from flwu import docx_evidence as docx, source_gate as gate


def package(document=None, extras=None, content_type=docx.MAIN_MIME):
    document = document or (f'<w:document xmlns:w="{docx.WORD}"><w:body>'
        '<w:p><w:r><w:t>Chambers contact</w:t></w:r></w:p>'
        '<w:tbl><w:tr><w:tc><w:p><w:r><w:t>JA@example.gov</w:t></w:r>'
        '</w:p></w:tc></w:tr></w:tbl></w:body></w:document>')
    parts = {'[Content_Types].xml': f'<Types xmlns="{docx.TYPES}">'
             f'<Override PartName="/word/document.xml" ContentType="{content_type}"/>'
             '</Types>', 'word/document.xml': document}
    parts.update(extras or {})
    result = io.BytesIO()
    with zipfile.ZipFile(result, 'w', zipfile.ZIP_DEFLATED) as archive:
        for name, body in parts.items():
            archive.writestr(name, body)
    return result.getvalue()


def retrieve(raw, mime=docx.MIME, url='https://court.gov/procedure.pdf', status=200):
    return gate.retrieve(url, transport=httpx.MockTransport(lambda request:
        httpx.Response(status, headers={'content-type': mime}, content=raw)))


def test_word_at_pdf_url_preserves_bytes_and_extracts_body_table_and_headers():
    raw = package(extras={'word/header1.xml': f'<w:hdr xmlns:w="{docx.WORD}">'
                         '<w:p><w:r><w:t>Division A</w:t></w:r></w:p></w:hdr>'})
    meta, saved = retrieve(raw)
    assert meta['success'] is True and saved == raw
    assert meta['url'] == meta['resolved_url'] == 'https://court.gov/procedure.pdf'
    assert meta['http_status'] == 200 and meta['retrieved_at']
    text, method, links = gate.extract(saved, meta)
    assert method == 'docx-xml-text-v1' and links == []
    assert text.splitlines() == ['DOCX part: word/document.xml', 'Chambers contact',
                               'JA@example.gov', 'DOCX part: word/header1.xml', 'Division A']


@pytest.mark.parametrize('raw,mime', [
    (b'<html>Login</html>', 'text/html'),
    (b'<html>Login</html>', docx.MIME),
    (b'PK not a package', docx.MIME),
    (package(document='<not-word/>'), docx.MIME),
    (package(document='<malformed'), docx.MIME),
    (package(content_type='application/vnd.ms-word.document.macroEnabled.main+xml'), docx.MIME),
    (package(extras={'word/vbaProject.bin': b'macro'}), docx.MIME),
    (package(), 'application/pdf'),
])
def test_pdf_endpoint_still_rejects_login_invalid_macro_or_misdeclared_packages(raw, mime):
    meta, saved = retrieve(raw, mime)
    assert meta['success'] is False and meta['error'] == 'Expected PDF signature'
    assert saved == raw


def test_failure_status_is_not_promoted_by_valid_word_bytes():
    raw = package()
    meta, saved = retrieve(raw, status=403)
    assert meta['success'] is False and saved == raw


def test_malformed_docx_without_pdf_extension_is_a_failed_observation():
    meta, saved = retrieve(b'not word', url='https://court.gov/procedure.docx')
    assert not meta['success'] and meta['error'] == 'Invalid or unsupported Word document'
    assert gate.extract(saved, meta) == ('', 'unavailable', [])


def test_expansion_member_and_xml_limits_fail_closed(monkeypatch):
    raw = package()
    with monkeypatch.context() as patch:
        patch.setattr(docx, 'MAX_EXPANDED_BYTES', 10)
        assert docx.text(raw) is None
    with monkeypatch.context() as patch:
        patch.setattr(docx, 'MAX_MEMBERS', 1)
        assert docx.text(raw) is None
    with monkeypatch.context() as patch:
        patch.setattr(docx, 'MAX_XML_BYTES', 10)
        assert docx.text(raw) is None


def test_entity_definitions_are_not_expanded():
    raw = package(document=f'<!DOCTYPE x [<!ENTITY secret "not a contact">]>'
                  f'<w:document xmlns:w="{docx.WORD}"><w:body><w:p><w:r>'
                  '<w:t>&secret;</w:t></w:r></w:p></w:body></w:document>')
    assert docx.text(raw) is None


def test_utf16_entity_declarations_and_duplicate_members_fail_closed():
    xml = (f'<!DOCTYPE x [<!ENTITY secret "not a contact">]>'
           f'<w:document xmlns:w="{docx.WORD}"><w:body><w:p><w:r>'
           '<w:t>&secret;</w:t></w:r></w:p></w:body></w:document>')
    assert docx.text(package(document=xml.encode('utf-16-be'))) is None
    output = io.BytesIO(package())
    with zipfile.ZipFile(output, 'a') as archive, pytest.warns(UserWarning, match='Duplicate name'):
        archive.writestr('word/document.xml', '<different/>')
    assert docx.text(output.getvalue()) is None


def test_corrupt_deflate_stream_is_a_failed_document():
    raw = bytearray(package())
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        info = archive.getinfo('word/document.xml')
        offset = info.header_offset + 30 + len(info.filename.encode()) + len(info.extra)
    raw[offset:offset + 4] = b'\xff\xff\xff\xff'
    assert docx.text(bytes(raw)) is None


def test_official_opinions_still_require_pdf(tmp_path):
    from flwu import opinion_discovery, history
    # document_error is the independent gate used by the actual opinion queue.
    raw = package()
    with history.database(tmp_path/'opinions.sqlite') as conn:
        history.record(conn, stream='test', mode='manual_research', scope={}, run_id='word',
            payload={'status': 'incomplete', 'contract': {}, 'findings': [], 'drafts': [], 'checks': []},
            artifacts={history.sha(raw): raw})
        error = opinion_discovery.document_error(conn,
            {'success': True, 'sha256': history.sha(raw)})
    assert error == 'Expected opinion PDF; saved response is not a PDF'


def test_source_persistence_hash_reuse_and_changed_contact(tmp_path):
    from flwu import history
    url = 'https://court.gov/procedure.pdf'
    registry = {'schema_version': 1, 'stream': 'research', 'review_protocol': gate.PROTOCOL,
                'sources': [{'id': gate.source_id(url), 'url': url}]}
    raw = package()
    with history.database(tmp_path/'history.sqlite') as conn:
        history.record(conn, stream='research', mode='manual_research', scope={}, run_id='initial',
            payload={'status': 'incomplete', 'contract': {}, 'findings': [], 'drafts': [], 'checks': []},
            artifacts={})
        gate.run(conn, registry, 'one', fetch=lambda address: retrieve(raw, url=address))
        task = gate.write_queue(conn, registry, tmp_path/'queue')['tasks'][0]
        observation = task['observation']
        assert observation['success'] and observation['extraction'] == 'docx-xml-text-v1'
        assert gate.blob(conn, observation['sha256']) == raw
        review = task['review_template'] | {
            'reviewer': 'Fixture reviewer', 'review_scope': 'Body contact only',
            'summary': 'Contact captured.', 'outcome': 'baseline_reviewed',
            'support': {'reason': 'Contact is supported by acquired Word text.', 'previous': [],
                'current': [{'sha256': observation['sha256'],
                    'text_sha256': observation['text_sha256'], 'quote': 'JA@example.gov',
                    'locator': 'DOCX word/document.xml, table paragraph'}]}}
        gate.accept(conn, registry, review)
        second = gate.run(conn, registry, 'two', fetch=lambda address: retrieve(raw, url=address))
        assert not second['tasks'] and len(second['reused_reviews']) == 1
        changed = package(document=f'<w:document xmlns:w="{docx.WORD}"><w:body><w:p>'
            '<w:r><w:t>newJA@example.gov</w:t></w:r></w:p></w:body></w:document>')
        third = gate.run(conn, registry, 'three', fetch=lambda address: retrieve(changed, url=address))
        assert len(third['tasks']) == 1 and third['tasks'][0]['reason'] == 'changed'
        current = third['tasks'][0]['observation']
        assert current['previous_sha256'] == observation['sha256']
        assert gate.blob(conn, current['sha256']) == changed
        assert gate.blob(conn, current['text_sha256']).decode().endswith('newJA@example.gov')

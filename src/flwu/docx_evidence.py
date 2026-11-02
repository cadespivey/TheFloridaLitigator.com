"""Bounded OOXML text aid; never render, execute or unpack a document to disk."""
from __future__ import annotations

import io
import re
import zipfile
import zlib
import xml.etree.ElementTree as ET

MIME = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
MAIN_MIME = MIME + '.main+xml'
WORD = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
TYPES = 'http://schemas.openxmlformats.org/package/2006/content-types'
MAX_MEMBERS = 256
MAX_EXPANDED_BYTES = 20_000_000
MAX_XML_BYTES = 4_000_000
PART = re.compile(r'word/(?:document|footnotes|endnotes|header\d+|footer\d+)\.xml\Z')


def _xml(package, name):
    info = package.getinfo(name)
    if info.file_size > MAX_XML_BYTES:
        raise ValueError('DOCX XML exceeds limit')
    data = package.read(name).decode('utf-8-sig')
    if '\x00' in data or '<!DOCTYPE' in data.upper() or '<!ENTITY' in data.upper():
        raise ValueError('DOCX XML declarations unsupported')
    return ET.fromstring(data)


def text(raw):
    """Validate a nonmacro Word package and extract paragraphs in document order.

    Part labels are locators, not rendered page numbers. Images, fields and layout
    are retained in original bytes; this aid cannot establish their equivalence.
    Invalid/unsupported packages return None, never an invented empty document.
    """
    try:
        with zipfile.ZipFile(io.BytesIO(raw)) as package:
            members = package.infolist()
            names = [item.filename for item in members]
            if (len(members) > MAX_MEMBERS or len(set(names)) != len(names)
                    or sum(item.file_size for item in members) > MAX_EXPANDED_BYTES
                    or any(item.flag_bits & 1 for item in members)
                    or any(name.lower().endswith('vbaproject.bin') for name in names)):
                return None
            types = _xml(package, '[Content_Types].xml')
            if types.tag != '{' + TYPES + '}Types':
                return None
            main = [item for item in types if item.get('PartName') == '/word/document.xml']
            if len(main) != 1 or main[0].get('ContentType') != MAIN_MIME:
                return None
            document = _xml(package, 'word/document.xml')
            if document.tag != '{' + WORD + '}document':
                return None
            parts = ['word/document.xml'] + sorted(name for name in names
                        if name != 'word/document.xml' and PART.fullmatch(name))
            result = []
            for name in parts:
                root = document if name == 'word/document.xml' else _xml(package, name)
                result.append('DOCX part: ' + name)
                for paragraph in root.iter('{' + WORD + '}p'):
                    result.append(''.join(node.text or '' for node in paragraph.iter('{' + WORD + '}t')))
            return '\n'.join(result)
    except (ValueError, KeyError, OSError, RuntimeError, NotImplementedError,
            zipfile.BadZipFile, zlib.error, ET.ParseError):
        return None

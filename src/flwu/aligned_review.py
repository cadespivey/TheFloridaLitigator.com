"""Complete structural reading aid. Alignment groups changes; it never classifies them."""
from difflib import SequenceMatcher
from flwu import history as h
from flwu.content_fingerprint import _tree


def tokens(raw):
    result = []
    def visit(node):
        if isinstance(node, dict) and 'tag' in node:
            opened=dict(open=node['tag'], attrs=node['attrs'])
            if node.get('duplicate_attribute_tags'): opened['duplicate_attribute_tags']=node['duplicate_attribute_tags']
            result.append(opened)
            for child in node['children']: visit(child)
            result.append(dict(close=node['tag']))
        elif isinstance(node, list):
            for child in node: visit(child)
        else: result.append(node)
    visit(_tree(raw))
    return result


def compare(before, after, content_type):
    result = dict(schema_version=1, before_sha256=h.sha(before), after_sha256=h.sha(after), groups=[])
    if 'html' in content_type.lower():
        try: old, new = tokens(before), tokens(after)
        except (ValueError,TypeError,RecursionError,UnicodeError): old, new = [],[]
        matcher = SequenceMatcher(None, [h.sha(v) for v in old], [h.sha(v) for v in new], autojunk=False)
        for kind, a, b, c, d in matcher.get_opcodes():
            if kind == 'equal': continue
            group = dict(kind=kind, before_range=[a,b], after_range=[c,d],
                         before=old[a:b], after=new[c:d],
                         context_before=old[max(0,a-2):a], context_after=new[d:d+2])
            identified=dict(id=h.sha(group), **group)
            # Decode embedded JSON/HTML without executing scripts. This exposes
            # dates, filenames, URLs and content IDs hidden in Next.js panels.
            from flwu.raw_comparison import decoded_view
            decoded=decoded_view(dict(changes=[dict(id=identified['id'],path=['aligned_group'],
                before=group['before'],after=group['after'])]))
            identified['decoded_fields']=decoded['field_changes']
            identified['decoding_limit_paths']=decoded['decoding_limit_paths']
            result['groups'].append(identified)
    if not result['groups'] and before != after:
        # Parser equivalence is not raw equivalence. Preserve this obligation.
        group = dict(kind='original_serialization', before_sha256=h.sha(before), after_sha256=h.sha(after))
        result['groups'].append(dict(id=h.sha(group), **group))
    return result


def template(comparison, alignment):
    return dict(schema_version=2, comparison_sha256=h.sha(comparison), alignment_sha256=h.sha(alignment),
                method='', groups=[dict(id=g['id'], observed_change='', impact='', unresolved=True)
                                   for g in alignment['groups']])


def validate(review, comparison, alignment):
    if (set(review) != {'schema_version','comparison_sha256','alignment_sha256','method','groups'}
            or review['schema_version'] != 2 or review['comparison_sha256'] != h.sha(comparison)
            or review['alignment_sha256'] != h.sha(alignment)
            or not isinstance(review['method'],str) or not review['method'].strip()
            or not isinstance(review['groups'],list)):
        raise ValueError('Aligned review must bind the exact original comparison, alignment and inspection method')
    expected = [g['id'] for g in alignment['groups']]
    if [g.get('id') for g in review['groups']] != expected:
        raise ValueError('Account for every aligned change group in order; added scripts and links cannot be omitted')
    for group in review['groups']:
        if (set(group) != {'id','observed_change','impact','unresolved'}
                or any(not isinstance(group[k],str) or not group[k].strip() for k in ('observed_change','impact'))
                or group['unresolved'] is not False):
            raise ValueError('Completed aligned review needs an observed change and supported impact for every group; unresolved groups cannot prove reuse')

"""Deterministic original-content differences; never a relevance decision."""
from __future__ import annotations
import json
import re
from bs4 import BeautifulSoup, Tag, NavigableString
from flwu import history as h


def required(observation):
    return bool(observation and observation.get('previous_sha256')
                and observation.get('sha256') != observation['previous_sha256']
                and observation.get('text_sha256')
                and observation.get('text_sha256') == observation.get('previous_text_sha256'))


def html_structure(raw):
    def decoded(value):
        if isinstance(value,str):
            try:return json.loads(value)
            except (ValueError,TypeError):pass
        return value
    nodes=[]
    for node in BeautifulSoup(raw,'html.parser').descendants:
        if isinstance(node,Tag):
            nodes.append(dict(tag=node.name,attrs={k:decoded(v) for k,v in node.attrs.items()}))
        elif isinstance(node,NavigableString):
            nodes.append(dict(kind=type(node).__name__,value=decoded(str(node))))
    return nodes


def compare(before,after,content_type):
    changes=[]
    def add(path,old,new):
        item=dict(path=path,before=old,after=new)
        changes.append(dict(id=h.sha(item),**item))
    def walk(a,b,path):
        if type(a) is not type(b):add(path,a,b)
        elif isinstance(a,dict):
            for key in sorted(a.keys()|b.keys()):
                child=path+[key]
                if key not in a:add(child,{'absent':True},b[key])
                elif key not in b:add(child,a[key],{'absent':True})
                else:walk(a[key],b[key],child)
        elif isinstance(a,list):
            for index in range(max(len(a),len(b))):
                if index>=len(a):add(path+[index],{'absent':True},b[index])
                elif index>=len(b):add(path+[index],a[index],{'absent':True})
                else:walk(a[index],b[index],path+[index])
        elif a!=b:add(path,a,b)
    if 'html' in content_type.lower():
        kind='html_structure'
        walk(html_structure(before),html_structure(after),['nodes'])
        if not changes:
            add(['serialization'],{'sha256':h.sha(before)}, {'sha256':h.sha(after)})
        limitation='Parser comparison includes attributes, embedded JSON, scripts, comments and text. It is not browser rendering; inspect originals when a change needs visual or execution context.'
    else:
        kind='original_bytes'
        start=0
        while start<min(len(before),len(after)) and before[start]==after[start]:start+=1
        end=0
        while end<min(len(before)-start,len(after)-start) and before[-end-1]==after[-end-1]:end+=1
        def span(raw):
            stop=len(raw)-end
            return dict(start=start,end=stop,sha256=h.sha(raw[start:stop]),bytes=stop-start)
        add(['original_bytes'],span(before),span(after))
        limitation='Byte-span hashes do not explain significance. Inspect original documents with an appropriate parser or visual tool; unresolved non-text changes remain unfinished.'
    return dict(schema_version=1,kind=kind,before_sha256=h.sha(before),after_sha256=h.sha(after),
                changes=changes,limitation=limitation)


def template(comparison):
    return dict(comparison_sha256=h.sha(comparison),method='',
                changes=[dict(id=c['id'],reason='') for c in comparison['changes']])


def review_quality_issue(review):
    """Reject duplicated explanations, not judge semantic/legal correctness.

    Also applies when selecting already saved reviews for reuse. History remains
    immutable; a deficient receipt cannot prove content/component equivalence.
    """
    if review is None:return None
    if not isinstance(review,dict) or not isinstance(review.get('changes'),list):
        return 'Malformed original-content review'
    reasons=[]
    for item in review['changes']:
        if not isinstance(item,dict) or not isinstance(item.get('reason'),str) or not item['reason'].strip():
            return 'Every original-content change needs an explanation'
        reasons.append(' '.join(item['reason'].casefold().split()))
    if len(reasons)!=len(set(reasons)):
        return 'Repeated boilerplate change reasons are not a completed review; explain the observed difference for each change'
    return None


def validate(review,comparison):
    if not isinstance(review,dict) or set(review)!={'comparison_sha256','method','changes'}:
        raise ValueError('Changed bytes with identical extracted text require raw_change_review')
    if review['comparison_sha256']!=h.sha(comparison) or not isinstance(review['method'],str) or not review['method'].strip():
        raise ValueError('Original-content review requires the exact comparison and inspection method')
    items=review['changes']
    if (not isinstance(items,list) or any(not isinstance(v,dict) or set(v)!={'id','reason'}
            or not isinstance(v['reason'],str) or not v['reason'].strip() for v in items)
            or [v['id'] for v in items]!=[v['id'] for v in comparison['changes']]):
        raise ValueError('Explain every original-content change; identical text is insufficient')
    issue=review_quality_issue(review)
    if issue:raise ValueError(issue)


def decoded_view(comparison, *, max_depth=32):
    """Readable evidence aid; original comparison IDs and review remain authoritative.

    Parse nested HTML attributes and JSON without executing scripts, following
    links or deciding relevance. Retain unparsed values at the explicit depth cap.
    """
    limits = []
    def unique(pairs):
        if len({k for k,v in pairs})!=len(pairs):raise ValueError('Duplicate JSON key')
        return dict(pairs)
    decoder=json.JSONDecoder(object_pairs_hook=unique)
    def decode(value, path, depth):
        if depth >= max_depth:
            if isinstance(value, (dict, list, str)):
                limits.append(path)
            return value
        if isinstance(value, dict):
            return {k:decode(v, path+[k], depth+1) for k,v in value.items()}
        if isinstance(value, list):
            return [decode(v, path+[i], depth+1) for i,v in enumerate(value)]
        if not isinstance(value, str):
            return value
        stripped = value.lstrip()
        assignment=re.match(r'\s*var\s+([A-Za-z_$][\w$]*)\s*=\s*',value)
        if assignment:
            try:parsed,end=decoder.raw_decode(value[assignment.end():])
            except (ValueError,RecursionError):pass
            else:
                if isinstance(parsed,(dict,list)):
                    return dict(decoded_assignment=dict(variable=assignment[1],
                        prefix=value[:assignment.end()],value=decode(parsed,path+['assignment'],depth+1),
                        suffix=decode(value[assignment.end()+end:],path+['suffix'],depth+1)))
        if stripped.startswith(('{', '[')):
            try:
                parsed = json.loads(value)
            except (ValueError, RecursionError):
                pass
            else:
                return {'decoded_json': decode(parsed, path+['decoded_json'], depth+1)}
        if stripped.startswith('<'):
            parsed = html_structure(value)
            if any('tag' in node for node in parsed):
                return {'decoded_html': decode(parsed, path+['decoded_html'], depth+1)}
        return value
    changes = []
    for item in comparison['changes']:
        changes.append(dict(id=item['id'], path=item['path'],
                            before=decode(item['before'], [item['id'], 'before'], 0),
                            after=decode(item['after'], [item['id'], 'after'], 0)))
    fields=[]
    def difference(a,b,path,origin):
        if type(a) is type(b) and isinstance(a,dict):
            for key in sorted(a.keys()|b.keys()):
                if key not in a or key not in b:
                    fields.append(dict(original_change_id=origin,path=path+[key],
                                       before=a.get(key,{'absent':True}),after=b.get(key,{'absent':True})))
                else:difference(a[key],b[key],path+[key],origin)
        elif type(a) is type(b) and isinstance(a,list):
            for index in range(max(len(a),len(b))):
                if index>=len(a) or index>=len(b):
                    fields.append(dict(original_change_id=origin,path=path+[index],
                        before=a[index] if index<len(a) else {'absent':True},
                        after=b[index] if index<len(b) else {'absent':True}))
                else:difference(a[index],b[index],path+[index],origin)
        elif a!=b or type(a) is not type(b):
            fields.append(dict(original_change_id=origin,path=path,before=a,after=b))
    for item in changes:difference(item['before'],item['after'],item['path'],item['id'])
    return dict(schema_version=1, comparison_sha256=h.sha(comparison),
                changes=changes, decoding_limit_paths=limits,
                field_changes=fields,
                limitation='Decoded inspection aid only. Original comparison and bytes remain authoritative. '
                'HTML parsing is not rendering; no scripts or links were executed. '
                'No relevance or timestamp-causation determination is made. '
                'Depth-limited values remain unmodified and require original inspection.')

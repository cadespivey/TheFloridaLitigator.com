"""Reader-focused news checks and exact-issue exclusion projections.

Research findings, conflicts and completion states remain in evidence records.
This does not decide legal significance or replace source/citation validation.
"""
import copy
import json
from datetime import datetime

from flwu.publication import digest

PROCESS_PHRASES=('research is incomplete','source coverage is incomplete',
    'missing findings do not establish','documented difference between official-source compilations',
    'both statements are retained without deciding which source controls')


def validate_news_text(text):
    folded=' '.join(text.casefold().split())
    if any(phrase in folded for phrase in PROCESS_PHRASES):
        raise ValueError('Public news must describe the supported legal/procedural change and practical effect; keep research-process notes internal')


def validate_change(candidate,citations):
    if candidate['section']=='case_law':return
    analysis=candidate.get('change_analysis')
    required={'material','previous_requirement','current_requirement','practical_effect','basis_quote'}
    if (not isinstance(analysis,dict) or set(analysis)!=required or analysis['material'] is not True
            or any(not isinstance(analysis[k],str) or not analysis[k].strip() for k in required-{'material'})):
        raise ValueError('Included statute/rule news requires change_analysis: material=true, previous_requirement, current_requirement, practical_effect, basis_quote; exclude inconsequential/source-only differences')
    if ' '.join(analysis['previous_requirement'].casefold().split())==' '.join(analysis['current_requirement'].casefold().split()):
        raise ValueError('An unchanged requirement is not a material legal update')
    if not any(analysis['basis_quote'] in cite.get('quote','') for cite in citations):
        raise ValueError('Change analysis must identify an exact quotation in the acquired publication evidence')
    validate_news_text(candidate['summary'])


def project(archive,issues):
    """Exclude specifically reviewed non-news entries; preserve original archives."""
    folder=archive/'editorial'
    if folder.is_symlink():raise ValueError('Editorial directory symlinks are not permitted')
    by_id={issue['id']:issue for issue in issues};seen=set();result=copy.deepcopy(issues)
    for path in sorted(folder.glob('*.json')):
        if path.is_symlink():raise ValueError('Editorial record symlinks are not permitted')
        record=json.loads(path.read_text())
        if (not isinstance(record,dict) or set(record)!={'issue_id','content_sha256','excluded_items','reviewer','reviewed_at'}
                or not isinstance(record['excluded_items'],list) or not record['excluded_items']
                or not isinstance(record['reviewer'],str) or not record['reviewer'].strip()):
            raise ValueError('Invalid editorial exclusion record')
        original=by_id.get(record['issue_id'])
        if not original or original['content_sha256']!=record['content_sha256'] or record['issue_id'] in seen:
            raise ValueError('Editorial exclusion must bind once to an existing exact issue')
        when=datetime.fromisoformat(record['reviewed_at'].replace('Z','+00:00'))
        if when.tzinfo is None:raise ValueError('Editorial review requires a timezone')
        seen.add(record['issue_id']);ids=[]
        existing={item['id'] for section in original['sections'].values() for item in section['items']}
        for item in record['excluded_items']:
            if (not isinstance(item,dict) or set(item)!={'id','reason'} or item['id'] not in existing
                    or not isinstance(item['reason'],str) or not item['reason'].strip()):
                raise ValueError('Editorial exclusion requires an existing item and specific internal reason')
            ids.append(item['id'])
        if len(ids)!=len(set(ids)):raise ValueError('Duplicate editorial item exclusion')
        issue=next(v for v in result if v['id']==record['issue_id'])
        for section in issue['sections'].values():section['items']=[i for i in section['items'] if i['id'] not in ids]
        # Reader projection has its own content checksum. Original capture/report,
        # reporting dates and archive bytes are unchanged; no report is finalized.
        issue['content_sha256']=digest({k:v for k,v in issue.items() if k!='content_sha256'})
    return result

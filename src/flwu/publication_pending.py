"""Explicit accounting for unfinished work in the pinned acquisition queue."""
from flwu import history as h


def pending(queue):
    sources = queue.get('source_reviews')
    opinions = queue.get('opinion_reviews')
    discovery = queue.get('discovery')
    if not all(isinstance(x, dict) for x in (sources, opinions, discovery)):
        raise ValueError('Standard update snapshot lacks source/opinion/discovery queues')
    result = {}

    def add(kind, task, unavailable=False, hashes=()):
        identity = kind + ':' + h.sha(task)
        result[identity] = {'task': task, 'unavailable': unavailable,
                            'hashes': {x for x in hashes if x}}

    for task in sources['tasks']:
        add('source', task, task['reason'] in ('retrieval_failed', 'not_fetched'),
            [(task.get('observation') or {}).get('sha256')])
    for task in opinions['tasks']:
        add('opinion', task, bool(set(task['reasons']) &
            {'official_status_source_unavailable', 'opinion_download_unavailable'}),
            [(task.get('source_observation') or {}).get('sha256'),
             task['opinion'].get('status_source', {}).get('sha256')])
    for task in sources['effective_date_tasks']:
        add('effective_date', task)
    for url in sources['unregistered_previous_sources']:
        add('unregistered_source', {'url': url})
    for court in discovery['courts']:
        if not court['complete']:
            add('listing_failure', court, True)
    for key in ('detail_failures', 'tracked_identity_failures'):
        for failure in discovery[key]:
            add(key, failure, True)
    return result


def template(queue):
    return [{'task_id': key, 'decision': '', 'reason': '', 'citations': []}
            for key in pending(queue)]


def validate(queue, dispositions, index):
    expected = pending(queue)
    if not isinstance(dispositions, list) or any(not isinstance(d, dict) for d in dispositions):
        raise ValueError('Pending acquisition tasks require explicit dispositions')
    ids = [d.get('task_id') for d in dispositions]
    if (any(not isinstance(key, str) for key in ids) or len(ids) != len(set(ids))
            or set(ids) != set(expected)):
        raise ValueError('Every pending acquisition task requires exactly one disposition')
    for disposition in dispositions:
        if set(disposition) != {'task_id', 'decision', 'reason', 'citations'}:
            raise ValueError('Use the generated pending-task disposition fields')
        task = expected[disposition['task_id']]
        if not isinstance(disposition['reason'], str) or not disposition['reason'].strip():
            raise ValueError('Pending-task disposition requires a substantive explanation')
        citations = disposition['citations']
        if not isinstance(citations, list):
            raise ValueError('Pending-task citations must be a list')
        for cite in citations:
            index.validate(cite)
            if not cite.get('quote'):
                raise ValueError('Pending-task exclusion requires quoted evidence')
        if disposition['decision'] == 'unavailable':
            supplemental_failure = (disposition['task_id'].startswith('unregistered_source:')
                                    and index.unavailable(task['task']['url']))
            if not task['unavailable'] and not supplemental_failure:
                raise ValueError('Available unreviewed evidence cannot be marked unavailable')
        elif disposition['decision'] == 'scope_excluded':
            if not citations:
                raise ValueError('Scope exclusion requires acquired cited support')
            if task['hashes'] and not any(c['sha256'] in task['hashes'] for c in citations):
                raise ValueError('Scope exclusion must cite the pending task source')
        else:
            raise ValueError('Finish the review and refresh the queue, or record supported scope_excluded/unavailable')

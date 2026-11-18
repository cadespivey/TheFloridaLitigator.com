"""Task-local research limits; editorial instructions never change evidence gates."""


def source_role(url):
    from urllib.parse import urlsplit
    parsed=urlsplit(url);host=parsed.hostname or '';path=parsed.path.lower()
    if host in ('flrules.org','www.flrules.org'):
        return dict(kind='administrative_rulemaking',instruction='Florida Administrative Code/Register, not court procedural rules. Briefly screen for an actual civil/commercial change; draft development notices are follow-up/discovery unless an adopted change is separately supported.')
    if host=='www.flsenate.gov' and path.startswith('/session/bills'):
        return dict(kind='legislation_discovery',instruction='Pending-bill listing/discovery. Screen briefly for an enacted in-scope change or existing observation; do not analyze every pending bill or generate technical receipt loops.')
    if host=='flcourts-media.flcourts.gov' and path.startswith('/_search/opinions'):
        return dict(kind='opinion_discovery',instruction='Reconcile official entry identities/status with mandatory discovery. Feed metadata is not a holding or a legal update; substantive summaries belong to opinion tasks.')
    if '/statutes' in path:
        return dict(kind='statutory_comparison',instruction='Retain the full compilation; interpret supported changes relevant to civil/commercial practice. A changed index/filter is not an amendment.')
    return dict(kind='court_or_other_source',instruction='Use the source title and acquired content to identify the actual contact, procedure or legal change; do not infer significance from the host alone.')


def guidance(kind):
    task_notes = {
        'source_review':
            'Interpret only the returned source changes and their supported prior findings. '
            'For an out-of-scope change, use the existing source-review outcome and cited '
            'reason; do not delete retained findings or invent a scope_excluded outcome.',
        'opinion_review':
            'Screen civil/commercial relevance first. Relevant opinions need a concise '
            'cited holding, disposition and author names. Do not investigate the underlying '
            'lawsuit or specialized criminal/family merits.',
        'publication_mapping':
            'Use decision exclude with candidate null for an out-of-scope finding, with '
            'a short cited reason. Preserve supported personnel projections separately '
            'when needed. Do not rewrite an accepted opinion summary at mapping time.',
        'directory_review':
            'Finish this person: contacts, assignment, official procedure links and a short '
            'practical civil operating checklist. Noncivil assignments need only contacts, '
            'assignment, links and basic scheduling/submission/appearance instructions. '
            'Do not expand into motion recipes or every linked form/calendar.',
        'directory_removal':
            'Review only the named entry and supplied departure/scope evidence. '
            'Preserve unaffected people and assignments in other counties. An omitted '
            'name alone is not a departure; do not investigate individual litigation.',
        'coverage_review':
            'Use scope_excluded only for a supported scope exclusion. Use unavailable '
            'for a real saved failure; missing in-scope evidence is not no-change. '
            'A scope exclusion never authorizes fabricating successful retrieval.',
        'roster_review':
            'Check supplied named membership, assignments and supported removals. '
            'Do not restart county collection or infer departure from an omitted name.',
        'publication_acceptance':
            'Review the current report and affected directories for supported, concise '
            'updates. Do not audit historical reports. Documented conflicts and intentional '
            'nonreview of out-of-scope detail do not require further substantive research.',
    }
    return dict(
        policy_path='docs/workflow/RESEARCH_SCOPE.md',
        purpose='Identify and briefly summarize Florida case law, statutes, bar rules, '
                'court procedural rules and judicial-system personnel changes relevant '
                'to civil litigators, prioritizing commercial litigation.',
        instructions=[
            'Code compares source hashes and official statuses before model review. '
            'Do not reopen reused_reviews or completed machine mappings. Source changes '
            'alone do not establish a legal change.',
            'Before another search, identify the in-scope actual change or missing '
            'personnel/practical operating field it will answer. Stop when supported.',
            'Pending bills, rulemaking processes and general agency regulation need '
            'only brief screening or status verification for an actual in-scope change. '
            'No exhaustive proposal, regulatory, form, penalty-schedule or litigation-merits research.',
            'Preserve the entire statutes corpus, full requested roster and collected '
            'originals. Retention does not require full substantive review. Keep documents '
            'collected, content reviewed and conflicts recorded distinct.',
            'Preserve conflicting official statements with their sources and dates; '
            'do not decide which controls or block publication solely for that conflict. '
            'Missing in-scope evidence and inaccurate records still require attention.',
            'Keep pinned dates, registry, contracts, evidence and receipt schemas unchanged. '
            'Use this task\'s exact template, save path and submit command. This guidance '
            'is not a receipt field and does not waive evidence or publication validation.',
        ],
        task_instruction=task_notes.get(kind, 'Apply the bounded scope and exact returned task contract.'),
    )


def attach_scope(conn, config, state, *, resume=False, expansion=False):
    """Project current scope from the pinned contract and the selected next state."""
    import json
    from pathlib import Path
    from flwu import history, workflow

    if workflow.review_protocol(conn, config) < 2:
        return state
    phase = state['phase']
    progress = state.get('review_progress', {})
    completed = progress.get('saved_review_decisions', 0)
    failures = progress.get('failed_short_answers', 0)
    checkpoints = progress.get('checkpointed_reviews', 0)
    stop = 'publication_complete' if config['mode'] == 'publish' else 'preview_complete'
    remaining = dict(sources=progress.get('remaining_source_reviews'),
                     opinions=progress.get('remaining_opinion_reviews'), checkpoints=checkpoints)
    window = [config['start'], config['end']]
    if window[0] is None:
        from flwu import opinion_discovery
        row = conn.execute("SELECT json_extract(payload,'$.opinion_discovery.bounds.start') FROM captures "
                           "WHERE stream=? AND json_extract(payload,'$.opinion_discovery.run_id')=? "
                           "AND json_extract(payload,'$.opinion_discovery.checkpoint')='update-contract' LIMIT 1",
                           (opinion_discovery.stream_for(config['registry']['stream'])[0], config['run_id'])).fetchone()
        if row:window[0] = row[0]
    stages = ['acquire', 'review', 'project', 'verify', 'preview']
    if config['mode'] == 'publish':stages.append('release')
    capsule = dict(version=1, objective='Review and report Florida civil litigation developments',
                   reporting_window=window, mode=config['mode'], authorized_stages=stages,
                   stage=phase, task=state.get('task_handle') or state.get('identity'),
                   action=state.get('command') or state.get('next_command'), remaining=remaining,
                   closed=dict(reviews=completed, accepted_evidence='workflow/accepted/'),
                   exclusions='Historical audits and additional acquisition require a named in-scope gap.',
                   stop=stop)
    waivers = workflow.events(conn, config, kinds=('directory_identity_verification_waiver',))
    capsule['identity_waivers'] = [history.sha(event) for event in waivers]
    marker = dict(phase=phase, completed=completed, failures=failures,
                  checkpoints=checkpoints, task=capsule['task'], expansion=expansion)
    previous = workflow.events(conn, config, kinds=('scope_reminder',))
    last = previous[-1]['marker'] if previous else {}
    interval = config.get('scope_reminder_interval', 20)
    due = (resume or expansion or phase != last.get('phase')
           or completed - last.get('completed', 0) >= interval
           or (failures > last.get('failures', 0) and checkpoints > 0))
    result = dict(state, scope=capsule)
    if due and all(event['marker'] != marker for event in previous):
        workflow.record(conn, config, dict(kind='scope_reminder', version=1, marker=marker))
        result['scope_reminder'] = (
            'Use the returned task and saved decisions. Reopen only a named defect, material gap, '
            'conflict or changed dependency. Obtain approval before expanding scope. '
            'Stop at ' + stop + '.')
    projection = Path(config['run_dir']) / 'workflow' / 'current-scope.json'
    if not projection.is_file() or projection.read_bytes() != (
            json.dumps(capsule, indent=2, ensure_ascii=False, sort_keys=True) + '\n').encode():
        workflow.write(projection, capsule)
    return result

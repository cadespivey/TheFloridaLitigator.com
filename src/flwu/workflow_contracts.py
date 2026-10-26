"""Small task-local contracts, not an alternative validation implementation."""


def schema(template):
    """Describe fixed receipt keys; domain validators enforce evidence semantics."""
    if isinstance(template, dict):
        return dict(type='object', required=list(template), additionalProperties=False,
                    properties={k:schema(v) for k,v in template.items()})
    if isinstance(template, list):
        return dict(type='array', items=schema(template[0]) if template else {})
    if isinstance(template, bool):return dict(type='boolean')
    if isinstance(template, int):return dict(type='integer')
    if template is None:return {}  # Optional candidate/target IDs have task-specific rules.
    return dict(type='string')


def contract(kind, template):
    result=schema(template)
    # Collections whose members are model-authored carry explicit example shapes
    # in the task notes; these descriptions never relax the runtime validators.
    notes={
        'source_review': [
            'Copy receipt_template and edit its existing fields; do not invent outcome names or add fields. Read this output_contract before drafting.',
            'reviewer identifies the actual reviewing model from launcher/preflight evidence. Never infer cloud/local identity from the Codex client name. If unavailable, state model identity unavailable rather than guessing.',
            'support.current/previous members have exactly sha256, text_sha256, quote, locator. Preserve prefilled quotes and hashes; fill only blank quotes/locators from acquired text. Prefilled quotes require your substantive review, not retyping.',
            'findings members: key (stable string), kind, facts (complete object), citations (array), expected_version (prior_findings value or null for new).',
            'Finding citation: url, sha256, text_sha256, retrieved_at copied from observation; quote and locator from acquired text; http_status copied when present.',
            'updated_findings requires findings. baseline_reviewed and no_relevant_change require an empty findings list. Changed bytes require updated_findings or supported no_relevant_change.'
        ],
        'opinion_review': [
            'citations members: sha256, text_sha256, quote, locator, using source_observation or status_source. No invented hashes.',
            'relevance: relevant, not_relevant, or uncertain. Relevant requires summary, holding, disposition, authors (names only) and cited opinion text.',
            'uncertain does not complete screening; resolve uncertainty from the saved evidence or report the specific missing evidence.'
        ],
        'publication_mapping': [
            'decision: include, include_directory, exclude. include requires candidate with section, title, summary; opinion fields must equal accepted review.',
            'include_directory and exclude require candidate:null. Preserve exact source facts for include_directory.',
            'inventories/personnel members: key, kind, facts, citations. Inventory kind=source_inventory; facts.entities members: id (without person-), name, type (judge/clerk), counties, citation.',
            'Personnel key=person-<entity id>; kind=judge/clerk; facts.name, facts.fields contact objects with value/status/citation; optional facts.procedure and facts.governing_rules. Preserve all existing facts.',
            'removals members: person_id, reason, citations. Explicit departure evidence and corresponding named roster reconciliation required; omission is not removal.'
        ],
        'directory_review': [
            'targets members have exactly path and id. path must be one of inputs.scopes; id is an existing target ID or null for a new entry.',
            'identity_citations use full acquired citations. Existing county-specific assignments and unaffected people remain intact.'
            ,'assignment_updates members: path, value (new assignment text), reason, citations. Leave empty to preserve current assignments. Quoted evidence must name the person and assignment.'
        ],
        'coverage_review': ['decision is unavailable only for an unavailable task; scope_excluded requires acquired support. A failure is never no-change.'],
        'roster_review': ['Keep exact named people/removals. Fill substantive reason and supporting citation/removal reasons; do not invent names.'],
        'publication_acceptance': ['Change only reviewer, legal_review and visual_review after inspecting supplied report/site. Actual acceptance is separately validated.'],
    }
    # Candidate and citation objects can have domain-permitted optional fields.
    if kind=='publication_mapping':result['properties']['candidate']={}
    choices={
        'source_review': ('outcome', ['baseline_reviewed', 'no_relevant_change', 'updated_findings']),
        'opinion_review': ('relevance', ['relevant', 'not_relevant', 'uncertain']),
        'publication_mapping': ('decision', ['include', 'include_directory', 'exclude']),
        'coverage_review': ('decision', ['unavailable', 'scope_excluded']),
    }
    if kind in choices:
        field, values=choices[kind]
        result['properties'][field]['enum']=values
    return dict(receipt_schema=result, field_guidance=notes.get(kind,[]),
                validation='The submit command enforces task identity, acquired evidence, versions and domain rules; this schema describes the envelope.')

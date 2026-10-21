import json, hashlib, shutil, copy
from pathlib import Path
from flwu.history import now
p = Path(__file__).parent
oldroot = Path('/Users/cadespivey/florida-litigator-weekly-update')
old = json.loads((oldroot/'runs/county-st-lucie/2026-10-19/draft/checkpoint-025.json').read_text())
prior = next(f for f in old['payload']['findings'] if f['key'] == 'st-lucie-kameisha-presley')
c = copy.deepcopy(prior['citations'][0])
for field, hashfield, name in [('path', 'sha256', 'reused-profile.html'), ('text_path', 'text_sha256', 'reused-profile.txt')]:
    src = oldroot/c[field]
    assert hashlib.sha256(src.read_bytes()).hexdigest() == c[hashfield]
    shutil.copy2(src, p/name)
    c.pop(field)
c['locator'] = 'Presley profile: contact header, Indian River routing and basic operating instructions; original October 19 capture reused'
r = json.loads((p.parent/'initial-roster-astra/source-citation.json').read_text())
r.update(quote='Kameisha Presley', locator='October 20 Indian River filtered roster: Presley card')
d = copy.deepcopy(json.loads((p.parent/'cox-astra/reviewed-person.json').read_text())['citations'][2])
d.update(quote='Sara Paavola', locator='June 5 directory, page 5, Presley row')
ai = copy.deepcopy(json.loads((p.parent/'griffin-astra/reviewed-person.json').read_text())['citations'][2])
facts = dict(
    county='indian_river', circuit=19, name='Kameisha Presley', role='Child Support Hearing Officer',
    profile_url=c['url'], procedure_url=c['url'],
    assignment='Child Support Enforcement Hearing Officer; all circuit counties, family.',
    reviewed_at=now(), reviewed_by='Astra', review_status='reviewed',
    contact=dict(phone='(772) 462-1415', fax=None,
        office_address=['218 South Second Street', 'Fort Pierce, FL 34950'],
        assistant_name='Sarah Paavola', assistant_phone='(772) 462-1415', assistant_email=None,
        county_email='IRCHO@circuit19.org',
        contact_note='IRCHO@circuit19.org is the shared Indian River routing address, not a separately identified personal assistant email. June 5 directory spells the assistant’s first name Sara; profile spells Sarah.'),
    procedure_checklist={
        'chambers_communications': dict(status='reviewed', summary='Copy all parties and include the case style. Use the original email thread, avoid duplicates and name attachments descriptively. No ex parte messages.'),
        'hearing_scheduling': dict(status='reviewed', summary='Coordinate by assistant email; no online calendar. File the motion first; it must be visible in the clerk file or attached as a timestamped copy. File and serve notice immediately after reservation; notify the assistant and file/serve notice when cancelling.'),
        'proposed_orders': dict(status='reviewed', summary='Attorney cases: email Word orders using the office template, available on request, two business days before the hearing. Identify agreed orders in title and email.'),
        'courtesy_copies': dict(status='reviewed', summary='Indian River routing: IRCHO@circuit19.org. Hearing documents/exhibits due three business days before the hearing. The saved Presley profile has no separate courtesy-copy section; do not import the vacant office’s five-business-day deadline.'),
        'remote_appearances': dict(status='reviewed', summary='Request remote appearance by motion. The approving order supplies Zoom access; include the credentials and ADA notice in the hearing notice.'),
        'noncivil_substantive_procedures': dict(status='not_reviewed', summary='Child-support merits, enforcement sanctions and specialized forms are outside the commercial civil focus. Official links retained.')},
    summary='Circuit-wide child-support officer with Indian River routing. Contacts and basic operations reviewed; assistant-name spelling and AI notice discrepancy preserved.',
    stated_dates=dict(profile_revision=None, original_retrieval=c['retrieved_at'], directory_revision='2026-06-05'),
    conflicts=[dict(subject='Assistant first-name spelling', statements=['Profile: Sarah Paavola', 'June 5 directory: Sara Paavola'], disposition='Preserve both source statements without silently normalizing.'),
        dict(subject='AI notice', statements=['Saved profile includes AI disclosure/certification paragraph', 'Collected AO2026-06 expressly rescinds AO2025-10 effective June 15, 2026, signed June 16'], disposition='Preserve discrepancy without determining controlling authority.')],
    gaps=['No fax or separately identified personal assistant email in reviewed sources.'],
    review_scope=dict(collected='Full October 19 profile original/text reused; October 20 roster, June 5 directory and AI rescission order already collected.', content_reviewed='Contact header, assignment, Indian River routing and basic communications, scheduling, submissions and remote appearance. Relevant directory row and rescission reused.', not_reviewed='Child-support merits, sanctions, specialized forms and detailed exhibit policy. Collection does not imply full substantive review.'),
    procedure_links=[dict(text=l['label'], url=l['url']) for l in prior['facts']['official_links']],
    reuse=dict(prior_entity='st-lucie-kameisha-presley', prior_checkpoint=7337, hashes_verified=True, limitation='Original includes staging footer; original official URL and acquisition metadata retained. No fresh profile capture claimed.'))
(p/'reviewed-person.json').write_text(json.dumps(dict(key='indian-river-kameisha-presley', kind='person', facts=facts, citations=[c,r,d,ai]), indent=2)+'\n')

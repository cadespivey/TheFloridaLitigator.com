"""Stage the bounded editorial fixture in a disposable run for the invoking model."""
import argparse
import hashlib
import json
from pathlib import Path
import sqlite3
from unittest.mock import patch

from flwu import history, review_transport, workflow
from tests.test_inline_review_integration import source_answer
from tests.test_opinion_discovery import Server, opinion, pdf_bytes
from tests.test_workflow import environment

# Positions in normalized extracted text, checked against the immutable source digest.
CASES = [
    ('Fernandez', '2931600fb3430581d205f7c4ef5fac51c04790480694f4bc029ca71bac348420',
     [('While we doubt', 'missed mortgage payments.'), ('Reversed and remanded . SILBERMAN', 'SILBERMAN, Judge, Dissenting')]),
    ('Haddad', 'c1bd9476ec43537790391776903c38522f86ad258057dce09532585b3aac78ad',
     [('substitute this opinion', 'in its place.'), ('We accordingly assume', 'for another day.')]),
    ('Taplin Falls', '5294522361a3ec56cacb9c67633727e3e26a90b0b02c28dbf91c4a0d19f49ccc',
     [('The trial court struck', 'fees and costs on the merits.'), ('Because rule 1.530', 'Rule 1.540(a)')])
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('folder', type=Path)
    parser.add_argument('--originals', type=Path, required=True)
    parser.add_argument('--replay', type=Path, help='Use recorded cloud answers on the candidate')
    parser.add_argument('--result', type=Path)
    args = parser.parse_args()
    if bool(args.replay) != bool(args.result):
        parser.error('--replay and --result are used together')
    conn = sqlite3.connect(args.originals.resolve().as_uri()+'?mode=ro', uri=True)
    sources = []
    for name, digest, spans in CASES:
        raw = conn.execute('SELECT bytes FROM artifacts WHERE sha256=?',(digest,)).fetchone()[0]
        assert hashlib.sha256(raw).hexdigest() == digest
        text = ' '.join(raw.decode().split())
        excerpts = []
        for start, end in spans:
            a = text.index(start)
            b = text.index(end, a)+len(end)
            excerpts.append(text[a:b])
        sources.append(dict(name=name,text_sha256=digest,passages=excerpts))
    conn.close()
    args.folder.mkdir(exist_ok=False)
    workflow.write(args.folder/'fixture.json', sources)
    class SavedExcerpts(Server):
        def __init__(self, _):
            super().__init__([opinion(i) for i in range(1,4)])
            self.pdfs = {}
            for i, source in enumerate(sources,1):
                body=' '.join(source['passages'])
                if i==3:
                    body += ' Supplied comparison rule in this test: the ordinary deadline is fifteen days. Timely pending motions may affect the deadline.'
                body=body.replace('’',"'").replace('“','"').replace('”','"').replace('(','\\(').replace(')','\\)')
                self.pdfs[i]=pdf_bytes(body)
        def __call__(self,url):
            meta,raw=super().__call__(url)
            if '/content/download/' in url:raw=self.pdfs[int(url.split('/content/download/')[1].split('/')[0])]
            return meta,raw
    with patch('tests.test_workflow.Server',SavedExcerpts):
        run,db,_,_=environment(args.folder)
    state=review_transport.next_task(run)
    # These seed answers plant the named content defects for the verification role.
    # The opinion with the supplied deadline conflict is left to the invoking model.
    while state['phase']=='source_review' or (state['phase']=='opinion_review' and
                                               state['review_card']['opinion']['case_number']!='2026-3'):
        value=source_answer()
        if state['phase']=='opinion_review':
            number=state['review_card']['opinion']['case_number']
            text=('The panel held that a registry deposit is always essential to tender.' if number=='2026-1' else
                  'The substituted opinion assumed the motor-vehicle nexus for this case and expressly left the question open.')
            value=dict(relevance='relevant',summary=text,holding=text,authors=[],disposition='Reversed and remanded.' if number=='2026-1' else 'Substituted opinion.', evidence=['C1'])
        folder=run/'agent-steps'/state['task_handle'];folder.mkdir(parents=True,exist_ok=True)
        path=folder/'answer.json';workflow.write(path,value)
        state=review_transport.reply(run,state['task_handle'],path)
    assert state['phase']=='opinion_review'
    if not args.replay:
        print(json.dumps(dict(command=state['command'],card=state['review_card'],scope=state['scope']),indent=2))
        return
    previous = workflow.read(args.replay)
    assert previous['fixture'] == sources
    observed = []
    for value in previous['submitted']:
        card = state['review_card']
        observed.append(dict(phase=state['phase'], entries=[entry['ref'] for entry in card.get('entries', [])]))
        path = run/'agent-steps'/state['task_handle']/'answer.json'
        workflow.write(path, value)
        state = review_transport.reply(run, state['task_handle'], path)
    assert state['phase'] == 'preview_complete' and not state['publication_performed']
    with history.database(db) as conn:
        events = workflow.events(conn,workflow.load(run))
        proof = next(e['task']['inputs']['campaign'] for e in events if e['kind']=='decision'
                     and e['task']['kind']=='publication_acceptance')
    assert sorted(proof['verification_status'].values()) == ['individually_verified','reused','reused']
    workflow.write(args.result, dict(source=args.replay.name, cards=observed, final_phase=state['phase'],
                   publication=False, policy=proof['policy'], status=proof['verification_status']))
    print(observed, state['phase'])

if __name__=='__main__':
    main()

# Smaller-model repair: reduce the job, not just the file size

November 9, 2026. This supersedes the expanded implementation proposal in
`STRUCTURED_REVIEW_IMPROVEMENTS.md`. The replacement interface below is a design
for a small pilot, not a new active receipt schema.

## What the trial established

The same BF16 model, 20 original/extracted sources and baseline subset took
91m56s instead of 56m04s. Tool calls increased from 47 to 90; output tokens
increased from 26,986 to 40,348. Cached cumulative input is not unique evidence
volume, so its 2.86x increase alone does not explain runtime. The model still
made interpretive errors and corrupted a prefilled quotation. Typed clerk output
did improve and passed the directory-record validator.

The design mistake was giving a smaller model more orchestration: manifests,
fragment chains, old/new guide layers, citation assembly and reader scripts.
Smaller files did not make those jobs simpler. More detailed warnings did not
reliably prevent unsupported explanations.

There was also a specific code overreach: `workflow.materialize` upgraded all
changed HTML to mandatory aligned/raw review. Tasks 02 and 05 had no raw-review
basis and no raw-review field in the gate's original template. The guide added
that requirement. The narrow repair restores the gate's decision; it does not
waive required same-text raw review or change accepted history.

## Keep, remove, defer

| Keep | Stop expanding | Defer until a pilot proves useful |
| --- | --- | --- |
| Existing hash/status gates, originals, exact citations, version guards, typed person validation | Fragment navigation as a design goal; repeated policy reading; model-written parsers; full-record/citation retyping | Universal website field extraction, statewide source-recipe catalogs, new identity graphs and broad receipt/schema migrations |

**Generated receipts are useful only as hidden plumbing.** Code should preserve
the existing template's identity, hashes, exact quotes and version fields. The
model should not learn another receipt language or calculate identifiers.

**Field differences are useful only where reliable structured data already
exists.** Reuse existing text/decoded comparisons and verified field extractors.
Do not build a universal semantic parser for inconsistent court websites merely
to manufacture field differences. Unknown structure remains an explicit problem,
not an empty roster, missing contact or no-change finding.

## Proposed smaller interface

1. Code acquires, hashes, reuses completed reviews and prepares the evidence.
2. The model receives one self-contained task: one question, relevant before/after
   passages with short local references, and one short answer shape. No manifest
   traversal, source-code inspection, parser writing or repeated manual reading.
3. The model returns a decision, one or two supported sentences and the supplied
   evidence references. Add only the few domain fields the particular task needs.
   It may say evidence is insufficient; it must not invent an explanation.
4. Code inserts exact evidence and readonly metadata into the existing receipt,
   validates it, persists it and returns the next task. Code reports saved paths,
   counts and failures. It never invents the model's factual or relevance decision.

For a clerk change, ask who changed and what date/meaning the source states.
Do not request education, career history, CMS explanations or a theory of URL
routing. Opinion/rule analysis needs its own small task; this source-only trial
does not establish that those analyses work.

The regular research model should not be expected to adjudicate unfamiliar
JavaScript, opaque security tokens or parser failures. A future dispatcher should
separate technical maintenance from court-fact analysis. Such cases must retain
their unresolved evidence/status; routing them away is not permission to certify
no change, finalize an incomplete run or advance its baseline. That routing is
not implemented by the present narrow repair.

## Prove the interface before expanding it

Use the existing acquired evidence, with no production writes or publication.
First test two ordinary factual changes and one ambiguous/unsupported case.
Include an unseen example so this is not an answer template for one clerk.
Use the same selected model/settings; do not change the inference server.

Acceptance: one normal task card plus one answer submission; no model-written
scripts, hashes or citation objects; exact quotation preservation; correct date
meaning; no unsupported causal story; explicit uncertainty where required.
Measure total time, model output and tool calls, as well as accuracy. Then run
the full 20-source comparison. If it does not improve those results, stop and
revise; do not add more instructions or launch another long run by default.

The offline task-card illustrations under
`runs/simple-model-reconsideration-20261109/` are design examples only. They
use the real supplied text differences: about 1.6 KB for task 02 and 4.0 KB for
task 05, versus 32–39 KB entry guides plus linked evidence. They are not executable
receipts or a measured model speed/accuracy result. Original-content-only cases
are shown as unresolved technical work, not counted as completed research.

## Narrow repair evidence

The full suite passes 1,249 tests. The new regression test fails when the old
promotion is restored and passes with the correction. Read-only materialization
of the four real trial tasks confirms raw review remains for 01/11 and is no
longer imposed on 02/05; optional original comparisons remain available. No model
call, production write or new performance claim was needed for that check.

The skill entry is reduced from 454 lines to fewer than 120, with phase details
in lookup references. Repository AGENTS.md is reduced from 400 lines to 105;
the previous accumulated/legacy text is archived, not loaded by default.
A separate offline copy experiment
replaced the already-prefilled support objects in the failed clerk draft from its
authoritative template: all three whitespace-corrupted quotes became exact while
every model decision/finding stayed unchanged. This supports a small hidden
receipt adapter, not a broad schema framework. It does not fix semantic errors or
prove that the proposed interface is faster. The adapter is not implemented yet.

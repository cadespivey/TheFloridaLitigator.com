# CI runtime security — October 24, 2026

The published site is static HTML/CSS/browser JavaScript on GitHub Pages.
The repository has no PHP application, Composer manifest, Node server or npm
application dependency manifest. Node is used by GitHub Actions on hosted runners.
This review does not cover unrelated software installed on a developer machine.

The Pages v4 upload composite referenced a Node20 upload-artifact action.
All direct actions are now pinned to reviewed release commits with Node24
runtimes (or, for the upload composite, a Node24 transitive upload action).

- actions/checkout: v7.0.1 (`3d3c42e5aac5ba805825da76410c181273ba90b1`)
- actions/setup-python: v7.1.0 (`6d4fd22b20465ccc0f7354476588e8df7c9ca0e0`)
- actions/upload-pages-artifact: v5.0.0 (`fc324d3547104276b827a68afc52ff2a11cc49c9`)
- actions/configure-pages: v6.0.0 (`45bfe0192ca1faeb007ade9deae92b16b8254a0d`)
- actions/deploy-pages: v5.0.1 (`368f82528645a54fb793d4d04e342629a3f51346`)

Before checkout or any other JavaScript action, each job uses system Python
to locate its Runner.Worker ancestor and inspect that runner’s bundled Node24
binary. It requires a stable 24.x version at least 24.22.1, the October 21 security
release. Missing/unrecognized paths and older runtimes fail closed. It neither
installs a runtime nor changes the hosted runner. setup-node would affect PATH,
not prove the runtime used internally by JavaScript actions.

GitHub runner v2.338.1 declares NODE24_VERSION=24.22.1. Hosted rollout is still
verified per job rather than inferred from a release announcement. A failed
preflight requires a patched hosted runner; never suppress it to deploy.
Dependabot checks action updates daily; PRs require review and passing CI.
The minimum is a dated security floor, not a guarantee against future advisories.

Sources:
- https://nodejs.org/en/blog/release/v24.22.1
- https://nodejs.org/en/blog/vulnerability/october-2026-security-releases
- https://github.com/actions/runner/blob/v2.338.1/src/Misc/externals.sh
- https://github.com/actions/upload-pages-artifact/releases/tag/v5.0.0

Validation: nine focused runtime-gate tests pass, and the full local suite passes
661 tests. Hosted PR107 run40056642545 correctly refused Node24.21.0 before
checkout. This proves the guard works but does not establish patched deployment.
The generated workflow is kept in sync through publish_workflow_config and its
existing regression test. Runtime remediation on disposable hosted runners awaits
user approval; no machine-wide runtime upgrade or PHP installation was performed.

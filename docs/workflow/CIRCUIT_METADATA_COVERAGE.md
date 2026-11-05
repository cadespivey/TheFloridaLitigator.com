# Circuit source and metadata reconciliation — November 4, 2026

The ongoing registry was reconciled from all 67 reviewed county directories. All existing 924 entries are preserved; 1,742 published primary court/profile/procedure URLs are added, for 2,666 sources. The 1,643 other supporting URLs remain scope-review candidates. The pinned paused run is unchanged.

This is a source-registration and comparison assessment, not fresh source retrieval or a claim that new URLs already have compatible source-gate reviews. The first refresh can require initial bounded reviews. Published county pointers retain original hashes/timestamps and checkpoint identities; do not fabricate new gate receipts from directory review status.

| Circuit | Primary links already registered | Primary links after reconciliation | Comparison policy |
| --- | ---: | ---: | --- |
| [1](https://www.firstjudicialcircuit.org/) | 0 | 50 | Raw SHA-256; no supported special normalization from the available paired evidence. |
| [2](https://2ndcircuit.leoncountyfl.gov/) | 0 | 64 | Saved HTML formatting/structure differences remain reviewable. |
| [3](https://thirdcircuitfl.org/) | 0 | 37 | Saved structural/accessibility changes remain reviewable. |
| [4](https://www.jud4.org/) | 71 | 74 | Raw SHA-256; all 222 sources in the paused registry had identical bytes. |
| [5](https://www.circuit5.org/) | 0 | 79 | Raw SHA-256; no supported special normalization from the available paired evidence. |
| [6](https://www.jud6.org/) | 0 | 143 | Raw SHA-256; no supported special normalization from the available paired evidence. |
| [7](https://circuit7.org/) | 39 | 105 | Explicit Elementor/request metadata and court-scoped components. |
| [8](https://circuit8.org/) | 31 | 66 | Explicit WPBakery generated-ID bindings/nonce and court-scoped assets. |
| [9](https://ninthcircuit.org/) | 0 | 169 | Raw SHA-256; no supported special normalization from the available paired evidence. |
| [10](https://jud10.flcourts.org/) | 0 | 91 | Raw SHA-256; no supported special normalization from the available paired evidence. |
| [11](https://www.jud11.flcourts.org/) | 0 | 164 | Saved displayed-date/other changes remain significant; no assumed clock. |
| [12](https://www.jud12.flcourts.org/) | 0 | 52 | Raw SHA-256; no supported special normalization from the available paired evidence. |
| [13](https://www.fljud13.org/) | 0 | 113 | Raw SHA-256; no supported special normalization from the available paired evidence. |
| [14](https://jud14.flcourts.org/) | 0 | 47 | Saved navigation/content changes remain significant. |
| [15](https://www.15thcircuit.com/) | 0 | 87 | Raw SHA-256; no supported special normalization from the available paired evidence. |
| [16](https://keyscourts.net/) | 0 | 12 | Raw SHA-256; no supported special normalization from the available paired evidence. |
| [17](https://www.17th.flcourts.org/welcome/) | 0 | 193 | Raw SHA-256; no supported special normalization from the available paired evidence. |
| [18](https://flcourts18.org/) | 0 | 96 | Raw SHA-256; no supported special normalization from the available paired evidence. |
| [19](https://www.circuit19.org/) | 0 | 60 | Raw SHA-256; no supported special normalization from the available paired evidence. |
| [20](https://www.ca.cjis20.org/) | 0 | 129 | HTML CRLF-to-LF only; every other byte remains significant. |

Primary-link counts include published profile/procedure URLs (including county personnel) and circuit indexes, not all supporting citations. Cross-county shared URLs are deduplicated in the registry. Saved pairs from a directory can cite another court; this is not proof that the citing circuit uses that platform.

## Clerk comparison decisions

- Nassau: recognized CivicPlus Cloudflare request parameters are metadata; complete challenge logic is a separately reviewed component. Email masks decode to the actual address in the core. All 14 saved pairs retain equal content cores; changed challenge logic still requires compatible review.
- Putnam: a rotating `Secret Link` target remains an unexplained link change; no target is silently ignored.
- Duval: Blazor descriptors contain opaque serialized state. Their values and control references remain significant until a separately tested interpretation/binding policy is supported.
- St. Johns: plugin/style/script versions and an unsupported CleanTalk pixel format remain reviewable. Existing Circuit 7 rules are not applied just because both sites use Elementor.
- Clay: saved structural, popup/access and visible-content changes remain reviewable.

## Commands and save locations

Use the installed skill launcher for these `flwu` commands. Before a new run:

```sh
flwu source-gate reconcile --registry runs/updates/registry.json --directories website/county-directories --output RUN/next-registry.json --manifest RUN/registry-reconciliation.json
flwu source-gate context --registry RUN/next-registry.json --manifest RUN/registry-reconciliation.json --url EXACT_URL --limit 5
```

Inspect one returned reference at a time; follow `next_offset` with `--offset`. Read the indicated person in the county JSON and export a saved original through `history artifact --database DB --sha256 SHA --output RUN/file.bin`. The future ongoing registry is `runs/updates/registry.json`; its provenance manifest is `runs/updates/registry-reconciliation.json`. Preserve predecessor copies. An already pinned run resumes from its own registry/contract, never this expanded input.

No inference server was restarted and no paused research goal was resumed. Private paired captures and reconciliation manifests remain under `runs/statewide-source-reconciliation-20261104/`; source originals are not committed.

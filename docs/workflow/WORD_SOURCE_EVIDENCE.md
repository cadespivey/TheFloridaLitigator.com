# Court procedure documents served in Word format

Some court procedure URLs end in `.pdf` but return a Word document with the
official Word MIME type. The source gate accepts that response only after bounded
OOXML package validation. HTML, login pages, arbitrary ZIPs, malformed XML,
macro-enabled packages and oversized/ambiguous packages remain failures. Opinion
acquisition and review independently require PDF bytes; this source-format support
does not relax that requirement.

Original bytes, exact URL, retrieval time and SHA-256 remain the evidence. The
`docx-xml-text-v1` extraction is a deterministic reading aid with document-part
locators. It reads paragraphs and tables plus headers, footers, footnotes and
endnotes in their respective XML parts. It does not render pagination, execute
links/macros, interpret tracked changes, or certify images, fields and layout.
Use the original for any requirement that depends on those features. An empty
extraction is unfinished review, not an empty procedure manual.

For an older saved `Expected PDF signature` failure:

1. Inspect the observation's HTTP status, MIME and original bytes. A 403/404 or
   HTML response is still a retrieval failure; do not reinterpret it as Word.
2. Preserve that failed observation. Do not change its success flag or attach a
   reviewed extraction to it: `source-gate extract` requires a successful current
   observation.
3. After validating the supported parser, make one deliberate retrieval of that
   exact URL with a new supplemental run ID and a one-source registry in the same
   research stream. Use `source-gate run` through the pinned skill launcher. Save
   the registry, acquisition output and proof under the existing run directory.
   Do not restart the full seven-court run or alter its pinned dates/registry.
4. Request `workflow next-task` for the existing run. Process its new source task
   normally. Code decides byte changes; the model reviews the required contacts
   and practical operating changes and supplies exact acquired quotations.
5. Retain both the failed capture and the successful replacement observation.
   A parsed Word document is not a completed source review. For primarily family
   or criminal assignments, keep the review to contacts, assignment, official
   links and basic scheduling/submission/appearance instructions.

If the fresh response fails, record its exact failure and preserve the available
originals. Do not repeatedly retry, assert unchanged content, or substitute another
URL's acquisition metadata. Procedure revision/posting dates remain unknown unless
the source actually states them.

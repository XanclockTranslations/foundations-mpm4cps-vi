# Foundations of Multi-Paradigm Modelling for Cyber-Physical Systems — Vietnamese edition

[Tiếng Việt](README.md)

**[Machine Translated, Not Reviewed]**

This machine translation has not received human scholarly review. The AI checks
described below do not replace comparison with the original or expert review.

A project of [XanclockTranslations](https://github.com/XanclockTranslations).
[Source repository](https://github.com/XanclockTranslations/foundations-mpm4cps-vi) ·
[Feedback and corrections](https://github.com/XanclockTranslations/foundations-mpm4cps-vi/issues).

<img src="docs/images/cover.png" alt="Cover of the Vietnamese machine translation" width="320">

A Vietnamese machine translation of *Foundations of Multi-Paradigm Modelling
for Cyber-Physical Systems*, edited by Paulo Carreira, Vasco Amaral and Hans
Vangheluwe, Springer, 2020. [Original book and DOI](https://doi.org/10.1007/978-3-030-43946-0).

The A4 reading edition has **355 pages**: opening material, 9 chapters,
157 numbered figures, 11 tables, 6 exercise diagrams and 310 bibliography
entries. The source repository contains 181 artwork PDFs, including enlarged
reading excerpts and native cells for Table 4.1. Editable LaTeX was reconstructed
from the publisher PDF.

AI used: **GPT-6.1 Sol (Ultra)**. Prompting by **Bế Trọng Nghĩa (@ichxorya)**.
Separate AI agents compared the source and translation, artwork and layout.
This is an independent translation; those reports do not establish approval
by the authors, publisher or human subject experts. Review coverage and
limitations are described in the [review record](docs/review/README.md).

## Read and edit

The verified reading PDF is `foundations-mpm4cps-vi.pdf`; its companion source
package is `foundations-mpm4cps-vi-source.zip`. These files remain locally in
`release/` and are excluded from Git history. When creating a GitHub release,
attach them to GitHub Releases with the information in the
[release manifest](release/release-manifest.json). You can also build the PDF.

| Path | Contents |
|---|---|
| [translation/chapters](translation/chapters) | Canonical LaTeX sources for all 9 chapters |
| [translation/frontmatter](translation/frontmatter) | Cover, opening material, notices, contributors and editorial notes |
| [translation/bibliography.tex](translation/bibliography.tex) | 310 bibliography entries |
| [assets/clean](assets/clean) | 181 checked artwork PDFs |
| [assets/figure-crops.json](assets/figure-crops.json) | Source pages, crop provenance and relationships between figures |
| [source/manifest.json](source/manifest.json) | Original book identity, fingerprint and page mapping |
| [source/asset-inventory.json](source/asset-inventory.json) | Asset inventory and fingerprints |
| [TRANSLATION_GUIDE.md](TRANSLATION_GUIDE.md) | Terminology and editorial conventions |

Chapter, section, figure, equation and bibliography numbering follow the
original; translated pagination differs. Code, formal identifiers and numerical
data are retained. Explanatory labels are localized directly or accompanied by
Vietnamese keys. Confirmed source inconsistencies are explained in marked
notes. Source-raster limits and retained English software interfaces are
described in the review record. The original English PDF and working data are
outside the public source repository; the DOI above leads to the original book.

## Build the PDF

Use **Python 3.12 or later**, **pypdf 6.10.0** and
[Tectonic 0.17.0](https://github.com/tectonic-typesetting/tectonic/releases/tag/tectonic%400.17.0)
on `PATH`.
Tectonic supplies Latin Modern fonts and LaTeX packages from its bundle; the
first build may need network access to download that bundle.

Run from the project root:

```text
python -m pip install -r requirements.txt
python tools/check_project.py
python tools/build_book.py
```

The results are `output/book-draft.tex` and `output/book-draft.pdf`. Edit sources
in `translation/`, then rebuild. The generated `output/` directory is ignored by
Git. To select a compiler and cache directory:

```text
python tools/build_book.py --compiler PATH --cache-dir PATH
```

On Windows, the wrapper is also available:

```powershell
.\tools\build_book.ps1 -PythonCommand python -CompilerCommand tectonic
```

Text sources use UTF-8 and LF; the assembler writes LaTeX with the same
convention on every operating system. Release fingerprints identify the files
verified on 2026-10-14, including the historical CRLF LaTeX master in the ZIP.
They do not promise byte-identical newly compiled PDFs. Read
[CONTRIBUTING.md](CONTRIBUTING.md) before editing or creating a new release.
See the [publishing guide](docs/PUBLISHING.md) for remote, commit and Release steps.

## Source and license

© The original authors and editors, 2020. The original book and this adaptation
use [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Individual supplied
credits are retained, including “Intro Bond Graphs — Jan F. Broenink, ©1999”.

Cover photograph: © Donald Giannatti, 2018, on
[Unsplash](https://unsplash.com/photos/white-radar-telescope-on-grass-field-4qk3nQI3WHY),
under the separate [Unsplash License](https://unsplash.com/license). The
Vietnamese cover is newly typeset; CC BY does not replace the photograph's
license. See [license.md](license.md) for full attribution requirements, license
scope and retained notices. Attribution does not imply endorsement or approval.

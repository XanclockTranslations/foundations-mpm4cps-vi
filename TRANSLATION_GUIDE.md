# Vietnamese edition: translation and editorial conventions

These conventions apply to the complete Vietnamese translation of the 2020
English book, not a summary of its technical content. Canonical editable sources
are UTF-8 LaTeX in `translation/chapters/` and `translation/frontmatter/`.
Save text with LF line endings; edit these sources rather than generated files
in `output/`.

The original is identified by DOI, fingerprint and page mapping in
[source/manifest.json](source/manifest.json). Obtain it through
[the book DOI](https://doi.org/10.1007/978-3-030-43946-0), then compare the original
text and rendered pages where extraction is ambiguous, especially mathematics,
tables, code and figures. Raw extracts and historical working evidence are
outside the public repository; [docs/review/README.md](docs/review/README.md)
describes the retained review record.

## Fidelity

- Preserve section/subsection structure, definitions, lists, examples, equations,
  citations, exercises, acknowledgements and figure/table captions.
- Keep author names, code identifiers, formal notation, URLs and numbered
  bibliography citations unchanged. Bibliography numbers are global.
- Translate prose naturally and precisely. Put additional explanations in
  explicitly marked notes, separate from the author's prose, and explain the
  change in its review record.
- Do not silently correct factual errors in the original. Compare suspected
  errors with the source and record confirmed inconsistencies in marked inline
  or editorial notes.
- Preserve source page comments in the form `% Source: printed N / PDF M`.
- Review a changed passage for completeness against its source. Translation
  completeness, technical accuracy and page layout are separate claims; state
  which was checked and by whom.

## Terminology

Use these preferred renderings, with the English term on first occurrence.

| English | Vietnamese |
|---|---|
| cyber-physical system (CPS) | hệ thống thực-ảo (CPS) |
| multi-paradigm modelling (MPM) | mô hình hóa đa mô thức (MPM) |
| paradigm | mô thức |
| model / modelling | mô hình / mô hình hóa |
| modelling formalism | hệ hình thức mô hình hóa |
| formalism | hệ hình thức |
| modelling language | ngôn ngữ mô hình hóa |
| model-driven engineering (MDE) | kỹ nghệ hướng mô hình (MDE) |
| model-based systems engineering (MBSE) | kỹ nghệ hệ thống dựa trên mô hình (MBSE) |
| domain-specific modelling language (DSML) | ngôn ngữ mô hình hóa chuyên biệt miền (DSML) |
| abstraction / level of abstraction | trừu tượng hóa / mức trừu tượng |
| metamodel / metamodeling | siêu mô hình / siêu mô hình hóa |
| model transformation | biến đổi mô hình |
| refinement | tinh chỉnh |
| semantics / syntax | ngữ nghĩa / cú pháp |
| operational semantics | ngữ nghĩa thao tác |
| translational semantics | ngữ nghĩa chuyển dịch |
| deterministic / nondeterministic | tất định / không tất định |
| determinism / nondeterminism | tính tất định / tính không tất định |
| simulation / co-simulation | mô phỏng / đồng mô phỏng |
| verification / validation | kiểm chứng / thẩm định |
| continuous / discrete | liên tục / rời rạc |
| behaviour / structure | hành vi / cấu trúc |
| concurrent / concurrency | đồng thời / tính đồng thời |
| causal / acausal | nhân quả / phi nhân quả |
| state / event | trạng thái / sự kiện |
| timed system | hệ thống có yếu tố thời gian |
| Statecharts | Statecharts (biểu đồ trạng thái) |
| Petri net | mạng Petri |
| bond graph | đồ thị liên kết năng lượng (bond graph) |
| across variable / through variable | biến chênh lệch (across variable) / biến xuyên (through variable); keep the two categories distinct |
| exact / true solution (numerical analysis) | nghiệm chính xác; do not confuse with a real-valued solution, nghiệm thực |
| tachometer | cảm biến tốc độ quay (tachometer) |
| megamodel / mega-model | mô hình về các mô hình (megamodel); distinct from a metamodel |
| plant (control theory) | đối tượng điều khiển |
| plant model (Chapter 8 physical/hardware context) | mô hình phần vật lý; mô hình phần cứng for execution, deployment and binding contexts |

Explain terminology changes and apply them consistently in the affected text.

## LaTeX conventions

Use `\chapter`, `\section`, `\subsection`, `\subsubsection`, `\paragraph`,
`\textbf`, `\emph`, `\texttt`, `\url`, standard math and list environments.
Use `\chapterauthors{...}` after the title and `\section*{Tóm tắt}` for abstracts.
Use `[130]` directly for numbered bibliography citations until a checked BibTeX
database exists. Do not invent references or renumber citations.

Use `\sourcefigure{1.1}{17}{Vietnamese caption}` to reference a figure by its
original number and one-based source PDF page. The asset manifest resolves the
reference to the reviewed PDF in `assets/clean/`. Reproduce complete table
contents using standard LaTeX table environments and the native Table 4.1 cells
where applicable. Do not leave unresolved artwork placeholders in a release.

Keep source changes compilable. Run the project checks and rebuild as described
in [CONTRIBUTING.md](CONTRIBUTING.md), then inspect affected pages. Record source
comparisons, mathematical or artwork concerns, terminology decisions and actual
review coverage with the change.

## Reader presentation support

Keep complete original diagrams and their numbering. Enlarged native excerpts
are unnumbered `\sourceillustration` assets, explicitly identified as additions
by the translation. Record their parent figure, crop coordinates and source
fingerprint in the asset manifest. They support label reading; the complete
diagram remains the reference for connections crossing excerpt boundaries.

Preserve formal IDs and code comments. Add marked Vietnamese keys for ordinary
interface/process terms and pseudo-instruction phrases where needed. Explain
source clipping, missing traces and inconsistent captions/labels beside the
affected material; do not invent missing data or redraw a different scientific
diagram.

Presentation review is separate from source-fidelity review. Changed pages need
fresh inspection when their pixels change. Demonstrated exact pixel identity
can carry forward an earlier layout review, but a contact sheet alone does not
prove full-page inspection. Review and identify an intentional boundary-fragment
cleanup separately instead of describing it as an exact render match.

Retain supplied source notices and individual credits, including the imported
Jan F. Broenink ©1999 lecture credit and the cover photograph's separate
Unsplash License. See [license.md](license.md). Update asset provenance and
fingerprints deliberately after any intended artwork change.

## Build and release records

The portable assembler writes UTF-8/LF LaTeX consistently across operating
systems. The release verified on 2026-10-14 is a preserved historical snapshot;
its source ZIP includes the earlier CRLF master. Its fingerprints identify those
exact files. New compilation may change PDF metadata or bytes, and an old review
certificate must not be presented as fresh verification of changed output.
Record new review coverage and fingerprints for a new release.

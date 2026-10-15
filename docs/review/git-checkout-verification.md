# Git checkout build verification

Status: **passed**. The copied Git-visible snapshot contains 229 files (38,015,143 bytes); every path was checked for containment and every copied file matched its source SHA-256.

The portable checker and full `tools/build_book.ps1` assembly/build passed when invoked from a different working directory, with Python 3.12 and Tectonic 0.17.0 supplied as parameters. All **355 pages** match the protected reading edition in exact extracted text, full decoded RGB pixels, and dimensions using Poppler `-scale-to 1600`. The 355 reused reference renders were individually checked against the earlier release-bound RGB ledger before comparison.

- LF master SHA-256: `91496bb8362e9eca25000657c5e3da735392f34693ee8df4f6b181e1ae5f2ebc`. It equals the historical master after CRLF-to-LF conversion only.
- Protected reading PDF SHA-256: `007d2b11243a695baa14058a294ca1e9132d92da30ab02bd856b6fb5f78243de`.
- Protected source ZIP SHA-256: `3cd9f4252604b12f30cbb269860d2b7ba7b66fe8606dc128f92c6e9c851fde72`.
- Both protected artifacts retained identical hashes before and after verification.
- Missing glyphs, undefined references/control sequences, overfull boxes, and compile errors: **0** relevant issues. Existing underfull-box and `lineno.sty` UTF-8 warnings remain.

The JSON records all 355 page comparisons, runtime details, snapshot coverage, and any documentation changes after copying. This is a local build verification; no GitHub Actions run or publication is claimed. The historical release ZIP remains the previous verified snapshot; its bytes were not repackaged.

After the build, `README.md`, `README_EN.md`, `docs/review/README.md`, and `tools/check_project.py` were refreshed from the live repository. The updated checker passed, including 46 UTF-8/LF text files. The assembly tool, compiler wrappers, translated sources, and artwork inputs remained unchanged. The final copied Git-visible set contains 229 files (38,015,924 bytes), with every path and SHA-256 matching the live repository. The report files will be added afterward and are outside this build snapshot.

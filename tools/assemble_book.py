"""Assemble the complete Vietnamese edition into one editable LaTeX file."""
from pathlib import Path
import json
import re
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
(ROOT / "output").mkdir(parents=True, exist_ok=True)
preamble = r"""\documentclass[11pt,oneside]{book}
\usepackage{fontspec,textcomp}
\setmainfont{lmroman10-regular.otf}[BoldFont=lmroman10-bold.otf,ItalicFont=lmroman10-italic.otf,BoldItalicFont=lmroman10-bolditalic.otf]
\setsansfont{lmsans10-regular.otf}[BoldFont=lmsans10-bold.otf,ItalicFont=lmsans10-oblique.otf,BoldItalicFont=lmsans10-boldoblique.otf]
\setmonofont{lmmono10-regular.otf}[Scale=MatchLowercase]
\usepackage[a4paper,margin=22mm]{geometry}
\usepackage{amsmath,amssymb,array,longtable,booktabs,graphicx}
\usepackage{tikz}
\definecolor{covernavy}{HTML}{043E52}
\definecolor{covergold}{HTML}{F2C07A}
\allowdisplaybreaks[2]
\usepackage{xurl}
\usepackage[unicode,hidelinks]{hyperref}
\hypersetup{hypertexnames=false,pdftitle={Cơ sở mô hình hóa đa mô thức cho các hệ thống thực-ảo},pdfauthor={Paulo Carreira, Vasco Amaral, Hans Vangheluwe (biên tập bản gốc)},pdfsubject={Bản dịch tiếng Việt với sự hỗ trợ của AI từ ấn bản năm 2020}}
\usepackage{enumitem}
\usepackage{fvextra}
\DefineVerbatimEnvironment{verbatim}{Verbatim}{breaklines=true,breakanywhere=true,fontsize=\small}
\pagestyle{plain}
\setlength{\parskip}{4pt}
\setlength{\parindent}{1.2em}
\setlength{\emergencystretch}{2em}
\clubpenalty=10000
\widowpenalty=10000
\interfootnotelinepenalty=10000
\setlength{\tabcolsep}{4pt}
\renewcommand{\chaptername}{Chương}
\renewcommand{\contentsname}{Mục lục}
\renewcommand{\figurename}{Hình}
\renewcommand{\tablename}{Bảng}
\setcounter{secnumdepth}{3}
\setcounter{tocdepth}{2}
\makeatletter
\renewcommand{\@pnumwidth}{2.5em}
\renewcommand{\@tocrmarg}{3.5em}
\makeatother
\newcommand{\chapterauthors}[1]{\begin{center}\large #1\end{center}\medskip}
\newcommand{\presentationstart}{\par\begingroup\dimen0=\pagegoal\advance\dimen0 by -\pagetotal\ifdim\dimen0<110pt\newpage\fi\endgroup}
\newcommand{\sourcefigwidth}[1]{\ifcsname sourcefigwidth#1\endcsname\csname sourcefigwidth#1\endcsname\else0.95\fi}
\newcommand{\sourcefigheight}[1]{\ifcsname sourcefigheight#1\endcsname\csname sourcefigheight#1\endcsname\else0.85\fi}
\expandafter\def\csname sourcefigheight6.9\endcsname{0.93}
\expandafter\def\csname sourcefigheight8.9\endcsname{0.93}
\expandafter\def\csname sourcefigwidth5.2\endcsname{0.35}
\expandafter\def\csname sourcefigwidth5.4\endcsname{0.62}
\expandafter\def\csname sourcefigwidth5.6\endcsname{0.70}
\expandafter\def\csname sourcefigwidth5.8\endcsname{0.70}
\expandafter\def\csname sourcefigwidth5.10\endcsname{0.75}
\expandafter\def\csname sourcefigwidth5.11\endcsname{0.75}
\newcommand{\sourcefigure}[3]{\begin{figure}[htbp]\centering
\ifcsname sourcefigpath#1\endcsname
  \IfFileExists{\csname sourcefigpath#1\endcsname}{\includegraphics[width=\sourcefigwidth{#1}\linewidth,height=\sourcefigheight{#1}\textheight,keepaspectratio]{\csname sourcefigpath#1\endcsname}}{\fbox{\parbox{0.85\linewidth}{\centering Hình #1 đang được biên tập.}}}
\else
  \fbox{\parbox{0.85\linewidth}{\centering Hình #1 trong bản gốc, trang PDF #2.\\Hình đang được biên tập.}}
\fi
\par\smallskip\small\textbf{Hình #1.} #3\end{figure}}
\newcommand{\sourceillustration}[3]{\begin{figure}[htbp]\centering
\ifcsname sourcefigpath#1\endcsname
  \IfFileExists{\csname sourcefigpath#1\endcsname}{\includegraphics[width=\sourcefigwidth{#1}\linewidth,height=\sourcefigheight{#1}\textheight,keepaspectratio]{\csname sourcefigpath#1\endcsname}}{\fbox{\parbox{0.85\linewidth}{\centering Sơ đồ đang được biên tập.}}}
\else\fbox{\parbox{0.85\linewidth}{\centering Sơ đồ trong bản gốc, trang PDF #2, đang được biên tập.}}\fi
\par\smallskip\small #3\end{figure}}
\begin{document}
\frontmatter
\input{../translation/frontmatter/cover.tex}
\chapter*{Nguồn và ghi công}
Bản gốc: \emph{Foundations of Multi-Paradigm Modelling for Cyber-Physical Systems},
do Paulo Carreira, Vasco Amaral và Hans Vangheluwe biên tập, Springer, 2020.
DOI: \url{https://doi.org/10.1007/978-3-030-43946-0}.

\noindent Bản gốc © các tác giả và biên tập viên, 2020. Văn bản được cấp phép theo
Creative Commons Ghi công 4.0 Quốc tế (CC BY 4.0):
\url{https://creativecommons.org/licenses/by/4.0/}.

Bản tiếng Việt này là bản dịch có sự hỗ trợ của AI, được tái dựng từ PDF gốc.
Toàn bộ chín chương, phần mở đầu, bài tập và tài liệu tham khảo đã được chuyển
ngữ và dàn trang lại. Nguồn LaTeX của bản tiếng Việt được tái dựng để có thể
chỉnh sửa; nguồn này không phải mã nguồn LaTeX gốc của nhà xuất bản.
Đây là bản dịch độc lập có sự hỗ trợ của AI; việc ghi công Springer mô tả nguồn
tiếng Anh và không xác lập tư cách ấn bản chính thức của nhà xuất bản.
Việc ghi tên các tác giả không hàm ý họ bảo trợ hoặc phê duyệt bản dịch.

AI được sử dụng: \textbf{GPT-6.1 Sol (Ultra)}.\\
Người thực hiện prompting: \textbf{Bế Trọng Nghĩa} (\texttt{@ichxorya}).

\noindent\textbf{[Machine Translated, Not Reviewed]}\\
Bản dịch máy chưa được con người rà soát chuyên môn; các lượt kiểm tra bằng AI
không thay thế đánh giá học thuật. Dự án thuộc XanclockTranslations.\\
Kho nguồn và góp ý: \url{https://github.com/XanclockTranslations/foundations-mpm4cps-vi}.

Bản dịch được cung cấp theo CC BY 4.0. Khi sử dụng lại, hãy ghi công các tác giả
và biên tập viên gốc, dẫn nguồn tiếng Anh và bản dịch tiếng Việt, liên kết tới
giấy phép, đồng thời nêu rõ các thay đổi. Theo thông báo của bản gốc, hình ảnh và
tư liệu của bên thứ ba được bao gồm trong giấy phép của sách, trừ khi dòng ghi
công nêu điều kiện khác. Các dòng ghi công và trích dẫn riêng được giữ lại.

Dữ liệu hình gốc của Chương 2 có dòng ghi công ``Intro Bond Graphs ---
Jan F. Broenink, © 1999'', tương ứng với tài liệu
\emph{Introduction to Physical Systems Modelling with Bond Graphs} của tác giả
tại University of Twente. Bản dịch giữ lại ghi công này; các nhãn diễn giải
trong hình được Việt hóa.

Ảnh bìa: \copyright{} Donald Giannatti, 2018, trên Unsplash.\\
\url{https://unsplash.com/photos/white-radar-telescope-on-grass-field-4qk3nQI3WHY}.\\
Ảnh được sử dụng theo Giấy phép Unsplash: \url{https://unsplash.com/license}.
Bìa tiếng Việt được dàn mới; ảnh được cắt theo khổ bìa và đặt chữ lên trên.
Giấy phép CC BY 4.0 của bản dịch không thay thế Giấy phép Unsplash của ảnh bìa.
Số trang bản dịch khác số trang tiếng Anh. Số chương, mục, hình và tài liệu tham
khảo được giữ theo bản gốc để thuận tiện đối chiếu. Nhãn giải thích trong các
hình được chuyển ngữ trực tiếp hoặc bổ sung chú giải tiếng Việt; mã, tên trạng
thái, ký hiệu và dữ liệu hình thức được giữ theo bản gốc. Ghi chú biên tập ở
cuối sách nêu riêng một số điểm không nhất quán đã xác nhận trong nguồn.
"""
asset_manifest = json.loads((ROOT/"assets/figure-crops.json").read_text(encoding="utf-8"))
figure_definitions = []
text_width_pt=595.276-44*72/25.4
custom_widths={"5.2":.35,"5.4":.62,"5.6":.70,"5.8":.70,"5.10":.75,"5.11":.75}
for figure in asset_manifest["figures"]:
    name = figure["number"].replace(".","-")
    localized = ROOT/"assets"/f"figure-{name}-vi.pdf"
    clean = ROOT/"assets"/"clean"/localized.name
    if clean.exists() or localized.exists():
        asset_path = "../assets/clean/"+localized.name if clean.exists() else "../assets/"+localized.name
        native_width=float(PdfReader(clean if clean.exists() else localized).pages[0].mediabox.width)
        width_ratio=min(custom_widths.get(figure["number"],.95),native_width*figure.get('presentation_scale_cap',1.4)/text_width_pt)
        figure_definitions.append(r"\expandafter\def\csname sourcefigwidth"+figure["number"]+r"\endcsname{"+f"{width_ratio:.5f}"+"}")
        figure_definitions.append(r"\expandafter\def\csname sourcefigpath"+figure["number"]+r"\endcsname{"+asset_path+"}")
preamble = preamble.replace(r"\begin{document}","\n".join(figure_definitions)+"\n"+r"\begin{document}")
progress = json.loads((ROOT/"translation/progress.json").read_text(encoding="utf-8"))
ready = {c["chapter"] for c in progress["chapters"] if c["status"] in ("draft_complete_self_reviewed","translation_complete_reviewed")}
files = [p for p in sorted((ROOT / "translation" / "chapters").glob("chapter-??.tex"))
         if int(p.stem.rsplit("-",1)[1]) in ready]
parts = [preamble, (ROOT / "translation" / "frontmatter" / "original-notices.tex").read_text(encoding="utf-8"),
         (ROOT / "translation" / "frontmatter" / "opening.tex").read_text(encoding="utf-8"),
         "\n\\tableofcontents\n",
         (ROOT / "translation" / "frontmatter" / "contributors.tex").read_text(encoding="utf-8"),
         "\n\\mainmatter\n"]

def wrap_inline_identifiers(source):
    """Add invisible line-break opportunities without changing literal identifiers."""
    def wrap(match):
        value=match.group(1)
        value=value.replace(r"\_",r"\_\allowbreak{}").replace(".",r".\allowbreak{}")
        value=re.sub(r"(?<=[a-z])(?=[A-Z])",lambda _:r"\allowbreak{}",value)
        return r"\texttt{"+value+"}"
    # Verbatim source/code must remain untouched.
    blocks=re.split(r"(\\begin\{verbatim\}.*?\\end\{verbatim\})",source,flags=re.S)
    return "".join(block if block.startswith(r"\begin{verbatim}") else
                   re.sub(r"\\texttt\{([^{}]*)\}",wrap,block) for block in blocks)
included = []
for path in files:
    number = int(path.stem.rsplit("-", 1)[1])
    parts.append(f"\n\\setcounter{{chapter}}{{{number-1}}}\n")
    chapter_text=path.read_text(encoding="utf-8")
    if number==4:
        # Start each long algorithm with its heading and several opening lines.
        chapter_text,count=re.subn(r"(?=\\paragraph\{Thuật toán [12]\.)",lambda _:r"\presentationstart"+"\n",chapter_text)
        assert count==2,'Chapter4 algorithm starts did not match twice'
    if number==5:
        # This short listing fits on one page. Keep its trailing caption with
        # the literal code instead of allowing a detached caption on the next.
        pattern=r"(\\begin\{verbatim\}(?:(?!\\end\{verbatim\}).)*\\end\{verbatim\}\s*% Source:[^\n]+\n\\noindent\\textbf\{Đoạn mã 6\.\}[^\n]+\n)"
        chapter_text,count=re.subn(pattern,lambda m:r"\par\noindent\begin{minipage}{\linewidth}"+"\n"+m.group(1)+r"\end{minipage}\par"+"\n",chapter_text,flags=re.S)
        assert count==1,'Listing6 caption wrapper did not match exactly once'
    if number==8:
        # Consecutive run-in headings need body text in the same page block.
        pattern=r"(\\paragraph\{(?:Ứng dụng phần mềm|Yêu cầu hệ thống)\}\s*\\subparagraph\{Các cấu trúc\}\n[^\n]+\n)"
        chapter_text,count=re.subn(pattern,lambda m:r"\par\noindent\begin{minipage}{\linewidth}"+"\n"+m.group(1)+r"\end{minipage}\par"+"\n",chapter_text)
        assert count==2,'Chapter8 introductions did not match twice'
        pattern=r"(\\begin\{verbatim\}(?:(?!\\end\{verbatim\}).)*\\end\{verbatim\}\s*\\begin\{center\}\\small Đoạn mã 22:.*?\\end\{center\})"
        chapter_text,count=re.subn(pattern,lambda m:r"\par\noindent\begin{minipage}{\linewidth}"+"\n"+m.group(1)+"\n"+r"\end{minipage}\par"+"\n",chapter_text,flags=re.S)
        assert count==1,'Listing22 caption wrapper did not match once'
    parts.append(wrap_inline_identifiers(chapter_text))
    included.append(number)
if (ROOT/"translation/bibliography.tex").exists():
    parts.append("\n\\backmatter\n")
    if (ROOT/"translation/frontmatter/editorial-notes.tex").exists():
        parts.append((ROOT/"translation/frontmatter/editorial-notes.tex").read_text(encoding="utf-8"))
    parts.append((ROOT/"translation/bibliography.tex").read_text(encoding="utf-8"))
parts.append("\n\\end{document}\n")
output = ROOT / "output" / "book-draft.tex"
output.write_text("\n".join(parts), encoding="utf-8", newline="\n")
(ROOT / "output" / "assembly.json").write_text(json.dumps({"included_chapters":included,"full_book_complete":progress.get("full_book_complete",False),"status":"checked_translation" if progress.get("full_book_complete") else "final_review"},indent=2)+"\n",encoding="utf-8",newline="\n")
print(f"Assembled {output.name}; chapters: {included}")

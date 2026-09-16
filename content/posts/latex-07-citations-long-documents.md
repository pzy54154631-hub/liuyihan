+++
title = "引用与长文档：让每一句话都有来处"
date = "2026-09-16"
tag = "LaTeX 学习手记"
summary = "把脚注、引文、文献库、匿名访谈与附录放进同一个写作流程，练习可以持续修改的长文结构。"
authors = ["Ziyu.Peng", "刘毅涵"]
series = "latex"
order = 7
stage = "第三阶段 · 整理成完整作品"
+++

文章变长以后，最容易出错的地方往往不在正文：引用页码忘了补，章节顺序改了却没有更新编号，一段访谈不知道对应哪份材料。这一章把来源记录和文档结构一起整理，让后续修改更有把握。

这些方法适用于人文社科阅读笔记，也适用于经济学课程论文。具体引用格式仍以课程、学校或期刊要求为准。

[下载完整示例：引用与长文档](/liuyihan/assets/tutorial/examples/latex-07.tex)。它会生成配套书目文件，需要 XeLaTeX 和 Biber。**文件里的作者、文献、引文与访谈全部是虚构教学示例，不能当作真实材料引用。**

## 段落、脚注和引文各有位置

中文段落之间空一行即可，不需要在段首反复打空格，也不需要用许多 `\\` 拉开间距。`ctexart` 已经处理中文段落的基本格式；统一样式留在导言区，正文尽量只写内容。

说明性脚注适合交代术语范围、补充背景或记录转写约定。

```latex
这里的“社区”指日常交往的范围。\footnote{
  这是教学自拟的概念限定，用于展示脚注。
}
```

来源引用则回答“这句话依据哪份材料”。它和说明性脚注可能出现在相同位置，但逻辑用途不同。真实文献需要记录版本、作者、出版信息和具体定位；脚注编号不会替你验证这些信息。

长引文可以使用 `quote`；多段引文可考虑 `quotation`；需要保留诗行的文本可用 `verse`。下面是自拟句子，只展示版式。

```latex
\begin{quote}
材料的缺席，不能直接说明行动没有发生。
\end{quote}

\begin{verse}
旧页留微痕，\\
新问入书窗。
\end{verse}
```

正式引用时，应区分逐字引文、自己的概括与译文。档案定位可能是档号、卷次或叶码，不能为了整齐全部改成现代页码。多语言和嵌套引号可进一步使用 `csquotes`，并检查生成的引号是否符合目标格式。

## 用文献库保存信息，用命令表达关系

本章采用 `biblatex` 与 Biber：`.bib` 文件存储文献数据，Biber 处理数据，`biblatex` 决定引用与文献表的排版。两者是配合关系，具体介绍见 [biblatex 官方文档](https://ctan.org/pkg/biblatex) 与 [Biber 官方项目](https://ctan.org/pkg/biber)。

先看这份能够独立运行的最小文件。`filecontents*` 把示例书目写入文件，方便一次复制；正式项目通常直接维护独立的 `.bib` 文件。

```latex
% !TeX program = xelatex
% 以下作者、书名、出版信息全部为虚构教学示例。
\begin{filecontents*}{citation-demo.bib}
@book{sample2024,
  author = {Sample, Alice},
  title = {Local Memory: A Fictional Teaching Example},
  date = {2024},
  location = {Example City},
  publisher = {Fictional Teaching Press}
}
\end{filecontents*}

\documentclass[fontset=fandol]{ctexart}
\usepackage{csquotes}
\usepackage[backend=biber,style=authoryear]{biblatex}
\addbibresource{citation-demo.bib}
\usepackage[hidelinks]{hyperref}

\begin{document}
\section*{引用练习：全部为虚构教学内容}
\textcite[23--25]{sample2024} 展示叙述式引用。
这句话展示括号式引用\parencite[23]{sample2024}。
\printbibliography[title={参考文献（虚构示例）}]
\end{document}
```

保存为 `citation-demo.tex` 后，本地编译顺序如下。Biber 的参数不带 `.tex` 后缀。

```text
xelatex citation-demo.tex
biber citation-demo
xelatex citation-demo.tex
xelatex citation-demo.tex
```

第一次 LaTeX 编译生成控制文件，Biber 读取书目，后续编译再更新引用和文献表。能够自动调用 Biber 的编辑器或 `latexmk` 可以代办这一流程。下载版本的文件名是 `latex-07.tex`，手动运行时应相应使用 `biber latex-07`。

`filecontents*` 默认不会覆盖已经存在的同名文件。如果修改示例以后发现书目没有变化，直接打开生成的 `.bib` 修改，或在确认无需保留旧内容后重新生成。

## 选好引用制度，再统一写法

`\textcite{key}` 把作者放进句子中；`\parencite{key}` 生成括号引用；`\footcite{key}` 把引用放进脚注。可选参数 `[23--25]` 是这次引用的定位信息，和期刊条目中表示整篇文章范围的 `pages` 字段不同。

`style=authoryear` 是通用作者年份样式，并不等于 APA。若需要完整脚注制，可研究 `style=verbose` 或目标规范专门的样式；只把命令从 `\parencite` 换成 `\footcite`，不会自动让作者年份制变成完整脚注制。中文正文使用 `ctex`，也不意味着文献标点和排序会自动符合所有中文规范。

同一个项目不要同时加载 `natbib` 与 `biblatex`，也不要混入另一套 `\bibliographystyle`、`\bibliography` 流程。使用课程提供的模板时，先确定模板采用哪一套体系，再补充文献。

## 让交叉引用替你记住章节位置

```latex
\section{材料与方法}\label{sec:methods}
这里说明材料来源。

参见第~\ref{sec:methods}~节，
该部分位于第~\pageref{sec:methods}~页。

\section*{致谢}
\phantomsection
\addcontentsline{toc}{section}{致谢}
```

星号标题不自动编号，通常也不自动进入目录。最后两行把它加入目录并给链接一个锚点；无编号标题不能依靠普通 `\ref` 获得章节编号。正文中的标签可以统一使用 `sec:`、`fig:`、`tab:` 和 `app:` 前缀，检查时更容易定位。

`ctexart` 的主要层级是 `\section`；只有书籍、报告等相应文档类才使用 `\chapter`。目录显示深度 `tocdepth` 与编号深度 `secnumdepth` 也分别控制不同事情。

## 匿名材料与长文结构一起维护

下面的编号、时间和话语均为虚构。`description` 便于区分发言人，长文本可以自然分页；不要把整份访谈塞进一个不能分页的大盒子。

```latex
% 导言区：\usepackage{enumitem}
\begin{description}[leftmargin=2em,
                    font=\normalfont\bfseries]
  \item[访问者，00:12] 你怎样描述这处公共空间？
  \item[P03，00:18] 我会把它叫作碰面的地方。
  \item[转写说明] 方括号用于标记删节与补充说明。
\end{description}
```

真实项目中，应在方法部分解释编号规则，并把真实身份对应表与可共享源码分开保管。匿名化不仅发生在 PDF 正文里；文件名、注释和未使用的材料也可能包含身份信息。

长文章可以拆成多个正文文件，主文件集中保留样式。下面是结构片段，使用前需要创建对应的子文件。

```latex
\begin{document}
\maketitle
\tableofcontents
\input{sections/introduction}
\input{sections/literature-review}
\input{sections/methods}
\printbibliography
\appendix
\section{访谈提纲}\label{app:guide}
\input{sections/interview-guide}
\end{document}
```

子文件只写正文，不再放 `\documentclass` 或 `\begin{document}`。`\input` 不强制换页；`\include` 会在文件边界清页，适合另有分章需求的项目。`\appendix` 会切换后续编号形式，标题中不必手写“附录 A”。关于基本文档组织，可继续阅读 [LaTeX 项目官方文档入口](https://www.latex-project.org/help/documentation/)。

## 本章练习

先运行下载示例，确认目录、章节引用和文献表都没有问号。随后把一条虚构条目替换成自己确实读过的真实文献，核对作者、版本与引用页码。最后调整章节顺序，再编译，观察编号自动更新。

交稿前再读一次 PDF：文字来源是否可追溯，所有教学占位条目是否已经删除，附录编号是否清楚，生成的文件是否包含不应公开的材料。能编译，是整理完成的起点。

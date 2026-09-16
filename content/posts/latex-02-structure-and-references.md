+++
title = "把笔记组织成一篇文章"
date = "2026-09-16"
tag = "LaTeX 学习手记"
summary = "用标题、段落、目录与交叉引用整理一份中文报告，让内容增加之后仍然容易维护。"
authors = ["Ziyu Peng", "刘毅涵"]
series = "latex"
order = 2
stage = "第一阶段 · 写出第一份文档"
+++

一页笔记可以靠记忆找到内容，十页报告就需要明确的结构。LaTeX 的便利也从这里开始：章节改了顺序，编号和引用可以跟着更新；新增一段内容，不必重新手工填写目录页码。本章把第一章的小文档变成一份可扩展的中文报告。

## 标题说明内容关系

在 `ctexart` 中，常用层级依次是 `\section`、`\subsection` 和 `\subsubsection`。把章节看成“问题—分问题—具体讨论”，比只把它们理解成不同字号更有帮助。文章类没有 `\chapter`；需要“章”的长篇结构，可以考虑 `ctexrep` 或 `ctexbook`。

更深层的 `\paragraph`、`\subparagraph` 仍然是标题命令，不能因为名字里有 paragraph 就把它们当作普通换段命令。短报告通常两三级就足够；层级过深时，先检查内容能否合并，而不是再加一层编号。CTeX 的标题样式与中文配置可查阅 [CTeX 手册](https://ctan.org/pkg/ctex)。

## 中文段落：让结构出现在源码里

源码中**空一行**表示新段落。只按一次回车，通常仍属于同一段；不要用一连串 `\\` 制造段落和留白。中文标点可以直接输入，首行缩进交给文档类处理，避免手打全角空格。

```latex
这是第一段，交代要讨论的问题。
这一行仍属于第一段。

这是第二段，说明采用的材料和方法。
可以用 \textbf{关键词} 提醒读者注意重点。
```

短说明适合脚注，例如 `术语说明\footnote{这里补充定义。}`。脚注会自动编号，但不应承担正文的全部论证。文献来源则最好使用后面章节介绍的书目系统，让作者、年份与文献表保持一致。

## 从手写“第三节”换成稳定标签

`\label{sec:methods}` 是给一个位置取稳定的名字，`\ref{sec:methods}` 输出相应编号，`\pageref{sec:methods}` 输出页码。标签名不会直接出现在成品中；`sec:`、`fig:`、`tab:` 等前缀是便于管理的约定，并非强制语法。

章节标签放在标题命令后面。将来为图表加标签时，要放在对应 `\caption` 后面，因为说明文字命令会更新图表编号。标签应当唯一；两个位置使用同一个标签，会让引用含义不清楚。

```latex
\section{材料与方法}
\label{sec:methods}
本节说明材料的整理方式。

方法说明见第~\ref{sec:methods}~节，
位于第~\pageref{sec:methods}~页。
```

这里的 `~` 是不可断行空格，常用来避免“第”和编号被拆开。中文排版也可以采用适合模板的其他间距方式，关键是全文一致。

## 一个完整、可修改的报告骨架

下面是独立文件，不需要接在上一章示例末尾。保存并编译两遍后，再观察目录与交叉引用。

```latex
% !TeX program = xelatex
\documentclass[UTF8,a4paper,fontset=fandol]{ctexart}
\usepackage[margin=2.5cm]{geometry}
\usepackage[hidelinks]{hyperref}
\setcounter{tocdepth}{2}
\setcounter{secnumdepth}{2}

\title{课程报告的结构练习}
\author{\href{https://github.com/pzy54154631-hub}{\textit{Ziyu Peng}}, University of Colorado Boulder,
  \\[0.1em]College of Arts and Sciences, Statistics and Data Science
  \\[0.1em]Boulder, CO 80309, USA
  \\[0.1em]\href{mailto:Ziyu.PengSr@colorado.edu}{Ziyu.PengSr@colorado.edu}
  \\[0.35em]
  \href{https://pzy54154631-hub.github.io/liuyihan/}{刘毅涵}，暨南大学经济学院}
\date{}

\begin{document}
\maketitle
\tableofcontents
\clearpage

\section{研究问题}
\label{sec:question}
本例只演示文档结构，不包含实际研究结论。
材料范围见第~\ref{sec:materials}~节。

\section{材料与方法}
\label{sec:methods}
\subsection{材料范围}
\label{sec:materials}
这里说明准备使用哪些材料，以及为什么选择它们。

这里另起一段，说明材料的限制。
\footnote{本脚注仅用于演示补充说明。}

\subsection{整理步骤}
\begin{enumerate}
  \item 记录材料出处。
  \item 按主题进行整理。
  \item 检查说明与材料是否一致。
\end{enumerate}

\section{小结}
问题在第~\pageref{sec:question}~页提出。
当前文档已经可以自动更新编号。

\section*{致谢}
\phantomsection
\addcontentsline{toc}{section}{致谢}
这里放置不编号的致谢内容。
\end{document}
```

## 为什么经常要编译两遍

第一次编译会把编号、页码等信息写入辅助文件，下一次编译才能把这些信息填到之前出现的引用和目录中。因此第一次出现 `??`，不一定是标签写错；再次编译后仍有问号，再检查拼写、重复标签与报错。有时结构变化需要更多一遍，或者交给 `latexmk` 处理更新流程。

`tocdepth` 决定目录显示到几级，`secnumdepth` 决定标题编号到几级，两者不是一回事。本例都设为 2，让目录和编号到小节为止。改变其中一个值后，可以刻意比较差别。

## 无编号标题也可以进入目录

`\section*{致谢}` 不产生普通章节编号，也不会自动进入目录。示例用 `\addcontentsline` 加入目录条目；加载 `hyperref` 后，`\phantomsection` 用于建立对应的链接位置。不要再用普通 `\ref` 要求它输出一个不存在的章节编号。更复杂的目录与锚点设置见 [hyperref 手册](https://ctan.org/pkg/hyperref)。

## 小练习：让一次改动验证整个结构

在“材料与方法”前插入新章节，再编译。检查正文里的引用、目录编号和页码是否更新；把目录深度改为 1，确认小节仍存在，只是目录不再显示它们。最后把“致谢”移到小结前，检查目录链接能否到达正确位置。

[下载本章完整示例 latex-02.tex](/liuyihan/assets/tutorial/examples/latex-02.tex)

## 继续查阅

- [LaTeX 官方作者文档](https://www.latex-project.org/help/documentation/)：查找标准文档结构与命令说明。
- [CTeX 项目与手册](https://ctan.org/pkg/ctex)：中文标题、缩进与文档类。
- [hyperref 项目与手册](https://ctan.org/pkg/hyperref)：目录、引用和可点击链接。

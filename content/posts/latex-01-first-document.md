+++
title = "从一份中文文档开始"
date = "2026-07"
updated = "2026-09-16"
tag = "LaTeX 学习手记"
summary = "分清编辑器、编译器和宏包，用一页中文笔记建立能够反复使用的 LaTeX 起点。"
authors = ["Ziyu Peng", "刘毅涵"]
series = "latex"
order = 1
stage = "第一阶段 · 写出第一份文档"
+++

学一门排版工具，第一步不必做出复杂模板。先把一段中文、一条公式和一个标题变成清楚的 PDF，再回头理解每一行代码，往往更容易建立信心。本章的目标是一份能运行、能修改、也能解释的小文档。

## 先知道自己在操作什么

LaTeX 的工作方式是写下内容与结构，再由程序排版。输入 `\section{学习目标}`，是在说明“这里是一级标题”；字号、位置和编号由文档规则决定。它适合反复修改的课程报告、公式笔记与较长文档。短通知、多人临时编辑的表单，继续使用熟悉的办公软件也很合适。

初学时容易混淆三个名字：LaTeX 是文档系统，XeLaTeX 是本教程选择的编译程序，Overleaf 是可以在线编辑与编译项目的平台。在本地写作，则通常需要 TeX Live、MacTeX 等发行版提供程序、宏包和字体，编辑器本身不等于完整的编译环境。

中文文档在本系列中统一使用 **UTF-8 编码、`ctexart` 文档类和 XeLaTeX**。这样可以把精力先放在写作上，暂时不在不同引擎和字体方案之间切换。CTeX 本身也支持其他引擎，具体能力与设置见 [CTeX 项目与手册](https://ctan.org/pkg/ctex)。

如果还不熟悉在线编译界面，可以先配合[第 15 章：在 Overleaf 中编译与导出](/liuyihan/blog/latex-15-overleaf-workflow/)完成项目设置，再回到本章理解代码。

## 第一步：让完整文档运行起来

在 Overleaf 建立空白项目，把主文件内容替换为下面的代码，并在项目设置中选择 XeLaTeX。在本地则把它保存为 UTF-8 的 `latex-01.tex`，使用 XeLaTeX 编译。第一行是给编辑器看的提示，不会替所有平台自动切换编译器。

```latex
% !TeX program = xelatex
\documentclass[UTF8,a4paper,fontset=fandol]{ctexart}
\usepackage[margin=2.5cm]{geometry}
\usepackage{amsmath,amssymb}
\usepackage[hidelinks]{hyperref}

\title{一页学习笔记}
\author{\href{https://github.com/pzy54154631-hub}{\textit{Ziyu Peng}}, University of Colorado Boulder,
  \\[0.1em]Boulder, CO 80309, USA
  \\[0.35em]
  \href{https://pzy54154631-hub.github.io/liuyihan/}{刘毅涵}，暨南大学经济学院}
\date{}

\begin{document}
\maketitle

\section{这份笔记要解决什么}
先把内容写清楚，再让版式保持一致。
本例中的姓名用于展示作者排列方式。

\section{一条简单公式}
设五次练习的得分为 \(x_1,\ldots,x_5\)，平均值为
\[
  \bar{x}=\frac{1}{5}\sum_{i=1}^{5}x_i.
\]

\section{下次继续}
\begin{itemize}
  \item 改写一个标题，观察编号是否自动更新。
  \item 替换正文，保留清楚的段落结构。
\end{itemize}
\end{document}
```

编译完成后，应当看到标题、按顺序编号的三个部分、一条居中的公式和两条列表。先核对这些具体结果，再调整外观；如果连最小文档都不能运行，继续增加宏包只会让排查更困难。

## 第二步：认出文档的骨架

从 `\documentclass` 到 `\begin{document}` 之前是**导言区**，放文档类、宏包、标题与全局设置。正文位于 `\begin{document}` 和 `\end{document}` 之间。标题信息写在导言区，真正打印标题的是正文中的 `\maketitle`。

`ctexart` 面向中文文章；`a4paper` 选择纸张；`fontset=fandol` 选择 TeX 发行版中的 Fandol 中文字体，减少对某台电脑字体的依赖。`geometry` 管页边距，`amsmath` 管较丰富的数学环境，`amssymb` 补充数学字体与符号，`hyperref` 为引用和网址等建立链接。本例把它放在其他宏包之后；遇到特别说明的宏包，再按对应手册调整顺序。

宏包应当按需要加入。准备插图时再加载 `graphicx`，准备三线表时再加载 `booktabs`。把网上模板里所有宏包都复制进来，会增加冲突与解释成本。对于课程已有的正式模板，应先遵守模板要求，再借用本系列的正文写法。

## 第三步：理解三个常见符号

反斜线通常引出命令，花括号圈定参数或作用范围，百分号开始注释。例如 `\textbf{关键词}` 只把花括号内的内容加粗。源文件里的 `% 这里是说明` 不会显示在 PDF 中；正文要显示百分号，应写成 `10\%`。

文件名可以简单使用英文字母、数字与短横线，例如 `course-note.tex`。源文件是可继续编辑的内容，PDF 是排版后的阅读版本。分享项目时保留 `.tex` 和实际用到的图片、书目；只保存 PDF，以后就很难修改结构和公式了。

## 编译出错时，从第一条错误开始

遇到错误，先看日志中最早出现的明确错误及其附近代码。`Undefined control sequence` 常见于命令拼写错误或缺少宏包；`Missing $ inserted` 常见于在普通文字中直接使用数学上下标；中文乱码或字体错误则要检查编码、编译器与字体配置。

报错行有时只是程序终于发现问题的位置，真正漏掉的右花括号可能在前几行。每完成一小段就编译，能把需要检查的范围缩小。若出现 PDF，但仍有警告，也应继续核对：有输出并不等于每一项设置都正确。

## 小练习：做一页自己的课程笔记

把示例改成任意一门课的学习笔记，保留“问题、例子、下一步”三个部分；加粗一个关键词，再增加一条列表。完成后试着口头解释导言区、正文和宏包各负责什么。能够解释自己的五六个命令，比积攒一页看不懂的模板更有用。

[下载本章完整示例 latex-01.tex](/liuyihan/assets/tutorial/examples/latex-01.tex)

## 继续查阅

- [LaTeX 官方文档入口](https://www.latex-project.org/help/documentation/)：了解文档系统与作者指南。
- [CTeX 项目与中文手册](https://ctan.org/pkg/ctex)：查找中文文档类、字体与标题设置。
- [Overleaf：选择编译器](https://www.overleaf.com/learn/latex/Choosing_a_LaTeX_Compiler)：在线项目的编译器设置说明。

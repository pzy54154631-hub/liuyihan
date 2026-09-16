+++
title = "字体、颜色与代码：让整篇文档保持一致"
date = "2026-09-16"
tag = "LaTeX 学习手记"
summary = "统一中文字体、标题和页面样式，分清代码展示与执行，再用一个小流程图连接材料与表达。"
authors = ["Ziyu.Peng", "刘毅涵"]
series = "latex"
order = 6
stage = "第三阶段 · 整理成完整作品"
+++

一份文档好读，往往来自几条稳定的约定：同一级标题长得一样，同一种提示使用同一种颜色，正文有足够的呼吸空间。学会调整样式以后，更重要的是把这些设置集中起来，让后面的每一页自然保持一致。

本章沿用 XeLaTeX 与 `ctexart`。先完成一套简单样式，再处理代码和流程图，不需要一开始就收集很多宏包。

[下载完整示例：字体、版面与代码](/liuyihan/assets/tutorial/examples/latex-06.tex)。它包含中文正文、英文代码、中文源码和一个无需外部图片的小流程图。

## 字体设置先明确中文与西文

```latex
\documentclass[UTF8,a4paper,fontset=fandol]{ctexart}
\setmainfont{texgyrepagella-regular.otf}[
  BoldFont=texgyrepagella-bold.otf,
  ItalicFont=texgyrepagella-italic.otf,
  BoldItalicFont=texgyrepagella-bolditalic.otf]
\setmonofont{lmmono10-regular.otf}[BoldFont=lmmonolt10-bold.otf,
  ItalicFont=lmmono10-italic.otf]
```

`fontset=fandol` 为中文选择 TeX 发行版提供的 Fandol 字体集；`\setmainfont` 设置西文正文，`\setmonofont` 设置西文等宽字体。这里按 TeX 发行版中的字体文件名加载，避免部分电脑没有登记字体家族名而找不到字体；相关字体文件仍需要存在。在 XeLaTeX 下，`ctexart` 已经配置相关 Unicode 字体支持，因此不需要再叠加一套面向 pdfLaTeX 的传统字体编码方案。

若确实需要换中文字体，可在 XeLaTeX 的导言区使用 `\setCJKmainfont{字体名}`。前提是编译环境能够找到它：自己电脑上存在的字体，不代表共享项目或在线平台也存在。保留 Fandol 设置，是一个方便交换源码的起点。中文字体机制及跨引擎区别见 [ctex 官方文档](https://ctan.org/pkg/ctex)。

正文中的样式优先用语义清楚的命令：

```latex
\textbf{关键概念}
\emph{An Example Book}
\texttt{variable\_name}
{\kaishu 一小段局部楷体说明。}
{\large 一句较大的文字。}
```

最后两处用花括号限制作用范围，避免字号或字体一直延续到后文。中文的斜体、粗体效果由字体及配置共同决定，不能把西文字体的表现直接套在汉字上。`\textsc{Small Caps}` 也需要字体支持，不是中文标题的通用处理方法。

## 标题、留白与颜色放在导言区

下面是一组可以一起使用的设置。代码里的颜色值只是本章选用的示例，后续修改一个名字，就能保持全文统一。

```latex
\usepackage[margin=2.5cm,headheight=16pt]{geometry}
\usepackage{xcolor,fancyhdr}
\definecolor{inkblue}{HTML}{385A75}
\definecolor{paperblue}{HTML}{F1F5F8}
\ctexset{section={format=\Large\bfseries\color{inkblue}}}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{LaTeX 学习手记}
\fancyhead[R]{字体与版面}
\fancyfoot[C]{\thepage}
```

`geometry` 负责页面尺寸；`fancyhdr` 负责页眉页脚。标题页可能使用文档类规定的 `plain` 页面样式，因此它不一定和后续页面完全相同，这是需要阅读 PDF 检查的地方。

正文里，`\textcolor{inkblue}{文字}` 只改变花括号中的内容；单独写 `\color{inkblue}` 会影响其所在分组内后续的文字。提示信息最好同时有明确文字，不让颜色承担全部含义；打印成灰度后也应该能读懂。

```latex
\usepackage[expansion=false]{microtype}
```

这行可以加入 XeLaTeX 项目。微排版功能取决于引擎：XeTeX 支持字符边缘突出等功能，但不支持字体伸缩，所以这里显式关闭 `expansion`。它能改善部分细节，却不会替你拆开过宽的公式或表格。功能差异见 [microtype 官方文档](https://ctan.org/pkg/microtype)。

## 让读者看到代码，而不是让 LaTeX 执行它

正文写下 `\section{材料}` 会生成标题；教程有时需要把这条命令原样印出来。短代码可以用 `\verb|...|`，较长代码需要专门的环境。含下划线的变量名，放在这些环境中，也不需要逐个手动转义。

英文程序代码可以从 `listings` 开始。下面将设置放在导言区，将 `lstlisting` 放在正文。

```latex
% 导言区
\usepackage{listings}
\lstset{
  basicstyle=\ttfamily\small,
  breaklines=true,
  showstringspaces=false
}

% 正文
\begin{lstlisting}[language=Python]
values = [120, 80, 200]
total = sum(values)
print(total)
\end{lstlisting}
```

这里的 Python 代码只被排版，不会运行。若展示的是分析脚本，代码旁仍然需要解释输入是什么、输出是什么；一块彩色源码不会自动成为分析结论。

包含中文的 LaTeX 示例，使用 `fvextra` 提供的 `Verbatim` 往往更直接。它关注原样显示和断行，不默认提供程序语言的语法高亮。

```latex
% 导言区
\usepackage{fvextra}

% 正文
\begin{Verbatim}[breaklines=true,fontsize=\small]
\section{材料整理}
百分号写作 \%，与号写作 \&，下划线写作 \_。
\end{Verbatim}
```

注意大写的 `Verbatim` 与普通小写 `verbatim` 是不同环境；环境名称必须配对。复杂标题、图注等命令参数中也不宜随意塞入原样代码环境。中文显示仍依赖中文字体和引擎配置，示例使用的 XeLaTeX 与 Fandol 组合可作为起点。断行选项可以查阅 [fvextra 官方文档](https://ctan.org/pkg/fvextra)。

`minted` 是另一个选择，但需要和安装版本相配的外部高亮工具及执行权限设置。第一次整理笔记时，先把 `listings` 或 `Verbatim` 用稳妥；需要更丰富高亮时，再按 `minted` 当前手册配置，不要把“打开一个选项”当成所有环境都适用的答案。

## 一个小流程图就够开始

TikZ 适合让简单流程与文档一起维护。下载示例里把“输入材料—核对来源—输出文档”画成三个节点。下面的代码放在正文，导言区加载 `\usepackage{tikz}`。

```latex
\begin{tikzpicture}[
  every node/.style={draw,rounded corners,
    minimum width=25mm,minimum height=10mm}]
  \node (a) at (0,0) {输入材料};
  \node (b) at (4,0) {核对来源};
  \node (c) at (8,0) {输出文档};
  \draw[->] (a) -- (b);
  \draw[->] (b) -- (c);
\end{tikzpicture}
```

节点名称 `a`、`b`、`c` 用来连线，花括号中的文字用来显示。改文字不会破坏连线关系。更复杂的统计图，通常适合先由数据分析工具输出 PDF 或图片，再按上一章的方法插入；无需为了统一工具而手动画每一个点。

## 本章练习

把完整示例的主题色改成另一种深色，检查标题、页眉和图形是否保持协调；加入一段含中文注释的代码，观察是否缺字或超出页边。最后用普通大小阅读生成的 PDF，确认正文和代码都能轻松看清。

保存一个能稳定编译的版本，再逐次添加样式。若遇到报错，回到最后一次成功的改动，通常比一次更换多套主题更容易定位问题。

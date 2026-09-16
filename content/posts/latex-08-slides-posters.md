+++
title = "演示与海报：把一份笔记讲给别人听"
date = "2026-09-16"
tag = "LaTeX 学习手记"
summary = "从 Beamer 幻灯片走到学术海报，用三个独立示例理解页面、内容块、分栏与代码展示。"
authors = ["Ziyu Peng", "刘毅涵"]
series = "latex"
order = 8
stage = "第三阶段 · 整理成完整作品"
+++

笔记允许读者停下来细看，汇报却需要跟随讲话的节奏。把文章改成演示文稿时，先想清楚每一页回答什么，再决定放多少内容。海报又多了一层要求：读者可能从任何一个内容块开始阅读，标题和图注需要帮助他们找到路线。

这一章准备了三份独立文件。它们分别演示 Beamer 幻灯片、TikZ 海报和 Beamer 海报，都是排版练习，没有实际研究结果。

- [下载 Beamer 幻灯片示例](/liuyihan/assets/tutorial/examples/latex-08.tex)
- [下载 tikzposter 海报示例](/liuyihan/assets/tutorial/examples/latex-08-tikzposter.tex)
- [下载 beamerposter 海报示例](/liuyihan/assets/tutorial/examples/latex-08-beamerposter.tex)

每份文件都单独选择 XeLaTeX 编译，不要把三段文档类声明拼到同一个主文件里。

## Beamer：一页内容放在一个 frame 里

`beamer` 是文档类，`frame` 是一页逻辑内容的基本容器。下面是一个完整的中文最小示例。

```latex
% !TeX program = xelatex
\documentclass[aspectratio=169]{beamer}
\usepackage[UTF8,fontset=fandol]{ctex}
\usetheme{Madrid}
\setbeamertemplate{navigation symbols}{}
\title{怎样把一页报告讲清楚}
\author[Ziyu Peng, 刘毅涵]{\href{https://github.com/pzy54154631-hub}{\textit{Ziyu Peng}}, University of Colorado Boulder,
  \texorpdfstring{\\[0.1em]}{ }Boulder, CO 80309, USA
  \texorpdfstring{\\[0.35em]}{; }
  \href{https://pzy54154631-hub.github.io/liuyihan/}{刘毅涵}，暨南大学经济学院}
\date{}

\begin{document}
\begin{frame}
  \titlepage
\end{frame}

\begin{frame}{这一页只回答一个问题}
  \begin{block}{先给出要点}
    标题、图表与解释，应共同说明同一个问题。
  \end{block}
  \begin{itemize}
    \item 标明数据单位和来源。
    \item 留下听众理解图表的时间。
    \item 把细节放进附录或讲义。
  \end{itemize}
\end{frame}
\end{document}
```

`aspectratio=169` 指定 16:9 比例；`\usetheme` 控制整套视觉样式。主题可以之后再换，先确认内容结构成立。`\titlepage` 从前面定义的标题、作者、日期读取信息，修改一次就能更新封面。

`frame` 不一定只输出一张 PDF 页面：使用覆盖显示命令时，一页逻辑内容可以分成多个展示步骤。例如 `\pause` 会把后续内容延后显示。初学时先保持静态页面，确认逻辑连贯，再决定是否需要逐步揭示。框架与覆盖显示机制见 [Beamer 官方项目和手册](https://ctan.org/pkg/beamer)。

## 两栏是为了建立关系

可以把图放左边，把解释放右边，或者把问题和方法并排。Beamer 的列宽使用实际长度，下面两列各占正文宽度的 47%，中间留有空间。

```latex
\begin{frame}{图表与解释放在一起}
  \begin{columns}[T,onlytextwidth]
    \begin{column}{0.47\textwidth}
      \begin{block}{观察什么}
        先明确比较对象、范围与单位。
      \end{block}
    \end{column}
    \begin{column}{0.47\textwidth}
      \begin{block}{怎样解释}
        再交代结论成立的条件与局限。
      \end{block}
    \end{column}
  \end{columns}
\end{frame}
```

`T` 让两栏从顶部对齐；`onlytextwidth` 把总宽度限制在正文区域。装不下时优先拆成两页，或者把长段落改成真正需要口头说明的要点。把字号一直缩小，会让听众承担版面安排的问题。

## 代码页需要 fragile

原样代码与一般正文的读取方式不同。包含 `verbatim`、`lstlisting` 等内容的 Beamer 页，通常需要给 `frame` 加上 `[fragile]`。下面是正文片段。

```latex
\begin{frame}[fragile]{展示一段命令}
\begin{verbatim}
\section{A clear structure}
One question, one main message.
\end{verbatim}
\end{frame}
```

环境的结束命令最好各占一行，不把 `\end{frame}` 藏进其他命令或压缩成一行。中文源码的展示方式可以沿用上一章的 `fvextra`，同时保留 `fragile`。

下载的完整幻灯片还包含一个小表格，便于练习“说明—表格”对应关系。表里的金额都是虚构值，教学说明应和数字一起保留。

## tikzposter：用内容块搭起一张海报

`tikzposter` 自身就是文档类。它把海报组织成 `\block`，并通过 `columns` 和 `\column` 管理分栏。以下代码可单独保存编译。

```latex
% !TeX program = xelatex
% 作者：Ziyu Peng、刘毅涵
\documentclass[25pt,a0paper,portrait]{tikzposter}
\usepackage[UTF8,fontset=fandol]{ctex}
\usepackage[hidelinks]{hyperref}
\title{从问题到表达：一张学习海报}
\author{\href{https://github.com/pzy54154631-hub}{\textit{Ziyu Peng}}, University of Colorado Boulder,
  \\[0.1em]Boulder, CO 80309, USA
  \\[0.35em]
  \href{https://pzy54154631-hub.github.io/liuyihan/}{刘毅涵}，暨南大学经济学院}
\institute{LaTeX 学习手记 · 教学示例}
% tikzposter 2.0 的标题缩放键兼容修正。
\makeatletter
\define@key{title}{titletextscale}{\def\TP@titletextscale{#1}}
\makeatother
% 中文标题使用正常直立字形，不请求小型大写字形。
\renewcommand{\sc}{\upshape}
\usetheme{Board}
\begin{document}
\maketitle
\block{先交代问题}{这张海报演示标题、分栏和内容块，不展示真实研究结果。}
\begin{columns}
  \column{0.5}
  \block{材料与方法}{用短句解释材料来源和处理步骤；真实项目需要注明数据范围。}
  \column{0.5}
  \block{结果与讨论}{图表应回答标题中的问题，并说明单位、来源与局限。}
\end{columns}
\block{继续阅读}{根据实际报告内容添加参考文献与联系方式。}
\end{document}
```

这里的 `0.5` 是比例，不需要追加 `\textwidth`。`a0paper` 与 `portrait` 分别设置纸张和方向，`25pt` 是海报级别的基础字号选项，不能把 A4 文章的字号直接搬过来。主题与内容块的设置可以查阅 [tikzposter 官方文档](https://ctan.org/pkg/tikzposter)。

这一文件是可工作的骨架。完整下载版还包含针对 `tikzposter 2.0` 标题缩放键的兼容修正，并把中文标题设为直立字形，避免旧主题请求中文小型大写字形产生替代警告。正式海报还需要安排图表、来源、留白与信息密度，不能把课程论文全文分成几个方块就直接印刷。

## beamerposter：保留 Beamer 的写法

另一条路线是在 `beamer` 文档类中加载 `beamerposter`。它提供大幅面页面和字体缩放，内容仍然放在 `frame` 中，分栏仍然使用 Beamer 的长度语法。

```latex
% !TeX program = xelatex
\documentclass{beamer}
\usepackage[UTF8,fontset=fandol]{ctex}
\usepackage[orientation=portrait,size=a0,scale=1.4]{beamerposter}
\usetheme{Madrid}
\setbeamertemplate{navigation symbols}{}
\setbeamertemplate{footline}{}

\begin{document}
\begin{frame}[t]
  \begin{center}
    {\LARGE\bfseries 从问题到表达\par}
    \bigskip
    \href{https://github.com/pzy54154631-hub}{\textit{Ziyu Peng}}, University of Colorado Boulder,
  \\[0.1em]Boulder, CO 80309, USA
  \\[0.35em]
  \href{https://pzy54154631-hub.github.io/liuyihan/}{刘毅涵}，暨南大学经济学院
  \end{center}
  \vspace{1cm}
  \begin{columns}[t,totalwidth=\textwidth]
    \begin{column}{0.48\textwidth}
      \begin{block}{问题与材料}
        此处是排版占位说明，不是真实研究结果。
      \end{block}
    \end{column}
    \begin{column}{0.48\textwidth}
      \begin{block}{表达与解释}
        交代图表单位、材料来源与结论适用范围。
      \end{block}
    \end{column}
  \end{columns}
\end{frame}
\end{document}
```

`scale` 调整相关字体缩放，并不等于把任何长度的内容都自动压进页面。不要同时把 `tikzposter` 的 `\column{0.5}` 原样搬来：两个系统使用相近的名字，却有不同语法。页面尺寸和缩放选项见 [beamerposter 官方文档](https://ctan.org/pkg/beamerposter)。

## 把完成标准放在实际阅读里

先完成三页小汇报：第一页提出问题，第二页放一个图表或例子，第三页解释结果与局限。然后用同一份内容做一张海报，只保留值得让读者驻足的部分。这样能比较两种媒介的信息组织方式，而不是只更换页面大小。

检查幻灯片时使用全屏演示，检查海报时既看整体，也放大到接近实际阅读尺寸。确认文字没有被裁切，列宽没有溢出，来源和图注可读；送印前再核对对方要求的纸张尺寸与方向。完整示例能帮助起步，最终版面仍需要以自己的内容来判断。

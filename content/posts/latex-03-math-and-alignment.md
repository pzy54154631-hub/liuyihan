+++
title = "把公式写得清楚，也写得准确"
date = "2026-09-16"
tag = "LaTeX 学习手记"
summary = "从行内公式到多行推导，理解上下标、数学符号、编号与对齐的选择。"
authors = ["Ziyu Peng", "刘毅涵"]
series = "latex"
order = 3
stage = "第二阶段 · 把公式与图表讲清楚"
+++

公式排版的目标，是让读者看清变量之间的关系。先判断它是句子的一部分、一条重要结论，还是一段推导，再选择环境，比先记住大量命令更实用。本章把几种经常混用的写法放到一起比较。

## 行内、独立显示与自动编号

句子里的短公式用 `\(...\)`，也可以使用 `$...$`。需要强调或较长的式子用 `\[...\]` 独立显示；需要后文引用时，使用 `equation` 自动编号。下面的代码片段放在正文，导言区先加载 `amsmath`。

```latex
样本均值记为 \(\bar{x}\)。

\[
\bar{x}=\frac{1}{n}\sum_{i=1}^{n}x_i
\]

\begin{equation}
  \bar{x}=\frac{1}{n}\sum_{i=1}^{n}x_i
  \label{eq:mean}
\end{equation}
由式~\eqref{eq:mean}~可计算算术平均值。
```

`\eqref` 会为公式编号带上括号。不应手写“公式（3）”，也不必为每个短式子都编号。独立公式仍然属于句子，是否加逗号或句号要看上下文。编号的作用是帮助定位，最好留给需要引用的关系。写完后，沿着正文依次读一遍公式前后的句子，检查它是否仍然是一段完整的解释。网页中的独立公式用另一层显示标记呈现；复制到 `.tex` 文件时，请使用本章代码块里的 LaTeX 环境。

## 上下标与花括号

`x_i` 的下标只有一个字符；`x_{i+1}` 把整个 `i+1` 放进下标。指数同理，`x^12` 只会把 `1` 作为上标，十二次方应写为 `x^{12}`。

```latex
\[
x_{i+1},\qquad x^{12},\qquad
\frac{a+b}{c+d},\qquad \sqrt{x},\qquad
\binom{n}{k}=\frac{n!}{k!(n-k)!}
\]
```

分式的分子、分母都由花括号包住。阅读源码时，可以把 `\frac{a+b}{c+d}` 理解成两块整体，逐一核对左右括号。括号需要随较高的分式调整大小时，可用 `\left(` 与 `\right)` 成对包围；普通小式子不必全部加上自动伸缩括号。

## 数学字母与函数名不是同一种文字

数学模式中的普通字母通常按变量处理，输入 `sin x` 会把 `s`、`i`、`n` 当作相邻变量；正弦应写成 `\sin x`。同样常用的有 `\log`、`\ln`、`\exp`、`\lim`、`\min` 和 `\max`。说明文字使用 `\text{...}`，例如下面的分段函数。

$$
f(x)=\begin{cases}x^2,&x\geq 0,\\-x,&x<0.\end{cases}
$$

```latex
\[
f(x)=
\begin{cases}
  x^2, & x\geq 0,\\
  -x,  & x<0.
\end{cases}
\]
```

常用符号不必一次背完，可以保留一个小索引：

| 写法 | 表示什么 | 写法 | 表示什么 |
| --- | --- | --- | --- |
| `\alpha`、`\beta` | $\alpha$、$\beta$ | `\Gamma`、`\Delta` | $\Gamma$、$\Delta$ |
| `\leq`、`\geq` | $\leq$、$\geq$ | `\in`、`\notin` | $\in$、$\notin$ |
| `\subseteq` | $\subseteq$ | `\cup`、`\cap` | $\cup$、$\cap$ |
| `\sum`、`\prod` | $\sum$、$\prod$ | `\forall`、`\exists` | $\forall$、$\exists$ |
| `\infty`、`\partial` | $\infty$、$\partial$ | `\mathbb{R}` | $\mathbb{R}$ |

`\mathbb` 的常用支持来自 `amssymb` 所加载的 AMS 字体功能。不是每个希腊字母都存在独立的大写命令，例如通常直接用拉丁字母 `A`、`B` 表示对应的大写字形，不要猜写 `\Alpha`。

## 按推导关系选择多行环境

`align` 适合几行等式沿等号对齐，`&` 标记对齐位置，`\\` 换行。它的每行通常各有编号，`align*` 不编号；在 `align` 某行加入 `\notag`，可以仅去掉该行编号。`align` 已经是独立数学环境，不应再放进 `\[...\]` 或 `equation` 中。

若同一个长等式拆成几行而只需要一个编号，可在 `equation` 内使用 `split`。没有共同对齐点的长表达式可考虑 `multline`；几个独立公式逐行居中则可用 `gather`。这些环境的差异与限制见 [amsmath 用户手册](https://ctan.org/pkg/amsmath)。

## 完整示例：一页代数推导

```latex
% !TeX program = xelatex
\documentclass[UTF8,a4paper,fontset=fandol]{ctexart}
\usepackage[margin=2.5cm]{geometry}
\usepackage{amsmath,amssymb}
\usepackage[hidelinks]{hyperref}
\title{公式与对齐练习}
\author{\href{https://github.com/pzy54154631-hub}{\textit{Ziyu Peng}}, University of Colorado Boulder,
  \\[0.1em]Boulder, CO 80309, USA
  \\[0.35em]
  \href{https://pzy54154631-hub.github.io/liuyihan/}{刘毅涵}，暨南大学经济学院}
\date{}
\begin{document}
\maketitle
\section{逐步计算}
设 \(x\in\mathbb{R}\)，展开得到
\begin{align}
  (x+1)^2 &= x^2+2x+1,\label{eq:expand}\\
  (x+1)^2-x^2 &= 2x+1.\label{eq:difference}
\end{align}
式~\eqref{eq:difference}~由式~\eqref{eq:expand}~两边减去
\(x^2\) 得到。

\section{一个编号的多行公式}
\begin{equation}
\begin{split}
  (a+b)^2-(a-b)^2
    &= (a^2+2ab+b^2)\\
    &\quad -(a^2-2ab+b^2)\\
    &= 4ab.
\end{split}
\end{equation}

\section{分段定义}
\[
|x|=\begin{cases}
  x,  & x\geq 0,\\
  -x, & x<0.
\end{cases}
\]
\end{document}
```

## 易错点与小练习

在数学环境里不要用空行划分段落，不要用一串空格试图对齐等号。正文中的下划线要转义为 `\_`；数学下标则必须进入数学模式。报错时也检查 `\begin` 与 `\end` 的环境名是否一致。

练习时把示例中的平方展开改为两条自己能够验证的等式，分别用 `align*` 和 `equation` 加 `split` 排版，比较编号行为。然后故意把 `x^{12}` 改成 `x^12`，观察成品：这类错误不一定报错，必须阅读 PDF 才能发现。

[下载本章完整示例 latex-03.tex](/liuyihan/assets/tutorial/examples/latex-03.tex)

## 继续查阅

- [amsmath 官方项目页与用户手册](https://ctan.org/pkg/amsmath)：多行公式、编号与数学文字。
- [AMS 字体与 amssymb](https://ctan.org/pkg/amsfonts)：扩展数学符号和字母。
- [LaTeX 官方文档中的数学指南](https://www.latex-project.org/help/documentation/)：按主题查找进一步说明。

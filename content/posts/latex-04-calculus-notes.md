+++
title = "从微积分公式到一页推导笔记"
date = "2026-09-16"
tag = "LaTeX 学习手记"
summary = "整理极限、导数、积分、级数和偏导数的写法，把条件与解释放回公式旁边。"
authors = ["Ziyu Peng", "刘毅涵"]
series = "latex"
order = 4
stage = "第二阶段 · 把公式与图表讲清楚"
+++

一份好用的数学笔记，需要同时留下公式、适用条件与推导关系。只收集漂亮的公式，很容易在复习时忘记变量范围，也容易把记号误认为定义。本章以常见微积分内容练习排版，为后面的经济学和金融应用准备一套清楚的表达方式。

## 极限记号之后，要有条件

`\lim_{x\to a}f(x)=L` 表示一个极限关系，但它本身不是完整的极限定义。初学笔记中可以先写研究对象，再写极限与结论。例如，若函数在 $a$ 处有定义，且趋近方式在定义域内考虑，连续性可用下面的关系表达：

$$
\lim_{x\to a}f(x)=f(a).
$$

```latex
\[
\lim_{x\to a}f(x)=f(a),\qquad
\lim_{n\to\infty}a_n=A.
\]
```

`\to` 比手写字符箭头更统一，`\infty` 是无穷符号。一个是函数极限，一个是数列极限；排版相似，并不意味着变量的取值方式相同。在定义域端点处讨论连续性时，还要说明相应的单侧趋近。

## 导数：变量、算子与说明分开

导数定义在极限存在时写作

$$
f'(x)=\lim_{h\to0}\frac{f(x+h)-f(x)}{h}.
$$

```latex
\[
f'(x)=\lim_{h\to0}\frac{f(x+h)-f(x)}{h}.
\]
```

需要强调求导变量时，写 `\frac{\mathrm{d}}{\mathrm{d}x}`。本系列用正体 `\mathrm{d}` 表示微分记号，这是一种保持全文一致的排版选择。

常见法则可以按“对象—条件—结果”整理。例如，在相关函数可微的条件下，乘积法则为 $(uv)'=u'v+uv'$，链式法则为 $(f(g(x)))'=f'(g(x))g'(x)$。对数函数 $\ln x$ 在实数范围内需要 $x>0$；若写一般幂函数 $x^a$ 的求导公式，先取 $x>0$ 可避免对实指数定义域的含混。

## 积分：不要丢掉常数和微分

不定积分表示一族原函数，因此通常需要积分常数；定积分在条件满足时给出确定的数值。下面把二者放在一起，方便比较。

```latex
\begin{align*}
  \int x^2\,\mathrm{d}x &= \frac{x^3}{3}+C,\\
  \int_0^1 x^2\,\mathrm{d}x &= \frac{1}{3}.
\end{align*}
```

`\,` 在被积函数与微分之间加入一点空隙。对幂函数，$\int x^n\,\mathrm{d}x=x^{n+1}/(n+1)+C$ 要注明 $n\ne-1$，并在实函数有定义的区间内使用；$n=-1$ 时则涉及 $\ln|x|+C$。漂亮的分式不能代替这些数学条件。

分部积分可写成 $\int u\,\mathrm{d}v=uv-\int v\,\mathrm{d}u$。定积分换元时，除了替换被积函数与微分，也要转换上下限，或先回代原变量再计算，避免把两套变量混在同一个式子里。

## 级数：上下限与收敛范围一起记录

求和使用 `\sum_{n=0}^{\infty}`。几何级数最适合练习“条件紧挨着结论”的写法：

$$
\sum_{n=0}^{\infty}ar^n=\frac{a}{1-r},\qquad |r|<1.
$$

```latex
\[
\sum_{n=0}^{\infty}ar^n=\frac{a}{1-r},
\qquad |r|<1.
\]
```

指数函数的幂级数为 $e^x=\sum_{n=0}^{\infty}x^n/n!$，对所有实数 $x$ 都成立。把级数截断到有限项得到近似式时，应改用 `\approx` 或写出余项，而不能直接保留等号并删掉剩余部分。求和从 0 还是从 1 开始，也要随原式核对。

## 偏导数与向量：每个变量的位置都要明确

多元函数对单一变量求导使用 `\partial`。若 $z=f(x,y)$，其中 $x=x(t)$、$y=y(t)$，在相应可微条件下，链式法则写为

$$
\frac{\mathrm{d}z}{\mathrm{d}t}
=\frac{\partial f}{\partial x}\frac{\mathrm{d}x}{\mathrm{d}t}
+\frac{\partial f}{\partial y}\frac{\mathrm{d}y}{\mathrm{d}t}.
$$

梯度 `\nabla f`、散度 `\nabla\cdot\mathbf{F}`、旋度 `\nabla\times\mathbf{F}` 可作为后续符号索引；双重积分和三重积分则使用 `\iint`、`\iiint`。这些命令负责表达形式，具体计算仍需结合课程定义、区域和方向条件。

## 完整示例：将一个函数整理成学习卡片

```latex
% !TeX program = xelatex
\documentclass[UTF8,a4paper,fontset=fandol]{ctexart}
\usepackage[margin=2.5cm]{geometry}
\usepackage{amsmath,amssymb}
\usepackage[hidelinks]{hyperref}
\title{微积分学习卡片}
\author{\href{https://pzy54154631-hub.github.io/homepage/}{\textit{Ziyu Peng}}, University of Colorado Boulder
  \\[0.35em]
  \href{https://pzy54154631-hub.github.io/liuyihan/}{刘毅涵}，暨南大学经济学院}
\date{}
\begin{document}
\maketitle
\section{从函数到导数}
设 \(f(x)=x^2+2x\)，其中 \(x\in\mathbb{R}\)。
\begin{align*}
  f'(x) &= 2x+2,\\
  f''(x) &= 2.
\end{align*}
在 \(x=-1\) 处，一阶导数为零；
又因二阶导数为正，此处为严格局部极小值点。

\section{积分与验证}
\begin{align*}
  \int f(x)\,\mathrm{d}x
    &= \frac{x^3}{3}+x^2+C,\\
  \int_0^1 f(x)\,\mathrm{d}x
    &= \left[\frac{x^3}{3}+x^2\right]_0^1
     = \frac{4}{3}.
\end{align*}
对原函数再求导，可以检查不定积分的结果。

\section{拓展到两个变量}
设 \(g(x,y)=x^2+xy+y^2\)，则
\[
\nabla g=
\begin{pmatrix}
  2x+y\\
  x+2y
\end{pmatrix}.
\]
本例统一把梯度写成列向量。
\end{document}
```

## 小练习：检查式子，也检查适用范围

把函数改为 $f(x)=x^3$，重新写出一阶导数和从 0 到 1 的定积分；再把双变量函数改为 $g(x,y)=xy$，计算两个偏导数。最后给几何级数增加一行有限和，比较有限和与无穷级数的条件。完成后既检查括号、编号和对齐，也用手算确认结果。

[下载本章完整示例 latex-04.tex](/liuyihan/assets/tutorial/examples/latex-04.tex)

## 继续查阅

- [amsmath 项目与用户手册](https://ctan.org/pkg/amsmath)：积分、矩阵和多行数学环境。
- [AMS 字体与扩展符号](https://ctan.org/pkg/amsfonts)：实数集等数学字母的支持。
- [LaTeX 官方数学文档入口](https://www.latex-project.org/help/documentation/)：寻找数学排版指南及更完整的示例。

+++
title = "经济学模型：把约束、推导与供需图写清楚"
date = "2026-09-16"
tag = "LaTeX 学习手记"
summary = "从预算约束到拉格朗日条件，再用 PGFPlots 画一张可核对的供需图。"
authors = ["Ziyu Peng", "刘毅涵"]
series = "latex"
order = 9
stage = "第四阶段 · 带进经管课堂"
+++

前面学会公式、图形与交叉引用后，可以试着把它们放进一页经济学作业。重点不只是让一条公式居中：读者需要知道变量代表什么、结论依赖什么假设，以及图中的点为什么出现在那里。本篇用两个自设的小模型练习这些表达，参数均为教学设定。

## 先把问题写完整

考虑一个消费者在两种商品之间分配预算。$x,y$ 是消费数量，$p_x,p_y$ 是单价，$m$ 是可支配预算；所有价格和预算均为正。为便于求解，取 $0<\alpha<1$，并在 $x,y>0$ 上使用对数效用：

$$
\max_{x,y>0}\;\alpha\ln x+(1-\alpha)\ln y
\quad\text{s.t.}\quad p_xx+p_yy\le m.
$$

`\max` 会把“max”排成运算符，`\ln` 同理；不要直接输入斜体字母 `max` 或 `ln`。约束前的 `\text{s.t.}` 是普通说明文字。公式后的正文应解释符号，避免把一连串字母交给读者猜。预算约束与效用最大化的入门背景可以参照 [OpenStax 的消费选择章节](https://openstax.org/books/principles-microeconomics-3e/pages/6-1-consumption-choices)。

这里先写“支出不超过预算”，再根据效用对两种商品严格递增，说明最优点会花完预算。这一步使随后的等式约束有了理由。它不适用于所有偏好；例如出现饱和点时，就不能直接照搬。

## 多行推导要对齐推理关系

等式预算下，拉格朗日函数为：

$$
\mathcal L=\alpha\ln x+(1-\alpha)\ln y+\lambda(m-p_xx-p_yy).
$$

将两个边际条件与预算等式写进 `align` 环境，在 `&` 后对齐等号。`\partial` 表示偏导，`\mathcal L` 则把函数符号与普通字母区分开。消去乘子后可得：

$$
x^*=\frac{\alpha m}{p_x},\qquad y^*=\frac{(1-\alpha)m}{p_y}.
$$

本例的对数效用在正数域严格凹，预算可行集是凸集，因此这里的一阶条件能确定唯一最优选择。写“求得驻点”与写“求得最大值”之间，需要这样的数学依据；仅仅让推导排得整齐，并不会自动证明结论。

把 $m=100,p_x=5,p_y=10,\alpha=0.4$ 代入，得到 $x^*=8,y^*=6$。再算一次 $5\times8+10\times6=100$，既检查推导，也检查录入时是否把分母和下标抄错。

## 用供需图练习坐标和标注

接着换一个独立的市场模型：逆需求为 $p_D(q)=12-0.5q$，逆供给为 $p_S(q)=2+0.5q$。本章只画 $0\le q\le20$ 的示意范围，联立得到均衡 $(q^*,p^*)=(10,7)$。这两条线并不是前面的消费者模型推出来的，也不对应任何实际商品。

经济学图常把数量放在横轴、价格放在纵轴，所以绘图函数要输入“价格关于数量的表达式”。在 PGFPlots 中，横坐标的内部变量仍写作 `x`，即使轴标签叫 $q$。`axis cs:10,7` 则让文字跟着数据坐标定位，不必靠目测挪动。

把需求画为实线、供给画为虚线，再加上图例，即使黑白打印也能区分。均衡点的水平和垂直投影用于读数，不应误标成第三条经济曲线。完整示例使用 [PGFPlots](https://ctan.org/pkg/pgfplots) 绘图，图注同时标明模型参数为自设。

## 把模型解释放在推导之后

这组偏好下，$p_xx^*=\alpha m$，说明消费者把收入的 $\alpha$ 部分花在商品 $x$ 上。$\alpha=0.4$ 表示支出份额为四成，不是购买数量占全部商品数量的四成；两类商品的计量单位未必相同，数量也不能随意相加。课堂报告可以把这一句放在最终公式后，让数学解重新回到原来的经济问题。

若固定收入与另一个价格，只把 $p_x$ 翻倍，本例的 $x^*$ 会减半。但这是一组特定偏好假设下的比较静态结论，不能把它说成所有消费者的普遍规律。介绍模型时，区分设定、推导与解释，也是在给后续讨论留下清晰的边界。

## 可编译示例

[下载本章完整示例](/liuyihan/assets/tutorial/examples/latex-09.tex)。新建文件后选择 XeLaTeX，编译两遍，以更新图号引用。此文件独立运行，不需要外部图片或数据。

```latex
% !TeX program = xelatex
% 教学模型；所有参数均为自设，不代表真实市场。
\documentclass[UTF8,a4paper,fontset=fandol]{ctexart}
\usepackage[margin=2.5cm]{geometry}
\usepackage{amsmath,amssymb,pgfplots}
\pgfplotsset{compat=1.18}
\usepackage[hidelinks]{hyperref}
\title{经济学模型：预算、选择与市场}
\author{\href{https://github.com/pzy54154631-hub}{\textit{Ziyu Peng}}, University of Colorado Boulder,
  \\[0.1em]College of Arts and Sciences, Statistics and Data Science
  \\[0.1em]Boulder, CO 80309, USA
  \\[0.1em]\href{mailto:Ziyu.PengSr@colorado.edu}{Ziyu.PengSr@colorado.edu}
  \\[0.35em]
  \href{https://pzy54154631-hub.github.io/liuyihan/}{刘毅涵}，暨南大学经济学院}
\date{}
\begin{document}
\maketitle
\section{消费者选择}
设两种商品数量为 $x,y>0$，价格 $p_x,p_y>0$，
收入 $m>0$，偏好参数 $0<\alpha<1$。采用对数效用：
\begin{equation}
  \max_{x,y>0}\; \alpha\ln x+(1-\alpha)\ln y
  \quad\text{s.t.}\quad p_xx+p_yy\le m.
  \label{eq:choice}
\end{equation}
因效用对两种商品均严格递增，最优选择用尽预算。
将约束写成等式后，拉格朗日函数及一阶条件为
\begin{align}
 \mathcal L&=\alpha\ln x+(1-\alpha)\ln y
           +\lambda(m-p_xx-p_yy),\\
 \frac{\partial\mathcal L}{\partial x}
   &=\frac{\alpha}{x}-\lambda p_x=0,\\
 \frac{\partial\mathcal L}{\partial y}
   &=\frac{1-\alpha}{y}-\lambda p_y=0,\\
 p_xx+p_yy&=m.
\end{align}
得到唯一最优解
\[
 x^*=\frac{\alpha m}{p_x},\qquad
 y^*=\frac{(1-\alpha)m}{p_y}.
\]
例如 $m=100,p_x=5,p_y=10,\alpha=0.4$，
有 $x^*=8,y^*=6$，预算核对为 $5\times8+10\times6=100$。
这些值仅是教学设定。

\clearpage
\section{供需示意图}
下面是与上例独立的线性市场模型：
\[
 p_D(q)=12-0.5q,\qquad p_S(q)=2+0.5q.
\]
联立后得到 $q^*=10,p^*=7$。图中横轴是数量，纵轴是价格。
\begin{figure}[htbp]
\centering
\begin{tikzpicture}
\begin{axis}[
 width=0.8\linewidth,height=7cm,
 axis lines=left,xmin=0,xmax=20,ymin=0,ymax=13,
 xlabel={数量 $q$},ylabel={价格 $p$},
 xtick={0,5,10,15,20},ytick={0,2,7,12},
 legend style={at={(0.98,0.98)},anchor=north east},
 samples=2]
\addplot[blue,thick,domain=0:20]{12-0.5*x};
\addlegendentry{需求}
\addplot[red,dashed,thick,domain=0:20]{2+0.5*x};
\addlegendentry{供给}
\addplot[gray,densely dotted,forget plot]
 coordinates {(0,7) (10,7) (10,0)};
\addplot[black,only marks,mark=*,forget plot]
 coordinates {(10,7)};
\node[above left] at (axis cs:10,7) {$E(10,7)$};
\end{axis}
\end{tikzpicture}
\caption{自设线性供需模型；曲线不来自市场数据。}
\label{fig:supply-demand}
\end{figure}
如图~\ref{fig:supply-demand}，虚线投影帮助读出均衡坐标。
\end{document}
```

## 容易出错的地方

- **把条件藏在公式外。** 正价格、正收入和 $0<\alpha<1$ 决定本例解的性质，不能在套用模板时一并删掉。
- **只画出交点，没有核对数值。** 可以先代回两条方程：$12-0.5\times10=2+0.5\times10=7$。
- **使用 `$$...$$` 排 LaTeX 源文件。** 网页手记用它分隔展示公式；下载的 `.tex` 中采用 `\[...\]` 或 `equation`，需要多行对齐则采用 `align`。
- **图形替代解释。** 图注说明“画了什么”，正文还要说明“为什么这与问题有关”。

## 留一个小练习

先把预算改为 $m=120$，保持价格和偏好参数不变，更新最优消费量并核对支出；然后把逆供给改为 $p_S(q)=4+0.5q$，重新计算并标出市场均衡。前者应得到 $(9.6,7.2)$，后者应得到 $(8,8)$。若图中的点没有一起移动，说明公式、代码与文字还没有同步完成。

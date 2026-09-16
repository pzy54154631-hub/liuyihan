+++
title = "图片与表格：让材料自己说清楚"
date = "2026-09-16"
tag = "LaTeX 学习手记"
summary = "从图片编号和并排子图，到会换行的三线表与跨页材料表，把信息组织得清楚、可引用。"
authors = ["Ziyu.Peng", "刘毅涵"]
series = "latex"
order = 5
stage = "第二阶段 · 把公式与图表讲清楚"
+++

图表进入文档之后，写作就多了一条线索：正文提出问题，图表提供材料，图注解释读者应该看到什么。排版时最值得花时间的，往往不是加边框，而是把标题、单位、来源和编号安排好。

这一章从一张图片开始，再把同样的思路带到表格。学完后，可以整理一页课程报告，也可以做一份有编号、有说明的活动资料。

[下载完整示例：图片与表格](/liuyihan/assets/tutorial/examples/latex-05.tex)。示例用方框代替外部图片，保存后可直接用 XeLaTeX 编译；里面的预算和材料条目全部为虚构教学内容。

## 先分清图片与图片容器

`graphicx` 提供 `\includegraphics`，负责读取图片。`figure` 则是浮动环境，负责把图片、标题和编号放在合适的位置。它们的工作不同：图片可以不放进 `figure`，但一旦需要编号、图注和交叉引用，浮动环境通常更方便。

下面分成两步，避免把宏包命令复制到正文里。

```latex
% 导言区
\usepackage{graphicx}
\graphicspath{{images/}}
```

把图片保存为项目中的 `images/reading-map.png`，再把这一段写在正文中。文件名是示例，必须对应自己实际上传的图片。

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.72\linewidth]{reading-map.png}
  \caption{阅读材料的整理流程}
  \label{fig:reading-map}
\end{figure}

图~\ref{fig:reading-map}~展示了材料的整理顺序。
```

`h`、`t`、`b`、`p` 分别允许当前位置、页顶、页底和浮动页；它们提供可选位置，并不保证图片紧贴源码所在行。图表移动以后，正文中的引用仍然有效，因此尽量写“见图 1”，少写“如下图”。`~` 是不可断行空格，可以避免“图”和编号分到两行。

`\label` 要放在 `\caption` 后，因为图号由 `\caption` 更新。引用第一次显示问号时，先再编译一次；持续存在的问号才需要检查标签拼写和重复标签。

图片大小优先设一个维度，让原始比例保持不变。在表格单元、子图或列表里，`\linewidth` 表示当前位置可用的行宽，通常比整页的 `\textwidth` 更合适。

## 两张图并排，需要两个层次的说明

比较图常有一个总标题，再给每个面板一个子标题。加载 `subcaption` 后，可以用 `subfigure` **环境**创建面板；这里不需要加载同名的旧 `subfigure` **宏包**。

```latex
% 导言区：\usepackage{subcaption}
\begin{figure}[htbp]
  \centering
  \begin{subfigure}[t]{0.46\linewidth}
    \centering
    \fbox{\rule{0pt}{25mm}\rule{0.8\linewidth}{0pt}}
    \caption{方案甲}\label{fig:a}
  \end{subfigure}\hfill
  \begin{subfigure}[t]{0.46\linewidth}
    \centering
    \fbox{\rule{0pt}{25mm}\rule{0.8\linewidth}{0pt}}
    \caption{方案乙}\label{fig:b}
  \end{subfigure}
  \caption{两种版面的比较示意}\label{fig:comparison}
\end{figure}
```

这一段不依赖图片文件。两个 `\fbox` 是占位框，之后可分别换成 `\includegraphics[width=\linewidth]{...}`。子图内部的 `\linewidth` 已经是该面板的宽度，不能再按整页宽度塞入图片。子图标题与总标题的设置见 [subcaption 官方项目与手册](https://ctan.org/pkg/subcaption)。

## 短表：先让列有分工，再画横线

表格的外层 `table` 管理浮动、标题和编号，内层 `tabular` 或 `tabularx` 管理行列。`booktabs` 的三条横线分别对应表头上方、表头下方和表格底部。简洁的横线通常已经足够，不必给每个单元格画完整方框。

遇到说明文字很长的表格，`tabularx` 的 `X` 列会分配剩余宽度并自动换行；普通 `l`、`c`、`r` 列不会因此自动折行。

```latex
% 导言区
\usepackage{booktabs,array,tabularx}
\newcolumntype{Y}{>{\raggedright\arraybackslash}X}

% 正文：所有金额均为虚构教学数据
\begin{table}[htbp]
  \centering
  \caption{活动物料预算（虚构教学示例）}
  \label{tab:budget}
  \begin{tabularx}{\linewidth}{@{}lYr@{}}
    \toprule
    项目 & 用途说明 & 金额（元）\\
    \midrule
    印刷 & 提供知识卡片，并预留少量备用。 & 120\\
    文具 & 用于填写反馈和记录问题。 & 80\\
    合计 & 仅演示排版。 & 200\\
    \bottomrule
  \end{tabularx}
\end{table}
```

这里让项目左对齐、金额右对齐、长说明自动换行。`@{}` 移除两侧多余的列间留白；`\arraybackslash` 让换行命令 `\\` 在这个自定义列中正常工作。表头已经写了“元”，金额单元格就不必重复单位。处理小数较多的结果表时，下一步可以学习专门的数字对齐工具，而不是靠手打空格凑位置。

表格设计和横线规则可以继续查阅 [booktabs 官方文档](https://ctan.org/pkg/booktabs)。

## 长表：让分页成为结构的一部分

`tabularx` 会换行，却不能自动把整张表分到多页。文献目录、材料清单足够长时，使用 `longtable`，并直接放在正文中，**不要再套 `table`**。

```latex
% 导言区：\usepackage{longtable,booktabs}
\begin{longtable}{@{}p{0.15\linewidth}
  p{0.33\linewidth}p{0.40\linewidth}@{}}
\caption{材料目录（虚构示例）}\label{tab:materials}\\
\toprule 编号 & 材料 & 整理说明\\\midrule
\endfirsthead

\multicolumn{3}{c}{表~\thetable\ （续）}\\
\toprule 编号 & 材料 & 整理说明\\\midrule
\endhead

\midrule\multicolumn{3}{r}{续下页}\\
\endfoot
\bottomrule
\endlastfoot

D01 & 示例记录 & 核对来源、日期和页码。\\
D02 & 示例访谈 & 保留匿名编号与转写说明。\\
% 继续添加短行；完整下载示例包含跨页内容。
\end{longtable}
```

四个分界命令分别定义首个表头、后续表头、续页页脚和末页页脚。列宽之和还要给列间距留空间，不能简单让所有 `p{...}` 加起来正好等于整行宽度。这里使用固定宽度的 `p` 列；`longtable` 本身不提供 `X` 列。

它通常在行与行之间分页，不能把一格中整页长的访谈自然拆开。遇到这种材料，应把长文本还给正文，把表格用于索引或简要比较。标准 `longtable` 也不适合直接放进双栏文档、`minipage` 或 Beamer 幻灯片。分页机制与限制见 [longtable 官方文档](https://ctan.org/pkg/longtable)。

## 留给自己的检查与练习

把下载示例里的方框换成一张自己的图，修改图注，然后在前文引用它。接着把短表新增一行，确认总额、单位和说明仍然一致。最后让长表跨页，检查每一页都有表头，末页没有多余的“续下页”。

如果版面拥挤，先减少重复文字、拆分信息或调整列宽，再考虑字号。缩小整张表虽然容易，却可能把最需要阅读的内容一起缩得很小。

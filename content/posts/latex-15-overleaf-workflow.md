+++
title = "在 Overleaf 中编译：从上传源码到交出 PDF"
date = "2026-09-16"
tag = "LaTeX 学习手记"
summary = "从空白项目和本站源码 ZIP 两条路径出发，设置 XeLaTeX 与主文件，练习编译、查错、上传图片以及导出 PDF 和源码。"
authors = ["Ziyu Peng", "刘毅涵"]
series = "latex"
order = 15
stage = "第五阶段 · 把文档交给别人"
+++

已经写好一段 LaTeX，下一步是让它变成可以交给老师或同学的 PDF。Overleaf 把编辑器、TeX 环境与预览放在浏览器里，适合先开始写作，再逐步熟悉文档结构。本章用一份中文课程笔记走完整个流程，也说明怎样把本站整本教程放进自己的项目继续修改。

## 从空白项目开始，先认清三个区域

打开 [Overleaf 官网](https://www.overleaf.com/)，注册或登录后进入项目列表。选择 **New Project → Blank project**，填写项目名称，例如 `course-note`，再点 **Create**。进入编辑器后，在文件列表中打开生成的 `.tex` 主文件，通常名为 `main.tex`。创建流程可对照 [Overleaf 官方第一份项目指南](https://docs.overleaf.com/getting-started/your-first-project)。

把界面理解成三个区域：文件列表管理源码与图片，源码编辑区写内容，PDF 预览区显示编译结果。屏幕较窄时，可能需要切换文件、编辑和预览面板。此时最重要的是知道自己正在编辑哪个文件，以及编译完成后看的是哪一份文档。

项目名称只是便于自己查找的标签，不会自动改掉 PDF 正文中的标题；正文标题由 `\title{...}` 和 `\maketitle` 控制。可以先修改项目名称，再修改代码中的标题，对比这两处变化。

## 中文编译前，先设置三件事

在项目中点击齿轮图标，或打开 **File → Settings**，进入 **Compiler** 面板。本系列按以下设置使用：

- **Compiler：XeLaTeX。** 这是实际执行排版的引擎；源码开头的 `% !TeX program = xelatex` 只是编辑器提示，不能替代网页设置。
- **TeX Live version：优先使用平台提供的较新版本。** 这是宏包与程序所在的发行版。接手已有模板时，先沿用其已验证版本，排查兼容性问题时再有目的地切换。
- **Main document：main.tex。** 它决定默认从哪个文件开始编译，主文件应放在项目根目录。

以上选项都针对当前项目。另建一个项目后，应重新检查。具体位置见 [编译器与 TeX Live 设置](https://docs.overleaf.com/getting-started/recompiling-your-project/selecting-a-tex-live-version-and-latex-compiler) 和 [主文件设置](https://docs.overleaf.com/getting-started/recompiling-your-project/the-main-document)。

中文示例使用 `\documentclass[UTF8,a4paper,fontset=fandol]{ctexart}`：`ctexart` 负责中文文章，`fontset=fandol` 使用 TeX 发行版提供的 Fandol 字体。这样无需把自己电脑上的中文字体名称搬到云端。若课程模板另有字体要求，按模板说明处理，不要把字体名称随意改成 `SimSun` 就期待服务器一定装有它。

## 编译一份包含公式与表格的中文笔记

把主文件中的默认示例全部替换成下面的代码，避免留下第二组 `\documentclass` 或 `\begin{document}`。表中数字是虚构教学数据，用于检查排版和计算口径。

```latex
% !TeX program = xelatex
% SPDX-License-Identifier: MIT
% Copyright (c) 2026 Ziyu Peng and 刘毅涵
% Author: https://github.com/pzy54154631-hub?tab=repositories
\documentclass[UTF8,a4paper,fontset=fandol]{ctexart}
\usepackage[margin=2.5cm]{geometry}
\usepackage{amsmath,booktabs}
\usepackage[hidelinks]{hyperref}

\title{我的第一份 Overleaf 课程笔记}
\author{Ziyu Peng \and 刘毅涵}
\date{}

\begin{document}
\maketitle

\section{先说明数据}
以下是虚构的活动预算数据，单位为元。
差异定义为实际支出减预算，负数表示低于预算。

\begin{table}[htbp]
\centering
\caption{活动支出记录（虚构教学数据，单位：元）}
\label{tab:expense}
\begin{tabular}{@{}lrr@{}}
\toprule
项目 & 预算 & 实际 \\
\midrule
印刷 & 120 & 110 \\
交通 & 80 & 85 \\
物资 & 200 & 195 \\
\midrule
合计 & 400 & 390 \\
\bottomrule
\end{tabular}
\end{table}

\section{再解释结果}
表~\ref{tab:expense}~中的实际支出合计为 390 元。
总差异率为
\begin{equation}
  d=\frac{390-400}{400}\times100\%=-2.5\%.
  \label{eq:change}
\end{equation}
式~\eqref{eq:change}~说明总支出低于预算，
但不能据此推断每个项目都节省了支出。

\end{document}
```

点击 **Recompile**。出现 PDF 后，核对中文标题、三列数据表、编号公式，以及正文中的“表 1”和“式 (1)”。总额低于预算 10 元，差异率为 $-2.5\%$，交通一项却高于预算 5 元；排版成功后仍要检查这些含义是否一致。

[下载本章完整示例 latex-15.tex](/liuyihan/assets/tutorial/examples/latex-15.tex)

修改一句正文后再次编译，确认预览里确实出现了新内容。Overleaf 的编译设置也支持自动编译；初学时先用手动编译，便于把一次改动和它产生的结果对应起来。[官方重新编译说明](https://docs.overleaf.com/getting-started/recompiling-your-project)介绍了这些选项。

## 已下载本站完整源码，怎样上传整本教程

从[整本下载入口](/liuyihan/blog/latex/#downloads)取得 **完整 LaTeX 源码 ZIP**，回到 Overleaf 项目列表，选择 **New Project → Upload project**，上传 ZIP。平台会解压并建立项目；这是导入整个项目的入口，与现有项目中上传单张图片的操作不同。[官方上传项目说明](https://docs.overleaf.com/managing-projects-and-files/uploading-a-project)列出了完整流程。

上传后，找到根目录的 `main.tex`，打开并设为主文件，再选择 XeLaTeX 编译。本站提供的 **`main.tex` 已包含整本正文，可以独立编译**。源码包中的 `examples/` 是各章独立示例；`chapters-md/` 是网站文章来源；`generate_book.py` 用于在本地重新生成整本源码。第一次在线编译无需运行这个脚本，也无需把每一份示例手动拼进正文。

如果自己重新打包过 ZIP，检查是否多包了一层文件夹。主文件应直接出现在文件列表的根部，而不是藏在 `my-download/main.tex` 之下。保留实际需要的子目录结构，移动根文件时也要注意图片与引用路径。

还有一个容易误会的细节：**打开一份带 `\documentclass` 的独立示例再点 Recompile，Overleaf 可能直接编译这份示例。** 如果预览突然从整本变成一两页，先重新打开根目录 `main.tex` 再编译。练习某章时，另建一个项目，只上传该示例和必要资源，通常更清楚。这一行为与默认主文件的区别见[官方主文件说明](https://docs.overleaf.com/getting-started/recompiling-your-project/the-main-document)。

## 给报告加图片，要上传文件而不是电脑路径

在项目文件列表上方选择 **Upload**，可选择本地文件，也可将文件拖入上传窗口。整理图片时，创建 `figures` 文件夹，把图片放进去，文件名例如 `budget-chart.png`。上传入口与文件夹操作见[官方文件上传指南](https://docs.overleaf.com/managing-projects-and-files/adding-files-to-a-project/uploading-files-to-a-project)。

假设根目录有 `main.tex`，图片位于 `figures/budget-chart.png`，先在导言区加入 `\usepackage{graphicx}`，再在正文加入：

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.75\linewidth]{figures/budget-chart.png}
  \caption{预算与实际支出对比}
  \label{fig:budget}
\end{figure}
```

这段代码需要你先上传对应图片，不能直接粘进一个没有图片的项目。路径相对于项目文件组织填写，不能写本机的 `C:\Users\...` 或 `/Users/...`。文件名、大小写和扩展名都应一致：上传了 `Budget-Chart.PNG`，代码却写 `budget-chart.png`，就可能找不到文件。优先使用清楚的英文文件名，也方便把项目发给别人。

## 没有 PDF 时，先读第一条错误

打开 **Logs and output files** 查看错误信息；在 Recompile 的下拉菜单中选择 **Stop on first error**，可以让程序在首个错误处停下，减少后续连锁报错。先看第一条明确错误、它对应的源码，以及前几行是否漏了花括号或结束环境。官方提供了[错误排查方法](https://docs.overleaf.com/troubleshooting-and-support/fixing-latex-errors)。

`Undefined control sequence ... \toprule` 通常提示 `booktabs` 没有加载或命令拼写有误，先检查导言区。若是 `File 'xxx.sty' not found`，核对宏包名；学校模板自带的 `.sty`、`.cls` 文件应一并上传。不要把缺少模板文件的问题改成换一套文档类，从而破坏原本要求的格式。

`Extra alignment tab has been changed to \cr` 常见于表格一行的 `&` 太多。本例 `{lrr}` 表示三列，每行通常需要两个分隔用的 `&`；普通文字里的与号应写成 `\&`。`Missing $ inserted` 则先检查是否把 `_` 等数学符号直接写在普通正文中。

中文字体错误先核对 **XeLaTeX、`ctexart` 与 `fontset=fandol`** 是否配套，再看日志点名了哪一种字体。已经出现 PDF 也不能跳过日志：编译器有时会尽力绕过错误生成文件，结果可能缺字、丢内容，或并非刚刚修改后的完整版本。

## 引用有问号、预览没更新，怎样继续查

若“表 1”变成“表 ??”，先检查 `\ref{tab:expense}` 与 `\label{tab:expense}` 的拼写完全一致，并把表格的 `\label` 放在 `\caption` 之后。再次编译，让辅助文件完成更新；不要把引用手动改成数字，掩盖尚未解决的问题。

如果确认源码正确，却仍遇到旧目录或辅助文件相关错误，可以在 Recompile 下拉菜单中选择 **Recompile from scratch**，清除缓存的辅助文件并重新编译。它不会修正拼错的标签，也不能替代缺失的图片或书目文件。操作说明见[清理项目缓存](https://docs.overleaf.com/troubleshooting-and-support/clearing-the-project-cache)。

如果预览没有出现刚修改的内容，再核对当前打开的文件、Main document 与编译日志。含参考文献的项目还要检查 `.bib` 文件是否上传、引用键是否存在，以及模板使用的文献工具；单纯连续点 Recompile 不能解决不存在的引用键。

## 编译超时，先缩小问题范围

遇到 timeout，先开启 Stop on first error 排除源码错误，再试 **Fast [draft]** 模式判断图片处理是否耗时。这个模式会用占位框代替图片，不能直接作为最终交稿版本。若草稿可编译、正常模式超时，可压缩过大的照片，减少不必要的高分辨率图片，把耗时的绘图提前导出为 PDF，并逐段恢复内容定位问题。

排查时保留项目副本，再移除无关资源或简化复杂内容。把整个项目再次压成 ZIP 并不会让编译更快；需要减少的是实际处理的工作量。可用编译时间随方案和平台规则变化，本章不保证整本教程在所有账户中都能于额度内完成。具体诊断路径见 [Overleaf 编译超时指南](https://docs.overleaf.com/troubleshooting-and-support/fixing-and-preventing-compile-timeouts)；必要时可下载源码，转到本地 TeX Live 编译。

## 交付时，PDF 和源码分别保存

完成最后一次正常模式编译后，打开 PDF 检查标题、表格、公式、引用和页边距。然后使用预览区的 **Download PDF** 图标，或 **File → Download → Download as PDF**，保存阅读版本。

再选择 **File → Download → Download as source (.zip)**，保存可以继续修改的项目。**源码 ZIP 不包含刚刚编译好的最终 PDF，所以两份都要下载。** 这两种导出方式见[官方项目下载说明](https://docs.overleaf.com/managing-projects-and-files/downloading-a-project)。把编译器、TeX Live 版本与主文件名记进项目说明，下一次换电脑或交给同学时就容易恢复环境。

如果继续分发本站教程或修改版，请一并保留源码包内的版权与 MIT 许可文件；个人新写的内容可以另作说明。源码能打开、PDF 能阅读、环境能解释，这份项目才方便接着写。

## 小练习：独立完成一次交付

用本章示例建立项目，将物资实际支出从 195 改为 185 元，同时更新合计、正文与公式。预期实际合计为 380 元，总差异为 $-20$ 元，差异率为 $-5\%$。LaTeX 中的这些数字是静态文本，不会随着表格一格变化自动重算。

编译后核对中文正常、引用没有问号、金额解释一致，再分别下载 PDF 和源码 ZIP。在项目副本中暂时去掉 `booktabs`，练习从第一条错误找到原因，随后恢复并重新编译。做到这一步，你就走完了从内容、环境、查错到交付的一整条流程。

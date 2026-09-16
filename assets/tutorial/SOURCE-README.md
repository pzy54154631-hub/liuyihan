# LaTeX 学习手记 · 完整源码

作者：[Ziyu Peng](https://github.com/pzy54154631-hub)，University of Colorado Boulder；[刘毅涵](https://pzy54154631-hub.github.io/liuyihan/)，暨南大学经济学院。

本源码包对应 15 章完整教程，包含教程书稿与 17 份可独立编译的章节示例。线上目录：<https://pzy54154631-hub.github.io/liuyihan/blog/latex/>。

## 文件说明

- `main.tex`：完整教程的 LaTeX 主文件。
- `examples/`：各章可独立编译的示例。第 08 章含演示文稿与两种海报示例，因此共有 17 份 `.tex` 文件。
- `LICENSE.txt`：完整 MIT 许可证。
- `NOTICE.md`：作者、许可范围与第三方内容说明。
- `chapters-md/`：15 章网页正文的 Markdown 原稿。
- `generate_book.py`：可选的重新生成脚本；仅编辑或编译 `main.tex` 不需要运行它。

## 编译完整教程

解压源码包，在项目目录使用 **XeLaTeX** 编译 `main.tex`。所有文件均以 UTF-8 保存。建议安装带有中文宏包与 Fandol 字体的较完整 TeX Live 或 MacTeX 环境；也可以将整个文件包上传到 Overleaf，并将主文档设为 `main.tex`、编译器设为 XeLaTeX。

推荐使用能够自动更新目录和交叉引用的 `latexmk`：

```sh
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
```

也可以手动运行 XeLaTeX 两遍；如日志仍要求更新引用，再编译一次：

```sh
xelatex -interaction=nonstopmode -halt-on-error main.tex
xelatex -interaction=nonstopmode -halt-on-error main.tex
```

教程内的代码框是讲解内容，不会在编译教程书稿时逐一执行。要运行某一章的示例，请单独编译 `examples/` 中对应文件。

Overleaf 的逐步操作、主文件选择与排错见[第 15 章：在 Overleaf 中编译与导出](https://pzy54154631-hub.github.io/liuyihan/blog/latex-15-overleaf-workflow/)。

## 编译章节示例

在 `examples/` 目录运行，以下以第 01 章为例：

```sh
latexmk -xelatex -interaction=nonstopmode -halt-on-error latex-01.tex
```

第 07 章使用 `biblatex` 与 **Biber**，示例首次编译会生成配套的虚构书目文件。`latexmk` 通常会自动完成 Biber 流程；手动编译顺序为：

```sh
xelatex latex-07.tex
biber latex-07
xelatex latex-07.tex
xelatex latex-07.tex
```

该章生成的 `.bib` 文件包含明确标注的虚构教学文献。若改动代码中的 `filecontents*` 内容，应同时检查已经生成的同名 `.bib` 文件，因为默认不会覆盖已有文件。不要把虚构条目当作真实研究来源引用。

第 08 章的两个海报文件分别需要 `tikzposter` 与 `beamerposter` 宏包。若编译提示某宏包缺失，按日志安装相应宏包后重新编译。

## 编辑与分享

教程原创正文、PDF、LaTeX 源码和原创示例采用 **MIT 许可证**，允许自由编辑、复制、改编与分享。再发布全部或实质性部分时，请保留版权声明和完整 `LICENSE.txt` 文本。第三方宏包、字体与引用资料遵循各自原有许可；详细范围见 `NOTICE.md`。

经济、金融与会计例子用于说明公式、数据和报表的排版，示例数据不是实际研究结果或企业报表。修改数值后，应同时检查正文、公式与表格是否保持一致。

## 可选：从 Markdown 重新生成整本源码

如果习惯编辑 Markdown，可以修改 `chapters-md/` 中对应章节，然后重新生成 `main.tex`。这一步需要 Python 3.11 或更新版本和带 Pandoc 的 Python 包；普通 LaTeX 编译不需要它们。

```sh
python -m pip install pypandoc_binary
python generate_book.py --posts chapters-md --output main.tex
latexmk -xelatex main.tex
```

重新生成会覆盖 `main.tex`，请先保存你直接在 LaTeX 源文件中所做的修改。

# 毅涵的小站

刘毅涵的个人主页与博客。独立站点地址：**https://pzy54154631-hub.github.io/liuyihan/**。

本项目使用独立仓库与 GitHub Pages 部署，不依赖、不修改 `homepage` 仓库。

## 写一篇新手记

1. 在 GitHub 上打开 `content/posts`，选择 **Add file → Create new file**。
2. 文件名使用日期和英文短名，例如 `2026-09-20-learning-note.md`，粘贴下方格式并写正文。
3. 选择 **Commit changes** 保存到 `main`。发布完成后，首页、手记列表和 RSS 会自动更新。

```markdown
+++
title = "文章标题"
date = "2026-09-20"
tag = "学习笔记"
summary = "一两句话介绍这篇文章。"
+++

这里开始写正文，可以使用普通 Markdown。

## 一个小标题

继续写你的内容。
```

在开头字段中加入 `draft = true` 可暂缓发布该文章；如需保密，请不要将未发布的私人内容提交到公开仓库。

## 修改个人信息

编辑 `content/profile.json`。当前公开姓名、学校专业、经历与邮箱，不公开电话号码，也不提供含电话的简历下载。`projects` 保存“关于我”中的项目经历，可编辑标题、角色、时间、说明段落与作品链接。

样式在 `assets/site.css`；页面生成逻辑在 `build.py`，通用页面结构在 `templates/layout.html`。首页文案与文章均可随时修改。

## LaTeX 学习系列

目录位于 `/liuyihan/blog/latex/`。15 章按 5 个阶段排列，覆盖入门、公式图表、引用与展示、经管应用、AI 辅助写作和 Overleaf 实操。署名顺序为 Ziyu Peng、刘毅涵；首篇按作者提供的时间标为 2026 年 7 月，合集整理日保持 2026-09-16。其余篇章显示合集收录时间，不补造中间的具体日。`date` 支持 `YYYY-MM` 的月精度，`updated` 可记录合集整理日；RSS 对缺少日的日期不生成 `pubDate`。

章节正文在 `content/posts/latex-*.md`，可以直接在 GitHub 编辑。除了普通文章字段，系列文章还包含：

```toml
authors = ["Ziyu Peng", "刘毅涵"]
series = "latex"
order = 14
stage = "第四阶段 · 带进经管课堂"
```

修改 `order` 调整章节顺序，编号不要重复。系列目录、首页入口、前后章链接会自动生成。每章二级标题自动进入“本章目录”。网页中的行内数学用 `$...$`，独立公式用单独成行的 `$$` 分隔；LaTeX 源代码则放在 `latex` 代码框中，不会被当成网页公式处理。

下载源文件位于 `assets/tutorial/examples/`，全部示例压缩包由构建程序自动生成。已编译的 PDF 预览位于 `assets/tutorial/previews/`；更新源文件后也应重新编译并替换对应 PDF。修改正文中的完整代码时，也要同步修改对应 `.tex` 文件。示例使用 XeLaTeX；第 07 章参考文献另需 Biber。所有经济、金融、会计数据均为明确标注的教学示例。

公式使用随站点提供的 KaTeX 0.18.7，无需访问外部 CDN；许可证位于 `assets/vendor/katex/LICENSE`。教程阅读样式和复制按钮分别在 `assets/tutorial.css`、`assets/tutorial.js`。

### 完整 PDF 与源码

教程目录的“把整本手记带走”提供完整 PDF、单文件 LaTeX 源码和源码 ZIP；各章页尾也可下载整本。作者 **[Ziyu Peng](https://github.com/pzy54154631-hub)** 与 **[刘毅涵](https://pzy54154631-hub.github.io/liuyihan/)** 的姓名分别链接到 Ziyu Peng 的 GitHub 主页和刘毅涵的个人主页。下载版按姓名及学校分行署名，并补充 Ziyu Peng 的学院、专业、地址和邮箱。

- `assets/tutorial/latex-tutorial-complete.pdf`：15 章完整书稿。
- `assets/tutorial/latex-tutorial-complete.tex`：可直接使用 XeLaTeX 编译的单文件源码。
- `assets/tutorial/SOURCE-README.md`：源码包使用说明。
- `tools/generate_tutorial_book.py`：从网页 Markdown 重新生成书稿的维护工具。

完整源码 ZIP 由 `build.py` 自动打包，包含 `main.tex`、17 份独立示例、15 章 Markdown、重新生成脚本和许可说明。修改网页版章节后，若需要同步整本 PDF，请重新生成并编译书稿，再替换上述 `.tex` 和 `.pdf`；网站日常构建不会自动运行 TeX。

```sh
python -m pip install pypandoc_binary
python tools/generate_tutorial_book.py --posts content/posts --output work/book/main.tex
latexmk -xelatex -outdir=work/book/build work/book/main.tex
cp work/book/main.tex assets/tutorial/latex-tutorial-complete.tex
cp work/book/build/main.pdf assets/tutorial/latex-tutorial-complete.pdf
python build.py
python check_site.py
```

### 教程许可

本教程的原创正文、PDF、LaTeX 源码与原创示例采用 **MIT 许可**，允许自由编辑、复制、再发布和商用。分发全部或实质性部分时，请保留版权和完整许可声明。完整条款见 [LICENSE.txt](assets/tutorial/LICENSE.txt)，范围见 [NOTICE.md](assets/tutorial/NOTICE.md)。第三方宏包、字体、KaTeX 与引用资料保留原有许可；本声明不自动覆盖个人主页其他内容。

## 本地预览

需要 Python 3.11 或更新版本。

```sh
pip install -r requirements.txt
python build.py
python check_site.py
python -m http.server 8767 --directory dist
```

打开 `http://localhost:8767/liuyihan/`。

`check_site.py` 还需要 Node.js，用于检查全部网页公式能否渲染，同时检查站内链接、目录锚点和示例压缩包。GitHub 部署流程会自动执行这些检查。

## 插画

首页小兔读书插画为本项目生成的原创装饰素材，存放于 `assets/reading-bunny.webp`。

视觉方向参考可爱手账博客的粉蓝配色、纸张层次和贴纸细节，页面代码独立编写。

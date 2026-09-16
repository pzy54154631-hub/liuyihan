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

编辑 `content/profile.json`。当前公开姓名、学校专业、经历与邮箱，不公开电话号码，也不提供含电话的简历下载。

样式在 `assets/site.css`；页面生成逻辑在 `build.py`，通用页面结构在 `templates/layout.html`。首页文案与文章均可随时修改。

## LaTeX 学习系列

目录位于 `/liuyihan/blog/latex/`。14 章按 4 个阶段排列，覆盖入门、公式图表、引用与展示、经管应用和 AI 辅助写作。署名顺序为 Ziyu.Peng、刘毅涵；各篇实际发布日期为 2026-09-16，假期安排是建议学习路线。

章节正文在 `content/posts/latex-*.md`，可以直接在 GitHub 编辑。除了普通文章字段，系列文章还包含：

```toml
authors = ["Ziyu.Peng", "刘毅涵"]
series = "latex"
order = 14
stage = "第四阶段 · 带进经管课堂"
```

修改 `order` 调整章节顺序，编号不要重复。系列目录、首页入口、前后章链接会自动生成。每章二级标题自动进入“本章目录”。网页中的行内数学用 `$...$`，独立公式用单独成行的 `$$` 分隔；LaTeX 源代码则放在 `latex` 代码框中，不会被当成网页公式处理。

下载源文件位于 `assets/tutorial/examples/`，全部示例压缩包由构建程序自动生成。已编译的 PDF 预览位于 `assets/tutorial/previews/`；更新源文件后也应重新编译并替换对应 PDF。修改正文中的完整代码时，也要同步修改对应 `.tex` 文件。示例使用 XeLaTeX；第 07 章参考文献另需 Biber。所有经济、金融、会计数据均为明确标注的教学示例。

公式使用随站点提供的 KaTeX 0.18.7，无需访问外部 CDN；许可证位于 `assets/vendor/katex/LICENSE`。教程阅读样式和复制按钮分别在 `assets/tutorial.css`、`assets/tutorial.js`。

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

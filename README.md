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

## 本地预览

需要 Python 3.11 或更新版本。

```sh
pip install -r requirements.txt
python build.py
python -m http.server 8767 --directory dist
```

打开 `http://localhost:8767/liuyihan/`。

## 插画

首页小兔读书插画为本项目生成的原创装饰素材，存放于 `assets/reading-bunny.webp`。

视觉方向参考可爱手账博客的粉蓝配色、纸张层次和贴纸细节，页面代码独立编写。

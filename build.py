#!/usr/bin/env python3
"""Build a small static homepage and Markdown blog for GitHub Pages."""
from pathlib import Path
from datetime import date, datetime, timezone
from html import escape
from string import Template
from email.utils import format_datetime
import argparse
import json
import hashlib
import re
import shutil
import tomllib
import xml.etree.ElementTree as ET
import zipfile
from markdown_it import MarkdownIt
from mdit_py_plugins.dollarmath import dollarmath_plugin

ROOT = Path(__file__).parent.resolve()
BASE = '/liuyihan'
ORIGIN = 'https://pzy54154631-hub.github.io'
PUBLIC = ROOT / 'dist' / BASE.strip('/')
profile = json.loads((ROOT / 'content/profile.json').read_text())
layout = Template((ROOT / 'templates/layout.html').read_text())
STYLE_VERSION = hashlib.sha256((ROOT / 'assets/site.css').read_bytes() + (ROOT / 'assets/tutorial.css').read_bytes()).hexdigest()[:12]
md = MarkdownIt('commonmark', {'html': False}).enable('table').use(dollarmath_plugin, allow_labels=False)
SERIES_URL = f'{BASE}/blog/latex/'
SERIES_TITLE = '把想法写成漂亮的一页'
AUTHOR_GITHUB = 'https://github.com/pzy54154631-hub?tab=repositories'
TUTORIAL_ASSETS = f'{BASE}/assets/tutorial'

def author_name(name):
    if name in ('Ziyu.Peng', 'Ziyu Peng'):
        return f'<a class="author-link" href="{AUTHOR_GITHUB}" rel="author">Ziyu Peng ↗</a>'
    return e(name)

def tutorial_license():
    return f'''<aside class="tutorial-license"><span class="license-badge">MIT · 开源教程</span><p>本教程的正文、PDF、LaTeX 源码与原创示例采用 <a href="https://opensource.org/license/mit" rel="license">MIT 协议</a>。你可以自由编辑、复制、再发布及商用；再发布时请保留版权与许可声明。</p><p class="license-credit">© 2026 {author_name('Ziyu Peng')} · 刘毅涵 <span aria-hidden="true">/</span> <a href="{TUTORIAL_ASSETS}/LICENSE.txt">阅读完整许可</a> · <a href="{TUTORIAL_ASSETS}/NOTICE.md">许可适用范围</a></p></aside>'''

def full_downloads(chapters):
    example_count = len(list((ROOT / 'assets/tutorial/examples').glob('*.tex')))
    return f'''<section class="full-downloads" id="downloads" aria-labelledby="download-title"><div class="download-heading"><span class="eyebrow">TAKE THE WHOLE NOTEBOOK</span><h2 id="download-title">把整本手记带走</h2><p>{len(chapters)} 章完整正文、公式、代码与练习，离线阅读，也可以继续改写。</p></div><div class="download-grid"><a class="download-card" href="{TUTORIAL_ASSETS}/latex-tutorial-complete.pdf" download><span class="download-kind">PDF</span><div><h3>下载完整教程</h3><p>含封面、可点击目录与全部章节。</p></div><span aria-hidden="true">↓</span></a><a class="download-card" href="{TUTORIAL_ASSETS}/latex-tutorial-source.zip" download><span class="download-kind">TEX</span><div><h3>下载完整 LaTeX 源码</h3><p>完整主文件、{example_count} 份示例、编译说明与许可。</p></div><span aria-hidden="true">↓</span></a></div><div class="download-secondary"><a href="{TUTORIAL_ASSETS}/latex-tutorial-complete.tex" download>只下载整本 .tex 文件 ↓</a><a href="{TUTORIAL_ASSETS}/latex-examples.zip" download>只下载配套示例 ↓</a></div>{tutorial_license()}</section>'''

def compact_downloads():
    return f'''<aside class="complete-book-links"><span>想离线阅读整套教程？</span><a href="{TUTORIAL_ASSETS}/latex-tutorial-complete.pdf" download>完整 PDF ↓</a><a href="{TUTORIAL_ASSETS}/latex-tutorial-source.zip" download>完整 LaTeX 源码 ↓</a></aside>'''

def render_post(content):
    tokens = md.parse(content.strip())
    toc = []
    for i, token in enumerate(tokens):
        if token.type == 'heading_open':
            anchor = f'section-{len(toc) + 1}'
            token.attrSet('id', anchor)
            toc.append((anchor, tokens[i+1].content, token.tag))
    rendered = md.renderer.render(tokens, md.options, {})
    rendered = rendered.replace('<table>', '<div class="table-scroll" tabindex="0" role="region" aria-label="可横向滚动的表格"><table>')
    rendered = rendered.replace('</table>', '</table></div>')
    return rendered, toc

def example_links(p):
    stem = f'latex-{p["order"]:02}'
    return f'''<aside class="example-downloads"><span>边读边动手</span><a href="{BASE}/assets/tutorial/examples/{stem}.tex" download>下载本章源文件 ↓</a><a href="{BASE}/assets/tutorial/previews/{stem}.pdf">查看编译效果 PDF ↗</a></aside>'''

def e(value):
    return escape(str(value), quote=True)

def date_label(value):
    parts = value.split('-')
    if len(parts) == 2:
        return f'{parts[0]} 年 {int(parts[1])} 月'
    return value.replace('-', '.')

def post_dates(p):
    published = f'<time datetime="{p["date"]}">{"首发于" if p.get("updated") else "发布于"} {date_label(p["date"])}</time>'
    if p.get('updated'):
        published += f'<time datetime="{p["updated"]}">合集整理 {date_label(p["updated"])}</time>'
    elif p.get('series') == 'latex':
        published = f'<time datetime="{p["date"]}">合集收录 {date_label(p["date"])}</time>'
    return published

def post_data():
    result = []
    for path in (ROOT / 'content/posts').glob('*.md'):
        raw = path.read_text()
        if not raw.startswith('+++\n'):
            raise ValueError(f'{path.name}: missing TOML front matter')
        metadata, content = raw[4:].split('\n+++', 1)
        p = tomllib.loads(metadata)
        if p.get('draft', False):
            continue
        for field in ('title', 'date', 'tag', 'summary'):
            if not isinstance(p.get(field), str) or not p[field].strip():
                raise ValueError(f'{path.name}: invalid {field}')
        if re.fullmatch(r'\d{4}-\d{2}', p['date']):
            date.fromisoformat(p['date']+'-01')
        else:
            date.fromisoformat(p['date'])
        if p.get('updated'): date.fromisoformat(p['updated'])
        if not re.fullmatch(r'[a-z0-9-]+', path.stem):
            raise ValueError('Post filenames must use lowercase English letters, digits and hyphens')
        p['slug'] = path.stem
        p['url'] = f"{BASE}/blog/{p['slug']}/"
        p['html'], p['toc'] = render_post(content)
        p['authors'] = p.get('authors', [profile['name']])
        if not isinstance(p['authors'], list) or not all(isinstance(a, str) and a.strip() for a in p['authors']):
            raise ValueError(f'{path.name}: invalid authors')
        if p.get('series') and (p['series'] != 'latex' or not isinstance(p.get('order'), int) or p['order'] < 1):
            raise ValueError(f'{path.name}: invalid series/order')
        p['minutes'] = max(1, round(len(content) / 450))
        result.append(p)
    return sorted(result, key=lambda p: (p['date'], p['slug']), reverse=True)

def page(title, description, body, path='', active='', og_type='website', tutorial=False):
    canonical = f'{ORIGIN}{BASE}/{path}'
    return layout.substitute(title=e(title), description=e(description), canonical=e(canonical),
        base=BASE, style_version=STYLE_VERSION, email=e(profile['email']), body=body, year=date.today().year, og_type=og_type,
        extra_head=(f'<link rel="stylesheet" href="{BASE}/assets/vendor/katex/katex.min.css"><script defer src="{BASE}/assets/vendor/katex/katex.min.js"></script><script defer src="{BASE}/assets/tutorial.js"></script>' if tutorial else ''),
        home_current='aria-current="page"' if active == 'home' else '',
        blog_current='aria-current="page"' if active == 'blog' else '')

def cards(posts):
    return ''.join(f'''<a class="post-card" href="{p['url']}"><div class="post-label"><span class="post-tag">{e(p['tag'])}</span><time class="post-date" datetime="{p['date']}">{date_label(p['date'])}</time></div><div><h3>{e(p['title'])}</h3><p>{e(p['summary'])}</p></div><span class="post-arrow" aria-hidden="true">↗</span></a>''' for p in posts)

def series_card(posts):
    count = len([p for p in posts if p.get('series') == 'latex'])
    if not count: return ''
    return f'''<a class="series-feature" href="{SERIES_URL}"><div class="series-art" aria-hidden="true"><span class="paper-formula">Aa<br><i>∑ xᵢ</i></span><span class="paper-star">✦</span></div><div><span class="eyebrow">LATEX · A LEARNING NOTEBOOK</span><h2>{SERIES_TITLE}</h2><p>从第一份中文文档，到经济模型、金融现金流和会计报表。从 7 月的第一篇，逐步补充成 {count} 章学习手记，9 月中旬整理成册。</p><span class="series-caption">{count} 章 · 完整 PDF · 可编辑 LaTeX 源码 <span aria-hidden="true">↗</span></span></div></a>'''

def series_index(chapters):
    groups = {}
    for p in chapters: groups.setdefault(p['stage'], []).append(p)
    contents = ''
    for stage, entries in groups.items():
        rows = ''.join(f'''<a class="chapter-card" href="{p['url']}"><span class="chapter-no">{p['order']:02}</span><div><h3>{e(p['title'])}</h3><p>{e(p['summary'])}</p><span class="small-note">{(date_label(p["date"])+" · " if len(p["date"]) == 7 else "")}约 {p['minutes']} 分钟阅读 · 配套练习</span></div><span aria-hidden="true">↗</span></a>''' for p in entries)
        contents += f'<section class="chapter-group"><h2>{e(stage)}</h2>{rows}</section>'
    return f'''<main class="wrap" id="main"><div class="series-wrap"><nav class="breadcrumb"><a href="{BASE}/blog/">所有手记</a> / LaTeX 学习系列</nav><header class="series-header"><span class="hello">一页一页，把想法写清楚。</span><h1>{SERIES_TITLE}</h1><p class="series-subtitle">LaTeX 入门与经管专业排版手记</p><div class="article-meta"><span>{author_name("Ziyu Peng")} · 刘毅涵</span><span>{len(chapters)} 章 · 从入门到完整作品</span></div><p class="series-intro">写公式、整理数据、解释一个经济模型，最后把它们放进一份读起来舒服的报告。这套手记从原有的 LaTeX 教程展开，保留基础与进阶内容，也加入经济学、金融和会计中的常用表达，以及用 AI 辅助写作、修改和排错的方法。新增的 Overleaf 实操章，把建立项目、在线编译与导出串成一条完整流程。</p><div class="series-actions"><a class="button button-primary" href="{chapters[0]['url']}">从第一章开始 ↗</a><a class="button button-secondary" href="#downloads">整本下载与开源许可 ↓</a></div></header>{full_downloads(chapters)}<aside class="reading-plan"><strong>从七月的一页，到九月的一本</strong><p>首篇记于 2026 年 7 月，随后围绕公式、图表、经管课程与写作工具逐章补充。2026 年 9 月 16 日，将这些手记统一整理成合集，并提供完整 PDF 与源码。</p><span class="small-note">从第一章开始建立文档骨架；需要先熟悉在线编译时，可以先看<a href="{BASE}/blog/latex-15-overleaf-workflow/">第 15 章 Overleaf 实操</a>。</span></aside><div class="series-contents">{contents}</div><aside class="reading-plan"><strong>怎么使用这些手记</strong><p>先看网页中的效果与解释，再下载本章完整源文件，用 XeLaTeX 编译。代码框提供复制按钮；片段需按章节说明放入导言区或正文。第 07 章的参考文献还需要 Biber。经济、金融与会计章节均使用明确标注的教学示例。</p></aside></div></main>'''

def chapter_navigation(p, chapters):
    index = chapters.index(p)
    links = []
    if index:
        prev = chapters[index-1]
        links.append(f'<a href="{prev["url"]}"><span>← 上一章</span><strong>{e(prev["title"])}</strong></a>')
    else:
        links.append(f'<a href="{SERIES_URL}"><span>← 学习路线</span><strong>回到系列目录</strong></a>')
    if index+1 < len(chapters):
        nxt = chapters[index+1]
        links.append(f'<a href="{nxt["url"]}"><span>下一章 →</span><strong>{e(nxt["title"])}</strong></a>')
    else:
        links.append(f'<a href="{SERIES_URL}"><span>继续练习 ↗</span><strong>回到系列目录</strong></a>')
    return '<nav class="chapter-navigation" aria-label="章节导航">'+''.join(links)+'</nav>'

def project_cards():
    cards = []
    for project in profile.get('projects', []):
        paragraphs = ''.join(f'<p>{e(text)}</p>' for text in project['paragraphs'])
        cards.append(f'''<article class="about-project"><div class="project-heading"><div><span class="project-role">{e(project['role'])}</span><h3>{e(project['title'])}</h3></div><span class="experience-period">{e(project['period'])}</span></div>{paragraphs}<a class="text-link project-link" href="{e(project['url'])}">{e(project['link_label'])}</a></article>''')
    return ''.join(cards)

def home(posts):
    education = ''.join(f'''<div class="education-item"><strong>{e(x['name'])}</strong><p>{e(x['detail'])}</p><time>{e(x['period'])}</time></div>''' for x in profile['education'])
    experiences = ''.join(f'''<div class="experience-row"><div class="experience-top"><h4>{e(x['title'])}</h4><span class="experience-period">{e(x['period'])}</span></div><p>{e(x['text'])}</p></div>''' for x in profile['experiences'])
    skills = ''.join(f'''<div><div class="skill-name">{e(x['label'])}</div><div class="skill-tools">{e(x['tools'])}</div><p class="skill-text">{e(x['text'])}</p></div>''' for x in profile['skills'])
    return f'''<main id="main" class="wrap">
      <section class="hero" aria-labelledby="intro-title"><div><span class="hello">Hello, welcome to my little corner.</span><h1 id="intro-title">你好，我是<br><span>刘毅涵</span>。</h1><p class="school">暨南大学 · 经济学院金融专业</p><p class="hero-description">{e(profile['intro'])}</p><div class="hero-actions"><a class="button button-primary" href="{BASE}/blog/">读我的手记 <span aria-hidden="true">↗</span></a><a class="button button-secondary" href="#about">认识一下</a></div></div><div class="hero-art"><img src="{BASE}/assets/reading-bunny.webp" alt="一只小兔坐在笔记本旁读书的手绘插画" width="800" height="800" fetchpriority="high"><span class="art-caption">a little space to learn & grow</span></div></section>
      <section class="section" aria-labelledby="writing-title"><div class="section-heading"><div><span class="section-index">Notes & little discoveries</span><h2 id="writing-title">最近的手记</h2></div><a class="text-link" href="{BASE}/blog/">全部手记 ↗</a></div>{series_card(posts)}{cards([p for p in posts if not p.get('series')][:3])}</section>
      <section class="section" id="about" aria-labelledby="about-title"><div class="section-heading"><div><span class="section-index">A little about me</span><h2 id="about-title">关于我</h2></div><span class="small-note">学习，也参与身边的小事。</span></div><div class="about-grid"><div class="note-card tint-blue"><span class="tape" aria-hidden="true"></span><h3>我的学习足迹</h3>{education}</div><div class="note-card"><h3>课堂以外</h3>{experiences}</div></div>{project_cards()}<div class="skills-wrap"><div class="skills-heading"><h3>现在的技能工具箱</h3><span class="small-note">继续学习，也慢慢实践。</span></div><div class="skills-grid">{skills}</div></div></section>
      <section class="contact-section" aria-labelledby="contact-title"><div class="contact-paper"><div><h2 id="contact-title">有想交流的事情吗？</h2><p>关于学习、志愿服务，或一个有意思的问题，都可以写信给我。</p></div><a class="email-link" href="mailto:{e(profile['email'])}">{e(profile['email'])} ↗</a></div></section>
    </main>'''

def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')

def build():
    posts = post_data()
    chapters = sorted([p for p in posts if p.get('series') == 'latex'], key=lambda p: p['order'])
    if len({p['order'] for p in chapters}) != len(chapters):
        raise ValueError('Duplicate chapter number')
    if PUBLIC.exists(): shutil.rmtree(PUBLIC)
    PUBLIC.mkdir(parents=True)
    shutil.copytree(ROOT / 'assets', PUBLIC / 'assets')
    if chapters:
        with zipfile.ZipFile(PUBLIC / 'assets/tutorial/latex-examples.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
            for example in sorted((ROOT / 'assets/tutorial/examples').glob('*')):
                if example.is_file(): archive.write(example, example.name)
            archive.write(ROOT / 'assets/tutorial/LICENSE.txt', 'LICENSE.txt')
            archive.write(ROOT / 'assets/tutorial/NOTICE.md', 'NOTICE.md')
            archive.writestr('README.txt', 'LaTeX 入门与经管专业排版手记\n作者：Ziyu Peng、刘毅涵\nZiyu Peng GitHub：https://github.com/pzy54154631-hub?tab=repositories\n\n网页目录：https://pzy54154631-hub.github.io/liuyihan/blog/latex/\n默认使用 XeLaTeX 编译。第07章参考文献需 Biber，详见各文件注释和网页教程。\n所有专业数据均为教学示例。\n本教程源码与原创示例采用 MIT 许可，可自由编辑、复制、再发布及商用。再发布时保留版权与许可声明；详见 LICENSE.txt 与 NOTICE.md。\n')
        with zipfile.ZipFile(PUBLIC / 'assets/tutorial/latex-tutorial-source.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
            source = ROOT / 'assets/tutorial'
            archive.write(source / 'latex-tutorial-complete.tex', 'main.tex')
            archive.write(source / 'LICENSE.txt', 'LICENSE.txt')
            archive.write(source / 'NOTICE.md', 'NOTICE.md')
            archive.write(source / 'SOURCE-README.md', 'README.md')
            archive.write(ROOT / 'tools/generate_tutorial_book.py', 'generate_book.py')
            for example in sorted((source / 'examples').glob('*.tex')):
                archive.write(example, 'examples/'+example.name)
            for chapter in sorted((ROOT / 'content/posts').glob('latex-*.md')):
                archive.write(chapter, 'chapters-md/'+chapter.name)
    write(PUBLIC / '.nojekyll', '')
    write(PUBLIC / 'index.html', page('刘毅涵 · 毅涵的小站', profile['intro'], home(posts), active='home'))
    blog = f'''<main class="wrap" id="main"><header class="blog-header"><span class="eyebrow">YIHAN'S NOTEBOOK</span><h1>手记与小发现</h1><p>记录学习中的问题、生活里的观察，还有把事情慢慢弄明白的过程。</p></header>{series_card(posts)}<div class="blog-list">{cards([p for p in posts if not p.get('series')])}</div></main>'''
    write(PUBLIC / 'blog/index.html', page('手记 · 毅涵的小站', '刘毅涵的学习笔记、志愿服务思考与工具心得。', blog, 'blog/', 'blog'))
    if chapters:
        write(PUBLIC / 'blog/latex/index.html', page('LaTeX 学习手记 · '+SERIES_TITLE, '从中文文档、公式图表到经济学、金融和会计排版的完整学习系列。', series_index(chapters), 'blog/latex/', 'blog'))
    for p in posts:
        tutorial = p.get('series') == 'latex'
        authors = ' · '.join(e(a) for a in p['authors'])
        if tutorial: authors = ' · '.join(author_name(name) for name in p['authors'])
        series_link = f'<a href="{SERIES_URL}">LaTeX 学习系列</a> / 第 {p["order"]:02} 章' if tutorial else e(p['title'])
        toc = ('<details class="article-toc"><summary>本章目录</summary><ol>'+''.join(f'<li><a href="#{a}">{e(t)}</a></li>' for a,t,level in p['toc'] if level == 'h2')+'</ol></details>'+example_links(p)) if tutorial else ''
        chapter_label = f'<span class="chapter-kicker">CHAPTER {p["order"]:02} / {len(chapters):02}</span>' if tutorial else ''
        body = f'''<main id="main" class="wrap"><article class="article-wrap"><nav class="breadcrumb" aria-label="面包屑"><a href="{BASE}/blog/">所有手记</a> / {series_link}</nav><header class="article-header">{chapter_label}<span class="post-tag">{e(p['tag'])}</span><h1>{e(p['title'])}</h1><p class="article-summary">{e(p['summary'])}</p><div class="article-meta"><span>{authors}</span>{post_dates(p)}<span>约 {p['minutes']} 分钟阅读</span></div></header>{toc}<div class="article-body">{p['html']}</div>{compact_downloads()+tutorial_license()+chapter_navigation(p, chapters) if tutorial else ''}<footer class="article-end"><a class="text-link" href="{SERIES_URL if tutorial else BASE+'/blog/'}">← {'回到系列目录' if tutorial else '回到所有手记'}</a><a class="text-link" href="mailto:{e(profile['email'])}">读后想聊聊？写信给我 ↗</a></footer></article></main>'''
        write(PUBLIC / f"blog/{p['slug']}/index.html", page(p['title']+' · 毅涵的小站', p['summary'], body, f"blog/{p['slug']}/", 'blog', 'article', tutorial=tutorial))
    not_found = f'<main class="wrap not-found" id="main"><p class="eyebrow">迷路了也没关系</p><h1>404</h1><p>这一页暂时找不到，回小站首页看看吧。</p><a class="button button-primary" href="{BASE}/">回到首页</a></main>'
    write(PUBLIC / '404.html', page('页面未找到 · 毅涵的小站', '回到毅涵的小站首页。', not_found, '404.html'))
    feed = ET.Element('rss', {'version':'2.0'})
    channel = ET.SubElement(feed, 'channel')
    for tag, val in [('title',profile['site_name']),('link',ORIGIN+BASE+'/'),('description','刘毅涵的学习与生活手记'),('language','zh-cn')]: ET.SubElement(channel,tag).text=val
    for p in posts:
        item=ET.SubElement(channel,'item')
        fields = [('title',p['title']),('link',ORIGIN+p['url']),('guid',ORIGIN+p['url']),('description',p['summary'])]
        # RSS pubDate requires a complete day; a month-only date must not invent one.
        if len(p['date']) == 10:
            fields.append(('pubDate', format_datetime(datetime.fromisoformat(p['date']).replace(tzinfo=timezone.utc))))
        for tag,val in fields: ET.SubElement(item,tag).text=val
    write(PUBLIC / 'feed.xml', ET.tostring(feed, encoding='unicode', xml_declaration=True))
    sitemap = ET.Element('urlset', {'xmlns':'http://www.sitemaps.org/schemas/sitemap/0.9'})
    for url in [BASE+'/',BASE+'/blog/']+([SERIES_URL] if chapters else [])+[p['url'] for p in posts]: ET.SubElement(ET.SubElement(sitemap,'url'),'loc').text=ORIGIN+url
    write(PUBLIC / 'sitemap.xml', ET.tostring(sitemap, encoding='unicode', xml_declaration=True))
    print(f'Built {len(posts)} post(s) in {PUBLIC}')

if __name__ == '__main__':
    build()

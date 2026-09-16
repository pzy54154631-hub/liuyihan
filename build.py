#!/usr/bin/env python3
"""Build a small static homepage and Markdown blog for GitHub Pages."""
from pathlib import Path
from datetime import date, datetime, timezone
from html import escape
from string import Template
from email.utils import format_datetime
import argparse
import json
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
md = MarkdownIt('commonmark', {'html': False}).enable('table').use(dollarmath_plugin, allow_labels=False)
SERIES_URL = f'{BASE}/blog/latex/'
SERIES_TITLE = '把想法写成漂亮的一页'

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
        date.fromisoformat(p['date'])
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
        base=BASE, email=e(profile['email']), body=body, year=date.today().year, og_type=og_type,
        extra_head=(f'<link rel="stylesheet" href="{BASE}/assets/vendor/katex/katex.min.css"><script defer src="{BASE}/assets/vendor/katex/katex.min.js"></script><script defer src="{BASE}/assets/tutorial.js"></script>' if tutorial else ''),
        home_current='aria-current="page"' if active == 'home' else '',
        blog_current='aria-current="page"' if active == 'blog' else '')

def cards(posts):
    return ''.join(f'''<a class="post-card" href="{p['url']}"><div class="post-label"><span class="post-tag">{e(p['tag'])}</span><time class="post-date" datetime="{p['date']}">{p['date'].replace('-', '.')}</time></div><div><h3>{e(p['title'])}</h3><p>{e(p['summary'])}</p></div><span class="post-arrow" aria-hidden="true">↗</span></a>''' for p in posts)

def series_card(posts):
    count = len([p for p in posts if p.get('series') == 'latex'])
    if not count: return ''
    return f'''<a class="series-feature" href="{SERIES_URL}"><div class="series-art" aria-hidden="true"><span class="paper-formula">Aa<br><i>∑ xᵢ</i></span><span class="paper-star">✦</span></div><div><span class="eyebrow">LATEX · A LEARNING NOTEBOOK</span><h2>{SERIES_TITLE}</h2><p>从第一份中文文档，到经济模型、金融现金流和会计报表。把一个假期的学习，安排成 {count} 个小章节。</p><span class="series-caption">{count} 章 · 4 个学习阶段 · 附完整示例 <span aria-hidden="true">↗</span></span></div></a>'''

def series_index(chapters):
    groups = {}
    for p in chapters: groups.setdefault(p['stage'], []).append(p)
    contents = ''
    for stage, entries in groups.items():
        rows = ''.join(f'''<a class="chapter-card" href="{p['url']}"><span class="chapter-no">{p['order']:02}</span><div><h3>{e(p['title'])}</h3><p>{e(p['summary'])}</p><span class="small-note">约 {p['minutes']} 分钟阅读 · 配套练习</span></div><span aria-hidden="true">↗</span></a>''' for p in entries)
        contents += f'<section class="chapter-group"><h2>{e(stage)}</h2>{rows}</section>'
    return f'''<main class="wrap" id="main"><div class="series-wrap"><nav class="breadcrumb"><a href="{BASE}/blog/">所有手记</a> / LaTeX 学习系列</nav><header class="series-header"><span class="hello">一页一页，把想法写清楚。</span><h1>{SERIES_TITLE}</h1><p class="series-subtitle">LaTeX 入门与经管专业排版手记</p><div class="article-meta"><span>第一作者 Ziyu.Peng · 第二作者 刘毅涵</span><span>{len(chapters)} 章 · 从入门到完整作品</span></div><p class="series-intro">写公式、整理数据、解释一个经济模型，最后把它们放进一份读起来舒服的报告。这套手记从原有的 LaTeX 教程展开，保留基础与进阶内容，也加入经济学、金融和会计中的常用表达，以及用 AI 辅助写作、修改和排错的方法。</p><div class="series-actions"><a class="button button-primary" href="{chapters[0]['url']}">从第一章开始 ↗</a><a class="button button-secondary" href="{BASE}/assets/tutorial/latex-examples.zip" download>下载全部示例 ↓</a></div></header><aside class="reading-plan"><strong>给一个假期的学习安排</strong><p>可以每周完成一个阶段：先写出文档，再练公式图表，接着整理引用与展示，最后做一份经管课程报告。每天改一个小例子，隔几天把旧例子重新写一遍；节奏也可以按自己的课程调整。</p><span class="small-note">这是建议学习路线。全系列于 2026 年 9 月 16 日整理发布。</span></aside><div class="series-contents">{contents}</div><aside class="reading-plan"><strong>怎么使用这些手记</strong><p>先看网页中的效果与解释，再下载本章完整源文件，用 XeLaTeX 编译。代码框提供复制按钮；片段需按章节说明放入导言区或正文。第 07 章的参考文献还需要 Biber。经济、金融与会计章节均使用明确标注的教学示例。</p></aside></div></main>'''

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

def home(posts):
    education = ''.join(f'''<div class="education-item"><strong>{e(x['name'])}</strong><p>{e(x['detail'])}</p><time>{e(x['period'])}</time></div>''' for x in profile['education'])
    experiences = ''.join(f'''<div class="experience-row"><div class="experience-top"><h4>{e(x['title'])}</h4><span class="experience-period">{e(x['period'])}</span></div><p>{e(x['text'])}</p></div>''' for x in profile['experiences'])
    skills = ''.join(f'''<div><div class="skill-name">{e(x['label'])}</div><div class="skill-tools">{e(x['tools'])}</div><p class="skill-text">{e(x['text'])}</p></div>''' for x in profile['skills'])
    return f'''<main id="main" class="wrap">
      <section class="hero" aria-labelledby="intro-title"><div><span class="hello">Hello, welcome to my little corner.</span><h1 id="intro-title">你好，我是<br><span>刘毅涵</span>。</h1><p class="school">暨南大学 · 经济学院金融专业</p><p class="hero-description">{e(profile['intro'])}</p><div class="hero-actions"><a class="button button-primary" href="{BASE}/blog/">读我的手记 <span aria-hidden="true">↗</span></a><a class="button button-secondary" href="#about">认识一下</a></div></div><div class="hero-art"><img src="{BASE}/assets/reading-bunny.webp" alt="一只小兔坐在笔记本旁读书的手绘插画" width="800" height="800" fetchpriority="high"><span class="art-caption">a little space to learn & grow</span></div></section>
      <section class="section" aria-labelledby="writing-title"><div class="section-heading"><div><span class="section-index">Notes & little discoveries</span><h2 id="writing-title">最近的手记</h2></div><a class="text-link" href="{BASE}/blog/">全部手记 ↗</a></div>{series_card(posts)}{cards([p for p in posts if not p.get('series')][:3])}</section>
      <section class="section" id="about" aria-labelledby="about-title"><div class="section-heading"><div><span class="section-index">A little about me</span><h2 id="about-title">关于我</h2></div><span class="small-note">学习，也参与身边的小事。</span></div><div class="about-grid"><div class="note-card tint-blue"><span class="tape" aria-hidden="true"></span><h3>我的学习足迹</h3>{education}</div><div class="note-card"><h3>课堂以外</h3>{experiences}</div></div><div class="skills-wrap"><div class="skills-heading"><h3>现在的技能工具箱</h3><span class="small-note">继续学习，也慢慢实践。</span></div><div class="skills-grid">{skills}</div></div></section>
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
            archive.writestr('README.txt', 'LaTeX 入门与经管专业排版手记\n第一作者：Ziyu.Peng\n第二作者：刘毅涵\n\n网页目录：https://pzy54154631-hub.github.io/liuyihan/blog/latex/\n默认使用 XeLaTeX 编译。第07章参考文献需 Biber，详见各文件注释和网页教程。\n所有专业数据均为教学示例。\n')
    write(PUBLIC / '.nojekyll', '')
    write(PUBLIC / 'index.html', page('刘毅涵 · 毅涵的小站', profile['intro'], home(posts), active='home'))
    blog = f'''<main class="wrap" id="main"><header class="blog-header"><span class="eyebrow">YIHAN'S NOTEBOOK</span><h1>手记与小发现</h1><p>记录学习中的问题、生活里的观察，还有把事情慢慢弄明白的过程。</p></header>{series_card(posts)}<div class="blog-list">{cards([p for p in posts if not p.get('series')])}</div></main>'''
    write(PUBLIC / 'blog/index.html', page('手记 · 毅涵的小站', '刘毅涵的学习笔记、志愿服务思考与工具心得。', blog, 'blog/', 'blog'))
    if chapters:
        write(PUBLIC / 'blog/latex/index.html', page('LaTeX 学习手记 · '+SERIES_TITLE, '从中文文档、公式图表到经济学、金融和会计排版的完整学习系列。', series_index(chapters), 'blog/latex/', 'blog'))
    for p in posts:
        tutorial = p.get('series') == 'latex'
        authors = ' · '.join(e(a) for a in p['authors'])
        if tutorial: authors = '第一作者 '+e(p['authors'][0])+' · 第二作者 '+e(p['authors'][1])
        series_link = f'<a href="{SERIES_URL}">LaTeX 学习系列</a> / 第 {p["order"]:02} 章' if tutorial else e(p['title'])
        toc = ('<details class="article-toc"><summary>本章目录</summary><ol>'+''.join(f'<li><a href="#{a}">{e(t)}</a></li>' for a,t,level in p['toc'] if level == 'h2')+'</ol></details>'+example_links(p)) if tutorial else ''
        chapter_label = f'<span class="chapter-kicker">CHAPTER {p["order"]:02} / {len(chapters):02}</span>' if tutorial else ''
        body = f'''<main id="main" class="wrap"><article class="article-wrap"><nav class="breadcrumb" aria-label="面包屑"><a href="{BASE}/blog/">所有手记</a> / {series_link}</nav><header class="article-header">{chapter_label}<span class="post-tag">{e(p['tag'])}</span><h1>{e(p['title'])}</h1><p class="article-summary">{e(p['summary'])}</p><div class="article-meta"><span>{authors}</span><time datetime="{p['date']}">发布于 {p['date'].replace('-', '.')}</time><span>约 {p['minutes']} 分钟阅读</span></div></header>{toc}<div class="article-body">{p['html']}</div>{chapter_navigation(p, chapters) if tutorial else ''}<footer class="article-end"><a class="text-link" href="{SERIES_URL if tutorial else BASE+'/blog/'}">← {'回到系列目录' if tutorial else '回到所有手记'}</a><a class="text-link" href="mailto:{e(profile['email'])}">读后想聊聊？写信给我 ↗</a></footer></article></main>'''
        write(PUBLIC / f"blog/{p['slug']}/index.html", page(p['title']+' · 毅涵的小站', p['summary'], body, f"blog/{p['slug']}/", 'blog', 'article', tutorial=tutorial))
    not_found = f'<main class="wrap not-found" id="main"><p class="eyebrow">迷路了也没关系</p><h1>404</h1><p>这一页暂时找不到，回小站首页看看吧。</p><a class="button button-primary" href="{BASE}/">回到首页</a></main>'
    write(PUBLIC / '404.html', page('页面未找到 · 毅涵的小站', '回到毅涵的小站首页。', not_found, '404.html'))
    feed = ET.Element('rss', {'version':'2.0'})
    channel = ET.SubElement(feed, 'channel')
    for tag, val in [('title',profile['site_name']),('link',ORIGIN+BASE+'/'),('description','刘毅涵的学习与生活手记'),('language','zh-cn')]: ET.SubElement(channel,tag).text=val
    for p in posts:
        item=ET.SubElement(channel,'item')
        for tag,val in [('title',p['title']),('link',ORIGIN+p['url']),('guid',ORIGIN+p['url']),('description',p['summary']),('pubDate',format_datetime(datetime.fromisoformat(p['date']).replace(tzinfo=timezone.utc)))]: ET.SubElement(item,tag).text=val
    write(PUBLIC / 'feed.xml', ET.tostring(feed, encoding='unicode', xml_declaration=True))
    sitemap = ET.Element('urlset', {'xmlns':'http://www.sitemaps.org/schemas/sitemap/0.9'})
    for url in [BASE+'/',BASE+'/blog/']+([SERIES_URL] if chapters else [])+[p['url'] for p in posts]: ET.SubElement(ET.SubElement(sitemap,'url'),'loc').text=ORIGIN+url
    write(PUBLIC / 'sitemap.xml', ET.tostring(sitemap, encoding='unicode', xml_declaration=True))
    print(f'Built {len(posts)} post(s) in {PUBLIC}')

if __name__ == '__main__':
    build()

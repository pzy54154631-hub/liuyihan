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
from markdown_it import MarkdownIt

ROOT = Path(__file__).parent.resolve()
BASE = '/liuyihan'
ORIGIN = 'https://pzy54154631-hub.github.io'
PUBLIC = ROOT / 'dist' / BASE.strip('/')
profile = json.loads((ROOT / 'content/profile.json').read_text())
layout = Template((ROOT / 'templates/layout.html').read_text())
md = MarkdownIt('commonmark', {'html': False})

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
        p['html'] = md.render(content.strip())
        p['minutes'] = max(1, round(len(content) / 450))
        result.append(p)
    return sorted(result, key=lambda p: (p['date'], p['slug']), reverse=True)

def page(title, description, body, path='', active='', og_type='website'):
    canonical = f'{ORIGIN}{BASE}/{path}'
    return layout.substitute(title=e(title), description=e(description), canonical=e(canonical),
        base=BASE, email=e(profile['email']), body=body, year=date.today().year, og_type=og_type,
        home_current='aria-current="page"' if active == 'home' else '',
        blog_current='aria-current="page"' if active == 'blog' else '')

def cards(posts):
    return ''.join(f'''<a class="post-card" href="{p['url']}"><div class="post-label"><span class="post-tag">{e(p['tag'])}</span><time class="post-date" datetime="{p['date']}">{p['date'].replace('-', '.')}</time></div><div><h3>{e(p['title'])}</h3><p>{e(p['summary'])}</p></div><span class="post-arrow" aria-hidden="true">↗</span></a>''' for p in posts)

def home(posts):
    education = ''.join(f'''<div class="education-item"><strong>{e(x['name'])}</strong><p>{e(x['detail'])}</p><time>{e(x['period'])}</time></div>''' for x in profile['education'])
    experiences = ''.join(f'''<div class="experience-row"><div class="experience-top"><h4>{e(x['title'])}</h4><span class="experience-period">{e(x['period'])}</span></div><p>{e(x['text'])}</p></div>''' for x in profile['experiences'])
    skills = ''.join(f'''<div><div class="skill-name">{e(x['label'])}</div><div class="skill-tools">{e(x['tools'])}</div><p class="skill-text">{e(x['text'])}</p></div>''' for x in profile['skills'])
    return f'''<main id="main" class="wrap">
      <section class="hero" aria-labelledby="intro-title"><div><span class="hello">Hello, welcome to my little corner.</span><h1 id="intro-title">你好，我是<br><span>刘毅涵</span>。</h1><p class="school">暨南大学 · 经济学院金融专业</p><p class="hero-description">{e(profile['intro'])}</p><div class="hero-actions"><a class="button button-primary" href="{BASE}/blog/">读我的手记 <span aria-hidden="true">↗</span></a><a class="button button-secondary" href="#about">认识一下</a></div></div><div class="hero-art"><img src="{BASE}/assets/reading-bunny.webp" alt="一只小兔坐在笔记本旁读书的手绘插画" width="800" height="800" fetchpriority="high"><span class="art-caption">a little space to learn & grow</span></div></section>
      <section class="section" aria-labelledby="writing-title"><div class="section-heading"><div><span class="section-index">Notes & little discoveries</span><h2 id="writing-title">最近的手记</h2></div><a class="text-link" href="{BASE}/blog/">全部手记 ↗</a></div>{cards(posts[:3])}</section>
      <section class="section" id="about" aria-labelledby="about-title"><div class="section-heading"><div><span class="section-index">A little about me</span><h2 id="about-title">关于我</h2></div><span class="small-note">学习，也参与身边的小事。</span></div><div class="about-grid"><div class="note-card tint-blue"><span class="tape" aria-hidden="true"></span><h3>我的学习足迹</h3>{education}</div><div class="note-card"><h3>课堂以外</h3>{experiences}</div></div><div class="skills-wrap"><div class="skills-heading"><h3>现在的技能工具箱</h3><span class="small-note">继续学习，也慢慢实践。</span></div><div class="skills-grid">{skills}</div></div></section>
      <section class="contact-section" aria-labelledby="contact-title"><div class="contact-paper"><div><h2 id="contact-title">有想交流的事情吗？</h2><p>关于学习、志愿服务，或一个有意思的问题，都可以写信给我。</p></div><a class="email-link" href="mailto:{e(profile['email'])}">{e(profile['email'])} ↗</a></div></section>
    </main>'''

def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')

def build():
    posts = post_data()
    if PUBLIC.exists(): shutil.rmtree(PUBLIC)
    PUBLIC.mkdir(parents=True)
    shutil.copytree(ROOT / 'assets', PUBLIC / 'assets')
    write(PUBLIC / '.nojekyll', '')
    write(PUBLIC / 'index.html', page('刘毅涵 · 毅涵的小站', profile['intro'], home(posts), active='home'))
    blog = f'''<main class="wrap" id="main"><header class="blog-header"><span class="eyebrow">YIHAN'S NOTEBOOK</span><h1>手记与小发现</h1><p>记录学习中的问题、生活里的观察，还有把事情慢慢弄明白的过程。</p></header><div class="blog-list">{cards(posts)}</div></main>'''
    write(PUBLIC / 'blog/index.html', page('手记 · 毅涵的小站', '刘毅涵的学习笔记、志愿服务思考与工具心得。', blog, 'blog/', 'blog'))
    for p in posts:
        body = f'''<main id="main" class="wrap"><article class="article-wrap"><nav class="breadcrumb" aria-label="面包屑"><a href="{BASE}/blog/">所有手记</a> / {e(p['title'])}</nav><header class="article-header"><span class="post-tag">{e(p['tag'])}</span><h1>{e(p['title'])}</h1><div class="article-meta"><span>刘毅涵</span><time datetime="{p['date']}">{p['date'].replace('-', '.')}</time><span>约 {p['minutes']} 分钟阅读</span></div></header><div class="article-body">{p['html']}</div><footer class="article-end"><a class="text-link" href="{BASE}/blog/">← 回到所有手记</a><a class="text-link" href="mailto:{e(profile['email'])}">读后想聊聊？写信给我 ↗</a></footer></article></main>'''
        write(PUBLIC / f"blog/{p['slug']}/index.html", page(p['title']+' · 毅涵的小站', p['summary'], body, f"blog/{p['slug']}/", 'blog', 'article'))
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
    for url in [BASE+'/',BASE+'/blog/']+[p['url'] for p in posts]: ET.SubElement(ET.SubElement(sitemap,'url'),'loc').text=ORIGIN+url
    write(PUBLIC / 'sitemap.xml', ET.tostring(sitemap, encoding='unicode', xml_declaration=True))
    print(f'Built {len(posts)} post(s) in {PUBLIC}')

if __name__ == '__main__':
    build()

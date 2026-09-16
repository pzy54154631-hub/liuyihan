#!/usr/bin/env python3
"""Regenerate the editable book from all ordered tutorial Markdown posts.

Requires Python 3.11+ and pypandoc_binary. The generated main.tex itself does
not depend on Python or Pandoc; compile it directly with XeLaTeX twice.
"""
from pathlib import Path
import argparse
import json
import re
import subprocess
import tomllib
import pypandoc

HERE = Path(__file__).resolve().parent
SITE = 'https://pzy54154631-hub.github.io'
AUTHOR_URL = 'https://github.com/pzy54154631-hub?tab=repositories'

LICENSE = '''MIT License

Copyright (c) 2026 Ziyu Peng and 刘毅涵

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

PREAMBLE = r'''% !TeX program = xelatex
% Generated from the complete CHAPTER_COUNT-chapter web tutorial; editable standalone source.
% MIT License. Copyright (c) 2026 Ziyu Peng and 刘毅涵.
\documentclass[UTF8,a4paper,11pt,fontset=fandol,oneside,openany]{ctexbook}
\usepackage[margin=23mm,top=22mm,bottom=23mm,headheight=15pt,headsep=8mm]{geometry}
\usepackage{amsmath,amssymb,mathtools}
\usepackage{graphicx,xcolor,tikz}
\usepackage{longtable,booktabs,array,calc}
\usepackage{fvextra,fancyhdr,enumitem,needspace}
\usepackage[expansion=false]{microtype}
\usepackage{xurl}
\usepackage[unicode,colorlinks=true,linkcolor=InkPurple,urlcolor=InkPurple,
  pdftitle={LaTeX 学习手记：从中文笔记到经管报告},
  pdfauthor={Ziyu Peng; 刘毅涵},
  pdfsubject={完整CHAPTER_COUNT_ZH章教程与可编辑示例；MIT License}]{hyperref}
\usepackage{bookmark}
\definecolor{InkPurple}{HTML}{5A427A}
\definecolor{SoftPurple}{HTML}{EDE6F6}
\definecolor{PaperCream}{HTML}{FFF9EF}
\definecolor{Muted}{HTML}{69616D}
\definecolor{CodeInk}{HTML}{292334}
\setmainfont{texgyrepagella}[Extension=.otf,UprightFont=*-regular,
  BoldFont=*-bold,ItalicFont=*-italic,BoldItalicFont=*-bolditalic]
\setsansfont{texgyreheros}[Extension=.otf,UprightFont=*-regular,
  BoldFont=*-bold,ItalicFont=*-italic,BoldItalicFont=*-bolditalic]
\setmonofont{DejaVuSansMono}[Extension=.ttf,UprightFont=*,
  BoldFont=*-Bold,ItalicFont=*-Oblique,BoldItalicFont=*-BoldOblique,Scale=0.83]
\linespread{1.25}
\setlength{\parindent}{2em}
\setlength{\parskip}{0.25em}
\setlength{\emergencystretch}{3em}
\setlength{\LTpre}{0.5em}
\setlength{\LTpost}{0.8em}
\setcounter{tocdepth}{1}
\setcounter{secnumdepth}{1}
\setlist{itemsep=0.22em,topsep=0.4em,leftmargin=2em}
\ctexset{
  chapter={format=\raggedright\huge\bfseries\color{InkPurple},
    name={第,章},number=\arabic{chapter},beforeskip=0pt,afterskip=20pt},
  section={format=\large\bfseries\color{InkPurple},beforeskip=1.3em,afterskip=0.6em},
  subsection={format=\normalsize\bfseries\color{InkPurple},beforeskip=1em,afterskip=0.4em}
}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\color{Muted}LaTeX 学习手记}
\fancyhead[R]{\small\color{Muted}\nouppercase{\leftmark}}
\fancyfoot[L]{\footnotesize\color{Muted}Ziyu Peng \enspace / \enspace 刘毅涵}
\fancyfoot[R]{\small\color{InkPurple}\thepage}
\renewcommand{\headrulewidth}{0.35pt}
\renewcommand{\footrulewidth}{0pt}
\renewcommand{\chaptermark}[1]{\markboth{第\thechapter 章}{} }
\fancypagestyle{plain}{\fancyhf{}\fancyfoot[L]{\footnotesize\color{Muted}LaTeX 学习手记}
  \fancyfoot[R]{\small\color{InkPurple}\thepage}\renewcommand{\headrulewidth}{0pt}}
\DefineVerbatimEnvironment{TutorialCode}{Verbatim}{
  fontsize=\small,baselinestretch=1.03,breaklines=true,breakanywhere=true,
  breaksymbolleft={},breaksymbolright={},tabsize=2,
  frame=leftline,framesep=3mm,framerule=0.8pt,rulecolor=\color{SoftPurple},
  xleftmargin=4mm,xrightmargin=1mm,formatcom=\color{CodeInk}}
\providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
\newcommand{\pandocbounded}[1]{#1}
\newcounter{none}
\begin{document}
\begin{titlepage}
\pagecolor{PaperCream}
\begin{tikzpicture}[remember picture,overlay]
  \fill[SoftPurple] ([xshift=-25mm,yshift=-17mm]current page.north east) circle (63mm);
  \draw[InkPurple!25,line width=0.8pt] ([xshift=15mm,yshift=31mm]current page.south west) circle (49mm);
  \draw[InkPurple!15,line width=0.8pt] ([xshift=15mm,yshift=31mm]current page.south west) circle (58mm);
\end{tikzpicture}
\vspace*{18mm}
{\sffamily\small\color{InkPurple}LEARNING NOTES \quad / \quad COMPLETE EDITION\par}
\vspace{16mm}
{\fontsize{35}{47}\selectfont\bfseries\color{InkPurple}LaTeX 学习手记\par}
\vspace{7mm}
{\LARGE 从中文笔记到经管报告\par}
\vspace{8mm}
{\large CHAPTER_COUNT_ZH章完整教程 · 公式 · 表格 · 专业写作 · AI 协作\par}
\vspace{24mm}
{\large\href{https://github.com/pzy54154631-hub?tab=repositories}{Ziyu Peng}\enspace 第一作者\par}
\vspace{3mm}
{\large 刘毅涵\enspace 第二作者\par}
\vfill
{\small\color{Muted}合集整理：2026 年 9 月 16 日\quad / \quad MIT License\par}
\vspace{4mm}
{\small\href{https://pzy54154631-hub.github.io/liuyihan/blog/latex/}{在线阅读 · 章节目录与示例下载}\par}
\vspace*{11mm}
\end{titlepage}
\nopagecolor
\frontmatter
\chapter*{这本手记怎么读}
\addcontentsline{toc}{chapter}{这本手记怎么读}
这是一份从零起步、逐步写出完整课程报告的 LaTeX 教程。本书收录网站上CHAPTER_COUNT_ZH章的完整正文、公式、代码、练习与延伸阅读。读者可以顺序学习，也可以按当前任务查阅。

本系列于 2026 年 7 月发布首篇，随后逐章补充，于 2026 年 9 月 16 日整理成合集。

前四章建立中文文档、结构、公式与数学笔记的基础；第五至八章处理图片、表格、版式、引用与展示；第九至十二章把这些方法用于经济学模型、计量结果、金融现金流与会计报表；随后完成课程报告，学习怎样与 AI 协作写作和排错，并在 Overleaf 中导入、编译、协作与导出完整项目。

书中数学公式与示例代码承担不同作用：正文公式用于阅读，等宽字体中的代码用于复制和修改。部分代码是需要插入现有文档的片段；标注为完整示例的代码包含文档类与正文，可以另存为独立文件编译。经济、金融与会计中的教学数值和模拟情景，均应按各章说明理解。

\noindent\textbf{推荐编译方式：}中文文档使用 UTF-8 编码与 XeLaTeX；目录与交叉引用通常需要编译两遍。书中涉及书目的示例，还需要按该章说明运行 Biber。请先运行小例子，再逐步加入自己的内容。

\noindent\textbf{本书在线版本：}\href{https://pzy54154631-hub.github.io/liuyihan/blog/latex/}{刘毅涵的手记 · LaTeX 教程目录}。每章开头的“网页版”链接通往对应章节，可继续查阅配套示例与更新。

\chapter*{开放使用与许可}
\addcontentsline{toc}{chapter}{开放使用与许可}
\noindent\textbf{Copyright (c) 2026 Ziyu Peng and 刘毅涵}

本教程的原创正文、完整 PDF、LaTeX 源码与原创示例采用 MIT 许可证。你可以自由使用、复制、编辑、合并、再发布、分发，也可以用于商业用途；分发副本或实质性内容时，须保留版权声明与下列许可说明。

第三方宏包、字体、软件与引用文献遵循各自的许可证或版权条款；本许可不重新授予这些第三方内容的权利。本书中的外部链接用于延伸阅读。MIT 许可原文如下：

\begingroup\small\setlength{\parindent}{0pt}\setlength{\parskip}{0.6em}
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the ``Software''), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED ``AS IS'', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
\endgroup
\clearpage
\tableofcontents
\mainmatter
'''

def transform(node, prefix):
    if isinstance(node, list):
        return [transform(item, prefix) for item in node]
    if not isinstance(node, dict):
        return node
    if node.get('t') == 'CodeBlock':
        _attr, code = node['c']
        if '\\end{TutorialCode}' in code:
            raise ValueError('Reserved code delimiter in source')
        return {'t': 'RawBlock', 'c': ['latex', '\\begin{TutorialCode}\n' + code + '\n\\end{TutorialCode}']}
    if node.get('t') == 'Code':
        _attr, code = node['c']
        code_tex = ''.join(escape(c) + (r'\allowbreak{}' if c in '\\[]{}=/_.,-' else '') for c in code)
        return {'t': 'RawInline', 'c': ['latex', r'\texttt{' + code_tex + '}']}
    if node.get('t') == 'Header':
        level, attr, children = node['c']
        # H2 from the web articles becomes section under the book's chapter.
        attr[0] = prefix + attr[0]
        return {'t': 'Header', 'c': [max(1, level - 1), attr, transform(children, prefix)]}
    if node.get('t') == 'Link':
        attr, text, (url, title) = node['c']
        if url.startswith('/liuyihan/'):
            url = SITE + url
        elif url.startswith('#'):
            url = '#' + prefix + url[1:]
        return {'t': 'Link', 'c': [attr, transform(text, prefix), [url, title]]}
    return {key: transform(value, prefix) for key, value in node.items()}

def escape(value):
    replacements = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_', '{': r'\{', '}': r'\}', '^': r'\textasciicircum{}', '~': r'\textasciitilde{}'}
    return ''.join(replacements.get(char, char) for char in value)

def chinese_count(value):
    digits = '零一二三四五六七八九'
    if value < 10:
        return digits[value]
    if value < 100:
        tens, units = divmod(value, 10)
        return (digits[tens] if tens > 1 else '') + '十' + (digits[units] if units else '')
    return str(value)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--posts', type=Path, default=(HERE/'chapters-md' if (HERE/'chapters-md').is_dir() else HERE.parent/'content/posts'))
    parser.add_argument('--output', type=Path, default=HERE/'main.tex')
    args = parser.parse_args()
    chapters = []
    for path in args.posts.glob('latex-*.md'):
        _opening, header, body = path.read_text().split('+++', 2)
        meta = tomllib.loads(header)
        chapters.append((meta['order'], path, meta, body.replace('Ziyu.Peng', 'Ziyu Peng')))
    chapters.sort()
    if not chapters or [order for order, *_ in chapters] != list(range(1, len(chapters) + 1)):
        raise ValueError('Expected tutorial chapter orders to be unique and consecutive, starting at 1')
    preamble = PREAMBLE.replace('CHAPTER_COUNT_ZH', chinese_count(len(chapters))).replace('CHAPTER_COUNT', str(len(chapters)))
    out = [preamble]
    report = []
    for order, path, meta, body in chapters:
        doc = json.loads(pypandoc.convert_text(body, 'json', format='markdown+tex_math_dollars+tex_math_single_backslash+pipe_tables-raw_tex'))
        doc = transform(doc, f'c{order:02d}-')
        tex = pypandoc.convert_text(json.dumps(doc), 'latex', format='json', extra_args=['--wrap=preserve', '--top-level-division=section'])
        title = escape(meta['title'])
        title_display = title.replace('：', '：\\\\', 1) if order in (9, 14, 15) else title
        out += [f'\n\\chapter[{title}]{{{title_display}}}\n',
                f'\\label{{chapter:{order:02d}}}\n',
                '\\noindent{\\small\\color{Muted}'+escape(meta['stage'])+'\\quad / \\href{'+SITE+'/liuyihan/blog/'+path.stem+'/}{网页版}}\\par\\medskip\n', tex]
        report.append({'order': order, 'title': meta['title'], 'source': path.name,
                       'source_characters': len(body), 'code_blocks': body.count('```')//2})
    out += ['\n\\backmatter\n\\chapter*{继续写下去}\n',
            '从一页笔记开始，把结构、公式和资料来源逐步写清楚，再把能重复使用的部分积累成自己的工作方法。\\par\n',
            '\\noindent 第一作者：\\href{'+AUTHOR_URL+'}{Ziyu Peng}\\quad 第二作者：刘毅涵\\par\n',
            '\\noindent 在线目录：\\url{'+SITE+'/liuyihan/blog/latex/}\\par\n',
            '\\end{document}\n']
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(''.join(out))
    (args.output.parent/'LICENSE').write_text(LICENSE)
    (args.output.parent/'content-manifest.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(f'Generated {args.output}: {len(chapters)} chapters, {sum(item["code_blocks"] for item in report)} code blocks')

if __name__ == '__main__':
    main()

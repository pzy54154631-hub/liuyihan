#!/usr/bin/env python3
"""Check generated links, downloads, and all tutorial formulas before publishing."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import subprocess
import sys
import zipfile

ROOT = Path(__file__).parent
PUBLIC = ROOT / 'dist/liuyihan'

class Page(HTMLParser):
    def __init__(self, content):
        super().__init__()
        self.links, self.ids, self.maths = [], set(), []
        self.capture = None
        self.feed(content)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs: self.ids.add(attrs['id'])
        for key in ('href', 'src'):
            if key in attrs: self.links.append(attrs[key])
        classes = attrs.get('class', '').split()
        if 'math' in classes:
            self.capture = {'tex': '', 'display': 'block' in classes}

    def handle_data(self, data):
        if self.capture is not None: self.capture['tex'] += data

    def handle_endtag(self, tag):
        if self.capture is not None and tag in ('span', 'div'):
            self.maths.append(self.capture)
            self.capture = None

pages = {path: Page(path.read_text()) for path in PUBLIC.rglob('*.html')}
errors, formulas = [], []
for path, parsed in pages.items():
    for url in parsed.links:
        link = urlsplit(url)
        if link.scheme or link.netloc: continue
        if not link.path:
            target = path
        elif link.path.startswith('/liuyihan/'):
            target = PUBLIC / unquote(link.path.removeprefix('/liuyihan/'))
        else:
            target = path.parent / unquote(link.path)
        if target.is_dir(): target /= 'index.html'
        if not target.exists():
            errors.append(f'{path.relative_to(PUBLIC)}: missing {url}')
        elif link.fragment and target in pages and unquote(link.fragment) not in pages[target].ids:
            errors.append(f'{path.relative_to(PUBLIC)}: missing anchor {url}')
    formulas.extend({**m, 'page': str(path.relative_to(PUBLIC))} for m in parsed.maths)

node = subprocess.run(['node', '-e', r'''
const katex = require('./assets/vendor/katex/katex.min.js');
const fs = require('fs');
const formulas = JSON.parse(fs.readFileSync(0, 'utf8'));
let failures = 0;
for (const item of formulas) {
  try { katex.renderToString(item.tex, {displayMode: item.display, throwOnError: true, trust: false}); }
  catch (error) { console.error(item.page + ': ' + error.message); failures++; }
}
console.log(`Checked ${formulas.length} mathematical expressions`);
process.exit(failures ? 1 : 0);
'''], input=json.dumps(formulas), text=True, cwd=ROOT, capture_output=True)
print(node.stdout.strip())
if node.returncode: errors.append(node.stderr)
bundle = PUBLIC / 'assets/tutorial/latex-examples.zip'
if bundle.exists():
    with zipfile.ZipFile(bundle) as archive:
        broken = archive.testzip()
        if broken: errors.append(f'Broken archive entry: {broken}')
        print(f'Checked {len(archive.namelist())-1} downloadable examples')
if errors:
    print('\n'.join(errors), file=sys.stderr)
    sys.exit(1)
print(f'All local links and anchors valid across {len(pages)} pages')

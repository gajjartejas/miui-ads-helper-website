#!/usr/bin/env python3
"""Check generated pages, project-subpath links, accessibility basics, and size budgets."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
        self.tags = []
        self.headings = 0
        self.viewport = False
        self.has_main = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append(tag)
        self.headings += tag == 'h1'
        self.has_main |= tag == 'main'
        self.viewport |= tag == 'meta' and attrs.get('name') == 'viewport'
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, f'Duplicate ID: {attrs["id"]}'
            self.ids.add(attrs['id'])
        for name in ('href', 'src'):
            if name in attrs:
                self.links.append(attrs[name])
        if tag == 'img':
            assert all(k in attrs for k in ('alt', 'width', 'height')), 'Image needs alt and dimensions'


def check():
    routes = json.loads((ROOT / 'content/pages.json').read_text())
    parsed = {}
    for key in routes:
        path = ROOT / ('' if key == 'home' else key) / 'index.html'
        page = Page()
        page.feed(path.read_text())
        assert page.headings == 1 and page.viewport and page.has_main, path
        assert 'script' not in page.tags, f'JavaScript added to {path}'
        assert path.stat().st_size < 22000, f'HTML size budget exceeded: {path}'
        parsed[path.resolve()] = page
    for path, page in parsed.items():
        for href in page.links:
            url = urlsplit(href)
            if url.scheme or url.netloc:
                assert url.scheme in ('https', 'mailto'), href
                continue
            assert not url.path.startswith('/'), f'Link breaks project subpath: {href}'
            target = path.parent / unquote(url.path) if url.path else path
            if target.is_dir():
                target /= 'index.html'
            target = target.resolve()
            assert target.is_relative_to(ROOT), f'Escaping link: {href}'
            assert target.exists(), f'{path}: broken link {href}'
            if url.fragment and target in parsed:
                assert url.fragment in parsed[target].ids, f'Broken anchor: {href}'
    css = (ROOT / 'assets/style.css').read_text()
    assert '@media(max-width:680px)' in css and 'prefers-reduced-motion' in css
    assert '@import' not in css and 'url(' not in css
    assert len(css.encode()) < 15000
    print(f'PASS: {len(parsed)} pages; all local links/anchors; semantic landmarks; image dimensions; zero JS; responsive CSS; reduced motion; HTML <22 KB and CSS <15 KB.')
    for key in ('privacy', 'terms'):
        print(f'{key}: {(ROOT / key / "index.html").stat().st_size:,} bytes HTML')


if __name__ == '__main__':
    check()

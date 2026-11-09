#!/usr/bin/env python3
"""Build complete, script-free HTML pages using Python's standard library."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://gajjartejas.github.io/miui-ads-helper-website'
APP_REPO = 'https://github.com/gajjartejas/MIUIAdsHelper'
PAGES = json.loads((ROOT / 'content/pages.json').read_text())
LABELS = {'home': 'Home', 'help': 'Help', 'faq': 'FAQ', 'updates': 'Updates', 'translate': 'Translate', 'privacy': 'Privacy', 'terms': 'Terms'}


def build_page(key, metadata):
    home = key == 'home'
    prefix = './' if home else '../'
    route = '' if home else f'{key}/'
    url = f'{ORIGIN}/{route}'
    title = escape(metadata['title'])
    description = escape(metadata['description'], quote=True)

    def link(slug, label=None):
        href = prefix if slug == 'home' else f'{prefix}{slug}/'
        current = ' aria-current="page"' if key == slug else ''
        return f'<a href="{href}"{current}>{label or LABELS[slug]}</a>'

    def brand():
        return f'<a class="brand" href="{prefix}"><img src="{prefix}assets/app-icon.png" width="42" height="42" alt=""><span>MIUI Ads Helper<small>LESS NOISE. MORE CONTROL.</small></span></a>'

    content = (ROOT / f'content/{key}.html').read_text()
    if home:
        main = f'<main id="main" class="shell">{content}</main>'
    else:
        sidebar = ''.join(link(k) for k in LABELS)
        main = f'<main id="main" class="shell article-layout"><aside class="article-aside"><nav aria-label="Information pages">{sidebar}</nav></aside><article class="article"><p class="eyebrow">MIUI ADS HELPER / {LABELS[key].upper()}</p><h1>{title}</h1>{content}</article></main>'
    document = f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · MIUI Ads Helper</title><meta name="description" content="{description}">
<meta name="theme-color" content="#faf8f5"><link rel="canonical" href="{url}">
<meta property="og:title" content="{title} · MIUI Ads Helper"><meta property="og:description" content="{description}">
<meta property="og:type" content="website"><meta property="og:url" content="{url}"><meta property="og:image" content="{ORIGIN}/assets/app-icon.png">
<link rel="icon" href="{prefix}assets/app-icon.png"><link rel="stylesheet" href="{prefix}assets/style.css">
</head><body class="page-{key}"><a class="skip" href="#main">Skip to content</a>
<header class="header"><div class="shell header-inner">{brand()}<nav class="nav" aria-label="Main navigation">{link('home')}{link('help')}{link('faq')}{link('updates')}</nav><a class="header-link" href="https://play.google.com/store/apps/details?id=com.tejasgajjar.miuiadshelper">Get the app ↗</a></div></header>
{main}
<footer class="footer"><div class="shell"><div class="footer-top"><div class="footer-copy">{brand()}<p>A little guidance for a calmer Xiaomi experience. An independent, open-source project by Tejas Gajjar.</p></div><nav aria-label="Footer navigation"><div><strong>Explore</strong>{link('home')}{link('updates')}<a href="{APP_REPO}">Source code ↗</a></div><div><strong>Support</strong>{link('help')}{link('faq')}{link('translate')}<a href="mailto:gajjartejas26@gmail.com">Contact</a></div><div><strong>Legal</strong>{link('privacy', 'Privacy Policy')}{link('terms', 'Terms of Service')}</div></nav></div><div class="footer-bottom"><span>© 2026 Tejas Gajjar · MIUI Ads Helper</span><span>Not affiliated with Xiaomi. No tracking scripts on this website.</span></div></div></footer>
</body></html>
'''
    target = ROOT / route / 'index.html'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(document)
    return url


if __name__ == '__main__':
    urls = [build_page(key, metadata) for key, metadata in PAGES.items()]
    (ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{url}</loc></url>' for url in urls) + '</urlset>\n')
    (ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {ORIGIN}/sitemap.xml\n')
    print(f'Built {len(urls)} complete HTML pages. No JavaScript or runtime dependencies.')

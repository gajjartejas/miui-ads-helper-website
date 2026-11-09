# MIUI Ads Helper website

Lightweight public landing, support, privacy, and terms pages for MIUI Ads Helper, by Tejas Gajjar. Inspired by the structure of [kano-app-website](https://github.com/gajjartejas/kano-app-website), with independent MIUI Ads Helper branding and content. No mobile application source, credentials, or SDKs are included.

**Website:** https://gajjartejas.github.io/miui-ads-helper-website/

- [Privacy Policy](https://gajjartejas.github.io/miui-ads-helper-website/privacy/)
- [Terms of Service](https://gajjartejas.github.io/miui-ads-helper-website/terms/)
- [Help](https://gajjartejas.github.io/miui-ads-helper-website/help/)
- [FAQ](https://gajjartejas.github.io/miui-ads-helper-website/faq/)
- [Updates](https://gajjartejas.github.io/miui-ads-helper-website/updates/)
- [Translation](https://gajjartejas.github.io/miui-ads-helper-website/translate/)

## Edit and preview

Requires Python 3.9 or later, with no third-party dependencies.

```sh
# Edit content/*.html, content/pages.json, or assets/style.css, then:
python3 scripts/build.py
python3 scripts/check.py
python3 -m http.server 8000
```

Open http://localhost:8000/. Commit both source fragments and generated HTML. Each route is a complete HTML document: JavaScript, external fonts, analytics, and client-side routing are not used. Legal content is rendered in the initial HTML response. Images have explicit dimensions, legal pages have no entrance animation, and homepage motion respects Reduce Motion.

## Hosting

GitHub Pages serves `main` from the repository root. `.nojekyll` disables Jekyll. No npm install, bundler, or server runtime is needed. Relative URLs work under the repository project path. GitHub Pages handles HTTPS and CDN delivery; actual loading time depends on network conditions and hosting cache state.

Public legal content reflects the MIUI Ads Helper source reviewed on 9 November 2026, including Firebase diagnostics, device identifiers, and guide-associated package availability. Review these pages when the app's collection behavior, billing, or license changes. No account or authentication is required to read them.

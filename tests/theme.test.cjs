const { test } = require('node:test');
const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const { join } = require('node:path');
const { runInNewContext } = require('node:vm');
const assets = join(__dirname, '../assets');
const init = readFileSync(join(assets, 'theme-init.js'), 'utf8');
const script = readFileSync(join(assets, 'theme.js'), 'utf8');

function setup({ saved = null, dark = false, blocked = false } = {}) {
  const listeners = {};
  const attrs = {};
  const root = { dataset: {} };
  const media = { matches: dark, addEventListener: (type, fn) => { listeners.system = fn; } };
  const button = {
    hidden: true,
    setAttribute: (key, value) => { attrs[key] = value; },
    addEventListener: (type, fn) => { listeners.click = fn; },
  };
  const meta = { setAttribute: (key, value) => { attrs.meta = value; } };
  const storage = new Map(saved === null ? [] : [['miui-theme', saved]]);
  const context = {
    window: {
      matchMedia: () => media,
      addEventListener: (type, fn) => { listeners[type] = fn; },
    },
    document: {
      documentElement: root,
      querySelector: selector => selector.startsWith('meta') ? meta : button,
    },
    localStorage: {
      getItem: key => { if (blocked) throw new Error('Storage blocked'); return storage.get(key) ?? null; },
      setItem: (key, value) => { if (blocked) throw new Error('Storage blocked'); storage.set(key, value); },
    },
  };
  runInNewContext(init, context);
  const initialTheme = root.dataset.theme;
  runInNewContext(script, context);
  return { root, media, button, attrs, listeners, storage, initialTheme };
}

test('uses the system theme before content paints and does not save it as an explicit choice', () => {
  const site = setup({ dark: true });
  assert.equal(site.initialTheme, 'dark');
  assert.equal(site.attrs['aria-pressed'], 'true');
  assert.equal(site.button.hidden, false);
  assert.equal(site.storage.size, 0);
  site.media.matches = false;
  site.listeners.system();
  assert.equal(site.root.dataset.theme, 'light');
  assert.equal(site.attrs.meta, '#faf8f5');
});

test('a saved light preference overrides a dark system theme across pages', () => {
  const site = setup({ saved: 'light', dark: true });
  assert.equal(site.initialTheme, 'light');
  site.listeners.system();
  assert.equal(site.root.dataset.theme, 'light');
  site.listeners.click();
  assert.equal(site.storage.get('miui-theme'), 'dark');
  assert.equal(site.attrs['aria-pressed'], 'true');
  assert.equal(site.attrs.meta, '#19161b');
  const nextPage = setup({ saved: site.storage.get('miui-theme') });
  assert.equal(nextPage.initialTheme, 'dark');
});

test('the toggle works even when browser storage is unavailable', () => {
  const site = setup({ blocked: true });
  site.listeners.click();
  assert.equal(site.root.dataset.theme, 'dark');
  site.listeners.system();
  assert.equal(site.root.dataset.theme, 'dark');
  site.listeners.click();
  assert.equal(site.root.dataset.theme, 'light');
});

test('ignores invalid stored values and follows changes from another tab', () => {
  const site = setup({ saved: 'invalid', dark: true });
  assert.equal(site.initialTheme, 'dark');
  site.listeners.storage({ key: 'miui-theme', newValue: 'light' });
  assert.equal(site.root.dataset.theme, 'light');
  site.listeners.storage({ key: null });
  assert.equal(site.root.dataset.theme, 'dark');
});

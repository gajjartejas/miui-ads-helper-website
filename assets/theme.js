(() => {
  const root = document.documentElement;
  const button = document.querySelector('[data-theme-toggle]');
  const meta = document.querySelector('meta[name="theme-color"]');
  const system = window.matchMedia?.('(prefers-color-scheme: dark)');
  let preference;
  try { preference = localStorage.getItem('miui-theme'); } catch {}
  const isTheme = value => value === 'dark' || value === 'light';
  const apply = theme => {
    root.dataset.theme = theme;
    button?.setAttribute('aria-pressed', String(theme === 'dark'));
    meta?.setAttribute('content', theme === 'dark' ? '#19161b' : '#faf8f5');
  };
  const followPreference = () => apply(isTheme(preference) ? preference : system?.matches ? 'dark' : 'light');
  followPreference();
  if (button) {
    button.hidden = false;
    button.addEventListener('click', () => {
      preference = root.dataset.theme === 'dark' ? 'light' : 'dark';
      apply(preference);
      try { localStorage.setItem('miui-theme', preference); } catch {}
    });
  }
  system?.addEventListener('change', () => {
    if (!isTheme(preference)) followPreference();
  });
  window.addEventListener('storage', event => {
    if (event.key === 'miui-theme' || event.key === null) {
      preference = event.key === null ? null : event.newValue;
      followPreference();
    }
  });
})();

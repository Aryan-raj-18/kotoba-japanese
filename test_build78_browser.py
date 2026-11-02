"""Real rendered regressions for tester-reported settings and learning overflow.

Checks text ranges against padded card bounds, not only page scrollWidth.
Run explicitly: python test_build78_browser.py. Set KOTOBA_BASELINE78=1
to reproduce these checks with the previous release's CSS/controllers.
"""
import atexit
import json
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent

BOUNDS = r'''selector => {
 const issues = [];
 const visible = e => e.getClientRects().length && !e.closest('[hidden]');
 if (document.documentElement.scrollWidth > innerWidth + 2) issues.push('page horizontal overflow');
 for (const card of document.querySelectorAll(selector)) {
  if (!visible(card)) continue;
  const cr = card.getBoundingClientRect(), cs = getComputedStyle(card);
  const inset = Math.min(10, parseFloat(cs.paddingLeft));
  if (inset < 10) issues.push((card.id || card.className) + ' missing reading inset');
  for (const e of card.querySelectorAll('p,h2,strong,span,button')) {
   if (!visible(e) || !e.textContent.trim()) continue;
   if (e.scrollWidth > e.clientWidth + 2) issues.push((e.id || e.className) + ' text overflow');
   const range = document.createRange(); range.selectNodeContents(e);
   for (const r of range.getClientRects()) {
    if (!r.width || !r.height) continue;
    if (r.left < cr.left + inset - 2 || r.right > cr.right - inset + 2 ||
        r.top < cr.top + inset - 2 || r.bottom > cr.bottom - inset + 2)
     issues.push((e.id || e.className) + ' outside reading inset');
   }
  }
 }
 return [...new Set(issues)];
}'''

SCALE = r'''factor => {
 const nodes = [...document.querySelectorAll('main p,main h1,main h2,main button,main span,main strong')];
 const sizes = nodes.map(e => parseFloat(getComputedStyle(e).fontSize));
 nodes.forEach((e, i) => e.style.fontSize = sizes[i] * factor + 'px');
}'''


def run(base):
    from playwright.sync_api import sync_playwright
    report = {'states': [], 'errors': [], 'failures': [], 'settings': []}
    baseline = bool(os.environ.get('KOTOBA_BASELINE78'))
    out = ROOT / 'verification' / ('browser78-before' if baseline else 'browser78')
    out.mkdir(parents=True, exist_ok=True)
    atexit.register(lambda: (out / 'results.json').write_text(json.dumps(report, indent=2)))
    with sync_playwright() as pw:
        opts = {'args': ['--no-sandbox', '--disable-dev-shm-usage']}
        if os.environ.get('KOTOBA_CHROME'):
            opts['executable_path'] = os.environ['KOTOBA_CHROME']
            os.chmod(opts['executable_path'], 0o755)
        browser = pw.chromium.launch(**opts)
        ctx = browser.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True)
        ctx.add_init_script("""localStorage.setItem('kotoba:onboarding:v3','1');
          if(!localStorage.getItem('kotoba:theme'))localStorage.setItem('kotoba:theme','kyoto-night');
          window.KotobaStartupNative={introElapsedMs:()=>3000};
          Object.defineProperty(navigator,'deviceMemory',{get:()=>2});""")
        if baseline:
            for path in ('static/css/liquid-glass.css', 'static/js/liquid-glass.js', 'static/js/theme.js'):
                content = subprocess.check_output(['git', 'show', 'HEAD:' + path], cwd=ROOT).decode()
                ctx.route('**/' + path + '*', lambda route, request, content=content, path=path:
                          route.fulfill(body=content, content_type='text/css' if path.endswith('.css') else 'text/javascript'))
        p = ctx.new_page()
        p.on('pageerror', lambda e: report['errors'].append(str(e)))

        def go(route):
            assert p.goto(base + route).status == 200
            p.evaluate('document.fonts.ready')
            p.add_style_tag(content='html {scroll-behavior:auto !important} *,*::before,*::after {animation:none !important;transition:none !important}')
            # A busy, code-created wallpaper makes the blur/clear difference
            # visible without shipping a tester's personal photo in the repo.
            p.add_style_tag(content='body {background:repeating-linear-gradient(45deg,#b86744 0 16px,#204f65 16px 32px,#e3b96a 32px 48px) !important}')

        def check(label, selector):
            issues = p.evaluate(BOUNDS, selector)
            report['states'].append({'state': label, 'issues': issues})
            report['failures'].extend(label + ': ' + i for i in issues)

        # Exercise the real learn -> practice transition from the report.
        sizes = ((390, 1),) if baseline else ((320, 1), (390, 1), (390, 2), (560, 1), (800, 1))
        for width, scale in sizes:
            p.set_viewport_size({'width': width, 'height': 844})
            for chapter in ('hiragana-1', 'hiragana-2', 'katakana-1'):
                go('/roadmap/' + chapter)
                count = p.locator('#rm-vocab-data').evaluate('e=>JSON.parse(e.textContent).length')
                for _ in range(count):
                    p.locator('#rm-next').click()
                p.locator('#rm-quiz:not([hidden])').wait_for()
                quiz = p.locator('#rm-quiz-data').evaluate('e=>JSON.parse(e.textContent)')
                if scale != 1:
                    p.evaluate(SCALE, scale)
                check(f'{width} {scale}x {chapter} practice', '#rm-quiz')
                if width == 390 and scale == 1 and chapter == 'hiragana-2':
                    p.screenshot(path=str(out / 'hiragana-practice.png'), full_page=True)
                # Render every question and its answer/explanation, including combo and done.
                for index, q in enumerate(quiz):
                    options = p.locator('#rm-options button')
                    options.filter(has_text=re.compile('^' + re.escape(q['correct']) + '$')).click()
                    check(f'{width} {scale}x {chapter} answer {index + 1}', '#rm-quiz')
                    p.locator('#rm-continue').click()
                p.locator('#rm-done:not([hidden])').wait_for()
                check(f'{width} {scale}x {chapter} done', '#rm-done')
            for game, difficulty in [(g, d) for g in ('match', 'audio', 'kana', 'verbs', 'sentence')
                                     for d in ('easy', 'medium', 'hard')]:
                go('/games')
                if scale != 1:
                    p.evaluate(SCALE, scale)
                check(f'{width} {scale}x games picker', '.game-pick')
                if width == 390 and scale == 1 and game == 'match' and difficulty == 'easy':
                    p.screenshot(path=str(out / 'games-picker.png'), full_page=True)
                p.locator('.game-pick[data-game="' + game + '"]').click()
                p.locator('#game-levels [data-level="' + difficulty + '"]').click()
                p.locator('#game-start').click()
                p.locator('#game-stage:not([hidden])').wait_for()
                p.locator('.match-tile' if game == 'match' else '.game-question').first.wait_for()
                if scale != 1:
                    # The dynamically inserted board has its own new text nodes.
                    p.locator('#game-board').evaluate('''(board, factor) => {
                      const nodes=[...board.querySelectorAll('p,button,h2,span')];
                      const sizes=nodes.map(e=>parseFloat(getComputedStyle(e).fontSize));
                      nodes.forEach((e,i)=>e.style.fontSize=sizes[i]*factor+'px');
                    }''', scale)
                check(f'{width} {scale}x game {game} {difficulty}', '#game-stage,.game-question,.match-tile')
        # Test the real settings switch, contrast, persistence, and desktop anchoring.
        for width in (390, 1280):
            p.set_viewport_size({'width': width, 'height': 844})
            for theme in ('sakura-journey', 'kyoto-night'):
                go('/about')
                p.evaluate('theme => {localStorage.setItem("kotoba:theme",theme);KotobaTheme.apply(theme)}', theme)
                p.locator('#settings-btn').click()
                if not p.locator('#settings-panel').evaluate('e=>e.parentElement===document.body'):
                    report['failures'].append(f'{width}: settings trapped in header backdrop')
                for mode in ('off', 'on'):
                    if p.locator('html').get_attribute('data-glass') != mode:
                        p.locator('#liquid-glass-switch').click()
                    style = p.locator('#settings-panel').evaluate('''e => ({
                      blur:getComputedStyle(e).backdropFilter,
                      bg:getComputedStyle(e).backgroundColor,
                      quality:document.documentElement.dataset.glassQuality,
                      checked:document.getElementById('liquid-glass-switch').getAttribute('aria-checked')
                    })''')
                    report['settings'].append({'width': width, 'theme': theme, 'mode': mode, **style})
                    wanted = mode == 'on'
                    if ('blur(' in style['blur']) != wanted:
                        report['failures'].append(f'{width} {theme} settings {mode}: wrong blur {style}')
                    assert style['checked'] == str(wanted).lower()
                    if width == 390 and theme == 'kyoto-night':
                        p.screenshot(path=str(out / ('settings-' + mode + '.png')))
                    p.reload()
                    p.add_style_tag(content='body {background:repeating-linear-gradient(45deg,#b86744 0 16px,#204f65 16px 32px,#e3b96a 32px 48px) !important}')
                    assert p.locator('html').get_attribute('data-glass') == mode
                    assert p.locator('html').get_attribute('data-theme') == theme
                    p.locator('#settings-btn').click()
                a, b = report['settings'][-2:]
                if a['bg'] == b['bg']:
                    report['failures'].append(f'{width} {theme}: settings tint does not change')
                rect = p.locator('#settings-panel').bounding_box()
                assert rect['x'] >= 0 and rect['x'] + rect['width'] <= width + 1, rect
                assert rect['y'] >= 0 and rect['y'] + rect['height'] <= 844 + 1, rect
                if width == 390:
                    assert not p.locator('.site-main').is_visible()
                p.keyboard.press('Escape')
                assert p.locator('#settings-panel').is_hidden()
                assert p.locator('.site-main').is_visible()
                assert not p.locator('body').evaluate('e=>e.classList.contains("kotoba-settings-open")')
        # Unsupported engines must remain readable, and explain the fallback.
        fallback = browser.new_context()
        fallback.add_init_script("""localStorage.setItem('kotoba:onboarding:v3','1');
          window.KotobaStartupNative={introElapsedMs:()=>3000};
          const original=CSS.supports.bind(CSS);
          CSS.supports=(p,v)=>p.includes('backdrop-filter')?false:original(p,v);""")
        f = fallback.new_page()
        assert f.goto(base + '/about').status == 200
        assert f.locator('html').get_attribute('data-glass-quality') == 'lite'
        if not baseline:
            assert 'unavailable' in f.locator('#liquid-glass-hint').text_content()
        fallback.close()
        browser.close()
    (out / 'results.json').write_text(json.dumps(report, indent=2))
    assert not report['errors'], report['errors']
    assert not report['failures'], report['failures'][:25]
    print('PASS', len(report['states']), 'Roadmap/game states;', len(report['settings']), 'settings mode/appearance checks')


if __name__ == '__main__':
    import test_build76_browser as harness
    harness.run = run
    harness.main()

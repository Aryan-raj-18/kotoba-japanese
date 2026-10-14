"""Play Store visual layout preflight.

Renders *actual* Jinja page templates with representative data and production
CSS, checking both glass modes at common phone/tablet/desktop widths. These
are static responsive checks, not a substitute for exercising real sessions
or checking a physical Android WebView.

Requires: pip install playwright; python -m playwright install chromium
"""
import json
import os
import re
from pathlib import Path
from types import SimpleNamespace
from jinja2 import Environment, FileSystemLoader, ChainableUndefined
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / 'verification' / 'browser-layout'
CSS_FILES = ('style.css', 'ui-shell.css', 'journey.css', 'liquid-glass.css')
WIDTHS = (320, 390, 768, 1280)


def context():
    learner = {
        'due': 12, 'mastery': dict(Mastered=300, New=30, Familiar=40, Learning=50, Weak=2),
        'level': 4, 'xp': 1260, 'missions': [], 'xp_into_level': 50, 'xp_per_level': 100,
    }
    return dict(
        learner=learner, roadmap=dict(pct=8, total=91, sections=[], next_id='hiragana-1'),
        streak=dict(current=1), next_lesson=dict(icon='あ',stage='Foundation',minutes=5,
            title='Hiragana',section='First Steps',position=1,total=91,url='/roadmap/hiragana-1'),
        jlpt_count=2133,story_count=50,conversation_count=30,show_onboarding=False,
        levels=[dict(level='N5',description='Beginner',count=103,exam_count=30),
                dict(level='N4',description='Elementary',count=174,exam_count=20)],
        level='N5',label='N5 Beginner',entries=[dict(kanji='日',meaning='day, sun',
            on_yomi='ニチ',kun_yomi='ひ',level='N5',difficulty='easy')]*7,exam_count=40,
        categories=['Vocabulary','Grammar'],question_count=100,initial_entries=[],
        level_counts={'N5':103},active_level='N5',catalog_json='[]',grouped={},total=3741,
        data=[dict(char='あ',romaji='a',type='basic'),dict(char='ひ',romaji='hi',type='basic')],
        kana_type='Hiragana',hiragana=[],katakana=[],quiz_json='[]',quiz_count=10,
        chapter=dict(id='hiragana-1',title='Hiragana',level='N5',vocab=[],icon='あ'),
        summary={},already_completed=False, visited_count=0,visited_ids=[],
        default_level='beginner',japan_data={'places':[],'regions':[]},
        lists={'My Words':[dict(front='日本語',reading='にほんご',meaning='Japanese language',
            kind='vocab',key='1',url='/kanji/1')]},pages=1,page=1,query='water',
        results=[],suggestions=[],progress=dict(known=1,total=100,pct=1,decks=[]),
        flashcards=[],story={},stories=[],search_results=[],
    )


def prepared_templates():
    env = Environment(loader=FileSystemLoader(str(ROOT/'templates')),
                      undefined=ChainableUndefined, autoescape=True)
    env.globals.update(
        url_for=lambda name, **kw: '/static/'+kw.get('filename','') if name == 'static' else '/'+name,
        csrf_token=lambda: 'release-test',request=SimpleNamespace(endpoint='audit',args={}),
        app_version='1.0.0',study_kanji_reading=lambda entry:'みず',
        kana_readings=lambda s:[s],get_flashed_messages=lambda **kw:[],
    )
    for file in sorted((ROOT/'templates').glob('*.html')):
        if file.name.startswith('_') or file.name == 'base.html':
            continue
        html = env.get_template(file.name).render(**context())
        # This is a style/layout check, not an API-enabled app server.
        html = re.sub(r'<script\b[^>]*>.*?</script>', '', html, flags=re.I|re.S)
        html = re.sub(r'<link\b[^>]*rel="stylesheet"[^>]*>', '', html, flags=re.I|re.S)
        yield file.name, html


MEASURE = '''() => {
  const viewport=innerWidth;
  const overflowing=[];
  const selectors='.site-main h1,.site-main h2,.site-main h3,'+
    '.site-main .btn-primary,.site-main .category-heading,.site-main .mcq-review-row,'+
    '.site-main .exam-review-card,.site-main .kana-tile,.site-main .verb-row,'+
    '.site-main .vocab-row,.site-main .quiz-option';
  for (const el of document.querySelectorAll(selectors)) {
    const css=getComputedStyle(el), rect=el.getBoundingClientRect();
    if(css.display==='none'||css.visibility==='hidden'||rect.width<1)continue;
    if(el.scrollWidth>el.clientWidth+4 && ['hidden','clip'].includes(css.overflowX))
      overflowing.push({tag:el.tagName,text:(el.innerText||'').slice(0,55),pixels:el.scrollWidth-el.clientWidth});
  }
  return {horizontalPixels:document.documentElement.scrollWidth-viewport, overflowing};
}'''


def main():
    css = '\n'.join((ROOT/'static/css'/file).read_text(encoding='utf8') for file in CSS_FILES)
    templates = list(prepared_templates())
    OUTPUT.mkdir(parents=True,exist_ok=True)
    errors=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,args=['--no-sandbox'],
            executable_path=(os.environ.get('KOTOBA_CHROME') or ('/usr/bin/chromium' if Path('/usr/bin/chromium').exists() else None)))
        for width in WIDTHS:
            page=browser.new_page(viewport=dict(width=width,height=840),device_scale_factor=1)
            for name, markup in templates:
                page.set_content(markup,wait_until='domcontentloaded')
                page.add_style_tag(content=css)
                for mode in ('on','off'):
                    page.evaluate('(mode) => document.documentElement.setAttribute("data-glass", mode)',mode)
                    result=page.evaluate(MEASURE)
                    if result['horizontalPixels']>3 or result['overflowing']:
                        errors.append(dict(page=name,width=width,glass=mode,**result))
                if name in ('index.html','jlpt_practice.html','everyday.html','practice.html','roadmap.html','explore.html') and width in (390,1280):
                    page.screenshot(path=str(OUTPUT/(name[:-5]+'-'+str(width)+'.png')),animations='disabled')
            page.close()
        browser.close()
    result=dict(templates=len(templates),combinations=len(templates)*len(WIDTHS)*2,
                widths=list(WIDTHS),glass=['on','off'],errors=errors)
    (OUTPUT/'summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(f"Static Jinja/CSS layouts: {result['combinations']} checks, {len(errors)} issues")
    for issue in errors[:20]:print(issue)
    if errors:
        raise SystemExit(1)


if __name__=='__main__':main()

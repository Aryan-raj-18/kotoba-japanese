"""Live Flask/Chromium regression: real learning states and expanded SVG camera.
Run explicitly (not during unit discovery): python test_build76_browser.py.
"""
import json, os, subprocess, sys, tempfile, time, urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parent
ROUTES=['/','/explore','/kanji','/kanji/1','/kanji/160','/kanji/practice','/radicals','/radicals/r001','/hiragana','/katakana','/jlpt','/jlpt/N5','/jlpt/N1','/jlpt/N5/practice','/jlpt/N5/exam-practice','/jlpt/N5/mock','/everyday','/verbs','/grammar','/grammar/g-001','/roadmap','/roadmap/smartphones-apps','/speaking','/review','/flashcards','/writing-practice','/write','/japan','/dashboard','/streak','/practice','/games','/favorites','/mistakes','/backup','/sync','/privacy','/about','/feedback','/data-controls','/kanji-notification','/placement','/stories','/stories/neko-to-ame','/conversations','/conversations/self-introduction','/search?q=sor']
LAYOUT=r'''() => {
 const issues=[];const visible=e=>e.getClientRects().length && getComputedStyle(e).visibility!=='hidden' && !e.closest('[hidden],svg');
 if(document.documentElement.scrollWidth>innerWidth+2)issues.push('page overflow '+document.documentElement.scrollWidth+'/'+innerWidth);
 for(const e of document.querySelectorAll('main p,main h1,main h2,main h3,main button,main label,main .learn-kanji,main .mcq-kanji,main .flash-face')){
  if(!visible(e)||!e.textContent.trim())continue;
  const s=getComputedStyle(e),r=e.getBoundingClientRect();
  if(e.scrollWidth>e.clientWidth+3 && e.clientWidth && !['auto','scroll'].includes(s.overflowX) && !e.closest('.kana-table-wrap,.table-scroll'))issues.push((e.id||e.className||e.tagName)+': horizontal text '+e.scrollWidth+'/'+e.clientWidth);
  if(e.scrollHeight>e.clientHeight+4 && ['hidden','clip'].includes(s.overflowY) && s.textOverflow!=='ellipsis')issues.push((e.id||e.className||e.tagName)+': clipped text '+e.scrollHeight+'/'+e.clientHeight);
 }
 return [...new Set(issues)].slice(0,30);
}'''
def run(base):
 from playwright.sync_api import sync_playwright
 report={'pages':[],'states':[],'map':{},'errors':[]}
 import atexit
 (ROOT/'verification').mkdir(exist_ok=True)
 atexit.register(lambda:(ROOT/'verification/browser76.json').write_text(json.dumps(report,indent=2)))
 with sync_playwright() as pw:
  opts={'args':['--no-sandbox','--disable-dev-shm-usage']}
  if os.environ.get('KOTOBA_CHROME'):
   opts['executable_path']=os.environ['KOTOBA_CHROME'];os.chmod(opts['executable_path'],0o755)
  browser=pw.chromium.launch(**opts)
  p=browser.new_page(viewport={'width':390,'height':844})
  p.add_init_script("localStorage.setItem('kotoba:onboarding:v3','1');window.KotobaStartupNative={introElapsedMs:()=>3000};")
  p.on('pageerror',lambda error:report['errors'].append(str(error)))
  def go(route):
   response=p.goto(base+route);assert response.status==200,(route,response.status)
   p.evaluate('document.fonts.ready')
  def check(label):
   issues=p.evaluate(LAYOUT);report['states'].append({'state':label,'issues':issues});return issues
  def finish(label):
   issues=check(label);assert not issues,(label,issues)
  # Real rendered pages at narrow mobile, regular mobile and desktop widths.
  for width in (320,390,1280):
   p.set_viewport_size({'width':width,'height':844})
   for route in ROUTES:
    go(route);issues=check(str(width)+' '+route)
    report['pages'].append({'width':width,'route':route,'issues':issues})
  (ROOT/'verification').mkdir(exist_ok=True);(ROOT/'verification/browser76-pages.json').write_text(json.dumps(report,indent=2))
  p.set_viewport_size({'width':320,'height':844})
  # All five levels: actual kanji tests, answers, result cards and exam furigana.
  for level in ('N5','N4','N3','N2','N1'):
   go('/jlpt/'+level+'/practice');p.locator('#mcq-start-btn').click();p.locator('#mcq-options button').first.wait_for()
   for n in range(80):
    if p.locator('#mcq-panel-results').is_visible():break
    assert p.locator('#mcq-kanji').inner_text().strip(),level
    options=p.locator('#mcq-options button');assert options.count()>=2
    assert all(t.strip() for t in options.all_text_contents())
    finish(level+' kanji question');options.first.click()
   assert p.locator('#mcq-panel-results').is_visible();finish(level+' kanji results')
   go('/jlpt/'+level+'/exam-practice');p.locator('#exam-count-options [data-count="5"]').click();p.locator('#exam-start-btn').click();p.locator('#exam-options button').first.wait_for()
   for n in range(5):
    assert p.locator('#exam-question').inner_text().strip()
    assert all(t.strip() for t in p.locator('#exam-options button').all_text_contents())
    finish(level+' exam question');p.locator('#exam-options button').first.click()
    finish(level+' exam feedback');p.locator('#exam-next-btn').click()
   assert p.locator('#exam-panel-results').is_visible();finish(level+' exam results')
  # Selection changes survive navigation and remain visible before submitting.
  go('/jlpt/N5/mock');p.locator('#mock-start').click();p.locator('#mock-options button').first.wait_for();p.locator('#mock-options button').nth(1).click()
  selected=p.locator('#mock-options button').nth(1).inner_text();p.locator('#mock-next').click();p.locator('#mock-prev').click()
  assert p.locator('#mock-options button').nth(1).get_attribute('aria-pressed')=='true';p.locator('#mock-options button').first.click()
  finish('mock changed selection');p.locator('#mock-submit').click();p.locator('#mock-results:not([hidden])').wait_for();finish('mock review')
  go('/practice');p.locator('#start-btn').click();p.locator('#panel-learn:not([hidden])').wait_for()
  for n in range(40):
   if not p.locator('#panel-learn').is_visible():break
   assert p.locator('#learn-kanji').inner_text().strip();finish('learn card');p.locator('#learn-next').click()
  p.locator('#quiz-options button').first.click();p.locator('#panel-explain:not([hidden])').wait_for();finish('practice explanation')
  for route,start,front in [('/review','#review-start','#review-front'),('/flashcards','#fc-start','#fc-select-face'),('/speaking','#speaking-start','#speaking-run')]:
   go(route);p.locator(start).click();p.locator(front).wait_for();finish(route+' active')
  go('/review');p.locator('#review-start').click();p.locator('#review-reveal').click();finish('review revealed')
  for game in ('match','audio','kana','verbs','sentence'):
   go('/games');p.locator('.game-pick[data-game="'+game+'"]').click();p.locator('#game-start').click();p.locator('#game-stage:not([hidden])').wait_for();finish('game '+game)
  # Both glass modes in both color schemes, active panes and persisted setting.
  for color in ('light','dark'):
   p.emulate_media(color_scheme=color)
   for mode in ('on','off'):
    go('/about');p.locator('#settings-btn').click()
    if p.locator('html').get_attribute('data-glass')!=mode:p.locator('#liquid-glass-switch').click()
    assert p.locator('#liquid-glass-switch').get_attribute('aria-checked')==str(mode=='on').lower()
    p.reload();assert p.locator('html').get_attribute('data-glass')==mode
    go('/kanji/practice');p.locator('#mcq-start-btn').click();p.locator('#mcq-options button').first.wait_for()
    style=p.locator('#mcq-panel-quiz').evaluate('e=>({bg:getComputedStyle(e).backgroundColor,blur:getComputedStyle(e).backdropFilter,tint:parseFloat(getComputedStyle(e).backgroundColor.split("/")[1])})')
    assert style['bg'] not in ('transparent','rgba(0, 0, 0, 0)'),style
    if mode=='on':assert 'blur(' in style['blur'] and style['tint']>=.8,style
    else:assert style['blur']=='none' and style['tint']<=.3,style
    finish(color+' glass '+mode)
  p.evaluate('document.documentElement.dataset.glassQuality="lite";window.KotobaLiquidGlass.apply(true)')
  lite=p.locator('#mcq-panel-quiz').evaluate('e=>({blur:getComputedStyle(e).backdropFilter,bg:getComputedStyle(e).backgroundColor})')
  assert lite['blur']=='none' and '/' not in lite['bg'],lite
  finish('reduced transparency fallback')
  # The expanded map escapes all frosted ancestors; controls cannot be occluded.
  go('/japan');wrap=p.locator('#japan-map-wrap');original=wrap.evaluate('e=>e.parentElement.className')
  p.locator('#japan-map-expand').click();p.wait_for_timeout(60)
  assert wrap.evaluate('e=>e.parentElement===document.body')
  rect=wrap.bounding_box();assert rect['x']==0 and rect['y']==0 and abs(rect['width']-320)<1 and abs(rect['height']-844)<1,rect
  def zoom():return float(p.locator('#japan-map').get_attribute('data-zoom'))
  def reachable(selector):
   assert p.locator(selector).evaluate('e=>{const r=e.getBoundingClientRect();return e.contains(document.elementFromPoint(r.x+r.width/2,r.y+r.height/2))}'),selector
  reachable('#japan-zoom-in');z=zoom();p.locator('#japan-zoom-in').click();assert zoom()>z
  z=zoom();p.locator('#japan-zoom-out').click();assert zoom()<z
  p.locator('#japan-map').focus();p.keyboard.press('+');assert zoom()>1
  old=p.locator('#japan-map').get_attribute('viewBox');p.keyboard.press('ArrowRight');assert old!=p.locator('#japan-map').get_attribute('viewBox')
  p.locator('#japan-map-labels').click();assert wrap.evaluate('e=>e.classList.contains("hide-place-names")')
  p.locator('#japan-map-labels').click();assert p.locator('#japan-map-labels').get_attribute('aria-pressed')=='true'
  p.mouse.move(160,400);z=zoom();p.mouse.wheel(0,-100);p.wait_for_timeout(100);assert zoom()>z
  old=p.locator('#japan-map').get_attribute('viewBox');p.mouse.move(160,400);p.mouse.down();p.mouse.move(120,360,steps=5);p.mouse.up();p.wait_for_timeout(70);assert old!=p.locator('#japan-map').get_attribute('viewBox')
  # Real touch events exercise the mobile pinch camera in Chromium.
  p.locator('#japan-map-reset').click()
  cdp=p.context.new_cdp_session(p)
  def touch(kind,points):cdp.send('Input.dispatchTouchEvent',{'type':kind,'touchPoints':[{'x':x,'y':y,'id':i} for i,x,y in points]})
  touch('touchStart',[(1,130,400),(2,190,400)]);touch('touchMove',[(1,90,400),(2,230,400)]);touch('touchEnd',[]);p.wait_for_timeout(100);assert zoom()>1.5
  p.keyboard.press('Escape');assert not wrap.evaluate('e=>e.classList.contains("is-expanded")');assert wrap.evaluate('e=>e.parentElement.className')==original
  assert not p.locator('.site-main').evaluate('e=>e.inert')
  p.locator('#japan-map-expand').click();assert p.evaluate('window.KotobaNavigation.handleBack()');assert not wrap.evaluate('e=>e.classList.contains("is-expanded")')
  p.locator('#japan-map-expand').click();p.locator('#japan-map-reset').click();p.wait_for_timeout(400)
  p.locator('.jp-map-pin[data-place="tokyo"]').dispatch_event('click')
  assert p.locator('#japan-drawer').evaluate('e=>e.classList.contains("open")');assert not wrap.evaluate('e=>e.classList.contains("is-expanded")')
  report['map']={'viewport':rect,'zoom_buttons':True,'keyboard':True,'wheel':True,'pan':True,'selection':True,'restore':True,'labels':True,'touch_pinch':True,'native_back':True}
  browser.close()
 out=ROOT/'verification';out.mkdir(exist_ok=True);(out/'browser76.json').write_text(json.dumps(report,indent=2))
 issues=[x for x in report['pages'] if x['issues']]
 assert not issues,issues
 assert not report['errors'],report['errors']
 print('PASS',len(report['pages']),'rendered pages;',len(report['states']),'learning/layout states; glass and expanded map')

def main():
 if os.environ.get('KOTOBA_BASE_URL'):return run(os.environ['KOTOBA_BASE_URL'])
 import socket
 with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
 base='http://127.0.0.1:'+str(port);env=os.environ.copy()
 with tempfile.TemporaryDirectory(prefix='kotoba-ui76-') as data:
  env['KOTOBA_DATA_DIR']=data
  server=subprocess.Popen([sys.executable,'-m','flask','--app','app','run','--host','127.0.0.1','--port',str(port)],cwd=ROOT,env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  try:
   opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
   for n in range(200):
    try:opener.open(base,timeout=1);break
    except Exception:time.sleep(.1)
   run(base)
  finally:server.terminate();server.wait()
if __name__=='__main__':main()

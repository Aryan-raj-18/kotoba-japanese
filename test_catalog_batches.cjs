// Full catalog behavior with bounded initial DOM; simulated browser only.
const {JSDOM}=require('jsdom'),{spawnSync}=require('node:child_process'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const pkg=process.env.KOTOBA_TEST_PACKAGE,assets=pkg?path.join(pkg,'kotoba_app'):__dirname;
const code=(pkg?'import sys;sys.path.insert(0,'+JSON.stringify(pkg)+');from kotoba_app.app import app':'from app import app')+';import json;c=app.test_client();print(json.dumps({r:c.get(r).data.decode() for r in ["/kanji","/everyday"]}))';const r=spawnSync(process.env.KOTOBA_TEST_PYTHON||'python',['-c',code],{cwd:__dirname,encoding:'utf8',maxBuffer:10*1024*1024});assert.equal(r.status,0,r.stderr);const pages=JSON.parse(r.stdout);let checks=0;const check=(name,f)=>{f();checks++;console.log('PASS '+name);};const read=n=>fs.readFileSync(path.join(assets,'static/js',n),'utf8');const settle=()=>new Promise(r=>setImmediate(r));
async function setup(route){const dom=new JSDOM(pages[route.split('?')[0]],{url:'http://localhost'+route,runScripts:'outside-only',pretendToBeVisual:true});await settle();const w=dom.window,d=w.document;w.scrollTo=()=>{};w.Element.prototype.scrollIntoView=function(){};w.eval(read('search-match.js'));return{w,d};}
(async()=>{
 let t=await setup('/kanji');t.w.eval(read('kanji_list.js'));t.d.dispatchEvent(new t.w.Event('DOMContentLoaded'));const entries=JSON.parse(t.d.getElementById('kanji-catalog').textContent);
 check('Kanji first view is bounded while all original characters remain searchable',()=>{assert(entries.length>=2103);assert.equal(t.d.querySelectorAll('.kanji-card').length,96);});
 while(!t.d.getElementById('kanji-more').hidden)t.d.getElementById('kanji-more').click();check('Show more reaches every kanji once without losing earlier cards',()=>{const ids=[...t.d.querySelectorAll('.kanji-card')].map(c=>c.dataset.kanjiId);assert.equal(ids.length,entries.length);assert.equal(new Set(ids).size,entries.length);});
 const last=entries.at(-1);t.d.getElementById('kanji-filter').value=last[1];t.d.getElementById('kanji-filter').dispatchEvent(new t.w.Event('input'));check('search reaches characters beyond the initial batch',()=>assert([...t.d.querySelectorAll('.kanji-card')].some(c=>c.dataset.kanjiId===String(last[0]))));
 t.d.getElementById('kanji-filter').value='';t.d.querySelector('[data-kanji-level="N4"]').click();check('level changes retain correct links and complete N4 count',()=>{assert.equal(t.d.querySelectorAll('.kanji-card').length,96);assert.match(t.d.getElementById('kanji-visible-count').textContent,/174/);assert([...t.d.querySelectorAll('.kanji-card')].every(c=>new URL(c.href).searchParams.get('level')==='N4'));});t.w.close();
 t=await setup('/kanji?at='+last[0]);t.w.eval(read('kanji_list.js'));t.d.dispatchEvent(new t.w.Event('DOMContentLoaded'));await new Promise(r=>t.w.requestAnimationFrame(r));check('returning to a later character renders it before focus restoration',()=>assert.equal(t.d.activeElement.dataset.kanjiId,String(last[0])));t.w.close();
 t=await setup('/everyday');let requests=[];t.w.fetch=async u=>{requests.push(u);return{ok:true,json:async()=>({word:'最後',meaning:'last',reading:'さいご',romaji:'saigo',category:'Test',conversation:[]})}};t.w.eval(read('everyday.js'));t.d.dispatchEvent(new t.w.Event('DOMContentLoaded'));const words=JSON.parse(t.d.getElementById('everyday-catalog').textContent);
 const cats=[...new Set(words.map(w=>w[1]))];
 check('Everyday overview shows every category (a preview of each) and keeps the entire public list',()=>{assert(words.length>3700);assert.equal(t.d.querySelectorAll('.category-block').length,cats.length);assert(t.d.querySelectorAll('.everyday-row').length<=cats.length*12);assert(t.d.getElementById('everyday-more').hidden);});
 const firstBlock=t.d.querySelector('.category-block'),firstCat=firstBlock.dataset.cat,catTotal=words.filter(w=>w[1]===firstCat).length;
 check('Each category can be expanded to show all of its words',()=>{assert(catTotal>12);t.d.querySelector('.category-more').click();assert.equal(t.d.querySelector('.category-block[data-cat=\"'+firstCat.replace(/"/g,'\\"')+'\"]').querySelectorAll('.everyday-row').length,catTotal);});
 const tab=[...t.d.querySelectorAll('.cat-tab')].find(b=>b.dataset.cat===firstCat);tab.click();
 check('Choosing a category lists its words in batches without replacing existing buttons',()=>{const n=t.d.querySelectorAll('.everyday-row').length;assert.equal(n,Math.min(96,catTotal));if(catTotal>96){const first=t.d.querySelector('.everyday-row');t.d.getElementById('everyday-more').click();assert.equal(t.d.querySelector('.everyday-row'),first);assert.equal(t.d.querySelectorAll('.everyday-row').length,Math.min(192,catTotal));}});
 t.d.querySelector('.cat-tab[data-cat=\"all\"]').click();
 // The Everyday inline search/microphone were deliberately removed from the UI.
 // Test the supported category -> Show more flow instead of targeting a deleted input.
 const word=words.at(-1);
 check('Everyday has no section-specific search field or microphone',()=>{
   assert.equal(t.d.getElementById('everyday-filter'),null);
   assert.equal(t.d.querySelector('#everyday-list .voice-search-trigger'),null);
 });
 const lastTab=[...t.d.querySelectorAll('.cat-tab')].find(b=>b.dataset.cat===word[1]);
 assert(lastTab,'The last word must have an accessible category tab');lastTab.click();
 let loads=0;
 while(!t.d.getElementById('everyday-more').hidden && loads++ < 100) t.d.getElementById('everyday-more').click();
 check('category paging reaches the last word and opens the exact original entry',()=>{
   assert(loads<100,'Pagination must finish');
   const row=[...t.d.querySelectorAll('.everyday-row')].find(c=>c.dataset.idx===String(word[0]));
   assert(row,'The last word must remain reachable without an inline search');
   row.click();
   assert.equal(requests.at(-1),'/api/everyday/'+word[0]);
 });
 await settle();t.d.getElementById('modal-close').click();check('closing a word keeps its modal hidden',()=>assert(t.d.getElementById('word-modal').hidden));t.w.close();
 t=await setup('/everyday?entry='+word[0]);requests=[];t.w.fetch=async u=>{requests.push(u);return{ok:true,json:async()=>({word:'最後',category:'Test',conversation:[]})}};t.w.eval(read('everyday.js'));t.d.dispatchEvent(new t.w.Event('DOMContentLoaded'));await settle();check('global-search deep links open words outside the initial DOM',()=>{assert.equal(requests[0],'/api/everyday/'+word[0]);assert(!t.d.getElementById('word-modal').hidden);});t.w.close();
 console.log('All '+checks+' catalog batch interaction checks passed.');
})().catch(e=>{console.error(e);process.exitCode=1;});

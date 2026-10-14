document.addEventListener('DOMContentLoaded', () => {
  const filterInput = document.getElementById('everyday-filter');
  const tabs = document.querySelectorAll('.cat-tab');
  const entries=JSON.parse(document.getElementById('everyday-catalog').textContent),list=document.getElementById('everyday-list'),more=document.getElementById('everyday-more'),renderCount=document.getElementById('everyday-render-count');
  // "All" with no search shows EVERY category at once (a short preview of each, with a
  // per-category "Show all" button) so no category is hidden behind the first one.
  // A chosen category or a search shows its matches in batches with "Show more words".
  const PREVIEW=12,BATCH=96;
  let activeCat='all',limit=BATCH,filtered=entries,overview=true;const catLimit=new Map();
  function makeRow(e){const row=document.createElement('button');row.type='button';row.className='everyday-row';row.dataset.idx=e[0];row.dataset.search=e[7];
    for(const[cls,text]of [['everyday-emoji',e[2]],['everyday-word',e[3]],['everyday-reading',e[4]],['everyday-romaji',e[5]],['everyday-meaning',e[6]]]){const span=document.createElement('span');span.className=cls;span.textContent=text;row.append(span);}return row;}
  function render(){
    list.replaceChildren();
    const groups=new Map();filtered.forEach(e=>{if(!groups.has(e[1]))groups.set(e[1],[]);groups.get(e[1]).push(e);});
    let shown=0,budget=limit;
    groups.forEach((rows,cat)=>{
      let take;
      if(overview)take=Math.min(rows.length,catLimit.get(cat)||PREVIEW);
      else{take=Math.min(rows.length,budget);budget-=take;}
      if(take<=0)return;
      const block=document.createElement('section');block.className='category-block';block.dataset.cat=cat;
      const h=document.createElement('h2');h.className='category-heading';h.textContent=cat+' ('+rows.length+')';
      const table=document.createElement('div');table.className='everyday-table';
      rows.slice(0,take).forEach(e=>table.append(makeRow(e)));
      block.append(h,table);
      if(overview&&take<rows.length){const b=document.createElement('button');b.type='button';b.className='btn-ghost category-more';b.textContent='Show all '+rows.length+' in '+cat;b.addEventListener('click',()=>{catLimit.set(cat,rows.length);const y=window.scrollY;render();window.scrollTo(0,y);});block.append(b);}
      list.append(block);shown+=take;
    });
    more.hidden=overview||shown>=filtered.length;
    renderCount.textContent=filtered.length?(overview?'Showing '+shown+' of '+filtered.length+' words across '+groups.size+' categories':'Showing '+shown+' of '+filtered.length+' matching words'):'No words match this filter.';}
  // "Show more words" appends to the existing list (keeps earlier buttons and focus in place).
  function appendBatch(){
    const start=list.querySelectorAll('.everyday-row').length;limit+=BATCH;
    const counts=new Map();filtered.forEach(e=>counts.set(e[1],(counts.get(e[1])||0)+1));
    filtered.slice(start,limit).forEach(e=>{
      let block=[...list.children].find(b=>b.dataset&&b.dataset.cat===e[1]);
      if(!block){block=document.createElement('section');block.className='category-block';block.dataset.cat=e[1];
        const h=document.createElement('h2');h.className='category-heading';h.textContent=e[1]+' ('+counts.get(e[1])+')';
        const table=document.createElement('div');table.className='everyday-table';block.append(h,table);list.append(block);}
      block.querySelector('.everyday-table').append(makeRow(e));});
    const shown=list.querySelectorAll('.everyday-row').length;more.hidden=shown>=filtered.length;
    renderCount.textContent='Showing '+shown+' of '+filtered.length+' matching words';}
  function applyFilters(){const q=(filterInput?.value||'').trim();filtered=entries.filter(e=>(activeCat==='all'||e[1]===activeCat)&&(!q||KotobaSearchMatch.matches(e[7],q)));overview=activeCat==='all'&&!q;limit=BATCH;catLimit.clear();render();}
  tabs.forEach(tab=>tab.addEventListener('click',()=>{tabs.forEach(t=>t.classList.remove('active'));tab.classList.add('active');activeCat=tab.dataset.cat;applyFilters();}));
  if(filterInput)filterInput.addEventListener('input',applyFilters);more.addEventListener('click',appendBatch);
  applyFilters();

  // ---------------- word detail modal ----------------
  const modal = document.getElementById('word-modal');
  const convoEl = document.getElementById('modal-convo');

  function setText(id, value) {
    document.getElementById(id).textContent = value || '';
  }

  function renderModal(entry) {
    setText('modal-emoji', entry.emoji);
    setText('modal-word', entry.word);
    setText('modal-reading', `${entry.reading}  ·  ${entry.romaji}`);
    setText('modal-meaning', entry.meaning);
    const rank = entry.frequency_rank ? ` · Common #${entry.frequency_rank}` : '';
    const diff = entry.difficulty ? ` · ${entry.difficulty[0].toUpperCase() + entry.difficulty.slice(1)}` : '';
    setText('modal-category', `${entry.category}${diff}${rank}`);
    setText('modal-usage', entry.usage_note);
    const speakBtn = document.getElementById('modal-speak');
    if (speakBtn) speakBtn.onclick = () => window.KotobaSpeech && KotobaSpeech.speakReading(entry.word,entry.reading);
    const favBtn = document.getElementById('modal-favorite');
    if (favBtn) {
      favBtn.onclick = async () => {
        if (!window.KotobaLearn) return;
        const r = await KotobaLearn.favorite({kind:'vocab', id:entry.word, front:entry.word, reading:entry.reading || entry.romaji || '', meaning:entry.meaning, url:'/everyday'});
        if (r) { favBtn.textContent = r.added ? '★ Saved' : '☆ Save'; KotobaLearn.toast(r.added ? 'Saved to Favorites' : 'Removed from Favorites'); }
      };
    }

    convoEl.innerHTML = '';
    (entry.conversation || []).forEach(line => {
      const wrap = document.createElement('div');
      wrap.className = 'convo-line convo-' + line.speaker.toLowerCase();

      const who = document.createElement('span');
      who.className = 'convo-speaker';
      who.textContent = line.speaker;
      wrap.appendChild(who);

      const body = document.createElement('div');
      body.className = 'convo-body';
      [
        ['convo-kanji', line.kanji],
        ['convo-hiragana', line.hiragana],
        ['convo-romaji', line.romaji],
        ['convo-english', line.english],
      ].forEach(([cls, text]) => {
        const p = document.createElement('p');
        p.className = cls;
        p.textContent = text;
        body.appendChild(p);
      });
      const listen = document.createElement('button'); listen.type='button'; listen.className='line-speak'; listen.textContent='🔊'; listen.setAttribute('aria-label','Listen'); listen.onclick=()=>window.KotobaSpeech&&KotobaSpeech.speakReading(line.kanji,line.hiragana); body.appendChild(listen);
      wrap.appendChild(body);
      convoEl.appendChild(wrap);
    });
  }

  function closeModal() {
    requestId++;
    if(window.KotobaSpeech)KotobaSpeech.stop();
    modal.hidden = true;
    modal.classList.remove('is-open');
    modal.setAttribute('aria-hidden','true');
    if (returnFocus && returnFocus.isConnected) returnFocus.focus({preventScroll:true});
    returnFocus=null;
    document.body.style.overflow = '';
    document.body.classList.remove('word-modal-open');
  }

  let requestId=0;
  let returnFocus=null;
  async function openEntry(idx){const token=++requestId;returnFocus=document.activeElement;modal.hidden=false;modal.classList.add('is-open');modal.setAttribute('aria-hidden','false');document.body.style.overflow='hidden';document.body.classList.add('word-modal-open');modal.scrollTop=0;document.getElementById('word-modal-card').scrollTop=0;for(const id of ['modal-emoji','modal-word','modal-reading','modal-meaning','modal-category','modal-usage'])setText(id,'');convoEl.innerHTML='<p class="convo-loading">Loading...</p>';document.getElementById('modal-close').focus({preventScroll:true});try{const res=await fetch('/api/everyday/'+idx);if(!res.ok)throw Error('bad status');const entry=await res.json();if(token===requestId&&!modal.hidden)renderModal(entry);}catch(_){if(token===requestId&&!modal.hidden)convoEl.innerHTML='<p class="convo-loading">Could not load this word.</p>';}}
  list.addEventListener('click',e=>{const row=e.target.closest('.everyday-row');if(row)openEntry(row.dataset.idx);});
  // Exact global-search results open even outside the first displayed batch.
  const entry=new URLSearchParams(location.search).get('entry');if(entry!==null&&/^\d+$/.test(entry)&&entries.some(e=>String(e[0])===entry))openEntry(entry);

  document.getElementById('modal-close').addEventListener('click', closeModal);
  modal.addEventListener('click', (e) => { if (e.target === modal) closeModal(); });
  document.addEventListener('keydown', (e) => {
    if (modal.hidden) return;
    if (e.key === 'Escape') {e.preventDefault();closeModal();return;}
    if (e.key !== 'Tab') return;
    const focusable=[...modal.querySelectorAll('button:not([disabled]),a[href],input:not([disabled])')].filter(node=>node.getClientRects().length);
    if (!focusable.length) return;
    const first=focusable[0],last=focusable[focusable.length-1];
    if (e.shiftKey && document.activeElement===first) {e.preventDefault();last.focus();}
    else if (!e.shiftKey && document.activeElement===last) {e.preventDefault();first.focus();}
  });
});

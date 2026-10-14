// Offline cache routing, without a network or browser rendering claim.
const vm=require('node:vm'),fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=process.env.KOTOBA_TEST_PACKAGE?path.join(process.env.KOTOBA_TEST_PACKAGE,'kotoba_app'):__dirname;
const script=fs.readFileSync(path.join(root,'static/sw.js'),'utf8'),
      build=(fs.readFileSync(path.join(root,'app.py'),'utf8').match(/ASSET_BUILD\s*=\s*["'](\d+)["']/)||[])[1];
assert(build,'Application must publish a cache version');
const listeners={},calls=[],cached={body:'cached CSS'};
let networkAttempts=0;
const cache={
  addAll:async paths=>{assert(paths.every(p=>p.endsWith('?v='+build)));calls.push('install');},
  // The current worker tries an exact cache hit first. Only after a
  // network error does it allow the ignoreSearch fallback for old assets.
  match:async(req,opt)=>{
    calls.push({url:req.url,ignoreSearch:!!opt?.ignoreSearch});
    if(req.url.endsWith('?v='+build)||opt?.ignoreSearch)return cached;
    return undefined;
  }
};
vm.runInNewContext(script,{
  URL,
  self:{location:{origin:'http://localhost'},addEventListener:(n,f)=>listeners[n]=f,skipWaiting(){},clients:{claim(){}}},
  fetch:async()=>{networkAttempts++;throw Error('offline');},
  caches:{open:async name=>{assert.equal(name,'kotoba-shell-v100-build'+build);return cache;}},Promise
});
(async()=>{
  let result;
  listeners.install({waitUntil:p=>result=p});await result;
  console.log('PASS shell precaches the current versioned assets');

  listeners.fetch({request:{method:'GET',url:'http://localhost/static/css/style.css?v='+build},respondWith:p=>result=p});
  assert.equal(await result,cached);
  assert.equal(networkAttempts,0,'A cached current asset should not require a network request');
  assert.equal(calls.at(-1).ignoreSearch,false);
  console.log('PASS offline versioned requests use the exact cached asset first');

  listeners.fetch({request:{method:'GET',url:'http://localhost/static/css/style.css?v=stale'},respondWith:p=>result=p});
  assert.equal(await result,cached);
  assert.equal(networkAttempts,1);
  assert.equal(calls.at(-1).ignoreSearch,true);
  console.log('PASS offline cache misses fall back by ignoring the asset version query');

  for(const url of ['http://localhost/api/backup/data','http://localhost/kanji','https://external.invalid/static/other.js'])
    listeners.fetch({request:{method:'GET',url},respondWith(){throw Error('personal or external request intercepted');}});
  console.log('PASS personal pages, APIs and external requests bypass the cache');
  console.log('All 4 browser-cache routing checks passed.');
})().catch(e=>{console.error(e);process.exitCode=1;});

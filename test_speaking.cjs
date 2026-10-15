'use strict';
const {JSDOM}=require(process.env.JSDOM_MODULE||'jsdom'),{spawnSync}=require('node:child_process'),fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const rendered=spawnSync(process.env.KOTOBA_TEST_PYTHON||'python',['-c','from app import app; print(app.test_client().get("/speaking").data.decode())'],{cwd:__dirname,encoding:'utf8'});assert.equal(rendered.status,0,rendered.stderr);
async function setup(native=false){const dom=new JSDOM(rendered.stdout,{url:'http://localhost/speaking',runScripts:'outside-only'}),w=dom.window;await new Promise(r=>setImmediate(r));const records=[],actions=[],requests=[];
 w.HTMLMediaElement.prototype.pause=function(){};
 w.fetch=async()=>({ok:true,json:async()=>({items:[{id:'one',jp:'水',reading:'みず',english:'water',source:'Test'}]})});w.KotobaLearn={record:p=>records.push(p),action:a=>actions.push(a)};w.KotobaSpeech={speak:()=>{},stop:()=>{}};
 if(native)w.KotobaVoiceRecognitionNative={startSession:(lang,token)=>requests.push({lang,token}),stop:()=>{}};
 w.eval(fs.readFileSync(path.join(__dirname,'static/js/speaking.js'),'utf8'));w.document.dispatchEvent(new w.Event('DOMContentLoaded'));w.document.getElementById('speaking-start').click();await new Promise(r=>setImmediate(r));return {dom,w,records,actions,requests,d:w.document};}
(async()=>{let t=await setup();
 // No recognition on device: self-check path still awards exactly one score.
 t.d.getElementById('speaking-mic').click();await new Promise(r=>setImmediate(r));const b=t.d.querySelector('[data-self="good"]');for(let i=0;i<5;i++)b.dispatchEvent(new t.w.Event('click'));assert.equal(t.records.length,1);assert.equal(t.actions.length,1);t.d.getElementById('speaking-next').click();assert.equal(t.d.getElementById('speaking-score').textContent,'1 strong repetitions out of 1');t.dom.window.close();console.log('PASS repeated self-check awards exactly one score');
 // Native recognition.
 t=await setup(true);const $=id=>t.d.getElementById(id);
 assert.equal($('speaking-retry'),null,'the always-visible Retry button is gone');
 assert.equal($('speaking-fail').hidden,true);assert.equal($('speaking-next').hidden,true);
 $('speaking-mic').click();let token=t.requests[0].token;
 t.w.KotobaSpeakingNative._nativeResults(JSON.stringify(['<img src=x onerror=alert(1)>']),token);
 assert.equal($('speaking-result').querySelector('img'),null);
 assert.equal(t.records.length,0,'a failed attempt is not graded yet');
 assert.equal($('speaking-fail').hidden,false,'Try again + Next appear after a bad attempt');assert.equal($('speaking-next').hidden,true);
 t.w.KotobaSpeakingNative._nativeResults(JSON.stringify(['水']),token);assert.equal(t.records.length,0,'stale token ignored');
 // Try again starts a new listening session immediately.
 $('speaking-try-again').click();assert.equal(t.requests.length,2);assert.equal($('speaking-fail').hidden,true);token=t.requests[1].token;
 t.w.KotobaSpeakingNative._nativeResults(JSON.stringify(['水']),token);
 assert.equal(t.records.length,1);assert.equal(t.records[0].correct,true);assert.equal($('speaking-next').hidden,false);assert.equal($('speaking-fail').hidden,true);
 t.w.KotobaSpeakingNative._nativeResults(JSON.stringify(['水']),token);assert.equal(t.records.length,1);
 $('speaking-next').click();assert.equal($('speaking-score').textContent,'1 strong repetitions out of 1');t.dom.window.close();console.log('PASS native: bad attempt -> Try again/Next, good attempt -> Next only');
 // Incomplete sentence + Next records a miss once.
 t=await setup(true);const q=id=>t.d.getElementById(id);q('speaking-mic').click();token=t.requests[0].token;
 t.w.KotobaSpeakingNative._nativeResults(JSON.stringify(['み']),token);assert.equal(q('speaking-fail').hidden,false);
 q('speaking-skip').click();assert.equal(t.records.length,1);assert.equal(t.records[0].correct,false);assert.equal(q('speaking-score').textContent,'0 strong repetitions out of 1');t.dom.window.close();console.log('PASS incomplete sentence can be skipped with Next');
 // Recognizer error (no speech heard) -> Try again/Next.
 t=await setup(true);const r=id=>t.d.getElementById(id);r('speaking-mic').click();token=t.requests[0].token;
 t.w.KotobaSpeakingNative._nativeError("I didn't catch that.",token);assert.equal(r('speaking-fail').hidden,false);assert.equal(r('speaking-mic').disabled,false);t.dom.window.close();console.log('PASS no-speech error offers Try again/Next');
})().catch(e=>{console.error(e);process.exitCode=1;});

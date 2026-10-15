document.addEventListener('DOMContentLoaded',()=>{
 const stage=document.getElementById('speaking-stage');if(!stage)return;
 // PASS_SCORE: how closely the recognised text must match the WHOLE sentence.
 const PASS_SCORE=80;
 let level='all',source='all',items=[],idx=0,good=0,graded=false,credited=false,generation=0,recorder=null,recognition=null,stream=null,playbackUrl=null,nativeToken=null,lastHeard='';
 const $=id=>document.getElementById(id),intro=$('speaking-intro'),run=$('speaking-run'),done=$('speaking-done');
 const show=x=>[intro,run,done].forEach(p=>p.hidden=p!==x);
 // Result rows. Only ONE of them is ever visible at a time:
 //  fail      -> "Try again" + "Next"   (sentence not spoken fully / not recognised)
 //  selfcheck -> "Try again" + "Sounded good" (device has no speech recognition)
 //  next      -> "Next"                 (sentence was spoken correctly)
 const outcomeIds=['speaking-result','speaking-fail','speaking-selfcheck','speaking-next','speaking-playback'];
 const hideOutcomes=()=>outcomeIds.forEach(id=>$(id).hidden=true);
 function cleanup(){generation++;recognition?.abort();recognition=null;if(recorder?.state==='recording')recorder.stop();recorder=null;stream?.getTracks().forEach(t=>t.stop());stream=null;try{$('speaking-playback').pause();$('speaking-playback').currentTime=0;}catch(_){}if(playbackUrl)URL.revokeObjectURL(playbackUrl);playbackUrl=null;if(nativeToken)window.KotobaVoiceRecognitionNative?.stop();nativeToken=null;$('speaking-stop').hidden=true;$('speaking-mic').disabled=graded;}
 function message(text){$('speaking-result').hidden=false;$('speaking-result').textContent=text;}
 // Not spoken properly / incomplete: offer exactly Try again + Next.
 function fail(text){if(graded)return;$('speaking-stop').hidden=true;$('speaking-mic').disabled=false;message(text);$('speaking-selfcheck').hidden=true;$('speaking-next').hidden=true;$('speaking-fail').hidden=false;}
 function selfCheck(text){if(graded)return;$('speaking-stop').hidden=true;$('speaking-mic').disabled=false;message(text);$('speaking-fail').hidden=true;$('speaking-selfcheck').hidden=false;}
 document.querySelectorAll('#speaking-levels [data-level]').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('#speaking-levels [data-level]').forEach(x=>x.classList.remove('active'));b.classList.add('active');level=b.dataset.level;}));
 document.querySelectorAll('#speaking-sources [data-source]').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('#speaking-sources [data-source]').forEach(x=>x.classList.remove('active'));b.classList.add('active');source=b.dataset.source;$('speaking-situations').hidden=source!=='phrasebook';if(source!=='phrasebook')$('speaking-category').value='all';}));
 async function start(){cleanup();try{const r=await fetch(`/api/speaking_items?level=${encodeURIComponent(level)}&source=${encodeURIComponent(source)}&category=${encodeURIComponent(source==='phrasebook'?$('speaking-category').value:'all')}&count=15`);if(!r.ok)throw new Error();const d=await r.json();items=d.items||[];idx=0;good=0;credited=false;if(!items.length){message('No reviewed speaking items in this level yet. Choose All or a starter level.');return;}show(run);render();}catch(_){message('Could not load speaking practice. Please try again.');}}
 function normalize(s){return String(s||'').normalize('NFKC').replace(/[\s。、，．,.！？!?「」『』・~〜]/g,'').toLowerCase();}
 function editRatio(a,b){a=normalize(a);b=normalize(b);if(!a&&!b)return 1;const dp=Array.from({length:b.length+1},(_,i)=>i);for(let i=1;i<=a.length;i++){let prev=dp[0];dp[0]=i;for(let j=1;j<=b.length;j++){const old=dp[j];dp[j]=Math.min(dp[j]+1,dp[j-1]+1,prev+(a[i-1]===b[j-1]?0:1));prev=old;}}return 1-dp[b.length]/Math.max(a.length,b.length,1);}
 function render(){cleanup();graded=false;credited=false;lastHeard='';const x=items[idx];$('speaking-progress').textContent=`${idx+1} / ${items.length}`;for(const [name,value]of Object.entries({source:x.source,jp:x.jp,reading:x.reading,romaji:x.romaji,en:x.english}))$('speaking-'+name).textContent=value||'';hideOutcomes();$('speaking-mic').disabled=false;document.querySelectorAll('[data-self]').forEach(b=>b.disabled=false);}
 function grade(ok,chosen,quality){if(graded||!items[idx])return;graded=true;credited=!!ok;good+=credited?1:0;const x=items[idx];window.KotobaLearn?.record({kind:'speaking',id:x.id,front:x.jp,answer:x.jp,chosen,correct:ok,quality,reading:x.reading,meaning:x.english});window.KotobaLearn?.action('speaking');$('speaking-mic').disabled=true;$('speaking-stop').hidden=true;document.querySelectorAll('[data-self]').forEach(b=>b.disabled=true);}
 function recognized(heard){
  if(graded)return;
  const x=items[idx],best=heard.map(t=>({t,s:Math.max(editRatio(t,x.jp),editRatio(t,x.reading||x.jp))})).sort((a,b)=>b.s-a.s)[0];
  if(!best||!normalize(best.t)){fail('I could not hear any words.\nTap Try again to say the whole sentence, or Next to skip it.');return;}
  lastHeard=best.t;
  const pct=Math.max(0,Math.round(best.s*100));
  if(pct>=PASS_SCORE){
   message(`Well done · ${pct}% match\nRecognized: ${best.t}\nText matching is approximate; it does not measure pronunciation accuracy.`);
   grade(true,best.t,pct>=92?5:4);$('speaking-fail').hidden=true;$('speaking-selfcheck').hidden=true;$('speaking-next').hidden=false;return;
  }
  // Heard noticeably less than the target -> the sentence was cut short.
  const target=Math.min(normalize(x.jp).length||1,normalize(x.reading||x.jp).length||1),short=normalize(best.t).length<target*.7;
  fail(`${short?'That sounded like only part of the sentence.':'That did not match the sentence closely enough.'} · ${pct}%\nRecognized: ${best.t}\nSay the whole sentence, then try again — or go to the next one.`);
 }
 window.KotobaSpeakingNative={
  _nativeStatus:(status,token)=>{if(token!==nativeToken||graded)return;if(status==='listening')message('Listening… say the whole sentence.');else if(status==='processing')message('Checking what you said…');},
  _nativePartial:(text,token)=>{if(token!==nativeToken||graded)return;message(`Listening…\n${text}`);},
  _nativeResults:(payload,token)=>{if(token!==nativeToken)return;nativeToken=null;try{recognized(JSON.parse(payload));}catch(_){fail('Could not read the recognition result.\nTap Try again or Next.');}},
  _nativeError:(text,token)=>{if(token!==nativeToken)return;nativeToken=null;
   if(/not available|permission|could not start|microphone problem/i.test(text))selfCheck(text+' You can compare aloud and self-check.');
   else fail(`${text}\nTap Try again to say the whole sentence, or Next to skip it.`);}
 };
 async function startMic(){if(graded)return;window.KotobaVoiceSearch?.stop();window.KotobaSpeech?.stop();cleanup();const ticket=generation;
  $('speaking-mic').disabled=true;$('speaking-fail').hidden=true;$('speaking-selfcheck').hidden=true;$('speaking-next').hidden=true;$('speaking-playback').hidden=true;message('Listening… say the whole sentence.');
  if(window.KotobaVoiceRecognitionNative){nativeToken='speaking:'+ticket+':'+Date.now();$('speaking-stop').hidden=false;window.KotobaVoiceRecognitionNative.startSession('ja-JP',nativeToken);return;}
  const Rec=window.SpeechRecognition||window.webkitSpeechRecognition;
  if(Rec){try{
   let got=false,failed=false;recognition=new Rec();recognition.lang='ja-JP';recognition.maxAlternatives=3;
   recognition.onresult=e=>{if(ticket!==generation)return;got=true;recognized(Array.from(e.results[0],a=>a.transcript));};
   recognition.onnomatch=()=>{if(ticket!==generation||got)return;got=true;fail('I could not make that out.\nTap Try again to say the whole sentence, or Next to skip it.');};
   recognition.onerror=e=>{if(ticket!==generation||got||failed)return;failed=true;if(e&&(e.error==='no-speech'||e.error==='aborted'))fail('I did not hear anything.\nTap Try again to say the whole sentence, or Next to skip it.');else fallback(ticket);};
   recognition.onend=()=>{if(ticket!==generation||got||failed)return;failed=true;fail('I did not hear anything.\nTap Try again to say the whole sentence, or Next to skip it.');};
   recognition.start();$('speaking-stop').hidden=false;return;
  }catch(_){}}
  fallback(ticket);
 }
 async function fallback(ticket){try{const acquired=await navigator.mediaDevices.getUserMedia({audio:true});if(ticket!==generation){acquired.getTracks().forEach(t=>t.stop());return;}stream=acquired;const chunks=[];recorder=new MediaRecorder(stream);const current=recorder;recorder.ondataavailable=e=>{if(e.data.size)chunks.push(e.data);};recorder.onstop=()=>{acquired.getTracks().forEach(t=>t.stop());if(ticket!==generation)return;playbackUrl=URL.createObjectURL(new Blob(chunks,{type:current.mimeType||'audio/webm'}));$('speaking-playback').src=playbackUrl;$('speaking-playback').hidden=false;message('Listen to your recording and compare it with the target.');$('speaking-selfcheck').hidden=false;$('speaking-stop').hidden=true;};recorder.start();$('speaking-stop').hidden=false;message('Recording… say the whole sentence, then tap Stop.');}catch(_){if(ticket!==generation)return;selfCheck('Microphone is unavailable. Listen, repeat aloud, then self-check.');}}
 // "Try again": clear the previous attempt and listen again straight away.
 function retry(){if(!items[idx]||graded)return;cleanup();credited=false;lastHeard='';hideOutcomes();const playback=$('speaking-playback');playback.removeAttribute('src');$('speaking-mic').disabled=false;document.querySelectorAll('[data-self]').forEach(b=>b.disabled=false);startMic();}
 function advance(){cleanup();idx++;if(idx<items.length)render();else{show(done);$('speaking-score').textContent=`${good} strong repetitions out of ${items.length}`;window.Sfx?.complete();}}
 // "Next" after a failed attempt: skip, counted as not yet mastered.
 function skip(){if(!items[idx])return;if(!graded)grade(false,lastHeard||'Skipped',1);advance();}
 $('speaking-try-again').onclick=retry;
 $('speaking-skip').onclick=skip;
 $('speaking-listen').onclick=()=>{cleanup();if(!graded)$('speaking-mic').disabled=false;window.KotobaSpeech?.speakReading(items[idx].jp,items[idx].reading,.82);};
 $('speaking-mic').onclick=startMic;
 $('speaking-stop').onclick=()=>{if(recorder?.state==='recording'){recorder.stop();return;}if(recognition){try{recognition.stop();}catch(_){}return;}if(nativeToken)try{window.KotobaVoiceRecognitionNative?.finish?.();}catch(_){}};
 document.querySelectorAll('[data-self]').forEach(b=>b.addEventListener('click',()=>{if(b.dataset.self==='retry'){retry();return;}grade(true,'Self-check: good',4);$('speaking-selfcheck').hidden=true;$('speaking-next').hidden=false;}));
 $('speaking-next').onclick=()=>{if(!graded)return;advance();};
 $('speaking-start').onclick=start;$('speaking-again').onclick=()=>{window.KotobaSpeech?.stop();cleanup();show(intro);};window.addEventListener('pagehide',cleanup);
 window.addEventListener('kotoba-audio-before-play',cleanup);
 window.addEventListener('kotoba-voice-search-start',()=>{cleanup();if(!graded)$('speaking-mic').disabled=false;});
 document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='hidden')cleanup();});
});

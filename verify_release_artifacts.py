"""Verify signed APK/AAB identity, alignment and the actual packaged Python/assets.
Runs in CI with Python matching Chaquopy and Android SDK build-tools installed.
"""
import hashlib,io,json,marshal,os,re,shutil,struct,subprocess,types,zipfile,xml.etree.ElementTree as ET
from pathlib import Path
from verify_play_bundle import load_alignments
root=Path(__file__).resolve().parent;out=root/'verification';out.mkdir(exist_ok=True)
gradle=(root/'android/app/build.gradle').read_text();version=int(re.search(r'versionCode\s+(\d+)',gradle)[1]);name=re.search(r"versionName '([^']+)'",gradle)[1]
sdk=Path(os.environ.get('ANDROID_HOME',os.environ.get('ANDROID_SDK_ROOT','')))/'build-tools/36.0.0'
def run(label,args):
 p=subprocess.run([str(a) for a in args],capture_output=True,text=True)
 (out/(label+'.log')).write_text(p.stdout+p.stderr);assert p.returncode==0,(label,p.returncode,p.stderr[-2000:])
 return p.stdout+p.stderr
apk=root/'android/app/build/outputs/apk/release/app-release.apk';aab=root/'android/app/build/outputs/bundle/release/app-release.aab'
signature=run('apk-signature',[sdk/'apksigner','verify','--verbose','--print-certs',apk])
cert=re.search(r'certificate SHA-256 digest:\s*([a-fA-F0-9]+)',signature)[1].upper()
aab_cert=run('aab-certificate',['keytool','-printcert','-jarfile',aab]).replace(':','').upper();assert cert in aab_cert,'APK/AAB signing certificates differ'
assert 'ANDROID DEBUG' not in aab_cert,'Release must not use Android debug key'
badging=run('apk-version',[sdk/'aapt','dump','badging',apk]);assert f"versionCode='{version}'" in badging and f"versionName='{name}'" in badging
application_id = 'com.kotoba_japanese.app'
assert f"applicationId '{application_id}'" in gradle
assert f"package: name='{application_id}'" in badging
run('zip-alignment',[sdk/'zipalign','-c','-P','16','4',apk])
assert 'jar verified' in run('aab-signature',['jarsigner','-verify',aab])
bundletool=Path(os.environ['KOTOBA_BUNDLETOOL'])
run('bundle-validation',['java','-jar',bundletool,'validate','--bundle='+str(aab)])
config=run('bundle-config',['java','-jar',bundletool,'dump','config','--bundle='+str(aab)]);assert 'PAGE_ALIGNMENT_16K' in config
manifest=run('bundle-manifest',['java','-jar',bundletool,'dump','manifest','--bundle='+str(aab),'--module=base'])
assert f'android:versionCode="{version}"' in manifest and f'android:versionName="{name}"' in manifest
ns = '{http://schemas.android.com/apk/res/android}'
manifest_xml = ET.fromstring(manifest)
assert manifest_xml.attrib['package'] == application_id
application = manifest_xml.find('application')
assert application is not None
components = {e.attrib.get(ns+'name') for e in application if e.tag in ('activity', 'receiver')}
for component in ('MainActivity','ReminderAlarmReceiver','KanjiNotificationReceiver','ReminderBootReceiver'):
 assert 'com.kotoba.app.'+component in components, (component, components)
authorities = [e.attrib[ns+'authorities'] for e in application.findall('provider')]
assert application_id+'.androidx-startup' in authorities, authorities
assert all(a.startswith(application_id+'.') for a in authorities), authorities
assert 'com.kotoba.app.androidx-startup' not in authorities
metadata={'application_id':application_id,'provider_authorities':authorities,'android_components':sorted(components),'version':name,'version_code':version,'certificate_sha256':cert,'artifacts':{}};payloads=[];dexes=[]
for file,prefix in [(apk,''),(aab,'base/')]:
 info={'bytes':file.stat().st_size,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()};libs=[]
 with zipfile.ZipFile(file) as z:
  assert z.testzip() is None
  dexes.append({Path(n).name:z.read(n) for n in z.namelist() if n.endswith('.dex')})
  assert any(b'KotobaKanjiNotificationNative' in content for content in dexes[-1].values())
  payloads.append(z.read(prefix+'assets/chaquopy/app.imy'))
  for asset in ('kotoba-opening.html','kanji-notification.json'):
   assert z.read(prefix+'assets/'+asset)==(root/'android/app/src/main/assets'/asset).read_bytes(),asset
  for entry in z.namelist():
   if entry.endswith('.so'):
    align=load_alignments(z.read(entry));assert align and min(align)>=16384,(entry,align)
    libs.append({'name':entry,'minimum_PT_LOAD_alignment':min(align)})
 info['native_libraries']=libs;metadata['artifacts'][file.suffix]=info
assert payloads[0]==payloads[1];metadata['APK_AAB_payload_identical']=True
assert dexes[0]==dexes[1];metadata['APK_AAB_Dex_identical']=True
package=root/'android/app/src/main/python';asset_count=0;python_count=0
def equal_code(a,b):
 for key in ('co_code','co_names','co_varnames','co_freevars','co_cellvars','co_argcount','co_kwonlyargcount','co_posonlyargcount','co_flags'):assert getattr(a,key)==getattr(b,key),key
 assert len(a.co_consts)==len(b.co_consts)
 for x,y in zip(a.co_consts,b.co_consts):
  if isinstance(x,types.CodeType):assert isinstance(y,types.CodeType);equal_code(x,y)
  else:assert x==y
with zipfile.ZipFile(io.BytesIO(payloads[1])) as z:
 for f in package.rglob('*'):
  if not f.is_file() or '__pycache__' in f.parts:continue
  entry=f.relative_to(package).as_posix()
  if f.suffix=='.py':
   code=marshal.loads(z.read(entry+'c')[16:]);equal_code(code,compile(f.read_text(),code.co_filename,'exec'));python_count+=1
  else:assert z.read(entry)==f.read_bytes(),entry;asset_count+=1
 actual=out/'actual-package'
 if actual.exists():shutil.rmtree(actual)
 actual.mkdir();z.extractall(actual)
 assert not any('/login' in n or '/signup' in n for n in z.namelist() if '/templates/' in n)
 for f in actual.rglob('*.py'):f.unlink()
metadata.update(packaged_asset_matches=asset_count,compiled_modules_match=python_count,actual_package=str(actual))
public=json.loads((root/'release-content-hashes.json').read_text())
for path,digest in public.items():assert hashlib.sha256((root/path).read_bytes()).hexdigest()==digest,path
metadata['original_course_files_unchanged']=len(public)
(out/'artifact-verification.json').write_text(json.dumps(metadata,indent=2)+'\n')
print(f'PASS signed Build {version} ({name}), APK/AAB identity, 16 KB alignment, {asset_count} assets, {python_count} compiled modules, {len(public)} unchanged course files')

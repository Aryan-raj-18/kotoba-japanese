"""Verify bundled font coverage against the actual, unchanged course content."""
import json,re,unittest
from pathlib import Path
from fontTools.ttLib import TTFont
ROOT=Path(__file__).resolve().parent
class StudyFontCoverage76(unittest.TestCase):
 def test_actual_japanese_and_quiz_blank_have_glyphs(self):
  chars={ord('＿')}
  def strings(value):
   if isinstance(value,str):yield value
   elif isinstance(value,list):
    for item in value:yield from strings(item)
   elif isinstance(value,dict):
    for item in value.values():yield from strings(item)
  for file in (ROOT/'data').glob('*.json'):
   for value in strings(json.loads(file.read_text())):
    chars.update(map(ord,re.findall(r'[\u3040-\u30ff\u3400-\u9fff\uf900-\ufaff]',value)))
  available=set()
  for name in ('kotoba-mincho.woff2','kotoba-cjk-fallback.woff2','kotoba-rounded.woff2'):
   with TTFont(ROOT/'static/fonts'/name) as font:available.update(font.getBestCmap())
  self.assertFalse(chars-available,'Missing study glyphs: '+''.join(map(chr,sorted(chars-available))))
 def test_offline_fallback_is_registered_and_cached(self):
  css=(ROOT/'static/css/style.css').read_text();sw=(ROOT/'static/sw.js').read_text()
  self.assertIn('font-family:"Kotoba CJK Fallback"',css)
  self.assertIn('kotoba-cjk-fallback.woff2',sw)
  self.assertIn('"Kotoba Mincho", "Kotoba CJK Fallback", "Kotoba Rounded",',css)
if __name__=='__main__':unittest.main()

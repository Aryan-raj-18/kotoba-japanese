#!/usr/bin/env python3
"""Fail CI if the Play App Bundle is malformed or contains 4 KiB-aligned native ELF.

AAB alignment inspection is necessary but not sufficient: Play/bundletool must
also produce compatible APK splits. This tool does not prove Play acceptance.
"""
import hashlib
import json
import struct
import sys
import zipfile
from pathlib import Path


def load_alignments(raw):
    if not raw.startswith(b'\x7fELF'):
        return None
    end = '<' if raw[5] == 1 else '>' if raw[5] == 2 else None
    if end is None:
        raise ValueError('unknown ELF endian indicator')
    if raw[4] == 2:  # ELF64: 64-bit offsets
        header = struct.unpack_from(end + 'Q', raw, 32)[0]
        entry_size, count = struct.unpack_from(end + 'HH', raw, 54)
        fmt = end + 'IIQQQQQQ'
    elif raw[4] == 1:  # ELF32
        header = struct.unpack_from(end + 'I', raw, 28)[0]
        entry_size, count = struct.unpack_from(end + 'HH', raw, 42)
        fmt = end + 'IIIIIIII'
    else:
        raise ValueError('unsupported ELF class')
    result = []
    for n in range(count):
        fields = struct.unpack_from(fmt, raw, header + entry_size * n)
        if fields[0] == 1:  # PT_LOAD
            result.append(fields[-1])
    if not result:
        raise ValueError('native ELF has no PT_LOAD segments')
    return result


def main(path):
    bundle = Path(path)
    if not bundle.is_file() or bundle.stat().st_size < 1024:
        raise SystemExit('Missing or empty release .aab')
    report = {'bundle': bundle.name, 'bytes': bundle.stat().st_size,
              'sha256': hashlib.sha256(bundle.read_bytes()).hexdigest(), 'nativeLibraries': []}
    with zipfile.ZipFile(bundle) as z:
        corrupt = z.testzip()
        if corrupt:
            raise SystemExit('Invalid archive entry: ' + corrupt)
        if 'base/manifest/AndroidManifest.xml' not in z.namelist():
            raise SystemExit('Missing base/manifest/AndroidManifest.xml')
        for info in z.infolist():
            if not (info.filename.endswith('.so') or '/lib/' in info.filename and info.filename.endswith('.so')):
                continue
            align = load_alignments(z.read(info))
            if align is None:
                raise SystemExit('Invalid native library: ' + info.filename)
            report['nativeLibraries'].append({'name': info.filename, 'minLoadAlignment': min(align)})
            if min(align) < 16384:
                raise SystemExit(f'16 KiB page compatibility failure: {info.filename}, ELF PT_LOAD alignment {min(align)}')
    dest = Path(__file__).resolve().parent / 'verification/play-aab-verification.json'
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(report, indent=2) + '\n')
    print(f"PASS: valid release AAB; {len(report['nativeLibraries'])} native ELF libraries satisfy 16 KiB load alignment")
    print('SHA-256:', report['sha256'])
    print('Note: certificate, real APK splits, device tests and Play Console review are separate checks.')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python verify_play_bundle.py path/to/app-release.aab')
    main(sys.argv[1])

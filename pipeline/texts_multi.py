import csv, os, re, json
MD = '/mnt/user-data/outputs/тексти_2026-11-14_16.md'
md = open(MD, encoding='utf-8').read()
SEC = {'Податок': ('2026-11-14', '10:00', 'tax'), 'Tesla': ('2026-11-14', '10:00', 'tesla'), 'T-Roc': ('2026-11-14', '20:00', 'troc'),
       'ID. Tiguan': ('2026-11-15', '10:00', 'idtiguan'), 'Qashqai': ('2026-11-15', '20:00', 'qashqai'),
       'CR-V': ('2026-11-16', '10:00', 'crv'), 'XPeng': ('2026-11-16', '20:00', 'xpeng'), 'EQE': ('2026-11-16', '20:00', 'eqe')}
T = {}; sec = mk = net = None; inblock = False; buf = []
for line in md.split('\n'):
    if line.startswith('## '):
        sec = next((v for k, v in SEC.items() if k in line), None); mk = None
    elif line.startswith('### '):
        mk = 'ua' if 'УКРА' in line else 'lv'
    elif line.startswith('**') and not inblock:
        h = line.lower()
        net = 'ig' if 'instagram' in h else 'fb' if 'facebook' in h else 'th' if 'threads' in h else 'x' if h.startswith('**x') else None
    elif line.startswith('```'):
        if inblock and sec and net:
            T.setdefault(sec[2], {}).setdefault(mk, {})[net] = '\n'.join(buf).strip()
        buf = []; inblock = not inblock
    elif inblock:
        buf.append(line)
json.dump(T, open('/home/claude/day/texts.json', 'w'), ensure_ascii=False, indent=1)
for k, v in T.items():
    for m, d in v.items(): print(k, m, {n: len(t) for n, t in d.items()})

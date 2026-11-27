import csv, os
# CSV for Publer, 28-30.11.2026 (one file per network covering all three days). No final story (Viktoriia 27.11).
RAW = 'https://raw.githubusercontent.com/Toryworry/am-media/main'
OUT = '/home/claude/am-media/csv/2026-11-28_30'; os.makedirs(OUT, exist_ok=True)
DAYS = {'2026-11-28': {'ua': ['fuel', 'gt41'], 'lv': ['proto', 'gt41']},
        '2026-11-29': {'ua': ['idx', 'gt1'], 'lv': ['idx', 'gt1']},
        '2026-11-30': {'ua': ['bmw', 'su7'], 'lv': ['tyre', 'su7']}}
TIMES = ['10:00', '20:00']; ST = [('10:05', '10:06'), ('20:05', '20:06')]
T = {}  # T[date][time][mk][net]
for date in DAYS:
    md = open(f'/home/claude/am-media/pipeline/texts_{date}.md', encoding='utf-8').read()
    sec = mk = net = None; inb = False; buf = []
    for line in md.split('\n'):
        if line.startswith('## '):
            sec = next((t for t in TIMES if line[3:].startswith(t)), None); mk = None
        elif line.startswith('### '):
            mk = 'ua' if 'УКРА' in line else 'lv' if 'LATVIJA' in line else None
        elif line.startswith('**') and not inb:
            h = line.lower()
            net = 'ig' if 'instagram' in h else 'fb' if 'facebook' in h else 'th' if 'threads' in h else 'tg' if 'telegram' in h else 'x' if h.startswith('**x') else None
        elif line.startswith('```'):
            if inb and sec and mk and net: T.setdefault(date, {}).setdefault(sec, {}).setdefault(mk, {})[net] = '\n'.join(buf).strip()
            buf = []; inb = not inb
        elif inb: buf.append(line)
HEADER = ["Date", "Text", "Link(s)", "Media URL(s)", "Title", "Label(s)", "Alt text(s)", "Comment(s)", "Pin board, FB album, or Google category", "Post subtype", "CTA", "Reminder"]
def row(date, time, text, media, sub=''):
    r = [''] * 12; r[0] = f"{date.replace('-', '/')} {time}"; r[1] = text; r[3] = ','.join(media); r[5] = 'автоновини'; r[9] = sub; return r
FILES = {'UA_1_instagram.csv': ('ua', 'ig', True, 2200), 'UA_2_facebook.csv': ('ua', 'fb', False, 60000), 'UA_3_threads.csv': ('ua', 'th', False, 500),
         'UA_4_telegram.csv': ('ua', 'tg', False, 4096), 'UA_5_x.csv': ('ua', 'x', False, 280),
         'LV_1_instagram.csv': ('lv', 'ig', True, 2200), 'LV_2_facebook.csv': ('lv', 'fb', False, 60000), 'LV_3_x.csv': ('lv', 'x', False, 280)}
prob = []
for fn, (mk, net, stories, lim) in FILES.items():
    with open(f'{OUT}/{fn}', 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f); w.writerow(HEADER)
        for date, per in DAYS.items():
            for i, k in enumerate(per[mk]):
                text = T[date][TIMES[i]][mk][net]
                if len(text) > lim: prob.append((fn, date, k, len(text)))
                w.writerow(row(date, TIMES[i], text, [f'{RAW}/{date}/{mk}/{k}_{j}.jpg' for j in range(1, 5)]))
                if stories:
                    for s, j in zip(ST[i], (1, 2)): w.writerow(row(date, s, '', [f'{RAW}/{date}/{mk}/{k}_story{j}.jpg'], 'story'))
print('PROBLEMS', prob)
for d in T:
    for t in T[d]: print(d, t, {m: {n: len(x) for n, x in v.items()} for m, v in T[d][t].items()})

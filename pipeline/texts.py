import csv, os, re, sys
DATE = '2026-11-12'; D = DATE.replace('-', '/')
RAW = f'https://raw.githubusercontent.com/Toryworry/am-media/main/{DATE}'
OUT = f'/home/claude/am-media/csv/{DATE}'; os.makedirs(OUT, exist_ok=True)
md = open('/mnt/user-data/outputs/тексти_2026-11-12.md', encoding='utf-8').read()

# parse: section -> market -> network -> text
T = {}; sec = mk = net = None; inblock = False; buf = []
for line in md.split('\n'):
    if line.startswith('## '):
        sec = 'pajero' if 'Pajero' in line else 'ua_an' if 'UA' in line else 'lv_fuel' if 'LV' in line else None
        mk = 'ua' if sec == 'ua_an' else 'lv' if sec == 'lv_fuel' else None
    elif line.startswith('### '):
        mk = 'ua' if 'УКРА' in line else 'lv'
    elif line.startswith('**') and not inblock:
        h = line.lower()
        net = 'ig' if 'instagram' in h else 'fb' if 'facebook' in h else 'th' if 'threads' in h else 'x' if h.startswith('**x') else None
    elif line.startswith('```'):
        if inblock:
            T.setdefault(sec, {}).setdefault(mk, {})[net] = '\n'.join(buf).strip(); buf = []
        inblock = not inblock
    elif inblock:
        buf.append(line)

TIME = {'pajero': '10:00', 'ua_an': '20:00', 'lv_fuel': '20:00'}
STORY_T = {'pajero': ('10:05', '10:06'), 'ua_an': ('20:05', '20:06'), 'lv_fuel': ('20:05', '20:06')}
ORDER = {'ua': ['pajero', 'ua_an'], 'lv': ['pajero', 'lv_fuel']}
HEADER = ["Date", "Text", "Link(s)", "Media URL(s)", "Title", "Label(s)", "Alt text(s)", "Comment(s)", "Pin board, FB album, or Google category", "Post subtype", "CTA", "Reminder"]
def row(time, text, media, subtype=''):
    r = [''] * 12; r[0] = f'{D} {time}'; r[1] = text; r[3] = ','.join(media); r[5] = 'автоновини'; r[9] = subtype; return r
car = lambda mk, k: [f'{RAW}/{mk}/{k}_{i}.jpg' for i in range(1, 5)]
cov = lambda mk, k: [f'{RAW}/{mk}/{k}_1.jpg']
FILES = {
 'UA_1_instagram.csv': ('ua', 'ig', car, True, 2200), 'UA_2_facebook.csv': ('ua', 'fb', car, False, 60000),
 'UA_3_threads.csv': ('ua', 'th', cov, False, 500), 'UA_4_telegram.csv': ('ua', 'tg', cov, False, 1024),
 'UA_5_x.csv': ('ua', 'x', cov, False, 280),
 'LV_1_instagram.csv': ('lv', 'ig', car, True, 2200), 'LV_2_facebook.csv': ('lv', 'fb', car, False, 60000),
 'LV_3_x.csv': ('lv', 'x', cov, False, 280),
}
prob = []
for fn, (mk, key, media, stories, lim) in FILES.items():
    with open(f'{OUT}/{fn}', 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f); w.writerow(HEADER)
        for k in ORDER[mk]:
            t = T[k][mk]
            text = t['ig'].rsplit('\n\n#', 1)[0] if key == 'tg' else t[key]
            print(fn, k, len(text)); 
            if len(text) > lim: prob.append((fn, k, len(text)))
            w.writerow(row(TIME[k], text, media(mk, k)))
            if stories:
                for s, i in zip(STORY_T[k], (1, 2)): w.writerow(row(s, '', [f'{RAW}/{mk}/{k}_story{i}.jpg'], 'story'))
        if stories: w.writerow(row('20:10', '', [f'{RAW}/{mk}/final_story.jpg'], 'story'))
print('PROBLEMS', prob)

import csv, os, json
T = json.load(open('/home/claude/day/texts.json'))
RAW = 'https://raw.githubusercontent.com/Toryworry/am-media/main'
OUT = '/home/claude/am-media/csv/2026-11-20'; os.makedirs(OUT, exist_ok=True)
DAYS = {'2026-11-20': {'ua': ['idup', 'spyder'], 'lv': ['idup', 'spyder']}}
TIMES = ['10:00', '20:00']; ST = [('10:05', '10:06'), ('20:05', '20:06')]
HEADER = ["Date", "Text", "Link(s)", "Media URL(s)", "Title", "Label(s)", "Alt text(s)", "Comment(s)", "Pin board, FB album, or Google category", "Post subtype", "CTA", "Reminder"]
def row(date, time, text, media, sub=''):
    r = [''] * 12; r[0] = f"{date.replace('-', '/')} {time}"; r[1] = text; r[3] = ','.join(media); r[5] = 'автоновини'; r[9] = sub; return r
FILES = {'UA_1_instagram.csv': ('ua', 'ig', 4, True, 2200), 'UA_2_facebook.csv': ('ua', 'fb', 4, False, 60000), 'UA_3_threads.csv': ('ua', 'th', 1, False, 500),
         'UA_4_telegram.csv': ('ua', 'tg', 1, False, 1024), 'UA_5_x.csv': ('ua', 'x', 1, False, 280),
         'LV_1_instagram.csv': ('lv', 'ig', 4, True, 2200), 'LV_2_facebook.csv': ('lv', 'fb', 4, False, 60000), 'LV_3_x.csv': ('lv', 'x', 1, False, 280)}
prob = []
for fn, (mk, net, nimg, stories, lim) in FILES.items():
    with open(f'{OUT}/{fn}', 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f); w.writerow(HEADER)
        for date, mks in DAYS.items():
            for i, k in enumerate(mks[mk]):
                text = T[k][mk][net]
                if len(text) > lim: prob.append((fn, k, len(text)))
                w.writerow(row(date, TIMES[i], text, [f'{RAW}/{date}/{mk}/{k}_{j}.jpg' for j in range(1, nimg + 1)]))
                if stories:
                    for s, j in zip(ST[i], (1, 2)): w.writerow(row(date, s, '', [f'{RAW}/{date}/{mk}/{k}_story{j}.jpg'], 'story'))
            if stories: w.writerow(row(date, '20:10', '', [f'{RAW}/{date}/{mk}/final_story.jpg'], 'story'))
print('PROBLEMS', prob); print(sorted(os.listdir(OUT)))

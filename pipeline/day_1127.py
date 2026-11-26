import asyncio, os, sys
sys.path.insert(0, '/home/claude/day')
import tpl
from tpl import *
from playwright.async_api import async_playwright

REPO = '/home/claude/am-media'

CR = {'ignis_suzuki_': 'Suzuki', 'rrgt_rangerover_': 'Range Rover'}
for f in os.listdir('/home/claude/day/photos'):
    for pre, b in CR.items():
        if f.startswith(pre):
            tpl.PHOTO_CR[f] = {'ua': f'Фото: {b}', 'lv': f'Foto: {b}'}

NB = '\u00a0'
N = {
 'ignis': {'cover': 'edit', 'photo': 'ignis_suzuki_01.jpg', 'photo2': 'ignis_suzuki_04.jpg', 'photo3': 'ignis_suzuki_05.jpg', 'photo4': 'ignis_suzuki_02.jpg', 'pos2': '50% 60%', 'pos3': '50% 45%',
  'ua': dict(t1='Suzuki Ignis', t2='тепер електричний', sub='Продажі в Європі — з літа 2027 року',
             items=[f'Найменший Ignis в історії: 3,57{NB}м', f'Батарея на 26{NB}кВт·год і 91{NB}к.с.', 'Салон на чотирьох і кнопки для клімату', 'Конкуренти — Dacia Spring і Leapmotor T03'],
             factsnote='далі цифри →', big='3,57', bigunit=f'{NB}м', bigcap='довжина нового Ignis',
             badge=f'26{NB}кВт·год', badgesub='ємність батареї', statsub=f'Кліренс — 150{NB}мм',
             q1='А ви б узяли електричний Ignis', q2='для міста?'),
  'lv': dict(t1='Suzuki Ignis', t2='tagad elektrisks', sub='Pārdošana Eiropā – no 2027. gada vasaras',
             items=[f'Mazākais Ignis vēsturē: 3,57{NB}m', f'26{NB}kWh akumulators un 91{NB}ZS', 'Salons četriem un pogas klimatam', 'Konkurenti – Dacia Spring un Leapmotor T03'],
             factsnote='tālāk skaitļi →', big='3,57', bigunit=f'{NB}m', bigcap='jaunā Ignis garums',
             badge=f'26{NB}kWh', badgesub='akumulatora ietilpība', statsub=f'Klīrenss – 150{NB}mm',
             q1='Vai jūs izvēlētos elektrisko Ignis', q2='pilsētai?')},
 'rrgt': {'cover': 'dark', 'photo': 'rrgt_rangerover_evo-2.jpg', 'photo2': 'rrgt_rangerover_evo-3.jpg', 'photo3': 'rrgt_rangerover_evo-4.jpg', 'photo4': 'rrgt_rangerover_evo-5.jpg', 'pos2': '50% 50%', 'pos3': '50% 50%',
  'ua': dict(badgeC='', title1='Range Rover GT', title2='лише електричний', sub="Прем'єра — на початку 2027 року",
             items=['Найнижчий Range Rover в історії', f'Перша модель на платформі EMA на 800{NB}В', "Гібрид з'явиться пізніше, але не у 2027-му", 'Evoque і Velar знімуть з виробництва в середині 2027-го'],
             factsnote='далі цифри →', big='350', bigunit=f'{NB}кВт', bigcap='максимальна потужність заряджання',
             badge='10–80%', badgesub=f'приблизно за 20{NB}хв', statsub=f'800{NB}В — напруга платформи',
             q1='А що виберете ви:', q2='електричний Range Rover GT чи Velar?'),
  'lv': dict(badgeC='', title1='Range Rover GT', title2='tikai elektrisks', sub='Pirmizrāde – 2027. gada sākumā',
             items=['Zemākais Range Rover vēsturē', f'Pirmais modelis uz 800{NB}V EMA platformas', 'Hibrīds būs vēlāk, bet ne 2027. gadā', 'Evoque un Velar ražošanu pārtrauks 2027. gada vidū'],
             factsnote='tālāk skaitļi →', big='350', bigunit=f'{NB}kW', bigcap='maksimālā uzlādes jauda',
             badge='10–80%', badgesub=f'aptuveni 20{NB}min', statsub=f'800{NB}V – platformas spriegums',
             q1='Ko izvēlētos jūs:', q2='elektrisko Range Rover GT vai Velar?')},
}

DAYS = {'2026-11-27': ['ignis', 'rrgt']}
ONLY = sys.argv[1:]  # optional: keys to render

async def main():
    jobs = []
    for date, keys in DAYS.items():
        for mk in ('ua', 'lv'):
            m = MK[mk]; d = f'{REPO}/{date}/{mk}'; os.makedirs(d, exist_ok=True)
            covers = []
            for key in keys:
                n = dict(N[key]); t = n[mk]
                cov = {'light': cover_light, 'dark': cover_card, 'edit': cover_edit}[n['cover']](m, n, t)
                covers.append(f'file://{d}/{key}_1.jpg')
                if ONLY and key not in ONLY: continue
                jobs.append((f'{d}/{key}_1.jpg', cov, 1080, 1350))
                jobs.append((f'{d}/{key}_2.jpg', slide_facts(m, n, t, 2, 4), 1080, 1350))
                jobs.append((f'{d}/{key}_3.jpg', slide_stat(m, n, t, 3, 4), 1080, 1350))
                jobs.append((f'{d}/{key}_4.jpg', slide_cta(m, n, t, 4, 4), 1080, 1350))
                jobs.append((f'{d}/{key}_story1.jpg', story_cover(m, n, t), 1080, 1920))
                jobs.append((f'{d}/{key}_story2.jpg', story_facts(m, n, t, 'light' if n['cover'] == 'dark' else 'dark'), 1080, 1920))
            jobs.append((f'{d}/final_story.jpg', ('final', m, covers), 1080, 1920))
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page()
        for path, html, w, h in jobs:
            if isinstance(html, tuple): html = story_final(html[1], html[2])
            await pg.set_viewport_size({'width': w, 'height': h})
            open('/home/claude/day/d.html', 'w').write(html)
            await pg.goto('file:///home/claude/day/d.html'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
            await pg.screenshot(path=path, type='jpeg', quality=90)
        await b.close()
    print(len(jobs), 'images')

asyncio.run(main())

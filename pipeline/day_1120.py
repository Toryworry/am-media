import asyncio, os, sys
sys.path.insert(0, '/home/claude/day')
import tpl
from tpl import *
from playwright.async_api import async_playwright

REPO = '/home/claude/am-media'



for f in ['vw_1.jpg','vw_2.jpg','vw_3.jpg','vw_4.jpg']:
    tpl.PHOTO_CR[f] = {'ua': 'Фото: Volkswagen', 'lv': 'Foto: Volkswagen'}
for f in ['lb_1.jpg','lb_2.jpg','lb_3.jpg','lb_4.jpg']:
    tpl.PHOTO_CR[f] = {'ua': 'Фото: Lamborghini', 'lv': 'Foto: Lamborghini'}

N = {
 'idup': {'cover': {'ua': 'edit', 'lv': 'edit'}, 'photo': 'vw_1.jpg', 'photo2': 'vw_2.jpg', 'photo3': 'vw_3.jpg', 'photo4': 'vw_4.jpg', 'pos2': '50% 75%', 'pos3': '50% 62%',
  'ua': dict(badgeC='', title1='Volkswagen ID. UP', title2='електро-Up! за 20 000 €', t1='Volkswagen ID. UP:', t2='електро-Up! за 20 000 €',
             sub='Найдешевший електромобіль VW отримав назву',
             items=['Ціна — до 20 000 €', 'Щонайменше 250 км запасу ходу', '3,88 м завдовжки, чотири місця', 'Серійний випуск — у 2027 році'],
             factsnote='далі цифри →', big='305', bigunit=' л', bigcap='об\'єм багажника',
             badge='95 к.с.', badgesub='потужність електромотора', statsub='На фото — концепт ID. EVERY1, з якого виросте ID. UP',
             q1='А ви б узяли маленький електро-VW', q2='за 20 тисяч євро?'),
  'lv': dict(badgeC='', title1='Volkswagen ID. UP', title2='elektriskais Up! par 20 000 €', t1='Volkswagen ID. UP:', t2='elektriskais Up! par 20 000 €',
             sub='Lētākais VW elektroauto saņēmis nosaukumu',
             items=['Cena – līdz 20 000 €', 'Vismaz 250 km nobraukums', '3,88 m garš, četras vietas', 'Sērijveida ražošana – 2027. gadā'],
             factsnote='tālāk skaitļi →', big='305', bigunit=' l', bigcap='bagāžnieka tilpums',
             badge='95 ZS', badgesub='elektromotora jauda', statsub='Foto – koncepts ID. EVERY1, no kura tapis ID. UP',
             q1='Vai jūs pirktu mazu elektrisko VW', q2='par 20 tūkstošiem eiro?')},
 'spyder': {'cover': {'ua': 'dark', 'lv': 'dark'}, 'photo': 'lb_1.jpg', 'photo2': 'lb_2.jpg', 'photo3': 'lb_3.jpg', 'photo4': 'lb_4.jpg', 'pos2': '50% 45%', 'pos3': '50% 55%',
  'ua': dict(badgeC='', title1='Lamborghini Temerario Spyder', title2='920 к.с. під відкритим небом', tsize=60,
             sub='Перший серійний Lamborghini з електричним жорстким дахом',
             items=['Гібрид: V8 і три електромотори', '0–100 км/год за 2,8 с', 'Максимальна швидкість — 343 км/год', 'Дах ховається вертикально за сидіннями'],
             factsnote='далі цифри →', big='10 000', bigunit='', bigcap='обертів за хвилину — межа для V8',
             badge='920 к.с.', badgesub='сумарна потужність', statsub='З відкритим дахом центр ваги нижчий на 3 мм',
             q1='А що виберете ви:', q2='купе чи кабріолет?'),
  'lv': dict(badgeC='', title1='Lamborghini Temerario Spyder', title2='920 ZS zem klajas debess', tsize=60,
             sub='Pirmais sērijveida Lamborghini ar elektrisku cieto jumtu',
             items=['Hibrīds: V8 un trīs elektromotori', '0–100 km/h 2,8 sekundēs', 'Maksimālais ātrums – 343 km/h', 'Jumts paslēpjas vertikāli aiz sēdekļiem'],
             factsnote='tālāk skaitļi →', big='10 000', bigunit='', bigcap='apgriezieni minūtē – V8 robeža',
             badge='920 ZS', badgesub='kopējā jauda', statsub='Ar atvērtu jumtu smaguma centrs ir par 3 mm zemāk',
             q1='Ko izvēlētos jūs:', q2='kupeju vai kabrioletu?')},
}

DAYS = {'2026-11-20': {'ua': ['idup', 'spyder'], 'lv': ['idup', 'spyder']}}
async def main():
    jobs = []
    for date, mks in DAYS.items():
        for mk, keys in mks.items():
            m = MK[mk]; d = f'{REPO}/{date}/{mk}'; os.makedirs(d, exist_ok=True)
            covers = []
            for key in keys:
                n = dict(N[key]); n['cover'] = N[key]['cover'][mk]; t = n[mk]
                cov = {'light': cover_light, 'dark': cover_card, 'edit': cover_edit}[n['cover']](m, n, t)
                covers.append(f'file://{d}/{key}_1.jpg')
                jobs.append((f'{d}/{key}_1.jpg', cov, 1080, 1350))
                jobs.append((f'{d}/{key}_2.jpg', slide_facts(m, n, t, 2, 4), 1080, 1350))
                jobs.append((f'{d}/{key}_3.jpg', slide_stat(m, n, t, 3, 4), 1080, 1350))
                jobs.append((f'{d}/{key}_4.jpg', slide_cta(m, n, t, 4, 4), 1080, 1350))
                jobs.append((f'{d}/{key}_story1.jpg', story_cover(m, n, t), 1080, 1920))
                jobs.append((f'{d}/{key}_story2.jpg', story_facts(m, n, t, 'light' if n['cover'] == 'dark' else 'dark'), 1080, 1920))
            jobs.append((f'{d}/final_story.jpg', story_final(m, covers), 1080, 1920))
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page()
        for path, html, w, h in jobs:
            await pg.set_viewport_size({'width': w, 'height': h})
            open('/home/claude/day/d.html', 'w').write(html)
            await pg.goto('file:///home/claude/day/d.html'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
            await pg.screenshot(path=path, type='jpeg', quality=90)
        await b.close()
    print(len(jobs), 'images')

asyncio.run(main())

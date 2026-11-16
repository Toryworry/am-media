import asyncio, os, sys
sys.path.insert(0, '/home/claude/day')
import tpl
from tpl import *
from playwright.async_api import async_playwright

REPO = '/home/claude/am-media'

for f in ['ix4_13.jpg', 'ix4_25.jpg', 'ix4_22.jpg', 'ix4_54.jpg']:
    tpl.PHOTO_CR[f] = {'ua': 'Фото: BMW', 'lv': 'Foto: BMW'}

# cover can differ per market: {'ua': 'edit', 'lv': 'dark'}
N = {
 'phantom': {'cover': {'ua': 'dark'}, 'photo': 'ph_0.jpg', 'photo2': 'ph_1.jpg', 'photo3': 'ph_2.jpg', 'photo4': 'ph_4.jpg', 'pos2': '50% 50%', 'pos3': '50% 60%',
  'ua': dict(badgeC='', title1='«Фантоми» вже', title2='на Львівщині й Одещині', tsize=76,
             sub='З 16 листопада поліція патрулює дороги на авто, схожих на звичайні',
             items=['Зовні — звичайні авто', 'Швидкість вимірюють у русі та на місці', 'Фіксують обидва напрямки руху', 'Працюють передусім на аварійних ділянках'],
             factsnote='далі цифри →', big='112', bigunit='тис.', bigcap='порушень швидкості на Київщині з вересня',
             badge='2', badgesub='нові області: Львівська та Одеська', statsub='Перевищення фіксують автоматично — без зупинки авто',
             q1='А ви за те, щоб «фантоми»', q2='працювали у вашій області?')},
 'ix4': {'cover': {'ua': 'edit', 'lv': 'dark'}, 'photo': 'ix4_13.jpg', 'photo2': 'ix4_25.jpg', 'photo3': 'ix4_22.jpg', 'photo4': 'ix4_54.jpg', 'pos2': '50% 60%', 'pos3': '50% 55%',
  'ua': dict(badgeC='', title1='BMW <span style=\"text-transform:none\">i</span>X4', title2='пішов у серію', t1='BMW <span style=\"text-transform:none\">i</span>X4', t2='пішов у серію',
             sub='Електричний кросовер-купе нового покоління Neue Klasse',
             items=['Випускають у Дебрецені, Угорщина', 'Дві версії: 374 і 469 к.с.', 'Зарядка до 400 кВт', 'Продажі — з березня 2027 року'],
             factsnote='далі цифри →', big='828', bigunit='км', bigcap='максимальний запас ходу за WLTP',
             badge='+387 км', badgesub='за 10 хвилин зарядки', statsub='Найпотужніша версія M60 — понад 600 к.с.',
             q1='А ви б пересіли на', q2='електричний BMW <span style=\"text-transform:none\">i</span>X4?'),
  'lv': dict(badgeC='', title1='BMW <span style=\"text-transform:none\">i</span>X4', title2='nonācis ražošanā', t1='BMW <span style=\"text-transform:none\">i</span>X4', t2='nonācis ražošanā',
             sub='Jaunās paaudzes Neue Klasse elektriskais kupejveida krosovers',
             items=['Ražo Debrecenā, Ungārijā', 'Divas versijas: 374 un 469 ZS', 'Uzlāde līdz 400 kW', 'Pārdošanā — no 2027. gada marta'],
             factsnote='tālāk skaitļi →', big='828', bigunit='km', bigcap='maksimālais nobraukums pēc WLTP',
             badge='+387 km', badgesub='10 minūšu uzlādē', statsub='Jaudīgākajai M60 versijai — vairāk nekā 600 ZS',
             q1='Vai jūs pārsēstos uz', q2='elektrisko BMW <span style=\"text-transform:none\">i</span>X4?')},
 'csdd': {'cover': {'lv': 'edit'}, 'photo': 'csdd_0.jpg', 'photo2': 'csdd_1.jpg', 'photo3': 'csdd_3.jpg', 'photo4': 'csdd_2.jpg', 'pos2': '50% 40%', 'pos3': '50% 60%',
  'lv': dict(t1='CSDD dāvinās', t2='8000 atstarotāju', sub='Lai gājēji tumsā būtu labāk pamanāmi',
             items=['4000 — festivālā “Staro Rīga” (15.–18.11)', '4000 — Narvesen veikalos no 21.11', 'Atstarotājus dalīs bez maksas', 'Kampaņu rīko CSDD, BALTA un Narvesen'],
             factsnote='tālāk skaitļi →', big='14', bigunit='%', bigcap='iedzīvotāju vienmēr lieto atstarotāju',
             badge='36', badgesub='gājēji gāja bojā tumsā 2025. gadā', statsub='Šogad tumsā bojā gājuši jau deviņi gājēji',
             q1='Vai jūs tumsā vienmēr', q2='lietojat atstarotāju?')},
}

DAYS = {'2026-11-17': {'ua': ['phantom', 'ix4'], 'lv': ['ix4', 'csdd']}}

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

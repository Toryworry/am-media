import asyncio, os, sys
sys.path.insert(0, '/home/claude/day')
import tpl
from tpl import *
from playwright.async_api import async_playwright

REPO = '/home/claude/am-media'


for f in ['cc_1.jpg','cc_2.jpg','cc_3.jpg','cc_4.jpg']:
    tpl.PHOTO_CR[f] = {'ua': 'Фото: Tesla', 'lv': 'Foto: Tesla'}
for f in ['tc_1.jpg','tc_2.jpg','tc_3.jpg','tc_4.jpg']:
    tpl.PHOTO_CR[f] = {'ua': 'Фото: Bentley', 'lv': 'Foto: Bentley'}

N = {
 'cybercab': {'cover': {'ua': 'edit', 'lv': 'edit'}, 'photo': 'cc_1.jpg', 'photo2': 'cc_2.jpg', 'photo3': 'cc_3.jpg', 'photo4': 'cc_4.jpg', 'pos2': '50% 60%', 'pos3': '50% 55%',
  'ua': dict(badgeC='', title1='Tesla Cybercab', title2='вже можна замовити', t1='Tesla Cybercab', t2='вже можна замовити',
             sub='Без керма й педалей — за $29 990',
             items=['Два місця, без керма й педалей', 'Ціна — $29 990 до податків', 'Обов\'язкова підписка — $299 на місяць', 'Поставки з грудня, поки лише в США'],
             factsnote='далі цифри →', big='$299', bigunit='', bigcap='на місяць коштує обов\'язкова підписка',
             badge='8 міст', badgesub='де він може їздити', statsub='Без підписки авто не поїде',
             q1='А ви б купили авто', q2='без керма?'),
  'lv': dict(badgeC='', title1='Tesla Cybercab', title2='jau var pasūtīt', t1='Tesla Cybercab', t2='jau var pasūtīt',
             sub='Bez stūres un pedāļiem – par $29 990',
             items=['Divas vietas, bez stūres un pedāļiem', 'Cena – $29 990 bez nodokļiem', 'Obligāts abonements – $299 mēnesī', 'Piegādes no decembra, pagaidām tikai ASV'],
             factsnote='tālāk skaitļi →', big='$299', bigunit='', bigcap='mēnesī maksā obligātais abonements',
             badge='8 pilsētas', badgesub='kur tas drīkst braukt', statsub='Bez abonementa auto nebrauks',
             q1='Vai jūs pirktu auto', q2='bez stūres?')},
 'torcal': {'cover': {'ua': 'dark', 'lv': 'dark'}, 'photo': 'tc_1.jpg', 'photo2': 'tc_2.jpg', 'photo3': 'tc_3.jpg', 'photo4': 'tc_4.jpg', 'pos2': '50% 55%', 'pos3': '50% 60%',
  'ua': dict(badgeC='', title1='Bentley Torcal', title2='розпродали на рік уперед', tsize=70,
             sub='Перший електромобіль марки ще навіть не почали випускати',
             items=['Замовлення на 2027 рік уже вичерпано', 'Випуск — з першої половини 2027-го', 'До 600 км запасу ходу за WLTP', 'У США — від $222 495'],
             factsnote='далі цифри →', big='16', bigunit='хв', bigcap='зарядка з 10 до 80%',
             badge='888 к.с.', badgesub='у версії Torcal S', statsub='Перший електромобіль в історії Bentley',
             q1='А ви б обрали', q2='електричний Bentley?'),
  'lv': dict(badgeC='', title1='Bentley Torcal', title2='izpārdots gadu uz priekšu', tsize=70,
             sub='Zīmola pirmo elektroauto vēl nav pat sākuši ražot',
             items=['2027. gada pasūtījumi jau izpārdoti', 'Ražošana – no 2027. gada pirmās puses', 'Līdz 600 km nobraukums pēc WLTP', 'ASV – no $222 495'],
             factsnote='tālāk skaitļi →', big='16', bigunit='min', bigcap='uzlāde no 10 līdz 80%',
             badge='888 ZS', badgesub='versijā Torcal S', statsub='Pirmais elektroauto Bentley vēsturē',
             q1='Vai jūs izvēlētos', q2='elektrisko Bentley?')},
}

DAYS = {'2026-11-19': {'ua': ['cybercab', 'torcal'], 'lv': ['cybercab', 'torcal']}}
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

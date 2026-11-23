import asyncio, os, sys
sys.path.insert(0, '/home/claude/day')
import tpl
from tpl import *
from playwright.async_api import async_playwright

REPO = '/home/claude/am-media'

CR = {'gtr_nissan_': 'Nissan', 'fer_': 'Ferrari'}
for f in os.listdir('/home/claude/day/photos'):
    for pre, b in CR.items():
        if f.startswith(pre):
            tpl.PHOTO_CR[f] = {'ua': f'Фото: {b}', 'lv': f'Foto: {b}'}

N = {
 'gtr': {'cover': 'edit', 'photo': 'gtr_nissan_hakosuka.jpg', 'photo2': 'gtr_px_9347165.jpg', 'photo3': 'gtr_px_11026047.jpg', 'photo4': 'gtr_px_11585908.jpg', 'pos2': '50% 30%', 'pos3': '50% 60%',
  'ua': dict(t1='Новий GT-R отримає', t2='круглі фари', sub='Як у легендарних моделях 1970-х',
             items=['Про круглі фари сказав новий дизайн-директор Nissan Меттью Вівер', 'Так виглядали перші GT-R: «Hakosuka» 1969 року і «Kenmeri» 1973-го', 'Повністю електричним новий GT-R не буде', 'Дату прем\'єри й характеристики поки не називають'],
             factsnote='далі цифри →', big='18', bigunit=' років', bigcap='стільки випускали R35',
             badge='2025', badgesub='рік, коли R35 зняли з виробництва', statsub='«Якщо ми робитимемо R36, у нього будуть круглі фари»',
             q1='А який GT-R вам ближчий:', q2='класичний з круглими фарами чи сучасний R35?'),
  'lv': dict(t1='Jaunais GT-R saņems', t2='apaļus lukturus', sub='Kā leģendārajiem 70. gadu modeļiem',
             items=['Par apaļajiem lukturiem runāja Nissan jaunais dizaina vadītājs Metjū Vīvers', 'Tādi bija pirmajiem GT-R: “Hakosuka” (1969) un “Kenmeri” (1973)', 'Pilnībā elektrisks jaunais GT-R nebūs', 'Pirmizrādes datums un tehniskie dati vēl nav zināmi'],
             factsnote='tālāk skaitļi →', big='18', bigunit=' gadi', bigcap='tik ilgi ražoja R35',
             badge='2025', badgesub='gads, kad R35 ražošana beidzās', statsub='“Ja mēs veidosim R36, tam būs apaļi lukturi”',
             q1='Kurš GT-R jums tuvāks:', q2='klasiskais ar apaļiem lukturiem vai mūsdienīgais R35?')},
 'fer296': {'cover': 'dark', 'photo': 'fer_pic_4_5_002.jpg', 'photo2': 'fer_pic_4_5_007.jpg', 'photo3': 'fer_pic_4_5_006.jpg', 'photo4': 'fer_pic_4_5_001.jpg', 'pos2': '50% 60%', 'pos3': '50% 55%',
  'ua': dict(badgeC='', title1='Ferrari 296', title2='без гібрида',
             sub='Challenge Stradale — гоночна машина для звичайних доріг',
             items=['Електромотор і батарею прибрали: лише V6 бітурбо, 670\u00a0к.с.', 'Суха маса — 1330 кг, на 140 кг менше, ніж у 296 GTB', 'Притискна сила — 617 кг на швидкості 250 км/год', '0–100 км/год за 2,8 с'],
             factsnote='далі цифри →', big='1330', bigunit=' кг', bigcap='суха маса — на 140 кг менше, ніж у 296 GTB',
             badge='670 к.с.', badgesub='проти 830 к.с. у 296 GTB', statsub='0–100 км/год — за 2,8 с',
             q1='А що для вас важливіше в спортивному авто:', q2='потужність чи мала вага?'),
  'lv': dict(badgeC='', title1='Ferrari 296', title2='bez hibrīda',
             sub='Challenge Stradale – sacīkšu auto parastiem ceļiem',
             items=['Elektromotors un akumulators noņemti: tikai V6 biturbo, 670\u00a0ZS', 'Sausā masa – 1330 kg, par 140 kg mazāk nekā 296 GTB', 'Piespiedējspēks – 617 kg pie 250 km/h', '0–100 km/h 2,8 sekundēs'],
             factsnote='tālāk skaitļi →', big='1330', bigunit=' kg', bigcap='sausā masa – par 140 kg mazāk nekā 296 GTB',
             badge='670 ZS', badgesub='pret 830 ZS 296 GTB', statsub='0–100 km/h – 2,8 sekundēs',
             q1='Kas jums sporta auto ir svarīgāks:', q2='jauda vai mazs svars?')},
}

DAYS = {'2026-11-24': ['gtr', 'fer296']}
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

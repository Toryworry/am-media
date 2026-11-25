import asyncio, os, sys
sys.path.insert(0, '/home/claude/day')
import tpl
from tpl import *
from playwright.async_api import async_playwright

REPO = '/home/claude/am-media'

CR = {'boxster_hq_': 'Porsche', 'denza_': 'Denza'}
for f in os.listdir('/home/claude/day/photos'):
    for pre, b in CR.items():
        if f.startswith(pre):
            tpl.PHOTO_CR[f] = {'ua': f'Фото: {b}', 'lv': f'Foto: {b}'}

NB = '\u00a0'
N = {
 'boxster': {'cover': 'edit', 'photo': 'boxster_hq_341550.jpg', 'photo2': 'boxster_hq_341752.jpg', 'photo3': 'boxster_hq_341846.jpg', 'photo4': 'boxster_hq_341545.jpg', 'pos2': '50% 55%', 'pos3': '50% 50%',
  'ua': dict(t1='Електричний Porsche Boxster', t2='майже готовий', sub='Прем\'єра — на початку 2027 року',
             items=['Батарея стоїть за сидіннями, на місці двигуна', f'Найпотужніший 718 в історії: понад 250{NB}км/\u2060год', 'Усі версії задньопривідні, задні колеса підрульові', 'Віртуальна коробка PDK і звук опозитної «шістки»'],
             factsnote='далі цифри →', big=f'4{NB}млн', bigunit='', bigcap='кілометрів проїхали прототипи',
             badge=f'<{NB}3{NB}с', badgesub=f'розгін до 100{NB}км/год у топовій версії', statsub=f'Тести — від −30{NB}°C до +51{NB}°C',
             q1='А ви б узяли', q2='електричний Boxster?'),
  'lv': dict(t1='Elektriskais Porsche Boxster', t2='gandrīz gatavs', sub='Pirmizrāde – 2027. gada sākumā',
             items=['Akumulators atrodas aiz sēdekļiem, motora vietā', f'Jaudīgākais 718 vēsturē: vairāk nekā 250{NB}km/h', 'Visām versijām aizmugurējo riteņu piedziņa, aizmugurējie riteņi stūrējami', 'Virtuāla PDK kārba un sešcilindru boksera skaņa'],
             factsnote='tālāk skaitļi →', big=f'4{NB}milj.', bigunit=f'{NB}km', bigcap='tik nobraukuši prototipi',
             badge=f'<{NB}3{NB}s', badgesub=f'0–100{NB}km/h augstākajai versijai', statsub=f'Testi – no −30{NB}°C līdz +51{NB}°C',
             q1='Vai jūs izvēlētos', q2='elektrisko Boxster?')},
 'denza': {'cover': 'dark', 'photo': 'denza_0eprk3.jpg', 'photo2': 'denza_BX1rnv.jpg', 'photo3': 'denza_1ZPrOW.jpg', 'photo4': 'denza_ko8ygQ.jpg', 'pos2': '50% 60%', 'pos3': '50% 60%',
  'ua': dict(badgeC='', title1='Denza тягне Boeing 747', title2='на двох колесах', sub='Літак важить 180 тонн',
             items=['Три заїзди: на 4, 3 і 2 колесах', f'Загалом літак проїхав 1,6{NB}км', 'Тягнули лише на електриці, під зливою', 'Авто серійне, лише з баластом і опорами'],
             factsnote='далі цифри →', big='180', bigunit=f'{NB}т', bigcap='вага Boeing 747-400',
             badge=f'544{NB}к.с.', badgesub=f'і 760{NB}Нм: потужність Denza B5', statsub=f'4,5{NB}т баласту в салоні',
             q1='А що вразило вас більше:', q2=f'Touareg V10 із Boeing чи Denza на двох колесах?'),
  'lv': dict(badgeC='', title1='Denza velk Boeing 747', title2='uz diviem riteņiem', sub='Lidmašīna sver 180 tonnas',
             items=['Trīs braucieni: uz 4, 3 un 2 riteņiem', f'Kopā lidmašīna nobrauca 1,6{NB}km', 'Vilka tikai ar elektrību, lietusgāzē', 'Auto ir sērijveida, tikai ar balastu un balstiem'],
             factsnote='tālāk skaitļi →', big='180', bigunit=f'{NB}t', bigcap='Boeing 747-400 svars',
             badge=f'544{NB}ZS', badgesub=f'un 760{NB}Nm: Denza B5 jauda', statsub=f'4,5{NB}t balasta salonā',
             q1='Kas jūs pārsteidza vairāk:', q2=f'Touareg V10 ar Boeing vai Denza uz diviem riteņiem?')},
}

DAYS = {'2026-11-26': ['boxster', 'denza']}
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

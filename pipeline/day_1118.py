import asyncio, os, sys
sys.path.insert(0, '/home/claude/day')
import tpl
from tpl import *
from playwright.async_api import async_playwright

REPO = '/home/claude/am-media'


for f in ['bmwi3_000482918.jpg','bmwi3_000482910.jpg','bmwi3_000482896.jpg','bmwi3_000482919.jpg']:
    tpl.PHOTO_CR[f] = {'ua': 'Фото: BMW', 'lv': 'Foto: BMW'}
for f in ['ctr_04.jpg','ctr_03.jpg','ctr_01.jpg','ctr_15.jpg']:
    tpl.PHOTO_CR[f] = {'ua': 'Фото: Honda', 'lv': 'Foto: Honda'}

N = {
 'hybrids': {'cover': {'ua': 'dark'}, 'photo': 'hyb_9615358.jpg', 'photo2': 'hyb_33359730.jpg', 'photo3': 'hyb_4895432.jpg', 'photo4': 'hyb_11320632.jpg', 'pos2': '50% 60%', 'pos3': '50% 55%',
  'ua': dict(badgeC='', title1='Гібриди жовтня:', title2='що купують українці', tsize=84,
             sub='Понад 3,6 тис. реєстрацій — на 20,5% більше, ніж торік',
             items=['Понад 3,6 тис. гібридів за жовтень', '+20,5% порівняно з торішнім жовтнем', 'Нові: лідер Toyota RAV4 (181)', 'Вживані: лідер Ford Fusion (163)'],
             factsnote='далі цифри →', big='36', bigunit='%', bigcap='нових авто серед гібридів жовтня',
             badge='53%', badgesub='було рік тому', statsub='Решту гібридів привозять уживаними',
             q1='А ви б пересіли', q2='на гібрид?')},
 'bmwi3': {'cover': {'ua': 'edit', 'lv': 'dark'}, 'photo': 'bmwi3_000482918.jpg', 'photo2': 'bmwi3_000482910.jpg', 'photo3': 'bmwi3_000482896.jpg', 'photo4': 'bmwi3_000482919.jpg', 'pos2': '50% 55%', 'pos3': '50% 60%',
  'ua': dict(badgeC='', title1='BMW <span style="text-transform:none">i</span>3 M60', title2='отримає «передачі»', t1='BMW <span style="text-transform:none">i</span>3 M60', t2='отримає «передачі»',
             sub='Імітація перемикання підрульовими пелюстками — як у Hyundai Ioniq 5 N',
             items=['Імітація перемикання підрульовими пелюстками', 'Лише у версії M60: 612 к.с. і 875 Нм', 'Ідею підгледіли в Hyundai Ioniq 5 N', 'У продажу — наступного року'],
             factsnote='далі цифри →', big='912', bigunit='км', bigcap='запас ходу нового BMW <span style="text-transform:none">i</span>3 50 xDrive за WLTP',
             badge='+423 км', badgesub='за 10 хвилин зарядки', statsub='Новий <span style="text-transform:none">i</span>3 уже виробляють у Мюнхені',
             q1='А вам потрібні «передачі»', q2='в електромобілі?'),
  'lv': dict(badgeC='', title1='BMW <span style="text-transform:none">i</span>3 M60', title2='saņems “pārnesumus”', t1='BMW <span style="text-transform:none">i</span>3 M60', t2='saņems “pārnesumus”', tsize=78,
             sub='Pārslēgšanas imitācija ar lāpstiņām – kā Hyundai Ioniq 5 N',
             items=['Pārslēgšanas imitācija ar lāpstiņām pie stūres', 'Tikai versijā M60: 612 ZS un 875 Nm', 'Ideja aizgūta no Hyundai Ioniq 5 N', 'Pārdošanā – nākamgad'],
             factsnote='tālāk skaitļi →', big='912', bigunit='km', bigcap='jaunā BMW <span style="text-transform:none">i</span>3 50 xDrive nobraukums pēc WLTP',
             badge='+423 km', badgesub='10 minūšu uzlādē', statsub='Jauno <span style="text-transform:none">i</span>3 jau ražo Minhenē',
             q1='Vai jums elektroauto', q2='vajag “pārnesumus”?')},
 'honda': {'cover': {'lv': 'edit'}, 'photo': 'ctr_04.jpg', 'photo2': 'ctr_03.jpg', 'photo3': 'ctr_01.jpg', 'photo4': 'ctr_15.jpg', 'pos2': '50% 55%', 'pos3': '50% 60%',
  'lv': dict(t1='Atjaunotais', t2='Honda Civic Type R', sub='Honda to rādīs Losandželosas autošovā',
             items=['Jauns buferis labākai dzesēšanai', 'Pirmo reizi – apsildāmi sēdekļi', 'Iebūvēts Google ar Gemini', '315 ZS un tikai manuālā kārba'],
             factsnote='tālāk skaitļi →', big='30', bigunit='', bigcap='gadus šogad svin Civic Type R',
             badge='315 ZS', badgesub='un tikai manuālā kārba', statsub='Autošova preses diena – 19. novembrī',
             q1='Vai jūs izvēlētos hečbeku', q2='ar manuālo kārbu?')},
}

DAYS = {'2026-11-18': {'ua': ['hybrids', 'bmwi3'], 'lv': ['bmwi3', 'honda']}}
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

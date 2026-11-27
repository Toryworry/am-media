import asyncio, os, sys
sys.path.insert(0, '/home/claude/day')
import tpl
from tpl import *
from playwright.async_api import async_playwright

# Creatives for 28, 29 and 30.11.2026 (Friday batch). Per-market news lists: DAYS[date][mk].
REPO = '/home/claude/am-media'

CR = {'gt41_ford_': 'Ford', 'porsche_porsche_': 'Porsche', 'idx_vw_': 'Volkswagen', 'bmwota_bmw_': 'BMW', 'su7_xiaomi_': 'MIIT'}
for f in os.listdir('/home/claude/day/photos'):
    for pre, b in CR.items():
        if f.startswith(pre):
            tpl.PHOTO_CR[f] = {'ua': f'Фото: {b}', 'lv': f'Foto: {b}'}

NB = ' '
N = {
 'fuel': {'cover': 'edit', 'photo': 'fuel_px_34636185.jpg', 'photo2': 'fuel_px_12377482.jpg', 'photo3': 'fuel_px_12377481.jpg', 'photo4': 'fuel_px_34058522.jpg', 'pos2': '50% 50%', 'pos3': '50% 45%',
  'ua': dict(t1='Пальне дешевшає:', t2=f'А-95 мінус 9{NB}грн за місяць', sub='Ціни станом на 27 листопада',
             items=[f'А-95 у середньому — 81,60{NB}грн (було 90,91)', f'Дизель — 96,90{NB}грн (було 104,57)', f'Найдешевший А-95 — 75,70{NB}грн у KLO', f'Автогаз подорожчав на 6{NB}грн — до 61,41'],
             factsnote='далі цифри →', big='21%', bigunit='', bigcap='авто на AUTOMOTO.UA — з ГБО',
             badge=f'−9,31{NB}грн', badgesub='А-95 за місяць', statsub=f'+5,97{NB}грн — автогаз за місяць',
             q1='А на чому їздите ви:', q2='бензин, дизель чи газ?')},
 'proto': {'cover': 'edit', 'photo': 'crash_px_5835351.jpg', 'photo2': 'crash_px_5820892.jpg', 'photo3': 'crash_px_7736042.jpg', 'photo4': 'crash_px_6442699.jpg', 'pos2': '50% 60%', 'pos3': '50% 35%',
  'lv': dict(t1='Saskaņotais paziņojums:', t2='tagad biežāk bez policijas', sub='Izmaiņas spēkā no 25. novembra',
             items=['Policija izvērtēs, vai jābrauc uz vietu', f'Var aizpildīt, ja iesaistīti vairāk nekā 2{NB}auto', 'Atsevišķos gadījumos – vienpusēji', 'Vienmēr pēc policijas norādījumiem'],
             factsnote='tālāk skaitļi →', big='3+', bigunit=f'{NB}auto', bigcap='un paziņojumu tomēr var aizpildīt',
             badge=f'1{NB}vadītājs', badgesub='var aizpildīt vienpusēji', statsub='Izmaiņas stājās spēkā 25.11',
             q1='Vai jums ir nācies aizpildīt', q2='saskaņoto paziņojumu?')},
 'gt41': {'cover': 'dark', 'photo': 'gt41_ford_1.jpg', 'photo2': 'gt41_ford_2.jpg', 'photo3': 'gt41_ford_3.jpg', 'photo4': 'gt41_ford_1.jpg', 'pos2': '50% 50%', 'pos3': '50% 55%',
  'ua': dict(badgeC='', title1='Ford GT41:', title2='повернення в Ле-Ман', sub='Ford знову бореться за загальну перемогу',
             items=[f'Атмосферний V8 на 5,4{NB}л', f'671{NB}к.с. разом з електромотором', 'Назва — відсилання до GT40', 'Дебют — навесні 2027 року'],
             factsnote='далі цифри →', big='1969', bigunit='', bigcap='остання загальна перемога Ford',
             badge=f'671{NB}к.с.', badgesub='потужність GT41', statsub=f'2{NB}авто — у сезоні 2027 року',
             q1='А за кого вболіватимете в Ле-Мані:', q2='Ford чи Ferrari?'),
  'lv': dict(badgeC='', title1='Ford GT41:', title2='atgriešanās Lemānā', sub='Ford atkal cīnās par kopvērtējuma uzvaru',
             items=[f'5,4{NB}l atmosfēras V8', f'671{NB}ZS kopā ar elektromotoru', 'Nosaukums – atsauce uz GT40', 'Debija – 2027. gada pavasarī'],
             factsnote='tālāk skaitļi →', big='1969', bigunit='', bigcap='Ford pēdējā kopvērtējuma uzvara',
             badge=f'671{NB}ZS', badgesub='GT41 jauda', statsub=f'2{NB}auto – 2027. gada sezonā',
             q1='Par ko jutīsiet līdzi Lemānā:', q2='Ford vai Ferrari?')},
 'idx': {'cover': 'edit', 'photo': 'idx_vw_DB2026AU01083.jpg', 'photo2': 'idx_vw_DB2026AU01059.jpg', 'photo3': 'idx_vw_DB2026AU01074.jpg', 'photo4': 'idx_vw_DB2026AU01060.jpg', 'pos2': '50% 60%', 'pos3': '50% 60%',
  'ua': dict(t1='VW ID. Cross R-Line:', t2='потужність як у GTI', sub='Найпотужніша версія — з березня 2027 року',
             items=[f'223{NB}к.с. від ID. Polo GTI', f'До 428{NB}км на одному заряді', 'Блокування диференціала й адаптивна підвіска', f'Базова R-Line — від 37{NB}225{NB}€ у Німеччині'],
             factsnote='далі цифри →', big='6,9', bigunit=f'{NB}с', bigcap=f'розгін до 100{NB}км/год',
             badge=f'223{NB}к.с.', badgesub='потужність', statsub=f'Багажник — 475{NB}л',
             q1='А ви б узяли електричний', q2=f'кросовер VW на 223{NB}к.с.?'),
  'lv': dict(t1='VW ID. Cross R-Line:', t2='jauda kā GTI', sub='Jaudīgākā versija – no 2027. gada marta',
             items=[f'223{NB}ZS no ID. Polo GTI', f'Līdz 428{NB}km ar vienu uzlādi', 'Diferenciāļa bloķēšana un adaptīvā piekare', f'Bāzes R-Line – no 37{NB}225{NB}€ Vācijā'],
             factsnote='tālāk skaitļi →', big='6,9', bigunit=f'{NB}s', bigcap=f'0–100{NB}km/h',
             badge=f'223{NB}ZS', badgesub='jauda', statsub=f'Bagāžnieks – 475{NB}l',
             q1='Vai jūs izvēlētos VW elektrisko', q2=f'krosoveru ar 223{NB}ZS?')},
 'gt1': {'cover': 'dark', 'photo': 'porsche_porsche_342300.jpg', 'photo2': 'porsche_porsche_342309.jpg', 'photo3': 'porsche_porsche_342303.jpg', 'photo4': 'porsche_porsche_342302.jpg', 'pos2': '50% 50%', 'pos3': '50% 50%',
  'ua': dict(badgeC='', title1='Porsche 911 GT3', title2='на честь 911 GT1', sub='Єдиний такий у світі',
             items=['Ліврея, розписана вручну', 'Герб Porsche, як на GT1 у 1996 році', 'Карбонова кришка замість заднього скла', f'Серійний мотор: 510{NB}к.с. і 9000{NB}об/хв'],
             factsnote='далі цифри →', big='1,5', bigunit=f'{NB}року', bigcap='стільки створювали це авто',
             badge=f'510{NB}к.с.', badgesub='потужність', statsub=f'До 100{NB}км/год — за 3,4{NB}с',
             q1='А ви б наважилися на таку яскраву', q2='ліврею на своєму авто?'),
  'lv': dict(badgeC='', title1='Porsche 911 GT3', title2='par godu 911 GT1', sub='Vienīgais šāds pasaulē',
             items=['Ar rokām apgleznots krāsojums', 'Porsche ģerbonis kā uz GT1 1996. gadā', 'Oglekļa šķiedras vāks aizmugurējā stikla vietā', f'Sērijveida motors: 510{NB}ZS un 9000{NB}apgr./min'],
             factsnote='tālāk skaitļi →', big='1,5', bigunit=f'{NB}gadi', bigcap='tik ilgi veidoja šo auto',
             badge=f'510{NB}ZS', badgesub='jauda', statsub=f'0–100{NB}km/h – 3,4{NB}s',
             q1='Vai jūs uzdrošinātos uz tik spilgtu', q2='krāsojumu savam auto?')},
 'bmw': {'cover': 'edit', 'photo': 'bmwota_bmw_000518943.jpg', 'photo2': 'bmwota_bmw_000512934.jpg', 'photo3': 'bmwota_bmw_000512947.jpg', 'photo4': 'bmwota_bmw_000512943.jpg', 'pos2': '50% 45%', 'pos3': '50% 50%',
  'ua': dict(t1=f'BMW оновлює 16{NB}млн авто', t2=f'«по{NB}повітрю»', sub='Нове оновлення — у грудні',
             items=['24 нові й покращені функції', 'Голосовий асистент на основі ШІ', 'Навігація в 3D і прогноз зайнятості зарядок', 'Установка — близько 20 хвилин'],
             factsnote='далі цифри →', big='16', bigunit=f'{NB}млн', bigcap='BMW отримують оновлення',
             badge=f'88{NB}країн', badgesub='де працюють оновлення', statsub='24 оновлення з 2018 року',
             q1='А ви оновлюєте програмне', q2='забезпечення свого авто?')},
 'tyre': {'cover': 'edit', 'photo': 'tyre_px_6603945.jpg', 'photo2': 'tyre_px_6603957.jpg', 'photo3': 'tyre_px_34357281.jpg', 'photo4': 'tyre_px_30757600.jpg', 'pos2': '50% 60%', 'pos3': '50% 60%',
  'lv': dict(t1='No 1. decembra:', t2='tikai ziemas riepas', sub='Ar marķējumu “kalns un sniegpārsliņa”',
             items=['Ziemas periods – no 1.12 līdz 1.03', 'Riepas tikai ar M+S vairs neder', f'Minimālais protektors – 4{NB}mm', 'Nedrīkst jaukt radžotas un neradžotas'],
             factsnote='tālāk skaitļi →', big='4', bigunit=f'{NB}mm', bigcap='minimālais protektora dziļums',
             badge=f'5–6{NB}gadi', badgesub='pēc tam riepas labāk nomainīt', statsub=f'Prasība – auto ar pilno masu līdz 3,5{NB}t',
             q1='Vai jūs jau esat uzlikuši', q2='ziemas riepas?')},
 'su7': {'cover': 'dark', 'photo': 'su7_xiaomi_1.jpg', 'photo2': 'su7_xiaomi_3.jpg', 'photo3': 'su7_xiaomi_2.jpg', 'photo4': 'su7_xiaomi_1.jpg', 'pos2': '50% 50%', 'pos3': '50% 55%',
  'ua': dict(badgeC='', title1='Xiaomi SU7 Ultra', title2='хоче повернути рекорд', sub='Новий аеропакет для Нюрбургрингу',
             items=['Антикрило з DRS, як у 911 GT3 RS', 'Трековий бампер і шини Pirelli Trofeo RS', f'Та сама потужність: 1526{NB}к.с.', f'Максимальна швидкість — 318{NB}км/год'],
             factsnote='далі цифри →', big='≈10', bigunit=f'{NB}с', bigcap='треба скинути, щоб відібрати рекорд',
             badge='6:55,553', badgesub='рекорд Porsche Taycan Turbo GT', statsub='7:04,957 — коло SU7 Ultra у 2025 році',
             q1='А ви вірите, що Xiaomi', q2='відбере рекорд у Porsche?'),
  'lv': dict(badgeC='', title1='Xiaomi SU7 Ultra', title2='grib atgūt rekordu', sub='Jauns aerodinamikas komplekts Nirburgringai',
             items=['Spārns ar DRS kā 911 GT3 RS', 'Trases buferis un Pirelli Trofeo RS riepas', f'Tā pati jauda: 1526{NB}ZS', f'Maksimālais ātrums – 318{NB}km/h'],
             factsnote='tālāk skaitļi →', big='≈10', bigunit=f'{NB}s', bigcap='jānomet, lai atņemtu rekordu',
             badge='6:55,553', badgesub='Porsche Taycan Turbo GT rekords', statsub='7:04,957 – SU7 Ultra aplis 2025. gadā',
             q1='Vai jūs ticat, ka Xiaomi', q2='atņems rekordu Porsche?')},
}

DAYS = {
 '2026-11-28': {'ua': ['fuel', 'gt41'], 'lv': ['proto', 'gt41']},
 '2026-11-29': {'ua': ['idx', 'gt1'], 'lv': ['idx', 'gt1']},
 '2026-11-30': {'ua': ['bmw', 'su7'], 'lv': ['tyre', 'su7']},
}
ONLY = sys.argv[1:]  # optional: keys to render

async def main():
    jobs = []
    for date, per in DAYS.items():
        for mk, keys in per.items():
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
            # final story of the day is no longer made (Viktoriia 27.11)
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

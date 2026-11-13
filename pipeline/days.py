import asyncio, os, sys
sys.path.insert(0, '/home/claude/day')
import tpl
from tpl import *
from playwright.async_api import async_playwright

REPO = '/home/claude/am-media'

def cr(brand, files):
    for f in files:
        tpl.PHOTO_CR[f] = {'ua': f'Фото: {brand}', 'lv': f'Foto: {brand}'}
cr('Volkswagen', ['troc_1.jpg', 'troc_2.jpg', 'troc_3.jpg', 'troc_4.jpg', 'idt_73.jpg', 'idt_02.jpg', 'idt_prod.jpg', 'idt_10.jpg'])
cr('Nissan', ['qq_rel-4.jpg', 'qq_rel-7.jpg', 'qq_sb-6.jpg', 'qq_rel-12.jpg'])
cr('Honda', ['crve_1.jpg', 'crve_15.jpg', 'crve_20.jpg', 'crve_19.jpg'])
cr('XPeng', ['xp_6.webp', 'xp_4.webp', 'xp_10.webp', 'xp_8.webp'])
cr('Mercedes-Benz', ['eqe_e1.jpg'])

N = {
 'tax': {'cover': 'dark', 'photo': 'tax_keys.jpg', 'photo2': 'tax_5.jpg', 'photo3': 'tax_9.jpg', 'photo4': 'tax_6.jpg', 'pos2': '50% 50%', 'pos3': '50% 55%',
  'ua': dict(badgeC='', title1='Продати авто швидко', title2='стане дорожче',
             sub='З 2027 року — до 23% податку, якщо володіли авто менше ніж 183 дні',
             items=['Пільга лише за володіння понад 183 дні', 'Менше ніж 183 дні — 23% податку', 'Другий продаж за рік — 10%', 'Правила мають запрацювати з 1 січня 2027 року'],
             factsnote='далі цифри →', big='23', bigunit='%', bigcap='податок, якщо продати авто раніше ніж через пів року',
             badge='', badgesub='', statsub='Авто, отримані у спадщину, під обмеження не підпадають',
             q1='А ви вважаєте ці правила', q2='справедливими?')},
 'tesla': {'cover': 'dark', 'photo': 'tesla_1.jpg', 'photo2': 'tesla_3.jpg', 'photo3': 'tesla_4.jpg', 'photo4': 'tesla_2.jpg', 'pos2': '50% 50%', 'pos3': '50% 40%',
  'lv': dict(badgeC='', title1='Tesla autopilots', title2='tagad arī Somijā',
             sub='Tesla Assisted Driving atļauta jau 11 Eiropas valstīs, tostarp Latvijā',
             items=['Agrāk sistēmu sauca par FSD (Supervised)', 'Latvijā tā atļauta kopš oktobra beigām', 'Vairs nevar ilgstoši pārsniegt ātrumu par 50%', 'Lēmums par visu ES — ne agrāk kā decembrī'],
             factsnote='tālāk skaitļi →', big='11', bigunit='', bigcap='Eiropas valstis jau atļāvušas sistēmu',
             badge='~3 ned.', badgesub='tik ilgi pēc ES balsojuma jāgaida atļauja', statsub='Ziemā sniegs uz kamerām var ierobežot sistēmas darbību',
             q1='Vai jūs uzticētos Tesla', q2='ziemas ceļos?')},
 'troc': {'cover': 'edit', 'photo': 'troc_3.jpg', 'photo2': 'troc_1.jpg', 'photo3': 'troc_4.jpg', 'photo4': 'troc_2.jpg', 'pos2': '50% 55%', 'pos3': '50% 55%',
  'ua': dict(t1='Новий T-Roc R:', t2='перший тизер', sub='Volkswagen показав прототипи «зарядженого» кросовера',
             items=['Чотири вихлопні труби і ширші колеса', 'Платформа MQB evo, як у Golf', 'Найімовірніше — мотор від Golf R', 'Прем\'єру чекають до кінця листопада'],
             factsnote='далі цифри →', big='333', bigunit='к.с.', bigcap='потужність Golf R, мотор якого чекають у T-Roc R',
             badge='300 к.с.', badgesub='мав попередній T-Roc R', statsub='Офіційних характеристик Volkswagen ще не назвав',
             q1='А ви б узяли T-Roc R', q2='замість Golf R?'),
  'lv': dict(t1='Jaunais T-Roc R:', t2='pirmie foto', sub='Volkswagen parādīja jaudīgā krosovera prototipus',
             items=['Četras izplūdes caurules un platāki riteņi', 'MQB evo platforma, tāpat kā Golf', 'Visticamāk — Golf R motors', 'Pirmizrādi gaida līdz novembra beigām'],
             factsnote='tālāk skaitļi →', big='333', bigunit='ZS', bigcap='Golf R jauda, kura motoru gaida T-Roc R',
             badge='300 ZS', badgesub='bija iepriekšējam T-Roc R', statsub='Oficiālus tehniskos datus Volkswagen vēl nav nosaucis',
             q1='Vai jūs ņemtu T-Roc R', q2='Golf R vietā?')},
 'idtiguan': {'cover': 'dark', 'photo': 'idt_73.jpg', 'photo2': 'idt_02.jpg', 'photo3': 'idt_prod.jpg', 'photo4': 'idt_10.jpg', 'pos2': '50% 60%', 'pos3': '50% 55%',
  'ua': dict(badgeC='', title1='Електричний Tiguan', title2='пішов у серію', sub='Volkswagen почав виробництво ID. Tiguan',
             items=['Замінить ID.4 та ID.5', 'До 600 км запасу ходу', 'Буксирує причіп до 2 тонн', 'У дилерів — з початку 2027 року'],
             factsnote='далі цифри →', big='600', bigunit='км', bigcap='максимальний запас ходу',
             badge='220 кВт', badgesub='максимальна потужність', statsub='Зарядка — до 165 кВт для більшої батареї',
             q1='А ви б пересіли на', q2='електричний Tiguan?'),
  'lv': dict(badgeC='', title1='Elektriskais Tiguan', title2='nonācis ražošanā', sub='Volkswagen sāka ražot ID. Tiguan',
             items=['Aizstās ID.4 un ID.5', 'Nobraukums līdz 600 km', 'Velk piekabi līdz 2 tonnām', 'Pie dīleriem — no 2027. gada sākuma'],
             factsnote='tālāk skaitļi →', big='600', bigunit='km', bigcap='maksimālais nobraukums',
             badge='220 kW', badgesub='maksimālā jauda', statsub='Uzlāde — līdz 165 kW lielākajam akumulatoram',
             q1='Vai jūs pārsēstos uz', q2='elektrisko Tiguan?')},
 'qashqai': {'cover': 'edit', 'photo': 'qq_rel-4.jpg', 'photo2': 'qq_rel-7.jpg', 'photo3': 'qq_sb-6.jpg', 'photo4': 'qq_rel-12.jpg', 'pos2': '50% 60%', 'pos3': '50% 60%',
  'ua': dict(t1='Qashqai — 20 років:', t2='7,3 млн авто', sub='Кросовер, який створив цілий клас',
             items=['Концепт показали в Женеві 2004 року', '4,5 млн авто зібрали в Сандерленді', '65% усіх продажів Nissan у Європі', 'Нове покоління — у 2028 році, гібридне'],
             factsnote='далі цифри →', big='7,3', bigunit='млн', bigcap='стільки Qashqai продали за 20 років',
             badge='65%', badgesub='частка в продажах Nissan у Європі', statsub='На ювілей зробили унікальне авто з iPod у салоні',
             q1='А який Qashqai вам', q2='подобається найбільше?'),
  'lv': dict(t1='Qashqai — 20 gadi:', t2='7,3 miljoni auto', sub='Krosovers, kas radīja veselu klasi',
             items=['Koncepciju parādīja Ženēvā 2004. gadā', '4,5 miljoni auto saražoti Sanderlendā', '65% no Nissan pārdošanas Eiropā', 'Jaunā paaudze — 2028. gadā, hibrīds'],
             factsnote='tālāk skaitļi →', big='7,3', bigunit='milj.', bigcap='tik Qashqai pārdoti 20 gados',
             badge='65%', badgesub='daļa no Nissan pārdošanas Eiropā', statsub='Jubilejai izveidoja unikālu auto ar iPod salonā',
             q1='Kurš Qashqai jums', q2='patīk visvairāk?')},
 'crv': {'cover': 'dark', 'photo': 'crve_1.jpg', 'photo2': 'crve_15.jpg', 'photo3': 'crve_20.jpg', 'photo4': 'crve_19.jpg', 'pos2': '50% 45%', 'pos3': '50% 45%',
  'ua': dict(badgeC='', title1='Новий Honda CR-V:', title2='тільки гібрид', sub='Honda показала перший тизер сьомого покоління',
             items=['Нова платформа: жорсткіша й легша', 'Гібрид з двома електромоторами', 'Новий електричний повний привід', 'У США з\'явиться наступного року'],
             factsnote='далі цифри →', big='10', bigunit='%', bigcap='на стільки має зменшитися витрата пального',
             badge='30 років', badgesub='CR-V відзначить у 2027 році', statsub='Коли новинка дістанеться Європи, Honda поки не каже',
             q1='А ви б узяли', q2='CR-V-гібрид?'),
  'lv': dict(badgeC='', title1='Jaunā Honda CR-V:', title2='tikai hibrīds', sub='Honda parādīja pirmo septītās paaudzes mājienu',
             items=['Jauna platforma: stingrāka un vieglāka', 'Hibrīds ar diviem elektromotoriem', 'Jauna elektriskā pilnpiedziņa', 'ASV parādīsies nākamgad'],
             factsnote='tālāk skaitļi →', big='10', bigunit='%', bigcap='par tik jāsamazinās degvielas patēriņam',
             badge='30 gadi', badgesub='CR-V svinēs 2027. gadā', statsub='Kad jaunais modelis sasniegs Eiropu, Honda pagaidām nesaka',
             q1='Vai jūs ņemtu', q2='CR-V hibrīdu?')},
 'xpeng': {'cover': 'edit', 'photo': 'xp_6.webp', 'photo2': 'xp_4.webp', 'photo3': 'xp_10.webp', 'photo4': 'xp_8.webp', 'pos2': '50% 55%', 'pos3': '50% 55%',
  'ua': dict(t1='XPeng офіційно', t2='<br>в Україні', sub='Перші електромобілі мають прибути у грудні',
             items=['На старті — G6, G9 і P7+', 'Пізніше додасться кросовер-купе L03', 'Перші дилери — Київ, Львів, Вінниця', 'Ціни назвуть ближче до старту продажів'],
             factsnote='далі цифри →', big='8', bigunit='років', bigcap='гарантія на батарею й електромотор',
             badge='5 років', badgesub='загальна гарантія на авто', statsub='Або 160 000 км пробігу — залежно від того, що настане раніше',
             q1='А ви б розглянули XPeng', q2='як альтернативу Tesla?')},
 'eqe': {'cover': 'edit', 'photo': 'eqe_e1.jpg', 'photo2': 'eqe_p1.jpg', 'photo3': 'eqe_p4.jpg', 'photo4': 'eqe_p3.jpg', 'pos2': '50% 60%', 'pos3': '50% 50%',
  'lv': dict(t1='Mercedes atvadās', t2='no EQE un EQS SUV?', sub='Šos elektroauto vairs nevar pasūtīt, tikai nopirkt no noliktavas',
             items=['Bez pasūtījumiem — EQE, EQE SUV un EQS SUV', 'Paliek tikai EQS sedans', 'Vietā — elektriskā E-klase 2027. gadā', 'Oficiāli Mercedes vēl nav apstiprinājis'],
             factsnote='tālāk skaitļi →', big='4', bigunit='gadi', bigcap='tik ilgi noturējās EQE sedans',
             badge='2027', badgesub='elektriskās E-klases ienākšanas gads', statsub='ASV EQE no pārdošanas izņēma jau oktobrī',
             q1='Vai jūs tagad pirktu', q2='lietotu EQE?')},
}

DAYS = {
 '2026-11-14': {'ua': ['tax', 'troc'], 'lv': ['tesla', 'troc']},
 '2026-11-15': {'ua': ['idtiguan', 'qashqai'], 'lv': ['idtiguan', 'qashqai']},
 '2026-11-16': {'ua': ['crv', 'xpeng'], 'lv': ['crv', 'eqe']},
}

async def main():
    only = sys.argv[1:]  # optional filter: date or key
    jobs = []
    for date, mks in DAYS.items():
        for mk, keys in mks.items():
            m = MK[mk]; d = f'{REPO}/{date}/{mk}'; os.makedirs(d, exist_ok=True)
            covers = []
            for key in keys:
                n = N[key]; t = n[mk]
                cov = {'light': cover_light, 'dark': cover_card, 'edit': cover_edit}[n['cover']](m, n, t)
                covers.append(f'file://{d}/{key}_1.jpg')
                if only and date not in only and key not in only: continue
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

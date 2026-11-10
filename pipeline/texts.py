import csv, os

DATE = '2026-11-11'
D = DATE.replace('-', '/')
RAW = f'https://raw.githubusercontent.com/Toryworry/am-media/main/{DATE}'
OUT = f'/home/claude/day/csv_{DATE}'
os.makedirs(OUT, exist_ok=True)

TIME = {'byd': '10:00', 'merc': '20:00'}
STORY_T = {'byd': ('10:05', '10:06'), 'merc': ('20:05', '20:06')}
FINAL_T = '20:10'

T = {
 'byd': {
  'ua': {
   'ig': """BYD можуть перевірити на шпигунство 🕵️

14 євродепутатів попросили Єврокомісію оцінити, чи не становлять загрозу авто BYD. Йдеться про камери, GPS, мікрофони й датчики: депутати побоюються, що зібрані ними дані можуть потрапляти до китайської влади.

▪️ запит подали 4 листопада
▪️ оцінку має дати кібербезпекове агентство ЄС
▪️ BYD можуть визнати «постачальником високого ризику» і обмежити доступ його авто до стратегічної інфраструктури та держзакупівель

У BYD звинувачення заперечують: компанія каже, що дані європейських клієнтів у Китай не передаються.

Для розуміння масштабів: за 9 місяців BYD продав у Європі майже 284 тисячі авто — більше, ніж Ford. А в Україні BYD Sea Lion 06 став найпопулярнішим новим електромобілем вересня.

Заборони поки немає, власникам BYD нічого не загрожує.

Довіряєте китайським авто? 👇

#automoto #автоновини #BYD #електромобілі""",
   'fb': """14 євродепутатів просять перевірити BYD на шпигунство 🕵️

Їх турбують камери, GPS і датчики в авто: чи не потрапляють зібрані дані до китайської влади. BYD можуть визнати «постачальником високого ризику». У компанії все заперечують.

Заборони поки немає, власникам нічого не загрожує.

Довіряєте китайським авто? 👇""",
   'x': "14 євродепутатів просять ЄС перевірити BYD на шпигунство: їх турбують дані з камер і датчиків авто. BYD звинувачення заперечує. Заборони поки немає 🕵️",
  },
  'lv': {
   'ig': """BYD varētu pārbaudīt spiegošanā 🕵️

14 Eiropas Parlamenta deputāti lūdz Eiropas Komisiju izvērtēt, vai BYD auto nerada draudus. Runa ir par kamerām, GPS, mikrofoniem un sensoriem: deputāti baidās, ka savāktie dati var nonākt pie Ķīnas varas iestādēm.

▪️ pieprasījums iesniegts 4. novembrī
▪️ vērtējums jāsniedz ES kiberdrošības aģentūrai
▪️ BYD var atzīt par «augsta riska piegādātāju» un ierobežot tā auto piekļuvi stratēģiskajai infrastruktūrai un valsts iepirkumiem

BYD apsūdzības noliedz: uzņēmums apgalvo, ka Eiropas klientu dati uz Ķīnu netiek nodoti.

Mēroga izpratnei: 9 mēnešos BYD Eiropā pārdeva gandrīz 284 tūkstošus auto — vairāk nekā Ford.

Aizlieguma pagaidām nav, BYD īpašniekiem nekas nedraud.

Vai uzticaties Ķīnas auto? 👇

#automoto #autozinas #BYD #elektroauto""",
   'fb': """14 eiroparlamentārieši lūdz pārbaudīt BYD spiegošanā 🕵️

Viņus uztrauc auto kameras, GPS un sensori: vai savāktie dati nenonāk pie Ķīnas varas iestādēm. BYD var atzīt par «augsta riska piegādātāju». Uzņēmums visu noliedz.

Aizlieguma pagaidām nav, īpašniekiem nekas nedraud.

Vai uzticaties Ķīnas auto? 👇""",
   'x': "14 eiroparlamentārieši lūdz ES pārbaudīt BYD spiegošanā: viņus uztrauc dati no auto kamerām un sensoriem. BYD apsūdzības noliedz. Aizlieguma pagaidām nav 🕵️",
  },
 },
 'merc': {
  'ua': {
   'ig': """Бензин і дизель поховали зарано ⛽

Голова правління Mercedes-Benz Ола Келленіус вважає, що двигуни внутрішнього згоряння протримаються ще щонайменше 10, а ймовірно 15 років.

▪️ повний перехід на електрику, за його словами, займе 20–25 років, а не закінчиться у 2030 чи 2035 році
▪️ нові мотори Mercedes уже адаптують до майбутніх норм Euro 7
▪️ дизель і V8 залишаються в лінійці поряд із гібридами й електромобілями
▪️ за три роки компанія випустить 40 нових моделей — і з ДВЗ, і електричних

Головна умова — попит: ДВЗ житимуть, доки їх купують.

А що виберете ви: ДВЗ чи електро? 👇

#automoto #автоновини #MercedesBenz #дизель""",
   'fb': """Голова правління Mercedes-Benz Ола Келленіус: бензин і дизель проживуть ще щонайменше 10, а ймовірно 15 років ⛽

Повний перехід на електрику він оцінює у 20–25 років. Нові мотори вже адаптують до Euro 7, а за три роки Mercedes випустить 40 моделей — і з ДВЗ, і електричних.

А що виберете ви: ДВЗ чи електро? 👇""",
   'x': "Очільник Mercedes Ола Келленіус: бензин і дизель проживуть ще 10–15 років, а повний перехід на електрику триватиме 20–25 років. Нові мотори вже адаптують до Euro 7 ⛽",
  },
  'lv': {
   'ig': """Benzīnu un dīzeli norakstīja par agru ⛽

Mercedes-Benz vadītājs Ola Källenius uzskata, ka iekšdedzes dzinēji paliks vēl vismaz 10, iespējams, 15 gadus.

▪️ pilna pāreja uz elektrību, pēc viņa teiktā, aizņems 20–25 gadus, nevis beigsies 2030. vai 2035. gadā
▪️ jaunie Mercedes motori jau tiek gatavoti nākamajām Euro 7 normām
▪️ dīzelis un V8 paliek modeļu klāstā līdzās hibrīdiem un elektroauto
▪️ trīs gadu laikā uzņēmums izlaidīs 40 jaunus modeļus — gan ar iekšdedzes dzinējiem, gan elektriskus

Galvenais nosacījums — pieprasījums: iekšdedzes dzinēji dzīvos, kamēr tos pērk.

Un ko izvēlētos jūs: benzīnu, dīzeli vai elektro? 👇

#automoto #autozinas #MercedesBenz #dīzelis""",
   'fb': """Mercedes-Benz vadītājs Ola Källenius: benzīns un dīzelis dzīvos vēl vismaz 10, iespējams, 15 gadus ⛽

Pilnu pāreju uz elektrību viņš vērtē 20–25 gadu garumā. Jaunie motori jau tiek gatavoti Euro 7 normām, un trīs gadu laikā Mercedes izlaidīs 40 modeļus — gan ar iekšdedzes dzinējiem, gan elektriskus.

Un ko izvēlētos jūs: benzīnu, dīzeli vai elektro? 👇""",
   'x': "Mercedes vadītājs Ola Källenius: benzīns un dīzelis dzīvos vēl 10–15 gadus, bet pilna pāreja uz elektrību ilgs 20–25 gadus. Jaunie motori jau gatavoti Euro 7 ⛽",
  },
 },
}
ORDER = ['byd', 'merc']
HEADER = ["Date", "Text", "Link(s)", "Media URL(s)", "Title", "Label(s)", "Alt text(s)",
          "Comment(s)", "Pin board, FB album, or Google category", "Post subtype", "CTA", "Reminder"]
LIMITS = {'x': 280, 'fb_threads': 500, 'tg': 1024, 'ig': 2200}

def row(time, text, media, subtype=''):
    r = [''] * 12
    r[0] = f'{D} {time}'; r[1] = text; r[3] = ','.join(media); r[5] = 'автоновини'; r[9] = subtype
    return r

def carousel(mk, k): return [f'{RAW}/{mk}/{k}_{i}.jpg' for i in range(1, 5)]
def cover(mk, k): return [f'{RAW}/{mk}/{k}_1.jpg']

FILES = {
 'UA_1_instagram.csv': ('ua', 'ig', 'carousel', True),
 'UA_2_facebook_threads.csv': ('ua', 'fb', 'cover', False),
 'UA_3_telegram.csv': ('ua', 'ig_tg', 'cover', False),
 'UA_4_x.csv': ('ua', 'x', 'cover', False),
 'LV_1_instagram.csv': ('lv', 'ig', 'carousel', True),
 'LV_2_facebook.csv': ('lv', 'fb', 'carousel', False),
 'LV_3_x.csv': ('lv', 'x', 'cover', False),
}
problems = []
for fname, (mk, key, media, stories) in FILES.items():
    with open(f'{OUT}/{fname}', 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f); w.writerow(HEADER)
        for k in ORDER:
            t = T[k][mk]
            if key == 'ig_tg':
                text = t['ig'].rsplit('\n\n#', 1)[0]  # Telegram: без хештегів
                lim = LIMITS['tg']
            else:
                text = t[key]; lim = {'x': 280, 'fb': 500, 'ig': 2200}[key]
            if len(text) > lim: problems.append((fname, k, len(text), lim))
            w.writerow(row(TIME[k], text, carousel(mk, k) if media == 'carousel' else cover(mk, k)))
            if stories:
                s1, s2 = STORY_T[k]
                w.writerow(row(s1, '', [f'{RAW}/{mk}/{k}_story1.jpg'], 'story'))
                w.writerow(row(s2, '', [f'{RAW}/{mk}/{k}_story2.jpg'], 'story'))
        if stories:
            w.writerow(row(FINAL_T, '', [f'{RAW}/{mk}/final_story.jpg'], 'story'))
for k in ORDER:
    for mk in ('ua', 'lv'):
        for key in ('ig', 'fb', 'x'):
            print(k, mk, key, len(T[k][mk][key]))
print('PROBLEMS', problems)

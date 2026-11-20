import asyncio, os, sys
sys.path.insert(0, '/home/claude/day')
import tpl
from tpl import *
from playwright.async_api import async_playwright

REPO = '/home/claude/am-media'

CR = {'troc_': 'Volkswagen', 'f355_': 'Iconic Auctioneers', 'kia_': 'Kia', 'elantra_': 'Hyundai', 'deck_': 'Toyota', 'p550_': 'Porsche'}
for f in os.listdir('/home/claude/day/photos'):
    for pre, b in CR.items():
        if f.startswith(pre):
            tpl.PHOTO_CR[f] = {'ua': f'Фото: {b}', 'lv': f'Foto: {b}'}

N = {
 'troc': {'cover': 'edit', 'photo': 'troc_DB2026AU01177.jpg', 'photo2': 'troc_DB2026AU01174.jpg', 'photo3': 'troc_DB2026AU01178.jpg', 'photo4': 'troc_DB2026AU01183.jpg', 'pos2': '50% 60%', 'pos3': '50% 60%',
  'ua': dict(t1='Новий VW T-Roc R:', t2='333 к.с. і режим Drift', sub='Найпотужніший кросовер Volkswagen у Європі',
             items=['2,0-турбо + гібрид 48V — 333 к.с. і 420 Нм', '0–100 км/год за 5 секунд', 'Повний привід 4MOTION і DSG', 'Режими Race, Special і Drift'],
             factsnote='далі цифри →', big='333', bigunit=' к.с.', bigcap='найпотужніший кросовер VW у Європі',
             badge='5 с', badgesub='розгін 0–100 км/год', statsub='Максимальна швидкість — 250 км/год',
             q1='А ви б узяли T-Roc R', q2='чи краще Golf R?'),
  'lv': dict(t1='Jaunais VW T-Roc R:', t2='333 ZS un Drift režīms', sub='Jaudīgākais Volkswagen krosovers Eiropā',
             items=['2,0 turbo + 48V hibrīds – 333 ZS un 420 Nm', '0–100 km/h 5 sekundēs', 'Pilnpiedziņa 4MOTION un DSG', 'Režīmi Race, Special un Drift'],
             factsnote='tālāk skaitļi →', big='333', bigunit=' ZS', bigcap='jaudīgākais VW krosovers Eiropā',
             badge='5 s', badgesub='0–100 km/h', statsub='Maksimālais ātrums – 250 km/h',
             q1='Vai jūs izvēlētos T-Roc R', q2='vai tomēr Golf R?')},
 'f355': {'cover': 'dark', 'photo': 'f355_1.jpg', 'photo2': 'f355_8.jpg', 'photo3': 'f355_5.jpg', 'photo4': 'f355_2.jpg', 'pos2': '50% 60%', 'pos3': '50% 60%',
  'ua': dict(badgeC='', title1='Ferrari Кларксона', title2='продали за 405 000 £', tsize=86,
             sub='Рекорд для Ferrari F355 на аукціоні в Бірмінгемі',
             items=['Ferrari F355 GTS 1996 року', 'V8 3,5 л, 380 к.с. і «механіка»', 'Кларксон купив авто новим', 'Продали на аукціоні в Бірмінгемі'],
             factsnote='далі цифри →', big='405 000', bigunit=' £', bigcap='світовий рекорд для Ferrari F355',
             badge='200–250 тис. £', badgesub='таку ціну очікував аукціон', statsub='Кларксон проїхав на ньому близько 10 000 км',
             q1='А ви б переплатили за авто,', q2='яке належало відомій людині?'),
  'lv': dict(badgeC='', title1='Klārksona Ferrari', title2='pārdots par 405 000 £', tsize=86,
             sub='Rekords Ferrari F355 izsolē Birmingemā',
             items=['1996. gada Ferrari F355 GTS', 'V8 3,5 l, 380 ZS un manuālā kārba', 'Klārksons auto nopirka jaunu', 'Pārdots izsolē Birmingemā'],
             factsnote='tālāk skaitļi →', big='405 000', bigunit=' £', bigcap='pasaules rekords Ferrari F355',
             badge='200–250 tūkst. £', badgesub='tādu cenu gaidīja izsole', statsub='Klārksons ar to nobrauca ap 10 000 km',
             q1='Vai jūs pārmaksātu par auto,', q2='kas piederējis slavenam cilvēkam?')},
 'kia': {'cover': 'edit', 'photo': 'kia_sorento_25078.jpg', 'photo2': 'kia_carnival_24844.jpg', 'photo3': 'kia_sorento_25080.jpg', 'photo4': 'kia_carnival_24831.jpg', 'pos2': '50% 60%', 'pos3': '50% 60%',
  'ua': dict(t1='Kia готує нові Sorento і Carnival', t2='— і водневий мінівен', sub='Що відомо з внутрішнього документа компанії',
             items=['Новий Sorento — з 2028 року, з гібридом', 'Новий Carnival — з 2028 року, з гібридом', 'Водневий Carnival — до 2029 року', 'EV7 — новий електрокросовер'],
             factsnote='далі цифри →', big='2028', bigunit='', bigcap='рік, коли чекаємо нові Sorento і Carnival',
             badge='EV7', badgesub='новий електрокросовер Kia', statsub='На фото — нинішні Sorento і Carnival',
             q1='А що виберете ви: гібридний Sorento', q2='чи електричний EV7?'),
  'lv': dict(t1='Kia gatavo jaunus Sorento un Carnival', t2='– un ūdeņraža minivenu', sub='Kas zināms no uzņēmuma iekšējā dokumenta',
             items=['Jaunais Sorento – no 2028. gada, ar hibrīdu', 'Jaunais Carnival – no 2028. gada, ar hibrīdu', 'Ūdeņraža Carnival – līdz 2029. gadam', 'EV7 – jauns elektriskais krosovers'],
             factsnote='tālāk skaitļi →', big='2028', bigunit='', bigcap='gads, kad gaidām jaunos Sorento un Carnival',
             badge='EV7', badgesub='jauns Kia elektriskais krosovers', statsub='Foto – pašreizējie Sorento un Carnival',
             q1='Ko izvēlētos jūs: hibrīda Sorento', q2='vai elektrisko EV7?')},
 'elantra': {'cover': 'dark', 'photo': 'elantra_mk1.jpg', 'photo2': 'elantra_mk2.jpg', 'photo3': 'elantra_mk4.jpg', 'photo4': 'elantra_mk3.jpg', 'pos2': '50% 70%', 'pos3': '50% 55%',
  'ua': dict(badgeC='', title1='Нова Hyundai', title2='Elantra',
             sub='Восьме покоління показали в Лос-Анджелесі',
             items=['Нове покоління показали в Лос-Анджелесі', 'Бензин 2,0 л або гібрид 1,6 л', 'Великий екран і ШІ-асистент', 'У США за 10 місяців продали 140 тис.'],
             factsnote='далі цифри →', big='8 200', bigunit=' $', bigcap='середня ціна Elantra 2014 року в Україні',
             badge='', badgesub='', statsub='До 2010 — 5\u00a0100\u00a0$ · 2011–2015 — 7\u00a0700\u00a0$<br>2016–2020 — 11\u00a0000\u00a0$ · 2021+ — 17\u00a0400\u00a0$',
             q1='А ви б узяли вживану Elantra', q2='чи чекали б на нову?'),
  'lv': dict(badgeC='', title1='Jaunā Hyundai Elantra', title2='debitējusi ASV', tsize=86,
             sub='Astoto paaudzi parādīja Losandželosā',
             items=['Jauno paaudzi parādīja Losandželosā', 'Benzīns 2,0 l vai hibrīds 1,6 l', 'Liels ekrāns un MI asistents', 'Korejā jau pārdod kā Avante'],
             factsnote='tālāk skaitļi →', big='140 000', bigunit='+', bigcap='tik Elantra šogad pārdotas ASV',
             badge='', badgesub='', statsub='Eiropā Elantra oficiāli netiek pārdota',
             q1='Vai jūs gribētu, lai jaunā Elantra', q2='tiktu pārdota arī Eiropā?')},
 'deck': {'cover': 'edit', 'photo': 'deck_frente1.jpg', 'photo2': 'deck_tras2.jpg', 'photo3': 'deck_frente2.jpg', 'photo4': 'deck_tras1.jpg', 'pos2': '50% 55%', 'pos3': '50% 55%',
  'ua': dict(t1='Toyota зробила', t2='з\u00a0Corolla пікап', sub='Corolla Deck випускатимуть у Бразилії з 2027 року',
             items=['Схожий на кросовер Corolla Cross', 'Гібрид: бензин або етанол', 'Задній ряд і вантажна платформа', 'Виробництво — у Бразилії з 2027 року'],
             factsnote='далі цифри →', big='2027', bigunit='', bigcap='рік старту виробництва Corolla Deck',
             badge='Flex', badgesub='гібрид на бензині або етанолі', statsub='Поки що — лише для Латинської Америки',
             q1='А ви б узяли Corolla', q2='з кузовом пікапа?'),
  'lv': dict(t1='Toyota pārvērtusi', t2='Corolla par pikapu', sub='Corolla Deck ražos Brazīlijā no 2027. gada',
             items=['Līdzīgs Corolla Cross krosoveram', 'Hibrīds: benzīns vai etanols', 'Aizmugurējā rinda un kravas kaste', 'Ražošana Brazīlijā no 2027. gada'],
             factsnote='tālāk skaitļi →', big='2027', bigunit='', bigcap='Corolla Deck ražošanas sākuma gads',
             badge='Flex', badgesub='hibrīds ar benzīnu vai etanolu', statsub='Pagaidām – tikai Latīņamerikai',
             q1='Vai jūs izvēlētos Corolla', q2='ar pikapa virsbūvi?')},
 'p550': {'cover': 'dark', 'photo': 'p550_2.jpg', 'photo2': 'p550_3.jpg', 'photo3': 'p550_5.jpg', 'photo4': 'p550_6.jpg', 'pos2': '50% 60%', 'pos3': '50% 55%',
  'ua': dict(badgeC='', title1='Porsche зробила електричну', title2='копію легендарного 550\u00a0Spyder', tsize=66,
             sub='Разом з британською студією Hedley Studios',
             items=['Масштаб 80%, карбоновий кузов, 330–350\u00a0кг', 'Від 11 до 21 к.с., до 80 км/год', 'Лише 250 екземплярів', 'По звичайних дорогах їздити не можна'],
             factsnote='далі цифри →', big='69 500', bigunit=' £', bigcap='ціна Porsche 550 J',
             badge='80%', badgesub='масштаб від оригіналу', statsub='Ціна без податків. Перші авто — навесні 2027 року',
             q1='А ви б віддали майже 70 тисяч фунтів', q2='за таку «іграшку»?'),
  'lv': dict(badgeC='', title1='Porsche radījis leģendārā', title2='550\u00a0Spyder elektrisko kopiju', tsize=66,
             sub='Kopā ar britu studiju Hedley Studios',
             items=['80% mērogs, oglekļa šķiedra, 330–350\u00a0kg', 'No 11 līdz 21 ZS, līdz 80 km/h', 'Tikai 250 eksemplāri', 'Pa parastiem ceļiem braukt nedrīkst'],
             factsnote='tālāk skaitļi →', big='69 500', bigunit=' £', bigcap='Porsche 550 J cena',
             badge='80%', badgesub='oriģināla mērogs', statsub='Cena bez nodokļiem. Pirmie auto – 2027. gada pavasarī',
             q1='Vai jūs atdotu gandrīz 70 tūkstošus mārciņu', q2='par šādu “rotaļlietu”?')},
}

DAYS = {'2026-11-21': ['troc', 'f355'], '2026-11-22': ['kia', 'elantra'], '2026-11-23': ['deck', 'p550']}
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

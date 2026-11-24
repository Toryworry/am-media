import asyncio, os, sys
sys.path.insert(0, '/home/claude/day')
import tpl
from tpl import *
from playwright.async_api import async_playwright

REPO = '/home/claude/am-media'

CR = {'ti7_byd_': 'BYD', 'lynk_': 'Lynk & Co'}
for f in os.listdir('/home/claude/day/photos'):
    for pre, b in CR.items():
        if f.startswith(pre):
            tpl.PHOTO_CR[f] = {'ua': f'Фото: {b}', 'lv': f'Foto: {b}'}

NB = '\u00a0'
N = {
 'ti7': {'cover': 'edit', 'photo': 'ti7_byd_g4O6B9.jpg', 'photo2': 'ti7_byd_nAlRKx.jpg', 'photo3': 'def_px_11552314.jpg', 'photo4': 'ti7_byd_eo7rPV.jpg', 'pos2': '50% 55%', 'pos3': '50% 55%',
  'ua': dict(t1='BYD Ti7 заборонили', t2='в ЄС', sub='Суд визнав його надто схожим на Defender',
             items=['Суд у Нідерландах визнав, що дизайн Ti7 порушує права JLR на Defender', 'BYD не може продавати Ti7 в ЄС і випускати його в Угорщині', 'Заборона діятиме, доки дизайн суттєво не змінять', 'У Британії рішення не діє'],
             factsnote='далі цифри →', big=f'£20{NB}000', bigunit='', bigcap='на стільки Ti7 дешевший за Defender',
             badge=f'408{NB}к.с.', badgesub='сумарна потужність Ti7', statsub='гібрид із бензиновим мотором 1,5 л',
             q1='А що виберете ви:', q2='оригінальний Defender чи дешевший Ti7?'),
  'lv': dict(t1='BYD Ti7 aizliegts', t2='ES', sub='Tiesa atzina, ka tas pārāk līdzinās Defender',
             items=['Nīderlandes tiesa atzina, ka Ti7 dizains pārkāpj JLR tiesības uz Defender', 'BYD nedrīkst pārdot Ti7 ES un ražot to Ungārijā', 'Aizliegums būs spēkā, līdz dizains tiks būtiski mainīts', 'Lielbritānijā lēmums nav spēkā'],
             factsnote='tālāk skaitļi →', big=f'£20{NB}000', bigunit='', bigcap='par tik Ti7 ir lētāks nekā Defender',
             badge=f'408{NB}ZS', badgesub='Ti7 kopējā jauda', statsub='hibrīds ar 1,5 l benzīna motoru',
             q1='Ko izvēlētos jūs:', q2='oriģinālo Defender vai lētāko Ti7?')},
 'lynk': {'cover': 'dark', 'photo': 'lynk_cs_cliff.jpg', 'photo2': 'lynk_m1_eo7q3p.jpg', 'photo3': 'lynk_m1_qkYXbz.jpg', 'photo4': 'lynk_m1_L3yGLN.jpg', 'pos2': '50% 60%', 'pos3': '50% 55%',
  'ua': dict(badgeC='', title1='Lynk & Co 07 GT', title2='злетів зі скелі', sub='Так Geely показав, наскільки авто безпечне',
             items=[f'Серійний універсал злетів із трампліна за край скелі на 70{NB}км/год', 'Кілька разів перекинувся і зупинився на колесах', 'Усі 4 двері відчинилися, бокові вікна й лобове скло вціліли', 'Незалежного краш-тесту в 07 GT поки не було'],
             factsnote='далі цифри →', big='6', bigunit=f'{NB}с', bigcap='стільки подушки-шторки тримали тиск',
             badge=f'530{NB}к.с.', badgesub='гібрид: 1,5 турбо + 2 електромотори', statsub=f'Стрибок зі скелі — на швидкості 70{NB}км/год',
             q1='А чому ви довіряєте більше:', q2=f'ефектним краш\u2011шоу чи тестам Euro{NB}NCAP?'),
  'lv': dict(badgeC='', title1='Lynk & Co 07 GT', title2='nolidoja no klints', sub='Tā Geely parādīja, cik auto ir drošs',
             items=[f'Sērijveida universālis no tramplīna aizlidoja pāri klints malai ar 70{NB}km/h', 'Vairākas reizes apmetās un apstājās uz riteņiem', 'Visas 4 durvis atvērās, sānu logi un vējstikls palika veseli', 'Neatkarīga avārijas testa 07 GT vēl nav bijis'],
             factsnote='tālāk skaitļi →', big='6', bigunit=f'{NB}s', bigcap='tik ilgi aizkaru spilveni noturēja spiedienu',
             badge=f'530{NB}ZS', badgesub='hibrīds: 1,5 turbo + 2 elektromotori', statsub=f'Lēciens no klints – ar 70{NB}km/h',
             q1='Kam jūs uzticaties vairāk:', q2=f'iespaidīgiem avārijas šoviem vai Euro{NB}NCAP testiem?')},
}

DAYS = {'2026-11-25': ['ti7', 'lynk']}
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

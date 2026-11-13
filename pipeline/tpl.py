import asyncio, os, sys, json, importlib.util
FONTCSS = open('/home/claude/day/fonts.css').read()
from playwright.async_api import async_playwright

ROOT = '/home/claude/day'
PH = f'file://{ROOT}/photos/'
COND = "font-family: 'Roboto Condensed', sans-serif; font-weight: 900; text-transform: uppercase"
CAV = "font-family: Caveat, cursive; font-weight: 700"

MK = {
 'ua': dict(lang='ua', accent='#FF6C00', ink='#111111', accentText='#FF6C00', site='AUTOMOTO.UA', logo=f'file://{ROOT}/logo_ua.png', logoH=56, tag='АВТОНОВИНИ',
            facts='ЩО ВІДОМО', comments='пишіть у коментарях ↓', save='ЗБЕРЕЖІТЬ ПОСТ', question='ПИТАННЯ ДО ВАС',
            today='Сьогодні в автоновинах', fin1='Всі деталі —', fin2='в профілі', finnote='', more='повна історія — в пості ↗'),
 'lv': dict(lang='lv', accent='#296FB9', ink='#FFFFFF', accentText='#5C9BDB', site='AUTOMOTO.COM.LV', logo=f'file://{ROOT}/logo_lv.png', logoH=72, tag='AUTO ZIŅAS',
            facts='KAS ZINĀMS', comments='rakstiet komentāros ↓', save='SAGLABĀ IERAKSTU', question='JAUTĀJUMS JUMS',
            today='Šodien auto ziņās', fin1='Visas detaļas —', fin2='profilā', finnote='', more='pilns stāsts — ierakstā ↗'),
}


ARROW = '<svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'

def page(w, h, bg, fg, inner):
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{FONTCSS}body{{margin:0}}</style></head><body>
<div style="width:{w}px;height:{h}px;position:relative;overflow:hidden;background:{bg};font-family:Roboto,sans-serif;color:{fg}">{inner}</div></body></html>'''

def top(m, y, right, ptype='plaque', pbg=None, pfg=None):
    if ptype == 'plaque':
        r = f'<div style="background:{pbg or m["accent"]};color:{pfg or m["ink"]};font-weight:700;font-size:24px;letter-spacing:3px;padding:12px 22px">{right}</div>'
    else:
        r = f'<div style="border:3px solid {pfg};color:{pfg};border-radius:999px;font-weight:700;font-size:22px;letter-spacing:3px;padding:10px 22px">{right}</div>'
    return f'<div style="position:absolute;left:72px;top:{y}px;right:72px;display:flex;justify-content:space-between;align-items:center"><img src="{m["logo"]}" style="height:{m["logoH"]}px;width:auto">{r}</div>'

# credits only for manufacturer photos; Pexels photos are not signed
PHOTO_CR = {
 'merc_1.jpg': {'ua': 'Фото: Mercedes-Benz', 'lv': 'Foto: Mercedes-Benz'},
 'ktm_1_up.jpg': {'ua': 'Фото: KTM X-Bow', 'lv': 'Foto: KTM X-Bow'}, 'ktm_2_up.jpg': {'ua': 'Фото: KTM X-Bow', 'lv': 'Foto: KTM X-Bow'}, 'ktm_cut.png': {'ua': 'Фото: KTM X-Bow', 'lv': 'Foto: KTM X-Bow'},
 **{f'pajero_{i}.jpg': {'ua': 'Фото: Mitsubishi', 'lv': 'Foto: Mitsubishi'} for i in (1, 4, 5, 7)},
 **{p: {'ua': 'Фото: Polestar', 'lv': 'Foto: Polestar'} for p in ('polestar_exterior-17.jpg','polestar_exterior-02.jpg','polestar_exterior-21.jpg','polestar_exterior-20.jpg','polestar_interior-04.jpg')},
 **{f'cupra_terramar_{i}.jpg': {'ua': 'Фото: Cupra', 'lv': 'Foto: Cupra'} for i in ('03','07','10','12')},
 'rav4_1_up.jpg': {'ua': 'Фото: Toyota', 'lv': 'Foto: Toyota'}, 'rav4_2_up.jpg': {'ua': 'Фото: Toyota', 'lv': 'Foto: Toyota'},
}
def pcr(m, photo, c, css):
    t = PHOTO_CR.get(photo, {}).get(m['lang'], '')
    return credit(t, c, css) if t else ''

def credit(t, c, css):
    return f'<div style="position:absolute;{css};font-size:18px;color:{c}">{t}</div>'

# ---------- covers 1080x1350 ----------
def cover_light(m, n, t, H=1350, y0=0, topY=64):
    # light cutout cover (E). y0 shifts content for story
    return page(1080, H, '#ECEAE6', '#111', f'''{top(m, topY, m['tag'])}
<div style="position:absolute;left:40px;top:{210+y0}px;{COND};font-size:300px;line-height:.85;letter-spacing:-8px;color:#DCD8D1;white-space:nowrap">{t['bgword']}</div>
<img src="{PH}{n['cut']}" style="position:absolute;left:30px;top:{330+y0}px;width:1020px;height:auto">
<div style="position:absolute;left:560px;top:{812+y0}px;{CAV};font-size:52px;color:#111;transform:rotate(-3deg)">{t['note']}</div>
<div style="position:absolute;left:72px;top:{880+y0}px;width:720px;background:{m['accent']};color:{m['ink']};border-radius:44px;padding:44px 52px 56px;box-sizing:border-box">
<div style="{COND};font-size:80px;line-height:.95;letter-spacing:-1px">{t['title']}</div>
<div style="font-size:30px;font-weight:500;margin-top:16px;line-height:1.3">{t['sub']}</div></div>
<div style="position:absolute;left:740px;top:{1110+y0}px;width:120px;height:120px;border-radius:50%;background:#111;display:flex;align-items:center;justify-content:center;border:8px solid #ECEAE6">{ARROW}</div>
{pcr(m, n['cut'], '#8a8a8a', f'right:72px;top:{1290+y0}px')}''')

def cover_card(m, n, t, H=1350, y0=0, photoH=700):
    return page(1080, H, '#111', '#fff', f'''{top(m, 56 + y0, m['tag'])}
<img src="{PH}{n['photo']}" style="position:absolute;left:48px;top:{160+y0}px;width:984px;height:{photoH}px;object-fit:cover;object-position:50% 45%;border-radius:36px">
{f'<div style="position:absolute;left:96px;top:{90+photoH+y0}px;transform:rotate(-4deg);background:{m[chr(97)+"ccent"]};color:{m["ink"]};font-weight:900;font-size:96px;letter-spacing:-2px;padding:4px 26px 10px">{t["badgeC"]}</div>' if t['badgeC'] else ''}
<div style="position:absolute;left:72px;right:72px;top:{230+photoH+y0}px;display:flex;flex-direction:column;gap:22px">
<div style="{COND};font-size:{104 if max(len(t['title1']),len(t['title2']))<=16 else 86}px;line-height:.92;letter-spacing:-1px">{t['title1']}<br>{t['title2']}</div>
<div style="font-size:34px;font-weight:500;color:#d9d9d9">{t['sub']}</div></div>
{pcr(m, n['photo'], '#9e9e9e', f'right:72px;top:{174+photoH+y0}px')}
{'' if H != 1350 else f"""<div style="position:absolute;left:-40px;bottom:34px;width:1200px;height:56px;background:{m['accent']};transform:rotate(-2deg);display:flex;align-items:center;overflow:hidden;white-space:nowrap"><span style="{COND};font-size:30px;letter-spacing:2px;color:{m['ink']}">{m['tag']} ✦ {m['site']} ✦ {m['tag']} ✦ {m['site']} ✦ {m['tag']} ✦ {m['site']}</span></div>"""}''')

def cover_edit(m, n, t, H=1350, y0=0, topY=64, photoH=None):
    pt = n.get('ptop', 650)
    if photoH is None: photoH = 1350 - pt - 100 if pt != 650 else 600
    return page(1080, H, '#F6F5F2', '#111', f"""{top(m, topY, m['tag'])}
<div style="position:absolute;left:72px;right:72px;top:{190+y0}px">
<div style="{COND};font-size:96px;line-height:.92;letter-spacing:-1px;color:#111">{t['t1']} <span style="color:{m['accentText']}">{t['t2']}</span></div>
<div style="font-size:34px;font-weight:500;color:#444;margin-top:24px;max-width:860px;line-height:1.3">{t['sub']}</div></div>
<img src="{PH}{n['photo']}" style="position:absolute;left:48px;top:{pt+y0}px;width:984px;height:{photoH}px;object-fit:cover;object-position:50% 50%;border-radius:36px">
<div style="position:absolute;right:96px;top:{pt-50+y0}px;width:112px;height:112px;border-radius:50%;background:{m['accent']};display:flex;align-items:center;justify-content:center;border:8px solid #F6F5F2">{ARROW}</div>
{pcr(m, n['photo'], '#8a8a8a', f'right:72px;top:{pt+10+photoH+y0}px')}""")

# ---------- slides (theme follows the cover) ----------
def TH(n):
    if n['cover'] == 'dark':
        return dict(bg='#111', fg='#fff', line='#333', cr='#9e9e9e', sub='#e6e6e6', sub2='#bdbdbd')
    return dict(bg='#F6F5F2', fg='#111', line='#DDD9D2', cr='#8a8a8a', sub='#333', sub2='#666')

def slide_facts(m, n, t, idx, total):
    c = TH(n)
    items = ''.join(f'<div style="display:flex;gap:28px;align-items:baseline;padding:22px 0;border-top:2px solid {c["line"]}"><div style="{COND};font-size:48px;color:{m["accentText"]};min-width:70px">0{i+1}</div><div style="font-size:38px;font-weight:500;line-height:1.25">{s}</div></div>' for i, s in enumerate(t['items']))
    return page(1080, 1350, c['bg'], c['fg'], f'''{top(m, 56, f'0{idx} / 0{total}', 'pill', pfg=c['fg'])}
<img src="{PH}{n['photo2']}" style="position:absolute;left:48px;top:160px;width:984px;height:430px;object-fit:cover;object-position:{n.get('pos2','50% 50%')};border-radius:32px">
<div style="position:absolute;left:90px;top:540px;transform:rotate(-4deg);background:{m['accent']};color:{m['ink']};{COND};font-size:60px;padding:6px 24px 10px">{m['facts']}</div>
{pcr(m, n['photo2'], c['cr'], 'right:72px;top:604px')}
<div style="position:absolute;left:72px;right:72px;top:670px">{items}</div>
<div style="position:absolute;left:72px;bottom:56px;{CAV};font-size:52px;transform:rotate(-2deg)">{t['factsnote']}</div>''')

def slide_stat(m, n, t, idx, total):
    c = TH(n)
    unit = f'<span style="font-size:120px;letter-spacing:0">{t["bigunit"]}</span>' if t.get('bigunit') else ''
    return page(1080, 1350, c['bg'], c['fg'], f'''{top(m, 56, f'0{idx} / 0{total}', 'pill', pfg=c['fg'])}
<div style="position:absolute;left:60px;top:150px;{COND};font-size:340px;line-height:.9;letter-spacing:-10px;color:{m['accent']}">{t['big']}{unit}</div>
<div style="position:absolute;left:72px;top:480px;font-weight:700;font-size:32px;letter-spacing:3px;text-transform:uppercase">{t['bigcap']}</div>
<img src="{PH}{n.get('photo3', n['photo'])}" style="position:absolute;left:48px;top:560px;width:984px;height:470px;object-fit:cover;object-position:{n.get('pos3','50% 50%')};border-radius:32px">
{pcr(m, n.get('photo3', n['photo']), c['cr'], 'right:72px;top:1040px')}
<div style="position:absolute;left:72px;right:72px;bottom:80px;display:flex;flex-direction:column;gap:18px">
{f'<div style="display:flex;gap:18px;align-items:center;flex-wrap:wrap"><div style="background:{m["accent"]};color:{m["ink"]};font-weight:900;font-size:44px;padding:6px 18px">{t["badge"]}</div><div style="font-size:32px;font-weight:500;color:{c["sub"]}">{t["badgesub"]}</div></div>' if t.get('badge') else ''}
<div style="font-size:32px;font-weight:500;color:{c['sub2']}">{t['statsub']}</div></div>''')

def slide_cta(m, n, t, idx, total):
    c = TH(n)
    return page(1080, 1350, c['bg'], c['fg'], f'''{top(m, 56, f'0{idx} / 0{total}', 'pill', pfg=c['fg'])}
<img src="{PH}{n.get('photo4', n['photo'])}" style="position:absolute;left:48px;top:160px;width:984px;height:560px;object-fit:cover;object-position:50% 50%;border-radius:28px">
<div style="position:absolute;left:72px;top:690px;transform:rotate(-3deg);background:{m['accent']};color:{m['ink']};font-weight:900;font-size:34px;letter-spacing:2px;padding:10px 22px">{m['question']}</div>
{pcr(m, n.get('photo4', n['photo']), c['cr'], 'right:72px;top:732px')}
<div style="position:absolute;left:72px;right:72px;top:800px;{COND};font-size:{100 if len(t['q1']+t['q2'])<=40 else 80}px;line-height:.95;letter-spacing:-2px">{t['q1']} <span style="color:{m['accentText']}">{t['q2']}</span></div>
<div style="position:absolute;left:72px;top:1125px;{CAV};font-size:58px;transform:rotate(-2deg)">{m['comments']}</div>
''')

# ---------- stories 1080x1920 ----------
def story_cover(m, n, t):
    if n['cover'] == 'light':
        return cover_light(m, n, t, H=1920, y0=300, topY=230)
    if n['cover'] == 'edit':
        return cover_edit(m, n, t, H=1920, y0=200, topY=230, photoH=720 if n.get('ptop', 650) == 650 else 1460 - n['ptop'])
    return cover_card(m, n, t, H=1920, y0=180, photoH=760)

def story_facts(m, n, t, theme):
    dark = theme == 'dark'
    bg, fg, line, crc = ('#111', '#fff', '#333', '#9e9e9e') if dark else ('#F6F5F2', '#111', '#DDD9D2', '#8a8a8a')
    items = ''.join(f'<div style="display:flex;gap:28px;align-items:baseline;padding:22px 0;border-top:2px solid {line}"><div style="{COND};font-size:52px;color:{m["accentText"]};min-width:76px">0{i+1}</div><div style="font-size:40px;font-weight:500;line-height:1.25">{s}</div></div>' for i, s in enumerate(t['items']))
    return page(1080, 1920, bg, fg, f'''{top(m, 230, m['tag'])}
<img src="{PH}{n['photo2']}" style="position:absolute;left:48px;top:350px;width:984px;height:560px;object-fit:cover;object-position:{n.get('pos2','50% 50%')};border-radius:36px">
<div style="position:absolute;left:90px;top:860px;transform:rotate(-4deg);background:{m['accent']};color:{m['ink']};{COND};font-size:64px;padding:6px 26px 10px">{m['facts']}</div>
{pcr(m, n['photo2'], crc, 'right:72px;top:924px')}
<div style="position:absolute;left:72px;right:72px;top:1000px">{items}</div>
<div style="position:absolute;left:72px;top:1650px;{CAV};font-size:60px;transform:rotate(-2deg)">{m['more']}</div>''')

def story_final(m, thumbs):
    s = 0.42; w, h = round(1080*s), round(1350*s)
    th = ''.join(f'<img src="{u}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({r}deg);border-radius:22px;box-shadow:0 24px 60px rgba(0,0,0,.35)">' for u, x, y, r in [(thumbs[1], 560, 500, 5), (thumbs[0], 70, 470, -5)])
    return page(1080, 1920, m['accent'], m['ink'], f'''{top(m, 230, m['tag'], pbg='#111', pfg='#fff')}
<div style="position:absolute;left:72px;top:380px;font-weight:700;font-size:40px">{m['today']}</div>{th}
<div style="position:absolute;left:72px;right:72px;top:1150px"><div style="{COND};font-size:128px;line-height:.9;letter-spacing:-2px">{m['fin1']}<br>{m['fin2']}</div>
{f'<div style="{CAV};font-size:72px;margin-top:26px;transform:rotate(-2deg)">{m["finnote"]}</div>' if m['finnote'] else ''}</div>''')


# Moule du mail de la newsletter Content AI Influence (validé par Geoffrey le 29/09/2026).
# Transforme la page web d'un numéro en mail pour Gmail.
# Usage : python3 moule_mail.py page.html mail.html [lien de la page web]
# Besoin : Python 3 et BeautifulSoup (pip install beautifulsoup4).
# N'utilise que ce que l'outil d'envoi Gmail garde (test du 29/09/2026) : chaque réglage écrit sur l'élément,
# fonds en background-color ou bgcolor ; ni liste de styles en tête, ni classes, ni réglages par écran,
# ni dégradé, ni ombre, ni box-sizing, ni « background » en raccourci.
# Une seule mise en page : colonne de 640 px maximum, qui se resserre sur téléphone.
import sys, re, copy, datetime
sys.path.insert(0, 'pylib')
from bs4 import BeautifulSoup

ENTREE = sys.argv[1] if len(sys.argv) > 1 else 'newsletter.html'
SORTIE = sys.argv[2] if len(sys.argv) > 2 else 'mail.html'
LIEN_WEB = sys.argv[3] if len(sys.argv) > 3 else None   # par défaut : la page GitHub Pages du numéro
src = BeautifulSoup(open(ENTREE, encoding='utf-8').read(), 'html.parser')

D = "font-family:'Helvetica Neue',Arial,sans-serif;"
B = "-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif"
M = "font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;"
TON = {'t-tiktok':'#0E7490','t-meta':'#BE185D','t-youtube':'#B91C1C','t-ai':'#6D28D9','t-market':'#047857'}

S = {
 'web':    'font-size:13px;line-height:1.5;color:#8B93A1;padding:18px 0 0;text-align:right;',
 'mast':   'padding:30px 0 6px;text-align:center;',
 'h1':     D + 'font-size:31px;font-weight:800;line-height:1.1;letter-spacing:-0.025em;color:#15181F;margin:0 0 14px;text-align:center;',
 'meta':   'font-size:14px;line-height:1.5;color:#585F6D;margin:0 0 18px;text-align:center;',
 'metaN':  D + 'font-size:15px;font-weight:700;color:#15181F;',
 'theme':  D + 'font-size:11px;font-weight:700;line-height:1.3;color:#15181F;text-align:center;padding:7px 0 0;',
 'prog':   'background-color:#FAFAFB;border:1px solid #E7E9ED;border-radius:8px;padding:16px 20px 10px;margin:22px 0 0;',
 'progT':  D + 'font-size:15px;font-weight:800;color:#15181F;margin:0 0 6px;',
 'progL':  D + 'font-size:14.5px;font-weight:650;line-height:1.4;color:#15181F;padding:7px 0;',
 'progN':  D + 'font-size:12.5px;font-weight:500;line-height:1.4;color:#8B93A1;padding:7px 0 7px 10px;text-align:right;white-space:nowrap;',
 'sec':    'padding:46px 0 0;',
 'secL':   D + 'font-size:14.5px;font-weight:800;line-height:1.3;letter-spacing:0.08em;text-transform:uppercase;color:#15181F;padding:0 12px;white-space:nowrap;text-align:center;',
 'trait':  'height:2px;line-height:2px;font-size:0;background-color:#CDD2DA;',
 'secGap': 'height:28px;line-height:28px;font-size:0;',
 'fig':    'background-color:#FBF4E6;border:1px solid #E4CFA6;border-radius:8px;padding:28px 24px 16px;',
 'big':    D + 'font-size:64px;font-weight:900;line-height:1;letter-spacing:-0.04em;color:#EAA648;text-align:center;margin:0 0 14px;',
 'cap':    D + 'font-size:20px;font-weight:800;line-height:1.3;color:#15181F;text-align:center;margin:0 0 20px;',
 'figP':   'font-size:15.5px;line-height:1.72;color:#000919;margin:0 0 12px;',
 'head':   'border-left:4px solid #CDD2DA;padding:0 0 2px 18px;',
 'num':    D + 'font-size:13px;font-weight:800;letter-spacing:0.02em;',
 'filet':  'color:#CDD2DA;',
 'pill':   D + 'font-size:13px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;',
 'h3':     D + 'font-size:17.4px;font-weight:700;line-height:1.25;color:#15181F;margin:10px 0 0;',
 'srcTop': 'font-size:13.5px;line-height:1.5;color:#585F6D;margin:10px 0 0;',
 'blkGap': 'height:30px;line-height:30px;font-size:0;',
 'lab':    D + 'font-size:12.5px;font-weight:900;line-height:1.2;letter-spacing:0.15em;text-transform:uppercase;color:#C48A0E;margin:0 0 12px;',
 'p':      'font-size:16px;line-height:1.75;color:#2C313C;margin:0 0 12px;',
 'puce':   'font-size:9px;line-height:27px;color:#CDD2DA;',
 'li':     'font-size:16px;line-height:1.6;color:#2C313C;padding:0 0 10px;',
 'liB':    D + 'font-weight:650;color:#15181F;',
 'liS':    'font-size:14.5px;color:#585F6D;',
 'act':    'background-color:#FFF8EB;border-left:4px solid #8F5A0E;border-radius:0 16px 16px 0;padding:20px 20px 8px;',
 'quote':  D + 'font-size:17px;font-weight:600;line-height:1.5;color:#15181F;margin:0 0 12px;',
 'more':   'font-size:13.5px;line-height:1.6;color:#8B93A1;margin:24px 0 0;',
 'item':   'padding:0 0 36px;',
 'item2':  'border-top:1px solid #E7E9ED;padding:36px 0;',
 'empty':  'font-size:14.5px;line-height:1.72;color:#585F6D;background-color:#FAFAFB;border:1px dashed #CDD2DA;border-radius:8px;padding:24px 22px 12px;',
 'emptyT': D + 'font-size:17px;font-weight:700;color:#15181F;margin:0 0 12px;',
 'emptyP': 'margin:0 0 12px;',
 'brief':  'padding:22px 0;border-bottom:1px solid #E7E9ED;',
 'bH':     D + 'font-size:17px;font-weight:700;line-height:1.38;color:#15181F;margin:8px 0 8px;',
 'bP':     'font-size:15px;line-height:1.72;color:#585F6D;margin:0 0 5px;',
 'bL':     'font-size:13.5px;line-height:1.6;margin:6px 0 0;',
 'tool':   'background-color:#FAFAFB;border:1px solid #E7E9ED;border-radius:8px;padding:26px 24px 12px;',
 'toolH':  D + 'font-size:22px;font-weight:700;letter-spacing:-0.02em;color:#15181F;margin:0 0 12px;text-align:center;',
 'verd':   'text-align:center;margin:0 0 18px;',
 'verdS':  D + 'display:inline-block;font-size:11px;font-weight:700;letter-spacing:0.11em;text-transform:uppercase;color:#047857;background-color:#ECF8F3;border:1px solid #9FD4BE;border-radius:999px;padding:4px 11px;white-space:nowrap;',
 'toolP':  'font-size:16.5px;line-height:1.7;color:#2C313C;margin:0 0 14px;',
 'why':    'font-size:15px;line-height:1.75;color:#18191B;margin:0 0 14px;',
 'arch':   'background-color:#FAFAFB;border:1px solid #E7E9ED;border-radius:8px;padding:24px 22px 20px;',
 'archGap':'height:20px;line-height:20px;font-size:0;',
 'archH':  D + 'font-size:19px;font-weight:700;line-height:1.3;color:#15181F;margin:0 0 20px;text-align:center;',
 'lbl':    D + 'font-size:12.5px;font-weight:800;line-height:1.2;letter-spacing:0.15em;text-transform:uppercase;color:#D3884A;margin:0 0 9px;',
 'aP':     'font-size:15px;line-height:1.72;color:#050C1A;margin:0 0 9px;',
 'aLi':    'font-size:15px;line-height:1.6;color:#050C1A;padding:0 0 8px;',
 'field':  'padding:0 0 16px;',
 'path':   M + 'font-size:12px;line-height:1.65;color:#8F5A0E;background-color:#FBF4E6;border:1px solid #E4CFA6;border-radius:4px;padding:10px 12px;',
 'trig':   D + 'font-size:14.5px;font-weight:600;line-height:1.5;color:#010B1E;margin:0;padding:16px 0 0;border-top:1px solid #E7E9ED;',
 'code':   M + 'font-size:12.5px;color:#8F5A0E;background-color:#FBF4E6;border:1px solid #E4CFA6;border-radius:3px;padding:2px 6px;',
 'watch':  'padding:18px 0;border-bottom:1px solid #E7E9ED;',
 'when':   D + 'font-size:15.5px;font-weight:700;line-height:1.5;color:#8F5A0E;margin:0 0 4px;',
 'what':   'font-size:16px;line-height:1.6;color:#000000;margin:0;',
 'small':  'font-size:13px;line-height:1.65;color:#585F6D;margin:6px 0 0;',
 'wSrc':   'font-size:13.5px;line-height:1.5;margin:8px 0 0;',
 'foot':   'font-size:13px;line-height:1.72;color:#8B93A1;margin:52px 0 0;padding:22px 0 0;border-top:1px solid #E7E9ED;',
 'footP':  'margin:0 0 9px;',
 'l':      'color:#8F5A0E;text-decoration:none;border-bottom:1px solid #E4CFA6;',
 'ld':     'color:#585F6D;text-decoration:none;border-bottom:1px solid #CDD2DA;',
}
st = lambda k, extra='': f' style="{S[k]}{extra}"'
T = lambda inner, extra='': f'<table width="100%" cellpadding="0" cellspacing="0" border="0"{extra}>{inner}</table>'

def bord(style, i, n):
    # Première ligne sans espace au-dessus, dernière sans trait ni espace en dessous
    esp = re.search(r'padding:(\d+)px 0;', style).group(1)
    if i == n - 1: return re.sub(r'padding:\d+px 0;border-bottom:[^;]*;', f'padding:{esp}px 0 0;' if i else 'padding:0;', style)
    if i == 0: return style.replace(f'padding:{esp}px 0;', f'padding:0 0 {esp}px;')
    return style

def inl(el, doux=False):
    el = copy.copy(el)
    for x in el.find_all('a'): x.attrs = {'href': x.get('href'), 'style': S['ld' if doux else 'l']}
    for x in el.find_all('code'): x.attrs = {'style': S['code']}
    for x in el.find_all('strong'): x.attrs = {'style': 'font-weight:700;'}
    return el.decode_contents().strip()

def rubrique(titre, contenu, count=None):
    trait = f'<div{st("trait")}>&nbsp;</div>'
    c = f' <span style="color:#8B93A1;font-weight:600;letter-spacing:0.06em;">{count}</span>' if count else ''
    return (f'<tr><td{st("sec")}>' + T(f'<tr><td width="50%" valign="middle">{trait}</td><td valign="middle" align="center"{st("secL")}>{titre}{c}</td>'
            f'<td width="50%" valign="middle">{trait}</td></tr>') + f'<div{st("secGap")}>&nbsp;</div>{contenu}</td></tr>')

def liste(ul, role='li', archive=False):
    rows = ''
    for li in ul.find_all('li', recursive=False):
        b, s = li.find('b'), li.find('span')
        txt = (f'<span{st("liB")}>{inl(b)}</span>' + (f' &nbsp;<span{st("liS")}>{inl(s)}</span>' if s else '')) if (b and not archive) else inl(li)
        rows += f'<tr><td width="16" valign="top"{st("puce")}>&#9679;</td><td{st(role)}>{txt}</td></tr>'
    return T(rows, ' style="margin:0 0 6px;"')

def paras(blk, action=False):
    out = ''
    for x in blk.find_all(['p', 'ul'], recursive=False):
        cl = x.get('class', [])
        if 'blk-label' in cl: out += f'<p style="{S["lab"].replace("#C48A0E", "#8F5A0E") if action else S["lab"]}">{inl(x)}</p>'
        elif 'quote' in cl:   out += f'<p{st("quote")}>{inl(x)}</p>'
        elif x.name == 'ul':  out += liste(x)
        else:                 out += f'<p{st("p")}>{inl(x)}</p>'
    return out

# ─── En-tête : titre, ligne d'infos, bulles des thèmes ───
titre = src.h1.get_text()
themes = [t.get_text().strip() for t in src.select('.meta-theme')]
EMO = {'Ads':'📣', 'Organique':'🌱', 'Influence':'🤝', 'UGC':'🎥', 'IA':'🤖'}
bulle = lambda e: (f'<table cellpadding="0" cellspacing="0" border="0" align="center"><tr><td width="52" height="52" align="center" valign="middle" bgcolor="#C27C12" style="border-radius:50%;">'
                   f'<table cellpadding="0" cellspacing="0" border="0"><tr><td width="42" height="42" align="center" valign="middle" bgcolor="#FBF4E6" '
                   f'style="border:2px solid #FFFFFF;border-radius:50%;font-size:20px;line-height:42px;">{e}</td></tr></table></td></tr></table>')
bulles = ''.join(f'<td width="20%" align="center" valign="top" style="padding:0 2px;">{bulle(EMO.get(t, "•"))}<div{st("theme")}>{t}</div></td>' for t in themes)
entete = (f'<tr><td{st("mast")}><h1{st("h1")}>{titre}</h1>'
          f'<p{st("meta")}><span{st("metaN")}>Formats courts</span>&nbsp;&nbsp;·&nbsp;&nbsp;⏱ 10 min de lecture</p>'
          + T(f'<tr>{bulles}</tr>', ' style="max-width:380px;" align="center"') + '</td></tr>')

prog = ''.join(f'<tr><td width="28"{st("progL")}>{x.select_one(".bandeau-emoji").get_text()}</td><td{st("progL")}>{x.select_one(".bandeau-nom").get_text()}</td>'
               f'<td{st("progN")}>{x.small.get_text()}</td></tr>' for x in src.select('.bandeau-liste a'))
programme = f'<tr><td><div{st("prog")}><p{st("progT")}>Au programme · {len(src.select(".bandeau-liste a"))} rubriques</p>{T(prog)}</div></td></tr>'

# ─── Rubriques ───
corps = ''
for sec in src.select('section'):
    lab = sec.select_one('.sec-label'); cnt = lab.select_one('.count')
    if cnt: cnt.extract()
    nom = lab.get_text().strip(); sid = sec.get('id'); h = ''
    if sid == 'chiffre':
        f = sec.select_one('.figure')
        h = (f'<div{st("fig")}><p{st("big")}>{f.select_one(".big").get_text()}</p><p{st("cap")}>{f.select_one(".cap").get_text()}</p>'
             + ''.join(f'<p{st("figP")}>{inl(p)}</p>' for p in f.find_all('p', recursive=False)) + '</div>')
    elif sid == 'items':
        for i, it in enumerate(sec.select('article.item')):
            pill = it.select_one('.pill'); ton = next(TON[c] for c in pill['class'] if c in TON)
            tete = (f'<div{st("head", f"border-left-color:{ton};")}><span{st("num", f"color:{ton};")}>{it.select_one(".num").get_text()}</span>'
                    f'<span{st("filet")}>&nbsp;&nbsp;|&nbsp;&nbsp;</span><span{st("pill", f"color:{ton};")}>{pill.get_text()}</span>'
                    f'<h3{st("h3")}>{inl(it.h3)}</h3><p{st("srcTop")}>{inl(it.select_one(".src-top"))}</p></div>')
            blocs = ''
            for blk in it.select('.item-body > .blk'):
                blocs += f'<div{st("blkGap")}>&nbsp;</div>'
                blocs += f'<div{st("act")}>{paras(blk, True)}</div>' if 'blk-action' in blk['class'] else paras(blk)
            more = it.select_one('.src-more')
            more = f'<p{st("more")}>{inl(more, doux=True)}</p>' if more else ''
            h += f'<div{st("item" if i == 0 else "item2")}>{tete}{blocs}{more}</div>'
    elif sid == 'campagne':
        e = sec.select_one('.empty')
        h = f'<div{st("empty")}><p{st("emptyT")}>{e.strong.get_text()}</p>' + ''.join(f'<p{st("emptyP")}>{inl(p)}</p>' for p in e.find_all('p')) + '</div>'
    elif sid == 'bref':
        br = sec.select('.brief')
        for i, b in enumerate(br):
            pill = b.select_one('.pill'); ton = next(TON[c] for c in pill['class'] if c in TON)
            h += (f'<div style="{bord(S["brief"], i, len(br))}"><span{st("pill", f"color:{ton};")}><span style="font-size:10px;">&#9679;</span>&nbsp; {pill.get_text()}</span>'
                  f'<p{st("bH")}>{inl(b.h4)}</p>'
                  + ''.join(f'<p{st("bL" if "lnk" in p.get("class", []) else "bP")}>{inl(p)}</p>' for p in b.find_all('p')) + '</div>')
    elif sid == 'outil':
        t = sec.select_one('.tool')
        h = (f'<div{st("tool")}><p{st("toolH")}>{t.h3.get_text()}</p><p{st("verd")}><span{st("verdS")}>{t.select_one(".verdict").get_text()}</span></p>'
             + ''.join(liste(p, 'why') if p.name == 'ul' else f'<p{st("why" if "why" in p.get("class", []) else "toolP")}>{inl(p)}</p>' for p in t.find_all(['p', 'ul'], recursive=False)) + '</div>')
    elif sid == 'archive':
        for i, c in enumerate(sec.select('.arch-card')):
            if i: h += f'<div{st("archGap")}>&nbsp;</div>'
            champs = ''
            for fl in c.select('.arch-field'):
                inner = ''
                for x in fl.find_all(['p', 'ul', 'div'], recursive=False):
                    if 'lbl' in x.get('class', []): inner += f'<p{st("lbl")}>{x.get_text()}</p>'
                    elif 'path' in x.get('class', []): inner += f'<div{st("path")}>{x.get_text().strip().replace(chr(10), "<br>")}</div>'
                    elif x.name == 'ul': inner += liste(x, 'aLi', archive=True)
                    else: inner += f'<p{st("aP")}>{inl(x)}</p>'
                champs += f'<div{st("field")}>{inner}</div>'
            h += f'<div{st("arch")}><p{st("archH")}>{c.h4.get_text()}</p>{champs}<p{st("trig")}>{inl(c.select_one(".trigger"))}</p></div>'
    elif sid == 'surveiller':
        lis = sec.select('.watch > li')
        for i, li in enumerate(lis):
            w = li.select_one('.what'); sm = w.small.extract(); s = w.select_one('.src').extract()
            h += (f'<div style="{bord(S["watch"], i, len(lis))}"><p{st("when")}>{inl(li.select_one(".when"))}</p><p{st("what")}>{w.get_text().strip()}</p>'
                  f'<p{st("small")}>{sm.get_text()}</p><p{st("wSrc")}>{inl(s)}</p></div>')
    corps += rubrique(nom, h, cnt.get_text() if cnt else None)

jour = datetime.datetime.strptime(re.search(r'\d{2}/\d{2}/\d{4}', titre).group(0), '%d/%m/%Y')
suivant = jour + datetime.timedelta(days=(7 - jour.weekday()) or 7)   # le lundi suivant
LIEN_WEB = LIEN_WEB or f'https://geoffreymoreno.github.io/content-ai-influence/numeros/{jour:%Y-%m-%d}.html'
MOIS = ['janvier','février','mars','avril','mai','juin','juillet','août','septembre','octobre','novembre','décembre']
pied = (f'<tr><td><div{st("foot")}><p{st("footP")}><strong style="color:#585F6D;">Newsletter Content-AI-Influence</strong> · numéro du {jour:%d/%m/%Y} · prochain numéro lundi {suivant.day} {MOIS[suivant.month - 1]} vers 6 h.</p>'
        f'<p{st("footP")}><a href="{LIEN_WEB}"{st("l")}>Lire ce numéro en version web →</a></p>'
        f'<p{st("footP")}>Sources FR et EN, restituées en français.</p></div></td></tr>')

fig = src.select_one('.figure')
apercu = f"{fig.select_one('.big').get_text()} {fig.select_one('.cap').get_text()} · {src.select_one('article.item h3').get_text()} · 10 min de lecture"
html = (f'<div style="display:none;max-height:0;overflow:hidden;">{apercu}{"&#847;&zwnj;&nbsp;" * 30}</div>'
        f'<table width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#FFFFFF"><tr><td align="center" style="padding:0 18px;">'
        f'<table width="640" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:640px;"><tr><td style="font-family:{B};color:#2C313C;text-align:left;">'
        + T(f'<tr><td{st("web")}><a href="{LIEN_WEB}"{st("l")}>Lire en version web →</a></td></tr>' + entete + programme + corps + pied)
        + '</td></tr></table></td></tr></table>')

# ─── Contrôle : uniquement des propriétés que l'outil d'envoi a gardées au test du 29/09/2026 ───
GARDEES = {'padding','padding-top','padding-bottom','padding-left','margin','font-family','font-size','font-weight','line-height','letter-spacing',
           'text-transform','text-align','color','background-color','border','border-left','border-left-color','border-top','border-bottom',
           'border-radius','white-space','display','max-height','overflow','width','max-width','height','text-decoration'}
props = {d.split(':')[0].strip() for s in re.findall(r'style="([^"]*)"', html) for d in s.split(';') if d.strip()}
assert props <= GARDEES, f'propriétés non testées : {props - GARDEES}'
assert '<style' not in html and 'class=' not in html
open(SORTIE, 'w', encoding='utf-8').write(html)
print('poids', len(html.encode('utf-8')), 'octets ; propriétés', sorted(props))

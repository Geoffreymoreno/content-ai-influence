# Moule de la note Obsidian d'un numéro (validé par Geoffrey le 29/09/2026) : transforme la page web d'un numéro en Markdown.
# Usage : python3 moule_note.py page.html note.md [lien de la page web] [numéro]
# Besoin : Python 3 et BeautifulSoup (pip install beautifulsoup4).
import sys, re, copy
sys.path.insert(0, 'pylib')
from bs4 import BeautifulSoup, NavigableString

ENTREE = sys.argv[1] if len(sys.argv) > 1 else 'newsletter.html'
SORTIE = sys.argv[2] if len(sys.argv) > 2 else 'note.md'
LIEN_WEB = sys.argv[3] if len(sys.argv) > 3 else None   # par défaut : la page GitHub Pages du numéro
NUMERO = sys.argv[4] if len(sys.argv) > 4 else '0'
src = BeautifulSoup(open(ENTREE, encoding='utf-8').read(), 'html.parser')
PLATEFORME = {'t-tiktok':'TikTok', 't-meta':'Meta', 't-youtube':'YouTube', 't-ai':'IA', 't-market':'Marché'}

def md(el):
    """Texte d'un élément en Markdown : gras, italique, liens, code."""
    out = ''
    for c in el.children:
        if isinstance(c, NavigableString): out += str(c)
        elif c.name in ('strong', 'b'): out += f'**{md(c).strip()}**'
        elif c.name == 'em': out += f'*{md(c).strip()}*'
        elif c.name == 'a': out += f'[{md(c).strip()}]({c.get("href")})'
        elif c.name == 'code': out += f'`{c.get_text()}`'
        elif c.name == 'sup': out += md(c)
        elif c.name == 'br': out += '\n'
        else: out += md(c)
    return re.sub(r'[ \t]+', ' ', out.replace(' ', ' ')).strip()

def liste(ul, archive=False):
    L = []
    for li in ul.find_all('li', recursive=False):
        b, s = li.find('b'), li.find('span')
        L.append(f'- **{md(b)}** — {md(s)}' if (b and s and not archive) else f'- {md(li)}')
    return '\n'.join(L)

def blocs(blk):
    """Paragraphes, listes et citations d'un bloc, séparés par une ligne vide."""
    P = []
    for x in blk.find_all(['p', 'ul'], recursive=False):
        cl = x.get('class', [])
        if 'blk-label' in cl: continue
        P.append(liste(x) if x.name == 'ul' else (f'*{md(x)}*' if 'quote' in cl else md(x)))
    return P

titre = src.h1.get_text()
jour = re.search(r'(\d{2})/(\d{2})/(\d{4})', titre)
iso = f'{jour.group(3)}-{jour.group(2)}-{jour.group(1)}'
LIEN_WEB = LIEN_WEB or f'https://geoffreymoreno.github.io/content-ai-influence/numeros/{iso}.html'
themes = [t.get_text().strip() for t in src.select('.meta-theme')]
fig = src.select_one('.figure')
plats = []
for p in src.select('.pill'):
    for c in p['class']:
        if c in PLATEFORME and PLATEFORME[c] not in plats: plats.append(PLATEFORME[c])

N = []
N.append('---')
N.append('type: newsletter')
N.append(f'date: {iso}')
N.append(f'numero: {NUMERO}')
N.append(f'lien_web: {LIEN_WEB}')
N.append(f'chiffre: "{fig.select_one(".big").get_text()} {fig.select_one(".cap").get_text()}"')
N.append('plateformes:'); N += [f'  - {p}' for p in plats]
N.append('tags:\n  - newsletter')
N.append('---\n')
N.append(f'# {titre}\n')
N.append(f'> [!info] Formats courts · 10 min de lecture\n> 🌐 [Lire la version web]({LIEN_WEB})\n>\n> Thèmes : {" · ".join(themes)}\n')

# Au programme : liens vers les titres de cette note
secs = src.select('section')
def nom(sec):
    lab = copy.copy(sec.select_one('.sec-label'))
    for c in lab.select('.count'): c.extract()
    return lab.get_text().strip().upper()   # grandes parties en majuscules (note Obsidian uniquement)
courts = {x.get('href')[1:]: x.get_text().strip() for x in src.select('.toc-inner a')}
N.append('**Au programme** : ' + ' · '.join(f'[[#{nom(s)}|{courts.get(s.get("id"), nom(s))}]]' for s in secs) + '\n')

for sec in secs:
    sid = sec.get('id')
    N.append('---\n')
    N.append(f'## {nom(sec)}\n')
    if sid == 'chiffre':
        N.append(f'### {fig.select_one(".big").get_text()}\n')
        N.append(f'**{fig.select_one(".cap").get_text()}**\n')
        N += [md(p) + '\n' for p in fig.find_all('p', recursive=False)]
    elif sid == 'items':
        for i, it in enumerate(sec.select('article.item')):
            if i: N.append('---\n')
            N.append(f'### {it.select_one(".num").get_text()} · {md(it.h3)}\n')
            N.append(f'**{it.select_one(".pill").get_text()}** · source : ' + md(it.select_one('.src-top')).lstrip('→ ') + '\n')
            for blk in it.select('.item-body > .blk'):
                lab = blk.select_one('.blk-label').get_text()
                P = blocs(blk)
                if 'blk-action' in blk['class']:
                    N.append(f'> [!tip] {lab}\n' + '\n>\n'.join('> ' + p.replace('\n', '\n> ') for p in P) + '\n')
                else:
                    N.append(f'**{lab}**\n')
                    N += [p + '\n' for p in P]
            more = it.select_one('.src-more')
            if more: N.append(md(more) + '\n')
    elif sid == 'campagne':
        e = sec.select_one('.empty')
        N.append(f'> [!note] {e.strong.get_text()}\n' + '\n>\n'.join('> ' + md(p) for p in e.find_all('p')) + '\n')
    elif sid == 'bref':
        for b in sec.select('.brief'):
            N.append(f'### {md(b.h4)}\n')
            N.append(f'**{b.select_one(".pill").get_text()}**\n')
            N += [md(p) + '\n' for p in b.find_all('p') if 'lnk' not in p.get('class', [])]
            N.append('→ ' + md(b.select_one('.lnk')) + '\n')
    elif sid == 'outil':
        t = sec.select_one('.tool')
        N.append(f'### {t.h3.get_text()}\n')
        N.append(f'**Verdict : {t.select_one(".verdict").get_text()}**\n')
        N += [(liste(p) if p.name == 'ul' else md(p)) + '\n' for p in t.find_all(['p', 'ul'], recursive=False)]
    elif sid == 'archive':
        for c in sec.select('.arch-card'):
            N.append(f'### {c.h4.get_text()}\n')
            for fl in c.select('.arch-field'):
                for x in fl.find_all(['p', 'ul', 'div'], recursive=False):
                    cl = x.get('class', [])
                    if 'lbl' in cl: N.append(f'**{x.get_text()}**\n')
                    elif 'path' in cl: N.append('`' + ''.join(x.get_text().split('\n')) + '`\n')
                    elif x.name == 'ul': N.append(liste(x, archive=True) + '\n')
                    else: N.append(md(x) + '\n')
            N.append(md(c.select_one('.trigger')) + '\n')
    elif sid == 'surveiller':
        for li in sec.select('.watch > li'):
            w = copy.copy(li.select_one('.what')); sm = w.small.extract(); s = w.select_one('.src').extract()
            N.append(f'**{md(li.select_one(".when"))}** · {md(w)}\n')
            N.append(f'*{md(sm)}* → {md(s)}\n')

N.append('---\n')
N.append(f'*Newsletter Content-AI-Influence — numéro du {titre[-10:]}. Sources FR et EN, restituées en français. [Version web]({LIEN_WEB})*\n')
texte = re.sub(r'\n{3,}', '\n\n', '\n'.join(N))
open(SORTIE, 'w', encoding='utf-8').write(texte)
print(SORTIE, len(texte.split('\n')), 'lignes')

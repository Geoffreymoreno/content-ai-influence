# Assemble la page web d'un numéro à partir de son contenu, puis refait la page d'accueil.
# Usage : python3 outils/assembler.py contenu/AAAA-MM-JJ.html
# Écrit numeros/AAAA-MM-JJ.html et index.html. Il faut BeautifulSoup (pip install beautifulsoup4).
import os, re, sys
from bs4 import BeautifulSoup

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
chemin = sys.argv[1]
iso = re.search(r'\d{4}-\d{2}-\d{2}', chemin).group(0)
a, m, j = iso.split('-')
titre = f'Newsletter {j}/{m}/{a}'
contenu = open(chemin, encoding='utf-8').read()
src = BeautifulSoup(contenu, 'html.parser')

# Rubriques, dans l'ordre de la page : (id, emoji, nom long, nom court du sommaire, repère)
def pluriel(n, mot):
    return f'{n} {mot}' + ('s' if n > 1 else '')

def repere(sec):
    i = sec['id']
    if i == 'chiffre':
        return sec.select_one('.big').get_text().strip()
    if i == 'items':
        return pluriel(len(sec.select('.item')), 'sujet')
    if i == 'campagne':
        return '1 analyse'
    if i == 'bref':
        return pluriel(len(sec.select('.brief')), 'brève')
    if i == 'outil':
        return sec.select_one('.tool-top h3').get_text().strip().split(' avec ')[0]
    if i == 'archive':
        return pluriel(len(sec.select('.arch-card')), 'note')
    if i == 'surveiller':
        return pluriel(len(sec.select('.when')), 'date')
    return ''

COURT = {'chiffre': 'Chiffre', 'campagne': 'Campagne', 'bref': 'News en bref', 'outil': 'Outil',
         'archive': 'Archive', 'surveiller': 'Sorties à surveiller'}
toc, bandeau = [], []
for sec in src.find_all('section'):
    lab = sec.select_one('.sec-label')
    for c in lab.select('.count'):
        c.decompose()
    emoji, nom = lab.get_text().strip().split(' ', 1)
    court = f'Les {len(sec.select(".item"))} news' if sec['id'] == 'items' else COURT[sec['id']]
    toc.append(f'      <a href="#{sec["id"]}">{emoji} {court}</a>')
    bandeau.append(f'      <a href="#{sec["id"]}"><span class="bandeau-emoji" aria-hidden="true">{emoji}</span>'
                   f'<span class="bandeau-nom">{nom}</span><small>{repere(sec)}</small></a>')

page = open(os.path.join(RACINE, 'gabarit', 'page.html'), encoding='utf-8').read()
page = (page.replace('{{TITRE}}', titre).replace('{{TOC}}', '\n'.join(toc)).replace('{{N}}', str(len(toc)))
            .replace('{{BANDEAU}}', '\n'.join(bandeau)).replace('{{CONTENU}}', contenu.rstrip('\n')))
os.makedirs(os.path.join(RACINE, 'numeros'), exist_ok=True)
open(os.path.join(RACINE, 'numeros', f'{iso}.html'), 'w', encoding='utf-8').write(page)

# Page d'accueil : tous les numéros, du plus récent au plus ancien
ESSAIS = {'2026-09-29.html': "Numéro d'essai", '2026-09-30.html': 'Essai du robot'}
accueil = open(os.path.join(RACINE, 'index.html'), encoding='utf-8').read()
lignes = []
for f in sorted(os.listdir(os.path.join(RACINE, 'numeros')), reverse=True):
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}\.html', f):
        y, mo, d = f[:10].split('-')
        note = ESSAIS.get(f, 'Lire')
        lignes.append(f'    <li><a href="numeros/{f}"><span class="titre">Newsletter {d}/{mo}/{y}</span>'
                      f'<span class="note">{note} <span class="fleche">→</span></span></a></li>')
accueil = re.sub(r'(<ul>\n).*?(\n  </ul>)', lambda x: x.group(1) + '\n'.join(lignes) + x.group(2), accueil, count=1, flags=re.S)
open(os.path.join(RACINE, 'index.html'), 'w', encoding='utf-8').write(accueil)
print(f'numeros/{iso}.html écrit ({len(toc)} rubriques), index.html à jour')

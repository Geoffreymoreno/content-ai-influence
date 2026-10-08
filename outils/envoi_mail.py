# Envoie un mail de la newsletter par le serveur de Gmail.
# Usage : python3 outils/envoi_mail.py mails/AAAA-MM-JJ.html ["Objet"]
# Adresses et mot de passe d'application : secrets GitHub, jamais écrits dans le dépôt.
# MAIL_DESTINATAIRE est un carnet « prénom=adresse », séparé par des virgules
# (une adresse sans prénom est acceptée). MAIL_POUR, facultatif, choisit des prénoms
# du carnet (« anthony », « geoffrey, anthony ») ; vide, le mail part à tout le carnet.
import os, sys, re, html, smtplib
from email.message import EmailMessage

chemin = sys.argv[1]
a, m, j = re.search(r'(\d{4})-(\d{2})-(\d{2})', chemin).groups()
page = open(chemin, encoding='utf-8').read()
note = re.match(r'\s*<!-- objet: (.+?) -->', page)   # objet imposé par le fichier (mails de test)
objet = (sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] else None) or (note.group(1) if note else f'Newsletter {j}/{m}/{a}')

texte = re.sub(r'<div style="display:none.*?</div>', '', page, count=1, flags=re.S)
texte = re.sub(r'</(p|h1|h3|tr|div)>', '\n', texte)
texte = html.unescape(re.sub(r'<[^>]+>', '', texte))
texte = re.sub(r'\n\s*\n+', '\n\n', texte).strip()

exp = os.environ['MAIL_EXPEDITEUR']
carnet = {}
for i, entree in enumerate(e.strip() for e in os.environ['MAIL_DESTINATAIRE'].split(',')):
    if entree:
        nom, _, adresse = entree.rpartition('=')
        carnet[nom.strip().lower() or f'adresse {i + 1}'] = adresse.strip()
pour = [n.strip().lower() for n in os.environ.get('MAIL_POUR', '').split(',') if n.strip()]
inconnus = [n for n in pour if n not in carnet]
if inconnus:
    sys.exit(f'Rien n\'est envoyé : prénom absent du carnet ({", ".join(inconnus)}). '
             f'Prénoms connus : {", ".join(carnet)}.')
dest = ', '.join(carnet[n] for n in (pour or carnet))
msg = EmailMessage()
msg['From'] = f'Content AI Influence <{exp}>'
msg['To'] = dest
msg['Subject'] = objet
msg.set_content(texte)
msg.add_alternative(page, subtype='html')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
    s.login(exp, os.environ['GMAIL_APP_PASSWORD'].replace(' ', ''))
    s.send_message(msg)
print('Envoyé :', objet, '→', ', '.join(pour or carnet))

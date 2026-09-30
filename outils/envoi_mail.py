# Envoie un mail de la newsletter par le serveur de Gmail.
# Usage : python3 outils/envoi_mail.py mails/AAAA-MM-JJ.html ["Objet"]
# Adresses et mot de passe d'application : secrets GitHub, jamais écrits dans le dépôt.
import os, sys, re, html, smtplib
from email.message import EmailMessage

chemin = sys.argv[1]
a, m, j = re.search(r'(\d{4})-(\d{2})-(\d{2})', chemin).groups()
objet = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] else f'Newsletter {j}/{m}/{a}'
page = open(chemin, encoding='utf-8').read()

texte = re.sub(r'<div style="display:none.*?</div>', '', page, count=1, flags=re.S)
texte = re.sub(r'</(p|h1|h3|tr|div)>', '\n', texte)
texte = html.unescape(re.sub(r'<[^>]+>', '', texte))
texte = re.sub(r'\n\s*\n+', '\n\n', texte).strip()

exp, dest = os.environ['MAIL_EXPEDITEUR'], os.environ['MAIL_DESTINATAIRE']
msg = EmailMessage()
msg['From'] = f'Content AI Influence <{exp}>'
msg['To'] = dest
msg['Subject'] = objet
msg.set_content(texte)
msg.add_alternative(page, subtype='html')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
    s.login(exp, os.environ['GMAIL_APP_PASSWORD'].replace(' ', ''))
    s.send_message(msg)
print('Envoyé :', objet)

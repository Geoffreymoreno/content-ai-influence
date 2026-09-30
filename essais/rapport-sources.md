# Rapport de lecture des sources — Essai routine 3

Date : 2026-09-30
User-Agent utilisé : `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36`

## 1. Flux RSS/Atom (35 adresses)

Mesure : `curl -s -o /tmp/f -m 25 -w '%{http_code}' -A '<UA>' URL` puis `grep -c -E '<item[ >]|<entry[ >]' /tmp/f`.
En cas de code `000` ou `403`, un `curl -sv` complémentaire a été lancé pour distinguer un refus au CONNECT (filtre réseau) d'un refus du site lui-même.

| Adresse | Code HTTP | Articles | Statut |
|---|---|---|---|
| https://about.fb.com/feed/ | 200 | 10 | OK |
| https://blog.google/rss/ | 200 | 1 | OK |
| https://blog.youtube/rss/ | 200 | 1 | OK |
| https://datareportal.com/home?format=rss | 200 | 0 | OK (flux vide) |
| https://digiday.com/feed/ | 200 | 15 | OK |
| https://fr.themedialeader.com/feed/ | 200 | 20 | OK |
| https://huggingface.co/blog/feed.xml | 200 | 870 | OK |
| https://lbbonline.com/news/feed | 200 | 20 | OK |
| https://liahaberman.substack.com/feed | 200 | 8 | OK |
| https://musebyclios.com/feed/ | 403 | 0 | refusé par le site (Cloudflare, réponse HTTP/2 403 directe, pas de blocage au CONNECT) |
| https://openai.com/news/rss.xml | 200 | 1239 | OK |
| https://passionfru.it/feed/ | 200 | 10 | OK |
| https://reutersinstitute.politics.ox.ac.uk/rss.xml | 200 | 10 | OK |
| https://siecledigital.fr/feed/ | 200 | 20 | OK |
| https://simonwillison.net/atom/everything/ | 200 | 30 | OK |
| https://techcrunch.com/feed/ | 200 | 20 | OK |
| https://the-decoder.com/feed/ | 200 | 10 | OK |
| https://variety.com/feed/rss/ | 301 | 0 | redirection non suivie (vers /feed/, ni bloqué ni refusé) |
| https://www.adweek.com/feed/ | 200 | 10 | OK |
| https://www.blogdumoderateur.com/feed/ | 200 | 30 | OK |
| https://www.cbnews.fr/rss.xml | 200 | 10 | OK |
| https://www.creativereview.co.uk/feed/ | 403 | 0 | refusé par le site (Cloudflare, challenge anti-bot, pas de blocage au CONNECT) |
| https://www.frandroid.com/feed | 200 | 15 | OK |
| https://www.iab.com/feed/ | 200 | 10 | OK |
| https://www.influencia.net/feed/ | 200 | 10 | OK |
| https://www.journaldunet.com/rss/ | 200 | 1 | OK |
| https://www.marketingdive.com/feeds/news/ | 200 | 1 | OK |
| https://www.nielsen.com/feed/ | 200 | 0 | OK (flux vide) |
| https://www.numerama.com/feed | 301 | 0 | redirection non suivie (vers /feed/, ni bloqué ni refusé) |
| https://www.pewresearch.org/feed/ | 200 | 100 | OK |
| https://www.platformer.news/rss/ | 200 | 1 | OK |
| https://www.socialmediatoday.com/feeds/news/ | 200 | 1 | OK |
| https://www.theverge.com/rss/index.xml | 200 | 10 | OK |
| https://www.youtube.com/feeds/videos.xml?channel_id=UCGg-UqjRgzhYDPJMr-9HXCg | 200 | 15 | OK |
| https://www.youtube.com/trends/index.rss | 200 | 0 | OK (flux vide) |

**Total adresses OK : 31 / 35**

Détail des 4 non-OK :
- 2 refus du site (403 direct depuis le serveur d'origine, aucun signe de blocage au CONNECT par le filtre réseau) : musebyclios.com, creativereview.co.uk
- 2 redirections HTTP 301 non suivies (curl sans `-L`), donc 0 article reçu à cette étape : variety.com, numerama.com

## 2. Lecture d'articles (6 adresses)

Mesure : code HTTP et taille en octets du corps reçu.

| Adresse | Code HTTP | Taille (octets) |
|---|---|---|
| https://r.jina.ai/https://about.instagram.com/blog | 403 | 5 731 |
| https://about.instagram.com/blog | 400 | 1 542 |
| https://newsroom.tiktok.com/en-us | 301 | 52 |
| https://ads.tiktok.com/business/en/blog | 200 | 1 365 580 |
| https://www.lesechos.fr/ | 403 | 367 |
| https://www.linkedin.com/business/marketing/blog | 200 | 115 395 |

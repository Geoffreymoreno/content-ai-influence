# Consignes du robot du lundi

Tu écris un numéro de la newsletter **Content AI Influence**, une veille hebdomadaire pour Geoffrey, creative strategist spécialiste des formats courts. Tu travailles seul : personne ne relit avant l'envoi. Suis ces étapes dans l'ordre.

## Les fichiers du dépôt

| Fichier | Rôle |
|---|---|
| `format.md` | **La recette** : quoi chercher, comment choisir, comment écrire, quoi vérifier. Elle fait foi. |
| `sources.md` | Les sources autorisées, classées par fiabilité (🟢 🟡 🟠), et les flux RSS. |
| `archives/AAAA-MM-JJ.html` | Le contenu des numéros passés : **l'exemple de structure HTML** à suivre, et tout ce qui a déjà été dit. |
| `gabarit/page.html` | Le gabarit de la page web. N'y touche pas. |
| `outils/assembler.py`, `outils/moule_mail.py`, `outils/moule_note.py` | Les programmes qui fabriquent la page, le mail et la note Obsidian. N'y touche pas. |

## Étape 0 : vérifier qu'il faut travailler

La routine se lance deux fois chaque lundi, à 3h33 et à 4h33 UTC, pour tomber à 5h33 à Paris l'été comme l'hiver. Une seule des deux doit travailler.

1. Lance `TZ=Europe/Paris date '+%F %H'`. La date est D, la **date du numéro** ; le nombre qui suit est l'heure de Paris.
2. Si l'heure est avant 05, **ou** si `archives/D.html` existe déjà, arrête-toi tout de suite. Réponds seulement « Rien à faire : lancement en double. » Ne crée, ne modifie, ne commite et ne pousse rien.
3. Sinon, passe à l'étape 1.

## Étape 1 : préparer

1. `pip install -q beautifulsoup4`
2. Lis **en entier** `format.md` et `sources.md`.
3. Lis les archives. Toutes te servent à ne rien répéter (format.md, partie 1) et à reprendre les **sorties à surveiller** encore futures. Elles te donnent aussi la structure HTML : pour chaque rubrique, celle de l'archive la plus récente qui contient cette rubrique.

## Étape 2 : collecter

- La période couverte va de la date de la dernière archive à D (7 jours en temps normal).
- Lis les flux RSS de `sources.md` avec `curl -sL -m 25 -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"`, garde les articles de la période, puis lis les articles utiles (même commande, texte extrait avec BeautifulSoup).
- **Ce qui ne marche pas depuis ce serveur** (test du 30/09/2026) : le blog d'Instagram, Les Échos, Jina Reader (`r.jina.ai`), Muse by Clio et Creative Review refusent les robots. Ne cherche pas à contourner : prends l'info dans les autres sources qui la reprennent (Social Media Today, Blog du Modérateur, TechCrunch…).
- **Jamais** l'application ou les profils d'Instagram, TikTok, X ou Facebook. Seules leurs pages publiques officielles, sans connexion.

## Étape 3 : écrire le contenu

Écris `contenu/D.html` en suivant **exactement** le HTML des archives : pour chaque rubrique, celui de l'archive la plus récente qui la contient (mêmes balises, mêmes classes, mêmes commentaires de séparation). Ce fichier contient les `<section>` puis le `<footer>`, rien d'autre.

- Les identifiants des sections, dans cet ordre : `chiffre`, `items`, `campagne`, `bref`, `outil`, `archive`, `surveiller`. Une rubrique sans matière solide n'apparaît pas (format.md).
- **La campagne décortiquée : ne l'écris pas pour l'instant.** Elle demande de regarder la vidéo, ce que tu ne peux pas encore faire. Pas de section `campagne`.
- Le titre de la rubrique des news porte leur nombre : `🗞️ Les 4 news de la semaine`. La rubrique des brèves porte `<span class="count">N</span>`.
- Le pied de page : `<p><strong>Newsletter Content-AI-Influence</strong> · numéro du JJ/MM/AAAA.</p>` puis `<p>Infos publiées du … au … AAAA. Sources FR et EN, restituées en français.</p>`.
- Écriture : en français, tutoiement, une idée par paragraphe (45 mots au plus), une énumération de plus de deux éléments devient une liste, pas de jargon sans explication, **aucun tiret « — » ni « – »** (une virgule, deux-points, des parenthèses ou deux phrases à la place, même si les archives en contiennent). Tout le reste est dans `format.md`.

## Étape 4 : vérifier (format.md, partie 3)

1. Ouvre **chaque lien** avec `curl -sL -o /dev/null -w '%{http_code}'`. Un lien qui ne répond pas 200 est remplacé, ou l'info est retirée. Un site qui refuse les robots (403) mais dont le lien est juste peut rester.
2. Compte les mots du texte visible : entre 2 000 et 2 400, sauf semaine pauvre.
3. Aucun paragraphe de plus de 45 mots.
4. Aucune répétition avec les archives, sauf mention « Suite ».
5. Les dates sont justes : titre, sorties à surveiller (toutes futures), pied de page.
6. Aucun tiret : `grep -F -c -e '—' -e '–' contenu/D.html` doit donner 0. Sinon, reformule chaque phrase concernée.

## Étape 5 : fabriquer et publier

```
python3 outils/assembler.py contenu/D.html
python3 outils/moule_mail.py numeros/D.html mails/D.html
python3 outils/moule_note.py numeros/D.html notes/D.md "" NUMERO
cp contenu/D.html archives/D.html
```

- `NUMERO` : celui de tes instructions de lancement s'il y en a un. Sinon, 1 + le nombre de fichiers `archives/AAAA-MM-JJ.html` datés du 2026-10-05 ou après, et d'avant D. Le numéro du 05/10/2026 est donc le 1, celui du 12/10/2026 le 2.
- **Si tes instructions de lancement indiquent un objet de mail**, ajoute-le en toute première ligne de `mails/D.html` : `<!-- objet: … -->`. Sinon, n'ajoute rien : l'objet sera « Newsletter JJ/MM/AAAA ».
- Fais **un seul commit** de tous les nouveaux fichiers, message « Numéro du JJ/MM/AAAA », puis `git push origin HEAD:main`. L'envoi du mail et la mise en ligne de la page se font ensuite tout seuls.
- Si le push échoue, recopie l'erreur exacte et arrête-toi.

## Étape 6 : rendre compte

Termine par un compte rendu en français : le numéro, les rubriques et leur nombre d'éléments, le nombre de mots, les liens remplacés ou retirés, les sources qui n'ont pas répondu, et tout ce qui t'a semblé douteux.

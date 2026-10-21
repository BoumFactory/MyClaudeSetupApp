---
niveau: 2GT
page: 5
pdf: 2gt.pdf
page_folder: 2GT
bo_reference: "BO Hebdo 14 du 2 avril 2026"
bo_url: "https://www.education.gouv.fr/bo/2026/Hebdo14"
page_image: ../../pages/2GT/page_005.png
transcription_meta:
  date: "2026-05-19T00:00:00Z"
  status: clean
  confidence: 0.95
  has_formulas: true
  has_tables: false
  source: "fitz get_text('text') + relecture multimodale (formules cassées rétablies)"
---

# Page 5 — Variables, fonctions, Automatismes (calcul numérique et algébrique)

## Variables et instructions élémentaires (suite)

### Contenus

- Affectation (notée ← en langage naturel).
- Séquence d'instructions.
- Instruction conditionnelle.
- Boucle bornée (`for`), boucle non bornée (`while`).

### Capacités attendues

- Choisir ou déterminer le type d'une variable (entier, flottant ou chaine de caractères).
- Concevoir et écrire une instruction d'affectation, une séquence d'instructions, une instruction conditionnelle.
- Écrire une formule permettant un calcul combinant des variables.
- Programmer, dans des cas simples, une boucle bornée, une boucle non bornée.
- Dans des cas plus complexes : lire, comprendre, modifier ou compléter un algorithme ou un programme.

## Notion de fonction

### Contenus

- Fonctions à un ou plusieurs arguments.
- Fonction renvoyant un nombre aléatoire. Série statistique obtenue par la répétition de l'appel d'une telle fonction.

### Capacités attendues

- Écrire des fonctions simples ; lire, comprendre, modifier, compléter des fonctions plus complexes. Appeler une fonction.
- Lire et comprendre une fonction renvoyant une moyenne, un écart type. Aucune connaissance sur les listes n'est exigée.
- Écrire des fonctions renvoyant le résultat numérique d'une expérience aléatoire, d'une répétition d'expériences aléatoires indépendantes.

## Automatismes

> Cette partie du programme vise à construire et à entretenir des habiletés dans les domaines du calcul, de l'information chiffrée et des représentations graphiques. Il s'agit d'automatiser le recours à des connaissances, des procédures, des méthodes et des stratégies. Leur acquisition permet aux élèves une meilleure réussite dans l'apprentissage des mathématiques, participe du développement de leur esprit critique par une meilleure maitrise des nombres et du calcul et leur permet une meilleure lecture et compréhension des représentations de données dont les graphiques.

Les capacités attendues énoncées ci-dessous n'ont pas vocation à faire l'objet d'un chapitre d'enseignement spécifique car les notions qui les sous-tendent ont été travaillées dans les classes antérieures et doivent être entretenues et consolidées au cours de l'année. Cependant les nouvelles notions du programme peuvent donner lieu également à un travail d'automatisation tout le long de l'année. Elles relèvent d'un entrainement régulier privilégiant l'activité mentale. Les différents thèmes proposés doivent être travaillés tout au long de l'année et la présentation par blocs thématiques ne signifie pas, bien au contraire, qu'il faille les aborder les uns après les autres. Les modalités de mise en œuvre peuvent être variées et prendre appui sur différents supports : à l'oral, à l'écrit, individuellement ou en groupe, utilisant éventuellement des outils numériques de vidéo-projection, de recensement instantané des réponses, etc.

### Calcul numérique et algébrique

- Comparer deux nombres directement ou par calcul :
  - de leur différence ;
  - s'ils sont strictement positifs, de leur quotient.
- Effectuer des opérations et des comparaisons entre des fractions simples.
- Effectuer des opérations sur les puissances.
- Passer d'une écriture d'un nombre à une autre (décimale, fractionnaire, pourcentage).
- Estimer un ordre de grandeur.
- S'assurer de la vraisemblance, de la cohérence d'un résultat.
- Effectuer des conversions d'unités : longueurs, aires, volumes, contenances, durées, vitesses, masses.
- Effectuer un calcul littéral élémentaire :
  - expressions additives : $-(a+b) = -a-b$, $\;-(a-b) = b-a$ ;
  - expressions multiplicatives : $x = 1 \times x$, $\;x = \dfrac{x}{1}$, $\;(-1) \times a = \dfrac{a}{-1} = -a$ ;
  - $0 = 0\,x$, $\;\dfrac{0}{a} = 0$, $\;\dfrac{x}{a} = \dfrac{1}{a}\,x$, $\;\dfrac{a\,b}{c} = a \times \dfrac{b}{c} = \dfrac{a}{c} \times b$.
- Développer, factoriser, réduire une expression algébrique simple :
  - identité de développement : $a(b+c) = ab + ac$ ;
  - factorisation : $a^2 - b^2 = (a-b)(a+b)$ ;
  - identités remarquables : $(a+b)^2 = a^2 + 2ab + b^2$, $\;(a-b)^2 = a^2 - 2ab + b^2$.
- Résoudre une équation $x^2 = a$, où $a$ est un réel donné et $x$ l'inconnue, en utilisant la propriété : $a^2 = b^2 \iff a = b \text{ ou } a = -b$.
- Isoler une variable dans une égalité (formules utilisées en mathématiques, en physique ou dans d'autres disciplines).
- Effectuer un calcul numérique à partir d'une formule (notamment pour des formules utilisées dans les autres disciplines).

## Notes de l'agent

- Les formules cassées dans le texte brut (fractions multilignes, exposants éclatés) ont été restaurées en LaTeX en croisant le texte et l'image.
- Confidence 0.95 (perte mineure : les présentations en deux colonnes du calcul littéral ont été linéarisées en LaTeX).
- Toutes les capacités listées ici relèvent du domaine `NB` (calcul numérique) ou `AL` (calcul littéral) pour 2GT et seront extraites comme **automatismes** (champ `automatismes` du JSON niveau, distincts des compétences atomiques).

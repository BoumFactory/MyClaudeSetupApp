---
name: moodle-cloze
description: Skill pour créer des questions Cloze (réponses intégrées) pour Moodle. Utiliser ce skill pour générer des questionnaires interactifs Moodle avec choix multiples, réponses courtes, numériques et réponses multiples. Couvre tous les types MULTICHOICE, SHORTANSWER, NUMERICAL, MULTIRESPONSE et leurs variantes.
---

# Moodle Cloze - Skill pour Questions à Réponses Intégrées

## Description

Skill spécialisé pour créer des questions Cloze Moodle (Embedded Answers), format permettant d'intégrer plusieurs sous-questions interactives dans un même texte. Idéal pour les évaluations formatives en mathématiques avec feedback personnalisé.

## Quand utiliser ce skill

- Création de questionnaires Moodle interactifs
- Évaluations auto-corrigées en ligne
- QCM avec réponses à saisir et/ou à sélectionner
- Tests combinant différents types de réponses (choix multiples, numériques, texte)

## Structure d'une question Cloze

### Format général

```
{POIDS:TYPE:~option1~option2~=bonne_reponse~option3}
```

**Composants :**
- `{` et `}` : délimiteurs obligatoires
- `POIDS` : nombre de points (1 par défaut, peut être omis)
- `TYPE` : type de sous-question (voir ci-dessous)
- `:` : séparateurs
- `~` : séparateur d'options
- `=` : marque la bonne réponse
- `#` : introduit un feedback

## Types de questions disponibles

### 1. MULTICHOICE - Choix unique (menu déroulant)

**Syntaxe de base :**
```
{1:MULTICHOICE:~option1~=bonne_reponse~option2}
```

**Variantes d'affichage :**

| Code | Affichage | Mélange |
|------|-----------|---------|
| `MULTICHOICE` ou `MC` | Menu déroulant | Non |
| `MULTICHOICE_V` ou `MCV` | Boutons radio verticaux | Non |
| `MULTICHOICE_H` ou `MCH` | Boutons radio horizontaux | Non |
| `MULTICHOICE_S` ou `MCS` | Menu déroulant | Oui |
| `MULTICHOICE_VS` ou `MCVS` | Boutons radio verticaux | Oui |
| `MULTICHOICE_HS` ou `MCHS` | Boutons radio horizontaux | Oui |

**Exemple avec feedback :**
```
{1:MULTICHOICE:~Sydney#Sydney n'est pas la capitale~=Canberra#Correct !~Melbourne#Essayez encore}
```

### 2. MULTIRESPONSE - Réponses multiples (cases à cocher)

Permet plusieurs bonnes réponses (chaque bonne réponse marquée avec `=`).

**Syntaxe :**
```
{1:MULTIRESPONSE:~=bonne1~=bonne2~mauvaise1~mauvaise2}
```

**Variantes :**

| Code | Affichage | Mélange |
|------|-----------|---------|
| `MULTIRESPONSE` ou `MR` | Cases verticales | Non |
| `MULTIRESPONSE_H` ou `MRH` | Cases horizontales | Non |
| `MULTIRESPONSE_S` ou `MRS` | Cases verticales | Oui |
| `MULTIRESPONSE_HS` ou `MRHS` | Cases horizontales | Oui |

**Exemple :**
```
{2:MULTIRESPONSE:~=2#Premier~=3#Oui~4#Non~=5#Oui~6#Non~=7#Oui}
```

### 3. SHORTANSWER - Réponse courte (texte à saisir)

**Syntaxe :**
```
{1:SHORTANSWER:~=reponse1~=reponse2#Feedback}
```

**Variantes :**

| Code | Comportement |
|------|--------------|
| `SHORTANSWER` ou `SA` ou `MW` | Insensible à la casse |
| `SHORTANSWER_C` ou `SAC` ou `MWC` | Sensible à la casse |

**Caractères spéciaux :**
- `*` : wildcard pour "toute autre réponse" (mettre en dernier)

**Exemple avec wildcard :**
```
{1:SHORTANSWER:~=Paris~=paris#Correct !~*#La bonne réponse est Paris.}
```

**Accepter plusieurs formes :**
```
{1:SHORTANSWER:~=3x + 6~=3x+6~=3x+ 6~=3 x + 6#Correct !}
```

### 4. NUMERICAL - Réponse numérique (avec tolérance)

**Syntaxe sans tolérance :**
```
{1:NUMERICAL:=42#Feedback}
```

**Syntaxe avec tolérance :**
```
{1:NUMERICAL:=valeur:tolerance#Feedback}
```

La tolérance définit l'intervalle accepté : [valeur - tolérance ; valeur + tolérance]

**Exemples :**
```
{1:NUMERICAL:=25:0}          // Réponse exacte : 25
{1:NUMERICAL:=3.14:0.01}     // Accepte 3.13 à 3.15
{1:NUMERICAL:=25.13:0.2}     // Accepte 24.93 à 25.33
```

**Réponses multiples acceptées :**
```
{1:NUMERICAL:~=3~=-3#Les deux solutions sont 3 et -3}
```

## Fonctionnalités avancées

### Pondération des questions

Le premier nombre indique les points. Questions difficiles = plus de points.

```
{1:NUMERICAL:=5:0}    // Vaut 1 point
{2:NUMERICAL:=5:0}    // Vaut 2 points
{3:NUMERICAL:=5:0}    // Vaut 3 points
```

### Notes partielles (crédits partiels)

Utiliser `%XX%` pour donner un pourcentage des points.

```
{2:NUMERICAL:=3.14159:0.00001#Parfait~%80%3.14:0.005#Bien~%50%3.1:0.05#Approximatif}
```

### Feedback détaillé

Toujours après le `#`, s'applique à l'option qui le précède.

```
{1:MULTICHOICE:~option1#Feedback pour option1~=bonne#Feedback pour bonne réponse}
```

### HTML dans les questions

Le HTML est supporté dans le corps de la question (hors des accolades).

```
<p><strong>Question :</strong> Calculer 2<sup>3</sup> = {1:NUMERICAL:=8:0}</p>
```

## Bonnes pratiques pour les mathématiques

### 1. Expressions algébriques (SHORTANSWER)

Prévoir plusieurs formats acceptés :
```
{1:SHORTANSWER:~=x² + 5x + 6~=x^2 + 5x + 6~=x2 + 5x + 6~=(x+2)(x+3)}
```

### 2. Fractions et décimaux

Pour π × 4² ≈ 50,27 :
```
{1:NUMERICAL:=50.27:0.1}
```

### 3. Équations avec solutions multiples

```
Les solutions de x² = 9 sont x = {1:SHORTANSWER:~=3 et -3~=-3 et 3~=3 ou -3~=-3 ou 3}.
```

### 4. Intervalles de réponses

Pour √2 ≈ 1,414 avec tolérance :
```
{1:NUMERICAL:=1.414:0.01}
```

### 5. Alternance des types

Varier les types pour maintenir l'attention :
- Concepts → MULTICHOICE
- Calculs → NUMERICAL
- Expressions → SHORTANSWER
- Propriétés multiples → MULTIRESPONSE

## Structure recommandée d'un fichier Cloze

```
::Titre de la question::

<h3>Titre affiché</h3>

<p>Contexte et consignes...</p>

<p><strong>Question 1 :</strong> Texte {1:TYPE:~...}</p>

<p><strong>Question 2 :</strong> Texte {1:TYPE:~...}</p>

<hr>

<p><strong>Partie B</strong></p>

<p>Question 3 : {2:TYPE:~...}</p>
```

## Protocole de création

### Phase 1 : Analyse du besoin

1. Identifier le niveau (collège/lycée)
2. Identifier le thème mathématique
3. Déterminer les objectifs pédagogiques
4. Décider du nombre de questions

### Phase 2 : Conception

1. Rédiger les énoncés en langage naturel
2. Identifier le type optimal pour chaque question :
   - Fait/définition → MULTICHOICE
   - Calcul exact → NUMERICAL (tolérance 0)
   - Calcul approché → NUMERICAL (avec tolérance)
   - Expression → SHORTANSWER (prévoir variantes)
   - Propriétés vraies → MULTIRESPONSE
3. Concevoir les distracteurs (erreurs plausibles)
4. Préparer les feedbacks

### Phase 3 : Rédaction

1. Structurer avec HTML (titres, paragraphes, hr)
2. Encoder chaque sous-question au format Cloze
3. Pondérer les questions selon difficulté
4. Tester la syntaxe (accolades équilibrées)

### Phase 4 : Vérification

Checklist avant export :
- [ ] Toutes les accolades sont équilibrées
- [ ] Chaque question a au moins une bonne réponse (avec `=`)
- [ ] Les SHORTANSWER prévoient plusieurs formats
- [ ] Les NUMERICAL ont une tolérance appropriée
- [ ] Les feedbacks sont informatifs
- [ ] Le HTML est correctement formaté

## Exemples complets par domaine

### Calcul littéral (3ème/2nde)

```
::Calcul littéral - Développement::

<h3>Développement et factorisation</h3>

<p><strong>1.</strong> Développer 3(x + 2) = {1:SHORTANSWER:~=3x + 6~=3x+6#Correct !~*#Pensez à multiplier chaque terme}</p>

<p><strong>2.</strong> Factoriser 6x + 12 = {1:SHORTANSWER:~=6(x + 2)~=6(x+2)#Correct !~*#Cherchez le facteur commun}</p>

<p><strong>3.</strong> (x + 3)² = {1:MULTICHOICE:~x² + 9#Erreur classique~x² + 3x + 9#Presque~=x² + 6x + 9#Correct !}</p>
```

### Fonctions (2nde/1ère)

```
::Fonctions - Second degré::

<p>Soit f(x) = x² - 6x + 8</p>

<p><strong>1.</strong> f(0) = {1:NUMERICAL:=8:0#Correct, f(0) = 0 - 0 + 8}</p>

<p><strong>2.</strong> Les racines de f sont {1:SHORTANSWER:~=2 et 4~=4 et 2~=x=2 et x=4#Correct}</p>

<p><strong>3.</strong> f est {1:MULTICHOICE:~=décroissante#Correct~croissante} sur ]-∞ ; 3]</p>

<p><strong>4.</strong> Le minimum de f vaut {1:NUMERICAL:=-1:0#Correct, f(3) = 9 - 18 + 8 = -1}</p>
```

### Probabilités (2nde/1ère)

```
::Probabilités - Bases::

<p>On lance un dé équilibré à 6 faces.</p>

<p><strong>1.</strong> P(obtenir 6) = {1:SHORTANSWER:~=1/6~=0.167~=0,167#Correct}</p>

<p><strong>2.</strong> P(nombre pair) = {1:SHORTANSWER:~=1/2~=0.5~=0,5~=3/6#Correct}</p>

<p><strong>3.</strong> Cochez les événements de probabilité 1/3 :
{1:MULTIRESPONSE:~obtenir 1#Non, P=1/6~=obtenir un multiple de 3#Oui (3 ou 6)~obtenir un nombre premier#Non, P=1/2~=obtenir un nombre > 4#Oui (5 ou 6)}</p>
```

## Ressources complémentaires

Voir le dossier `references/` pour :
- `syntaxe-complete.md` : Référence exhaustive de la syntaxe
- `exemples-par-niveau.md` : Banque d'exemples par niveau scolaire

## Import dans Moodle

1. Créer un fichier `.txt` avec le contenu Cloze
2. Dans Moodle : Banque de questions → Importer
3. Format : "Embedded answers (Cloze)"
4. Sélectionner le fichier et importer

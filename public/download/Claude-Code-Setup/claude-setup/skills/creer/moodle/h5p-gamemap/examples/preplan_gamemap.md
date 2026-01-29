# Préplan Game Map : L'Archipel des Suites

> Parcours gamifié enrichi sur les suites numériques (Première)

---

## Informations générales

- **Titre** : L'Archipel des Suites
- **Niveau** : 1ere
- **Thème** : Suites numériques
- **Style** : aventure

---

## Configuration du jeu

| Paramètre | Valeur | Description |
|-----------|--------|-------------|
| **Vies** | 4 | Chaque erreur retire une vie |
| **Roaming** | complete | Doit réussir pour avancer |
| **Brouillard** | visited | Seules les îles visitées sont visibles |
| **Afficher labels** | oui | Noms des îles visibles |
| **Afficher étoiles** | always | Toujours afficher les étoiles |
| **Animations** | oui | Activer les animations |

---

## Image de fond

- **Source** : archipel_suites.png
- **Dimensions** : 1920x1080

---

## Lore / Introduction

```html
<p style="text-align: center;"><strong>Bienvenue, navigateur !</strong></p>
<p style="text-align: center;">Explore l'Archipel des Suites et conquiers chaque île en répondant aux défis mathématiques.</p>
<p style="text-align: center;"><strong>Attention : tu n'as que 4 vies !</strong> Chaque erreur t'en coûte une.</p>
<p style="text-align: center;">Bonne chance pour atteindre l'Île du Trésor !</p>
```

---

## Étapes du parcours

### Étape 1 : Île de la Définition

- **Position** : x=12, y=72
- **Type** : singlechoiceset
- **Départ** : oui

**Questions** :

1. **Question** : Une suite numérique est une fonction définie sur :
   - [x] \(\mathbb{N} \to \mathbb{R}\) (entiers naturels vers réels)
   - [ ] \(\mathbb{R} \to \mathbb{N}\)
   - [ ] \(\mathbb{Z} \to \mathbb{R}\)
   - [ ] \(\mathbb{R} \to \mathbb{R}\)

2. **Question** : Le premier terme d'une suite peut être noté :
   - [x] \(u_0\) ou \(u_1\) selon la convention choisie
   - [ ] Toujours \(u_1\)
   - [ ] Toujours \(u_0\)
   - [ ] \(u_{-1}\)

3. **Question** : L'ensemble des termes d'une suite est :
   - [x] Dénombrable (on peut les numéroter)
   - [ ] Continu comme un intervalle
   - [ ] Fini
   - [ ] Vide

---

### Étape 2 : Île des Notations

- **Position** : x=23, y=45
- **Type** : blanks

**Consigne** :
```
Complète les notations des suites. Attention aux parenthèses !
```

**Texte à trous** :
```
La notation *\((u_n)\)* avec parenthèses désigne la *suite* entière. Sans parenthèses, *\(u_n\)* désigne un *terme* particulier de *rang* \(n\). Par exemple, *\(u_5\)* est le terme de rang *5*. On dit aussi que \(n\) est l'*indice* du terme.
```

---

### Étape 3 : Île du Vocabulaire

- **Position** : x=42, y=55
- **Type** : dragtext

**Consigne** :
```
Place les mots au bon endroit pour compléter les définitions sur les suites.
```

**Texte à compléter** :
```
Une suite est *croissante* si chaque terme est plus grand que le précédent : \(u_{n+1} > u_n\). Elle est *décroissante* si chaque terme est plus petit. Une suite qui n'est ni croissante ni décroissante est dite *non monotone*. Si une suite est croissante ou décroissante, on dit qu'elle est *monotone*. Une suite est *constante* si tous ses termes sont égaux.
```

---

### Étape 4 : Île Explicite

- **Position** : x=52, y=28
- **Type** : singlechoiceset

**Questions** :

1. **Question** : Soit \(u_n = 2n - 7\). Que vaut \(u_5\) ?
   - [x] 3
   - [ ] 10
   - [ ] -3
   - [ ] 5

2. **Question** : Soit \(v_n = n^2 + 1\). Que vaut \(v_3\) ?
   - [x] 10
   - [ ] 9
   - [ ] 7
   - [ ] 4

3. **Question** : Soit \(w_n = \frac{n}{n+1}\). Que vaut \(w_2\) ?
   - [x] \(\frac{2}{3}\)
   - [ ] \(\frac{1}{2}\)
   - [ ] \(\frac{3}{2}\)
   - [ ] 2

4. **Question** : Soit \(t_n = (-1)^n\). Que vaut \(t_4\) ?
   - [x] 1
   - [ ] -1
   - [ ] 4
   - [ ] -4

---

### Étape 5 : Île de la Récurrence

- **Position** : x=64, y=20
- **Type** : singlechoiceset

**Questions** :

1. **Question** : Une suite définie par récurrence nécessite de connaître :
   - [x] Le(s) premier(s) terme(s) et une relation entre termes consécutifs
   - [ ] Uniquement une formule explicite
   - [ ] Tous les termes de la suite
   - [ ] Seulement la limite

2. **Question** : Soit \(u_0 = 2\) et \(u_{n+1} = u_n + 3\). Que vaut \(u_1\) ?
   - [x] 5
   - [ ] 3
   - [ ] 6
   - [ ] 2

3. **Question** : Avec la même suite \(u_0 = 2\) et \(u_{n+1} = u_n + 3\), que vaut \(u_3\) ?
   - [x] 11
   - [ ] 9
   - [ ] 8
   - [ ] 14

---

### Étape 6 : Île du Calcul Intensif

- **Position** : x=75, y=22
- **Type** : singlechoiceset

**Questions** :

1. **Question** : Soit \(u_0 = 1\) et \(u_{n+1} = 3u_n + 1\). Que vaut \(u_1\) ?
   - [x] 4
   - [ ] 3
   - [ ] 2
   - [ ] 5

2. **Question** : Avec la même suite, que vaut \(u_2\) ?
   - [x] 13
   - [ ] 7
   - [ ] 10
   - [ ] 4

3. **Question** : Soit \(v_0 = 5\) et \(v_{n+1} = 2v_n - 1\). Que vaut \(v_1\) ?
   - [x] 9
   - [ ] 10
   - [ ] 4
   - [ ] 11

4. **Question** : Avec cette suite, que vaut \(v_2\) ?
   - [x] 17
   - [ ] 18
   - [ ] 19
   - [ ] 8

5. **Question** : Soit \(w_1 = 1\) et \(w_{n+1} = w_n^2 + 1\). Que vaut \(w_3\) ?
   - [x] 5
   - [ ] 3
   - [ ] 4
   - [ ] 2

---

### Étape 7 : Île du Trésor

- **Position** : x=80, y=42
- **Type** : blanks

**Consigne** :
```
Dernière épreuve ! Complète ce résumé sur les suites numériques.
```

**Texte à trous** :
```
La représentation graphique d'une suite est un *nuage* de *points* discrets, car une suite n'est définie que sur *\(\mathbb{N}\)*. Pour une suite *explicite*, on peut calculer directement n'importe quel terme avec la formule \(u_n = f(n)\). Pour une suite *récurrente*, on calcule chaque terme à partir du *précédent*. Une suite est *arithmétique* si la différence entre deux termes consécutifs est constante. Une suite est *géométrique* si le quotient entre deux termes consécutifs est constant.
```

---

## Écrans de fin

### Succès

```html
<p style="text-align: center;"><strong>Félicitations, navigateur !</strong></p>
<p style="text-align: center;">Tu as conquis l'Archipel des Suites et découvert le trésor !</p>
<p style="text-align: center;">Les suites numériques n'ont plus de secret pour toi.</p>
```

### Échec

```html
<p style="text-align: center;"><strong>Naufrage !</strong></p>
<p style="text-align: center;">Tu as perdu toutes tes vies avant d'atteindre le trésor.</p>
<p style="text-align: center;">Reprends la mer et réessaie !</p>
```

### Feedbacks par score

| Score | Message |
|-------|---------|
| 0-40% | Continue tes explorations, tu peux progresser ! |
| 41-70% | Bon voyage ! Tu maîtrises les bases. |
| 71-99% | Excellent parcours ! Tu es presque au sommet. |
| 100% | Parfait ! Tu es un vrai maître des suites ! |

---

## Couleurs (optionnel)

| Élément | Couleur |
|---------|---------|
| Stage non visité | `rgba(52, 152, 219, 0.85)` |
| Stage verrouillé | `rgba(127, 140, 141, 0.7)` |
| Stage réussi | `rgba(46, 204, 113, 0.85)` |
| Chemin normal | `rgba(44, 62, 80, 0.6)` |
| Chemin réussi | `rgba(46, 204, 113, 0.7)` |
| Style chemin | dotted |

---

## Résumé des questions

| Étape | Type | Nb questions/trous |
|-------|------|-------------------|
| 1. Définition | singlechoiceset | 3 QCM |
| 2. Notations | blanks | 7 trous |
| 3. Vocabulaire | dragtext | 5 mots |
| 4. Explicite | singlechoiceset | 4 QCM |
| 5. Récurrence | singlechoiceset | 3 QCM |
| 6. Calcul Intensif | singlechoiceset | 5 QCM |
| 7. Trésor | blanks | 8 trous |

**Total** : ~35 interactions

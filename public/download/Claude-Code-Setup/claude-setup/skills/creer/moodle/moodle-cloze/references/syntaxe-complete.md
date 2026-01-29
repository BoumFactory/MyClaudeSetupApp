# Syntaxe Moodle Cloze - Référence Complète

## Tableau récapitulatif des types

| Type complet | Abréviation | Description | Affichage |
|--------------|-------------|-------------|-----------|
| `MULTICHOICE` | `MC` | Choix unique | Menu déroulant |
| `MULTICHOICE_V` | `MCV` | Choix unique | Boutons radio verticaux |
| `MULTICHOICE_H` | `MCH` | Choix unique | Boutons radio horizontaux |
| `MULTICHOICE_S` | `MCS` | Choix unique mélangé | Menu déroulant |
| `MULTICHOICE_VS` | `MCVS` | Choix unique mélangé | Boutons radio verticaux |
| `MULTICHOICE_HS` | `MCHS` | Choix unique mélangé | Boutons radio horizontaux |
| `MULTIRESPONSE` | `MR` | Choix multiples | Cases à cocher verticales |
| `MULTIRESPONSE_H` | `MRH` | Choix multiples | Cases à cocher horizontales |
| `MULTIRESPONSE_S` | `MRS` | Choix multiples mélangés | Cases à cocher verticales |
| `MULTIRESPONSE_HS` | `MRHS` | Choix multiples mélangés | Cases à cocher horizontales |
| `SHORTANSWER` | `SA` ou `MW` | Réponse courte | Zone de texte (casse ignorée) |
| `SHORTANSWER_C` | `SAC` ou `MWC` | Réponse courte | Zone de texte (casse respectée) |
| `NUMERICAL` | `NM` | Réponse numérique | Zone de texte numérique |

## Syntaxe détaillée par type

### MULTICHOICE - Toutes variantes

```
{POIDS:TYPE:~option1#feedback1~option2#feedback2~=bonne_reponse#feedback_correct~option3}
```

**Éléments :**
- `POIDS` : entier (points attribués)
- `TYPE` : MC, MCV, MCH, MCS, MCVS, MCHS
- `~` : séparateur d'options (obligatoire avant chaque option)
- `=` : préfixe de la bonne réponse
- `#` : introduit le feedback (optionnel)

**Exemple complet :**
```
{2:MULTICHOICE_VS:~Premier choix#Non, ce n'est pas ça~=Deuxième choix#Bravo !~Troisième choix#Essayez encore~Quatrième choix#Pas tout à fait}
```

### MULTIRESPONSE - Toutes variantes

```
{POIDS:TYPE:~=bonne1#fb1~=bonne2#fb2~mauvaise1#fb3~mauvaise2#fb4}
```

**Points importants :**
- Plusieurs réponses peuvent être marquées correctes avec `=`
- La notation partielle est calculée automatiquement
- Chaque mauvaise réponse sélectionnée retire des points

**Exemple :**
```
{3:MULTIRESPONSE_S:~=Carré#Oui, 4 côtés égaux~=Losange#Oui, 4 côtés égaux~Rectangle#Non, côtés opposés égaux seulement~=Losange régulier#Oui, c'est un carré !}
```

### SHORTANSWER - Toutes variantes

```
{POIDS:TYPE:~=reponse1#fb1~=reponse2#fb2~*#feedback_defaut}
```

**Caractères spéciaux :**
- `*` : wildcard (toute autre réponse)
- Placer `*` en dernier pour le feedback par défaut

**Exemple avec plusieurs réponses acceptées :**
```
{1:SHORTANSWER:~=Paris~=paris~=PARIS~=La capitale est Paris#Toutes ces formes sont acceptées~*#La réponse attendue est Paris}
```

**Sensibilité à la casse :**
```
{1:SAC:~=Python#Correct avec majuscule~=python#Incorrect, majuscule requise}
```

### NUMERICAL

```
{POIDS:NUMERICAL:=valeur:tolerance#feedback}
```

**Formats de tolérance :**
- Sans tolérance : `=42` (exactement 42)
- Tolérance absolue : `=42:2` (de 40 à 44)
- Tolérance relative : `=%5%42` (±5% de 42)

**Notes partielles :**
```
{2:NUMERICAL:=3.14159:0.00001#100%~%75%3.1416:0.0001#75%~%50%3.14:0.01#50%~%25%3.1:0.1#25%}
```

**Réponses multiples :**
```
{1:NUMERICAL:~=5~=-5#Les deux solutions sont acceptées}
```

## Caractères spéciaux et échappement

| Caractère | Signification | Pour l'afficher littéralement |
|-----------|---------------|-------------------------------|
| `{` | Début de sous-question | `\{` |
| `}` | Fin de sous-question | `\}` |
| `~` | Séparateur d'options | `\~` |
| `=` | Marque bonne réponse | `\=` |
| `#` | Début de feedback | `\#` |
| `:` | Séparateur structurel | `\:` |

**Exemple avec caractères spéciaux :**
```
L'ensemble \{1, 2, 3\} contient {1:NUMERICAL:=3:0} éléments.
```

## Notation et pondération

### Points par question

```
{1:MC:...}  // 1 point
{2:MC:...}  // 2 points
{5:MC:...}  // 5 points
```

### Notes partielles

Utiliser `%XX%` avant la valeur :

```
{2:NUMERICAL:=100:0#Parfait~%80%99:1#Très proche~%50%95:5#Approximatif~%0%0:100#Réessayez}
```

### Calcul MULTIRESPONSE

Pour MULTIRESPONSE, Moodle calcule :
- Chaque bonne réponse cochée : +points
- Chaque mauvaise réponse cochée : -points
- Note minimale : 0 (pas de négatif)

## HTML supporté

### Balises recommandées

```html
<p>Paragraphe</p>
<strong>Gras</strong>
<em>Italique</em>
<br> ou <br/>
<hr>
<h3>Titre</h3>
<ul><li>Liste</li></ul>
<ol><li>Liste numérotée</li></ol>
<sup>Exposant</sup>
<sub>Indice</sub>
<table><tr><td>Tableau</td></tr></table>
```

### Exemple formaté

```html
<h3>Théorème de Pythagore</h3>

<p>Dans un triangle rectangle ABC, rectangle en A :</p>
<ul>
    <li>AB = 3 cm</li>
    <li>AC = 4 cm</li>
</ul>

<p><strong>Calculer BC</strong> = {2:NUMERICAL:=5:0#BC² = AB² + AC² = 9 + 16 = 25} cm</p>
```

## Erreurs courantes à éviter

### 1. Accolades non équilibrées

❌ `{1:MC:~a~=b~c`
✅ `{1:MC:~a~=b~c}`

### 2. Oubli du tilde initial

❌ `{1:MC:a~=b~c}`
✅ `{1:MC:~a~=b~c}`

### 3. Espace dans le type

❌ `{1:MULTI CHOICE:~...}`
✅ `{1:MULTICHOICE:~...}`

### 4. Pas de bonne réponse

❌ `{1:MC:~a~b~c}` (aucun `=`)
✅ `{1:MC:~a~=b~c}`

### 5. Tolérance mal formatée

❌ `{1:NUMERICAL:=5,2}` (virgule française)
✅ `{1:NUMERICAL:=5.2}` (point décimal)
✅ `{1:NUMERICAL:=5:0.2}` (valeur:tolérance)

### 6. Feedback après le séparateur

❌ `{1:MC:~a~=b~#feedback~c}`
✅ `{1:MC:~a~=b#feedback~c}`

## Validation syntaxique

Checklist de vérification :

1. **Structure globale**
   - [ ] Commence par `::`Titre`::`
   - [ ] Accolades `{` et `}` équilibrées

2. **Chaque sous-question**
   - [ ] Format `{poids:TYPE:~...}`
   - [ ] Au moins une réponse avec `=`
   - [ ] Type valide (voir tableau)

3. **Options**
   - [ ] Chaque option précédée de `~`
   - [ ] Feedbacks après `#` (optionnel)

4. **NUMERICAL**
   - [ ] Point décimal (pas virgule)
   - [ ] Tolérance avec `:` si besoin

5. **HTML**
   - [ ] Balises fermées correctement
   - [ ] Pas de `{` ou `}` non échappés dans le texte

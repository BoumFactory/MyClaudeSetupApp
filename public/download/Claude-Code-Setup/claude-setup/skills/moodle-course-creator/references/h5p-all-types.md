# Reference Complete : Tous les Types H5P

Liste exhaustive des types H5P disponibles, classes par usage pedagogique.

## Types pour Parcours Gamifies

### Branching Scenario
**Usage** : Parcours a embranchements, scenarios adaptatifs, escape games
**Capacites** :
- Image/video de fond par etape
- Choix multiples menant a differentes branches
- Integration de TOUS les types de quiz
- Scoring et feedback personnalise
**Ideal pour** : Jeux educatifs, simulations, parcours differencies

### Course Presentation
**Usage** : Diaporama interactif avec quiz integres
**Capacites** :
- Slides avec elements positionnables
- Quiz integres (QCM, V/F, trous, drag&drop)
- Navigation libre ou guidee
**Ideal pour** : Cours interactifs, capsules

### Interactive Book
**Usage** : Livre numerique structure
**Capacites** :
- Chapitres et sous-chapitres
- Tous types de contenus H5P
- Progression et resume
**Ideal pour** : Cours complets, manuels

### Game Map
**Usage** : Carte de jeu interactive
**Capacites** :
- Carte avec points de passage
- Progression visible
- Deblocage progressif
**Ideal pour** : Parcours gamifies, quetes

## Types de Quiz

### Quiz (Question Set)
- Enchainement de questions variees
- Types mixtes (QCM, V/F, trous...)
- Score final et feedback

### Single Choice Set
- Questions rapides
- Feedback immediat
- Enchainement automatique

### Multiple Choice
- QCM classique
- Une ou plusieurs reponses correctes
- Feedback par option

### True/False Question
- Vrai/Faux simple
- Feedback differencie

### Fill in the Blanks
- Textes a trous
- Syntaxe : `*reponse*` ou `*rep1/rep2*`
- Sensibilite a la casse configurable

### Drag the Words
- Mots a glisser dans le texte
- Syntaxe : `*mot*` pour les mots a placer

### Drag and Drop
- Glisser-deposer sur image
- Zones de depot multiples
- Feedback visuel

### Mark the Words
- Selection de mots dans un texte
- Syntaxe : `*mot*` pour les mots a selectionner

### Essay
- Reponse libre
- Mots-cles attendus
- Feedback automatique

### Dictation
- Dictee audio
- Correction automatique

### Arithmetic Quiz
- Calcul mental chronometre
- Operations configurables

## Types Multimedia

### Image Hotspots
- Points cliquables sur image
- **LIMITE** : Contenu statique uniquement (texte, image, video, audio)
- PAS de quiz dans les popups !

### Interactive Video
- Video avec interactions
- Quiz integres a des moments precis
- Chapitres et navigation

### Image Slider
- Galerie d'images
- Navigation par fleches

### Image Juxtaposition
- Comparaison avant/apres
- Curseur de comparaison

### Image Sequencing
- Remettre images dans l'ordre
- Verification automatique

### Collage
- Assemblage d'images
- Mise en page automatique

### Agamotto
- Sequence d'images progressives
- Curseur de transition

## Types Texte/Contenu

### Accordion
- Sections repliables
- Organisation du contenu

### Dialog Cards
- Cartes retournables
- Recto/verso

### Flashcards
- Cartes memoire
- Mode revision

### Documentation Tool
- Formulaire structure
- Export texte

### Cornell Notes
- Prise de notes structuree
- Format Cornell

### Timeline
- Frise chronologique
- Multimedia integre

### Information Wall
- Panneaux d'information
- Recherche integree

## Types Jeux

### Memory Game
- Paires a retrouver
- Images ou texte

### Crossword
- Mots croises
- Definitions personnalisees

### Find the Words
- Mots meles
- Grille configurable

### Find the Hotspot / Find Multiple Hotspots
- Trouver les zones sur une image
- Mode decouverte

### Guess the Answer
- Image avec question
- Reponse cachee

### Personality Quiz
- Quiz de personnalite
- Profils de resultats

### Sort the Paragraphs
- Remettre paragraphes dans l'ordre
- Logique textuelle

## Types Speciaux

### Iframe Embedder
- Integrer du contenu externe
- URL ou fichiers
- **Utile pour** : integrer d'autres H5P, sites externes

### Virtual Tour (360)
- Environnements 360 degres
- Navigation immersive

### AR Scavenger
- Realite augmentee
- Chasse au tresor

### Audio Recorder
- Enregistrement audio
- Production orale

### Speak the Words / Speak the Words Set
- Reconnaissance vocale
- Reponses orales

### KewAr Code
- Generation QR codes
- Liens personnalises

### Chart
- Graphiques (barres, camemberts)
- Donnees configurables

## Structure pour Parcours Gamifie

Pour creer un parcours type "escalade avec recompense" :

### Option 1 : Branching Scenario (RECOMMANDE)
```
Ecran 1 : Image de fond (echelle)
    -> Choix : "Gravir la premiere marche"
    -> Mene vers : Quiz Drag&Drop
    -> Si reussi : Ecran 2

Ecran 2 : Progression visible
    -> Choix : "Continuer"
    -> Mene vers : Quiz Fill in Blanks
    -> Si reussi : Ecran 3

... etc jusqu'a la recompense
```

### Option 2 : Course Presentation
```
Slide 1 : Image de fond avec bouton "Commencer"
Slide 2 : Quiz QCM (bloque jusqu'a reussite)
Slide 3 : Progression + bouton suivant
Slide 4 : Quiz Drag&Drop
... etc
```

### Option 3 : Game Map (si disponible)
```
Carte avec points numerotes
Chaque point = un H5P different
Progression lineaire ou libre
```

## Limites importantes

| Type | Peut contenir des quiz ? |
|------|-------------------------|
| Image Hotspots | NON - texte/image/video/audio seulement |
| Course Presentation | OUI - tous types |
| Interactive Book | OUI - tous types |
| Branching Scenario | OUI - tous types |
| Interactive Video | OUI - aux timestamps |
| Iframe Embedder | OUI - via URL externe |

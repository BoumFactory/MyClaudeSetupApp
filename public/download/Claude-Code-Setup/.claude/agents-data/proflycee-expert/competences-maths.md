# Compétences Mathématiques - ProfLycee

## Commande principale : `\CompMathsLyc`

### Syntaxe
```latex
\CompMathsLyc[options]{catégorie/item}
```

### Options disponibles (clés KV)
- `AffCateg=true/false` : affiche le nom de la catégorie
- `AffNumero=true/false` : affiche le numéro de la compétence
- `Court=true/false` : version courte des descriptions
- `Puce=true/false` : affiche des puces
- `TypePuce` : type de puce utilisé (défaut: `\textbullet~~`)

### Catégories de compétences

#### CH - Chercher
- **Analyser** (A/An) : Analyser un problème
- **Extraire** (E/Ex) : Extraire, organiser et traiter l'information utile
- **Observer** (O/Ob) : Observer, s'engager dans une démarche, expérimenter...
- **Valider** (V/Va) : Valider, corriger une démarche, ou en adopter une nouvelle
- **Tout** : Affiche toutes les compétences de la catégorie

#### MO - Modéliser  
- **Traduire** (T) : Traduire en langage mathématique une situation réelle
- **Utiliser** (U) : Utiliser, comprendre, élaborer une simulation numérique
- **Valider** (V) : Valider ou invalider un modèle
- **Tout** : Affiche toutes les compétences de la catégorie

#### RE - Représenter
- **Choisir** (C) : Choisir un cadre adapté pour traiter un problème
- **Passer** (P) : Passer d'un mode de représentation à un autre
- **Changer** (Ch) : Changer de registre
- **Tout** : Affiche toutes les compétences de la catégorie

#### CA - Calculer
- **Effectuer** (E) : Effectuer un calcul automatisable
- **Mettre** (M) : Mettre en œuvre des algorithmes simples
- **Exercer** (Ex) : Exercer l'intelligence du calcul
- **Contrôler** (C) : Contrôler les calculs
- **Tout** : Affiche toutes les compétences de la catégorie

#### RA - Raisonner
- **Utiliser** (U) : Utiliser les notions de logique élémentaire
- **Différencier** (D) : Différencier le statut des énoncés
- **Utiliser2** (U2) : Utiliser différents types de raisonnement
- **Effectuer** (E) : Effectuer des inférences
- **Tout** : Affiche toutes les compétences de la catégorie

#### CO - Communiquer
- **Opérer** (O) : Opérer la conversion langage naturel/symbolique
- **Développer** (D) : Développer une argumentation mathématique
- **Critiquer** (C) : Critiquer une démarche ou un résultat
- **S'exprimer** (S) : S'exprimer avec clarté et précision
- **Tout** : Affiche toutes les compétences de la catégorie

### Exemples d'utilisation

```latex
% Compétence spécifique
\CompMathsLyc{CH/Analyser}

% Version courte avec catégorie
\CompMathsLyc[Court=true,AffCateg=true]{MO/T}

% Toutes les compétences d'une catégorie avec puces
\CompMathsLyc[Puce=true]{RA/Tout}

% Raccourci avec lettres
\CompMathsLyc{CH/A}  % équivalent à CH/Analyser
```

### Versions courtes disponibles
Les versions courtes (Court=true) tronquent les descriptions longues avec "[\ldots]" pour économiser l'espace.

### Format de sortie
- Sans étoile : produit un `\noindent` automatique
- Avec étoile `\CompMathsLyc*` : pas de `\noindent` automatique

### Intégration pédagogique
Ces compétences correspondent au référentiel officiel des mathématiques au lycée et permettent d'identifier précisément les capacités travaillées dans chaque exercice ou activité.
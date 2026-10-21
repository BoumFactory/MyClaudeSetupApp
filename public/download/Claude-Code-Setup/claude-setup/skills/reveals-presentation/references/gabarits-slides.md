# Gabarits HTML de slides

Squelette HTML de base (celui des templates), conventions de formatage et exemples de slides (titre, contenu avec fragments, exercice avec formules).

## Structure HTML de base

```html
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Titre de la présentation</title>
  <meta name="author" content="Votre nom">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <!-- Reveal.js CSS -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/reveal.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/theme/white.css">

  <!-- Custom styles -->
  <style>
    /* Styles personnalisés selon le template */
  </style>
</head>
<body>
  <div class="reveal">
    <div class="slides">
      <!-- Slides ici -->
    </div>
  </div>

  <!-- Reveal.js JS -->
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/reveal.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/plugin/math/math.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/plugin/notes/notes.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/plugin/highlight/highlight.js"></script>

  <script>
    Reveal.initialize({
      // Configuration
    });
  </script>
</body>
</html>
```

## Conventions de formatage textuel

Pour les citations et mise en forme du texte :

- **Citations** : Utiliser les guillemets français `«\u00a0texte\u00a0»` ou `<q>texte</q>` pour le HTML sémantique
- **Mise en valeur** : Utiliser `<strong>texte</strong>` pour les termes importants
- **Emphase** : Utiliser `<em>texte</em>` pour l'emphase italique
- **Code/Variables** : Utiliser `<code>valeur</code>` pour les valeurs littérales

Exemple :
```html
<section>
  <h2>Exemple de citation</h2>
  <p>Selon le théorème, <q>la somme des angles d'un triangle vaut 180 degrés</q>.</p>
  <p>Il est <strong>important</strong> de noter que <em>tous</em> les triangles respectent cette propriété.</p>
</section>
```

## Slide de titre

```html
<section>
  <h1>Titre de la présentation</h1>
  <h3>Sous-titre</h3>
  <p>
    <small>Par <strong>Nom de l'auteur</strong></small><br>
    <small>Établissement</small><br>
    <small>Date</small>
  </p>
</section>
```

## Slide de contenu avec fragments

```html
<section>
  <h2>Titre de la slide</h2>

  <ul>
    <li class="fragment">Premier point</li>
    <li class="fragment">Deuxième point</li>
    <li class="fragment">Troisième point</li>
  </ul>

  <div class="fragment">
    <div class="box-info">
      <strong>Point important :</strong> Une information clé à retenir
    </div>
  </div>
</section>
```

## Slide avec exercice et formules mathématiques

```html
<section class="exercise">
  <h2>Exercice : Application directe</h2>

  <div class="exercise-header">
    <span class="difficulty">★☆☆</span>
    <span class="estimated-time">5 minutes</span>
  </div>

  <!-- Énoncé -->
  <div class="statement">
    <p><strong>Énoncé :</strong> Résoudre l'équation suivante :</p>
    <p>\[2x + 3 = 7\]</p>
  </div>

  <!-- Solution progressive -->
  <div class="fragment">
    <p><strong>Solution :</strong></p>
    <p>\begin{align}
      2x + 3 &= 7 \\
      2x &= 4 \\
      x &= 2
    \end{align}</p>
  </div>

  <!-- Résultat encadré -->
  <div class="fragment">
    <div class="result-box">
      \(x = 2\)
    </div>
  </div>
</section>
```

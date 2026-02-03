# Arborescences de Fichiers en LaTeX

Guide de référence pour afficher des arborescences de fichiers et dossiers dans les documents LaTeX bfcours.

## Package dirtree

Le package `dirtree` est **déjà chargé par bfcours** et permet de créer des arborescences de fichiers professionnelles et claires.

### Syntaxe de base

```latex
\begin{dirtree}{.1}
.1 Racine/.
.2 Sous-dossier1/.
.3 fichier1.txt.
.3 fichier2.pdf.
.2 Sous-dossier2/.
.3 fichier3.tex.
.4 sous-sous-dossier/.
.5 fichier-profond.txt.
\end{dirtree}
```

### Règles importantes

1. **Chaque ligne doit se terminer par un point** (`.`)
2. **Les niveaux sont indiqués par `.1`, `.2`, `.3`, etc.**
   - `.1` = Racine (niveau 0)
   - `.2` = Premier niveau de sous-dossiers
   - `.3` = Deuxième niveau
   - etc.
3. **Les dossiers doivent avoir un `/` à la fin** du nom
4. **Les underscores doivent être échappés** : `\_` au lieu de `_`

### Exemple complet avec projet LaTeX

```latex
\begin{dirtree}{.1}
.1 Mon\_Projet\_Cours/.
.2 Mon\_Cours.tex.
.2 enonce.tex.
.2 enonce\_figures.tex.
.2 sections/.
.3 01\_introduction.tex.
.3 02\_definitions.tex.
.3 03\_proprietes.tex.
.3 04\_exemples.tex.
.2 images/.
.3 figure1.png.
.3 figure2.pdf.
.2 annexes/.
.3 script\_generation.py.
.3 donnees.csv.
\end{dirtree}
```

### Exemple avec projet complet de séquence

```latex
\begin{dirtree}{.1}
.1 Sequence\_Vecteurs\_2nde/.
.2 PDFs/.
.3 Cours\_Vecteurs.pdf.
.3 Exercices\_Vecteurs\_ELEVE.pdf.
.3 Exercices\_Vecteurs\_PROF.pdf.
.3 DS\_Vecteurs\_ELEVE.pdf.
.3 DS\_Vecteurs\_PROF.pdf.
.2 Sources/.
.3 Cours\_Vecteurs/.
.4 Cours\_Vecteurs.tex.
.4 sections/.
.5 01\_introduction.tex.
.5 02\_operations.tex.
.3 Exercices\_Vecteurs/.
.4 Exercices\_Vecteurs.tex.
.4 enonce.tex.
.3 DS\_Vecteurs/.
.4 DS\_Vecteurs.tex.
.4 enonce.tex.
.2 Apps/.
.3 App\_Vecteurs.exe.
\end{dirtree}
```

## Intégration dans les environnements bfcours

### Dans un environnement Exemple

```latex
\begin{Exemple}[Structure du projet]
\acc{Organisation des fichiers :}

\begin{dirtree}{.1}
.1 Projet/.
.2 sources/.
.3 main.tex.
.2 output/.
.3 main.pdf.
\end{dirtree}

Cette structure sépare clairement les sources des sorties compilées.
\end{Exemple}
```

### Dans un environnement Remarque

```latex
\begin{Remarque}[Organisation recommandée]
Pour un projet de séquence complète, privilégiez l'arborescence suivante :

\begin{dirtree}{.1}
.1 Nom\_Sequence/.
.2 01\_Cours/.
.2 02\_Exercices/.
.2 03\_Evaluations/.
.2 04\_Applications/.
\end{dirtree}
\end{Remarque}
```

## Cas d'usage typiques

### 1. Documenter la structure d'un nouveau projet

Lorsque vous utilisez le skill `tex-document-creator`, vous pouvez documenter la structure créée :

```latex
\begin{Exemple}[Projet créé]
Le script a généré l'arborescence suivante :

\begin{dirtree}{.1}
.1 Nouveau\_Cours/.
.2 Nouveau\_Cours.tex.
.2 enonce.tex.
.2 enonce\_figures.tex.
.2 sections/.
.2 images/.
\end{dirtree}
\end{Exemple}
```

### 2. Expliquer un workflow de compilation

```latex
\begin{Methode}[Compilation d'un projet]
\acc{Étape 1 :} Organisation des fichiers

\begin{dirtree}{.1}
.1 Projet/.
.2 main.tex.
.2 bibliographie.bib.
.2 images/.
\end{dirtree}

\acc{Étape 2 :} Après compilation

\begin{dirtree}{.1}
.1 Projet/.
.2 main.tex.
.2 main.pdf.
.2 main.aux.
.2 main.log.
.2 bibliographie.bib.
.2 images/.
\end{dirtree}
\end{Methode}
```

### 3. Montrer l'évolution d'un projet

```latex
\begin{MultiColonnes}{2}
\tcbitem[title=Avant]
\begin{dirtree}{.1}
.1 Projet/.
.2 fichier.tex.
\end{dirtree}

\tcbitem[title=Après]
\begin{dirtree}{.1}
.1 Projet/.
.2 fichier.tex.
.2 sections/.
.3 intro.tex.
.3 corps.tex.
.2 images/.
\end{dirtree}
\end{MultiColonnes}
```

## Personnalisation visuelle

### Avec encadrement dans MultiColonnes

```latex
\begin{MultiColonnes}{2}[colframe=ex,boxrule=0.4pt]
\tcbitem[title=Structure source]
\begin{dirtree}{.1}
.1 src/.
.2 main.tex.
\end{dirtree}

\tcbitem[title=Structure output]
\begin{dirtree}{.1}
.1 output/.
.2 main.pdf.
\end{dirtree}
\end{MultiColonnes}
```

### Avec titre accentué

```latex
\acc{Arborescence du projet :}

\begin{dirtree}{.1}
.1 Projet/.
.2 fichiers.tex.
\end{dirtree}
```

## Erreurs courantes à éviter

### ❌ Erreur : Oubli du point final

```latex
\begin{dirtree}{.1}
.1 Dossier/          ← MAUVAIS : pas de point
.2 fichier.txt       ← MAUVAIS : pas de point
\end{dirtree}
```

### ✅ Correct : Point final obligatoire

```latex
\begin{dirtree}{.1}
.1 Dossier/.         ← BON
.2 fichier.txt.      ← BON
\end{dirtree}
```

### ❌ Erreur : Underscores non échappés

```latex
\begin{dirtree}{.1}
.1 Mon_Projet/       ← MAUVAIS : _ non échappé
\end{dirtree}
```

### ✅ Correct : Underscores échappés

```latex
\begin{dirtree}{.1}
.1 Mon\_Projet/.     ← BON : \_ échappé
\end{dirtree}
```

### ❌ Erreur : Mauvaise indentation des niveaux

```latex
\begin{dirtree}{.1}
.1 Racine/.
.3 fichier.txt.      ← MAUVAIS : saute .2
\end{dirtree}
```

### ✅ Correct : Niveaux progressifs

```latex
\begin{dirtree}{.1}
.1 Racine/.
.2 Dossier/.
.3 fichier.txt.      ← BON : .1 → .2 → .3
\end{dirtree}
```

## Alternative : Forest (pour arborescences complexes)

Pour des arborescences très complexes ou avec des annotations spéciales, le package `forest` peut être utilisé, mais `dirtree` suffit pour 95% des cas d'usage en documentation pédagogique.

## Bonnes pratiques

1. **Utiliser dirtree systématiquement** pour les arborescences de fichiers (ne pas utiliser de tableaux ASCII avec `├──` et `│`)
2. **Toujours échapper les underscores** dans les noms de fichiers
3. **Terminer chaque ligne par un point** sans exception
4. **Ajouter `/` aux noms de dossiers** pour les distinguer des fichiers
5. **Utiliser des niveaux progressifs** (pas de saut de `.2` à `.4`)
6. **Intégrer dans des environnements didactiques** (Exemple, Remarque, Methode)

## Exemples réels d'utilisation

### Documentation d'un agent

```latex
\begin{Exemple}[Structure générée par l'agent app-creator]
L'agent génère automatiquement l'arborescence suivante :

\begin{dirtree}{.1}
.1 app\_exercices\_vecteurs/.
.2 app.py.
.2 config.py.
.2 requirements.txt.
.2 static/.
.3 css/.
.4 main.css.
.3 js/.
.4 main.js.
.2 templates/.
.3 base.html.
.3 index.html.
.2 data/.
.3 content.json.
.2 tests/.
.3 test\_app.py.
.2 dist/.
.3 EducationalApp.exe.
\end{dirtree}

L'exécutable standalone est dans \texttt{dist/}.
\end{Exemple}
```

### Documentation d'un workflow

```latex
\begin{Activite}[Créer une séquence complète]
\acc{Étape 1 :} Créer l'arborescence

\begin{dirtree}{.1}
.1 Fonctions\_1ere/.
.2 Cours/.
.2 Exercices/.
.2 DS/.
\end{dirtree}

\acc{Étape 2 :} Remplir chaque dossier avec les documents LaTeX

\acc{Étape 3 :} Compiler tous les documents

Résultat final :

\begin{dirtree}{.1}
.1 Fonctions\_1ere/.
.2 Cours/.
.3 Cours\_Fonctions.tex.
.3 Cours\_Fonctions.pdf.
.2 Exercices/.
.3 Exercices\_Fonctions.tex.
.3 Exercices\_Fonctions.pdf.
.2 DS/.
.3 DS\_Fonctions.tex.
.3 DS\_Fonctions.pdf.
\end{dirtree}
\end{Activite}
```

## Résumé

- ✅ **Toujours utiliser `dirtree` pour les arborescences**
- ✅ **Point final obligatoire sur chaque ligne**
- ✅ **`/` pour les dossiers**
- ✅ **`\_` pour les underscores**
- ✅ **Niveaux progressifs (`.1`, `.2`, `.3`...)**
- ❌ **Jamais de tableaux ASCII avec caractères spéciaux**
- ❌ **Jamais de `verbatim` dans les tcolorbox**

---

**Référence créée le** : 2025-10-20
**Skill** : bfcours-latex
**Auteur** : Système .claude

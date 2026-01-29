# Système d'infobulles interactives

Le système d'infobulles permet d'ajouter des explications contextuelles au survol de termes importants dans les cours HTML/KaTeX.

## 6 catégories disponibles

| Classe | Couleur | Usage | Style de soulignement |
|--------|---------|-------|----------------------|
| `tip-def` | Rouge rubis | Définitions mathématiques | Pointillé |
| `tip-formule` | Orange | Formules à retenir | Tirets |
| `tip-prop` | Vert émeraude | Propriétés importantes | Pointillé |
| `tip-attention` | Rouge vif | Points d'attention, erreurs fréquentes | Ondulé + animation |
| `tip-astuce` | Cyan | Astuces et conseils | Pointillé |
| `tip-lien` | Bleu | Liens vers d'autres notions | Plein |

## Syntaxe

```html
<span class="tip-def" data-tip="Explication de la définition...">terme à définir</span>
```

### Attribut obligatoire

- `data-tip` : Le texte de l'infobulle (max ~200 caractères recommandé)

## Exemples d'utilisation

### Définition (tip-def)
```html
Une fonction est <span class="tip-def" data-tip="Une fonction est dérivable sur un intervalle I si elle admet un nombre dérivé en tout point de I.">dérivable sur un intervalle</span> si...
```

### Formule (tip-formule)
```html
La formule <span class="tip-formule" data-tip="On « descend » l'exposant n devant et on diminue l'exposant de 1.">$(x^n)' = nx^{n-1}$</span>
```

### Propriété (tip-prop)
```html
Ces <span class="tip-prop" data-tip="Propriétés fondamentales du calcul différentiel.">formules de dérivation</span> sont essentielles.
```

### Attention (tip-attention)
```html
<span class="tip-attention" data-tip="Ne pas oublier le facteur a ! C'est l'erreur la plus fréquente.">Le coefficient $a$ apparaît devant</span>
```

### Astuce (tip-astuce)
```html
<span class="tip-astuce" data-tip="« Dérivée du haut × bas − haut × dérivée du bas ». Attention à l'ordre !">Moyen mnémotechnique</span>
```

### Lien (tip-lien)
```html
Voir la <span class="tip-lien" data-tip="Section 2.1 : (u+v)' = u' + v'">formule de la somme</span>
```

## Rétrocompatibilité

L'ancienne classe `.vocab` avec `data-definition` reste fonctionnelle :

```html
<span class="vocab" data-definition="Explication...">terme</span>
```

Elle est automatiquement stylée comme `tip-def`.

## Bonnes pratiques

1. **Ne pas surcharger** : 3-5 infobulles par paragraphe maximum
2. **Textes concis** : Max 200 caractères par infobulle
3. **Cohérence** : Utiliser la même catégorie pour le même type d'information
4. **Pertinence** : Réserver les infobulles aux termes qui nécessitent vraiment une explication

## Caractéristiques visuelles

- Apparition fluide avec animation (0.3s)
- Ombre portée pour un effet de profondeur
- Fond dégradé pour chaque catégorie
- Flèche pointant vers le terme
- Largeur max : 320px
- Z-index élevé (1000) pour passer au-dessus des autres éléments

## Personnalisation (avancé)

Les couleurs peuvent être modifiées dans `styles/base.css` dans la section "INFOBULLES INTERACTIVES".

Chaque catégorie définit :
- Couleur du texte
- Couleur du soulignement
- Background du terme (gradient léger)
- Background de la bulle
- Couleur de la flèche

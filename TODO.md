# TODO - Refactoring bfcours.dev

## 1. Refactoring exercices des capsules tutoriel

### Probleme
Dans les capsules de tutoriel, la section "pratique" souffre de deux defauts :
1. **Redondance titre** : le label "A vous de jouer" est affiche par l'accordeon du composant Capsule.tsx (SECTION_CONFIG key "pratique", label "A vous de jouer"), ET repete en `<h3>` dans le HTML de parcours.ts (13 capsules sur 14 concernees)
2. **Exercices sans correction** : les exercices sont listes comme texte brut, sans solution depliable

### Prompt agent — instructions de resolution

<agent-instructions>

# Refactoring des exercices tutoriel — Capsules pratique

## Role

Expert frontend React/Next.js specialise en composants educatifs interactifs. Tu maitrises le HTML semantique, le CSS dark-theme et les patterns d'accessibilite.

## Contexte

<project>
- App Next.js (App Router) dans MyClaudeSetupApp
- Composant capsule : `src/components/tutorials/Capsule.tsx`
  - Affiche 3 sections accordeon : "A savoir" (info), "Exemple" (exemple), "A vous de jouer" (pratique)
  - Le label "A vous de jouer" est DEJA rendu par SECTION_CONFIG (ligne 35)
  - Le contenu HTML des sections est injecte via `dangerouslySetInnerHTML` + `processVocabulary()`
- Donnees : `src/data/parcours.ts`
  - Contient toutes les capsules avec leurs sections HTML (info, exemple, pratique)
  - 14 capsules ont une section pratique, 13 commencent par `<h3>A vous de jouer</h3>` (redondant)
  - 1 capsule (qv-overview) utilise deja le pattern `<details><summary>` pour les corrections — c'est le bon pattern
- Styles globaux : `src/app/globals.css` — contient les styles `.capsule-content`
</project>

## Instructions

Executer ces 3 etapes dans l'ordre. Lire chaque fichier AVANT de le modifier.

### Etape 1 : Supprimer les h3 redondants

Dans `src/data/parcours.ts`, pour CHAQUE capsule dont la section `pratique` commence par `<h3>A vous de jouer</h3>`, supprimer ce h3 et l'eventuel `<p>` d'introduction generique qui suit (ex: "Maintenant que...").

Ne PAS toucher aux h3/h4 qui sont des titres d'exercices specifiques (ex: `<h3>Exercice : tester le systeme</h3>`).

Verifier : la capsule `qv-overview` a un `<h3>Explorer</h3>` qui n'est PAS redondant — ne pas le supprimer.

### Etape 2 : Transformer les exercices en cartes avec solution depliable

Pour chaque exercice dans les sections `pratique`, appliquer ce pattern HTML :

```html
<div class="exercise-card">
  <div class="exercise-header">
    <span class="exercise-badge">Exercice 1</span>
    <!-- ou "Defi rapide", "Investigation", etc. -->
  </div>
  <div class="exercise-body">
    <p>Enonce de l'exercice visible directement...</p>
  </div>
  <details class="exercise-solution">
    <summary>Voir la solution</summary>
    <div class="solution-content">
      <p>Correction detaillee de l'exercice...</p>
    </div>
  </details>
</div>
```

Pour les corrections :
- Rediger une reponse pedagogique adaptee au public enseignant debutant en IA
- La correction doit etre concrete et actionnable (pas juste "la reponse est X")
- Pour les exercices de type "explorez/decouvrez", decrire ce que l'utilisateur devrait observer ou trouver
- Pour les exercices de type "envoyez ce prompt", donner un exemple de reponse attendue et ce qu'il faut en retenir

### Etape 3 : Ajouter les styles CSS

Dans `src/app/globals.css`, a l'interieur du scope `.capsule-content`, ajouter les styles pour les classes :

```css
/* Dans .capsule-content */
.exercise-card {
  margin-bottom: 1.5rem;
  padding: 1rem 1.25rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.exercise-header {
  margin-bottom: 0.75rem;
}

.exercise-badge {
  display: inline-block;
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #34d399;
  background: rgba(52, 211, 153, 0.1);
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
}

.exercise-body {
  margin-bottom: 0.75rem;
}

.exercise-body p,
.exercise-body ol,
.exercise-body ul {
  margin: 0.5rem 0;
}

.exercise-solution {
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  padding-top: 0.5rem;
}

.exercise-solution summary {
  cursor: pointer;
  color: #34d399;
  font-weight: 600;
  font-size: 0.9rem;
  padding: 0.5rem 0;
  list-style: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.exercise-solution summary::before {
  content: "▶";
  font-size: 0.7rem;
  transition: transform 0.2s;
}

.exercise-solution[open] summary::before {
  transform: rotate(90deg);
}

.solution-content {
  padding: 0.75rem 1rem;
  margin-top: 0.5rem;
  background: rgba(52, 211, 153, 0.05);
  border-radius: 8px;
  border-left: 3px solid rgba(52, 211, 153, 0.3);
}
```

## Contraintes

- Ne PAS creer de nouveaux composants React — tout est du HTML injecte via dangerouslySetInnerHTML
- Ne PAS modifier la structure du composant Capsule.tsx sauf si absolument necessaire
- Respecter le dark-theme existant (fond sombre, texte clair, accents emerald/green pour la section pratique)
- La capsule `qv-overview` a DEJA des `<details><summary>` bien formates — ne pas la casser, la mettre a jour pour utiliser les memes classes CSS
- Tester visuellement que le rendu est coherent sur toutes les capsules

## Format de sortie

Fichiers modifies :
1. `src/data/parcours.ts` — contenu HTML des sections pratique
2. `src/app/globals.css` — styles des cartes exercice

## Criteres de qualite (auto-verification)

- [ ] Aucun `<h3>A vous de jouer</h3>` ne subsiste dans parcours.ts
- [ ] Chaque exercice est dans une `div.exercise-card` avec badge, enonce, et solution depliable
- [ ] Chaque solution contient une correction pedagogique pertinente (pas de placeholder)
- [ ] Les styles CSS sont dans `.capsule-content` et n'affectent pas d'autres composants
- [ ] La capsule qv-overview conserve son format QCM fonctionnel
- [ ] Pas de regression visuelle sur les sections info et exemple

</agent-instructions>

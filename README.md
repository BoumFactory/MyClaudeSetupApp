# MyClaudeSetupApp - IA & Enseignement des Mathématiques

Application Next.js pour partager des connaissances sur l'intelligence artificielle au service des enseignants de mathématiques.

## Fonctionnalités

### Architecture Modulaire par Scopes

L'application est organisée en **scopes** thématiques, chacun représentant une section dédiée :

- **Claude Code** : Premier scope disponible avec présentations, téléchargements, vidéos et applications
- Possibilité d'ajouter facilement de nouveaux scopes

### Lecture Automatique des Ressources

- Scanner automatique des présentations reveal.js dans `src/public/render/Reveals/`
- Détection et organisation automatique du contenu
- Le site se met à jour automatiquement quand de nouvelles ressources sont ajoutées

### Viewer de Présentations Reveal.js

- Affichage des présentations HTML dans un iframe
- Navigation au clavier et tactile
- Mode plein écran
- Instructions d'utilisation intégrées

### Système de Téléchargement Intelligent

- Explorateur de fichiers pour `src/public/download/ClaudeCode/`
- Sélection granulaire (fichiers et dossiers)
- Génération de ZIP à la demande
- Respect automatique du `.gitignore`

### Intégration YouTube

- Composants pour intégrer des vidéos YouTube
- Vignettes et descriptions
- Liens directs vers YouTube

### Animations Mathématiques de Fond

- 9 animations mathématiques interactives en arrière-plan
- Bouton dans la navbar pour changer d'animation à la volée
- Tooltip informatif avec description de l'animation actuelle
- Animations disponibles :
  1. **Spirale de Fibonacci** - Le nombre d'or dans la nature
  2. **Épicycles de Fourier** - Cercles tournant sur des cercles
  3. **Champ Vectoriel** - Particules suivant des lignes de force
  4. **Courbes de Lissajous** - Harmonies de fréquences
  5. **Spirale d'Ulam** - Diagonales mystérieuses des nombres premiers
  6. **Attracteur de Lorenz** - Chaos déterministe (effet papillon)
  7. **Attracteur de Rössler** - Bande de Möbius chaotique
  8. **Triangle de Sierpiński** - Fractale par jeu du chaos
  9. **Courbe du Dragon** - Fractale par pliage de papier
- Performances optimisées avec Canvas API
- Choix sauvegardé en session pour persistance

## Stack Technique

- **Framework** : Next.js 15+ (App Router)
- **React** : 19+
- **TypeScript** : Typage strict
- **Styling** : Tailwind CSS avec thème cosmique personnalisé
- **UI Components** : shadcn/ui (Radix UI)
- **Icônes** : Lucide React
- **Validation** : Zod
- **Forms** : react-hook-form
- **ZIP** : JSZip
- **Gestionnaire de paquets** : pnpm

## Structure du Projet

```
MyClaudeSetupApp/
├── src/
│   ├── app/                          # Pages Next.js (App Router)
│   │   ├── layout.tsx                # Layout principal avec thème
│   │   ├── page.tsx                  # Page d'accueil
│   │   ├── globals.css               # Styles globaux
│   │   ├── loading.tsx               # Page de chargement
│   │   ├── not-found.tsx             # Page 404
│   │   ├── api/
│   │   │   └── download/
│   │   │       └── route.ts          # API pour générer les ZIP
│   │   └── claude-code/              # Scope Claude Code
│   │       ├── page.tsx
│   │       ├── presentations/
│   │       │   ├── page.tsx          # Liste des présentations
│   │       │   └── [slug]/
│   │       │       ├── page.tsx      # Viewer de présentation
│   │       │       └── not-found.tsx
│   │       ├── downloads/
│   │       │   └── page.tsx          # Explorateur de fichiers
│   │       ├── videos/
│   │       │   └── page.tsx          # Liste des vidéos
│   │       └── applications/
│   │           └── page.tsx          # Liste des applications
│   ├── components/
│   │   ├── ui/                       # Composants shadcn/ui
│   │   │   ├── button.tsx
│   │   │   └── card.tsx
│   │   ├── layout/                   # Composants de layout
│   │   │   ├── MainNav.tsx           # Navigation avec UX optimisée
│   │   │   └── Footer.tsx
│   │   ├── background/               # Animations de fond
│   │   │   ├── MathBackground.tsx
│   │   │   └── animations/           # 9 animations mathématiques
│   │   ├── presentations/            # Composants pour présentations
│   │   │   └── PresentationViewer.tsx
│   │   ├── downloads/                # Composants pour téléchargements
│   │   │   ├── FileExplorer.tsx
│   │   │   └── FileTreeItem.tsx
│   │   ├── youtube/                  # Composants YouTube
│   │   │   └── YouTubeEmbed.tsx
│   │   └── ScopeCard.tsx            # Carte de présentation de scope
│   ├── contexts/
│   │   └── BackgroundAnimationContext.tsx # Gestion des animations
│   ├── lib/
│   │   ├── utils.ts                  # Utilitaires généraux
│   │   ├── file-scanner.ts           # Scanner de fichiers
│   │   ├── zip-generator.ts          # Générateur de ZIP
│   │   ├── gitignore-parser.ts       # Parser .gitignore
│   │   └── data/
│   │       └── scopes.ts             # Configuration des scopes
│   ├── types/
│   │   └── index.ts                  # Types TypeScript
│   └── public/
│       ├── render/
│       │   ├── Reveals/              # Présentations reveal.js (HTML)
│       │   └── assets/               # Assets des présentations
│       └── download/
│           └── ClaudeCode/           # Fichiers téléchargeables
│               └── Applications_educatives/
├── .gitignore
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── next.config.js
├── postcss.config.js
├── components.json
└── README.md
```

## Installation et Démarrage

### Prérequis

- Node.js 18+
- pnpm (gestionnaire de paquets)

### Installation

```bash
# Cloner le projet
git clone <url-du-repo>
cd MyClaudeSetupApp

# Installer les dépendances
pnpm install
```

### Développement

```bash
# Lancer le serveur de développement
pnpm dev
```

L'application sera accessible sur [http://localhost:3000](http://localhost:3000)

### Build Production

```bash
# Construire l'application
pnpm build

# Lancer en production
pnpm start
```

### Vérification TypeScript

```bash
# Vérifier les erreurs TypeScript
pnpm type-check
```

## Ajouter du Contenu

### Ajouter une Présentation Reveal.js

1. Placez votre fichier HTML dans `src/public/render/Reveals/`
2. Les assets (images) dans `src/public/render/assets/`
3. L'application détectera automatiquement la nouvelle présentation
4. Elle sera visible sur `/claude-code/presentations`

### Ajouter des Fichiers Téléchargeables

1. Placez vos fichiers dans `src/public/download/ClaudeCode/`
2. Les fichiers listés dans `.gitignore` seront automatiquement exclus (sauf `dist/` et `build/` dans les téléchargements pour inclure les exécutables)
3. Ils seront accessibles depuis `/claude-code/downloads`

**Note** : Les dossiers `dist/` et `build/` sont inclus dans les téléchargements pour permettre aux utilisateurs d'obtenir les fichiers exécutables (.exe) ou les builds prêts à l'emploi.

### Ajouter des Vidéos YouTube

1. Modifiez `src/lib/data/scopes.ts`
2. Ajoutez vos vidéos dans le tableau `claudeCodeVideos`
3. Elles apparaîtront sur `/claude-code/videos`

### Ajouter un Nouveau Scope

1. Ajoutez le scope dans `src/lib/data/scopes.ts` :

```typescript
{
  id: 'nouveau-scope',
  title: 'Nouveau Scope',
  slug: 'nouveau-scope',
  description: 'Description du scope',
  icon: 'Code2',
  color: 'cosmic-600',
  gradient: 'from-cosmic-500 to-cosmic-700',
  path: '/nouveau-scope',
}
```

2. Créez le dossier `src/app/nouveau-scope/`
3. Ajoutez `page.tsx` avec le contenu du scope
4. Le scope apparaîtra automatiquement dans la navigation

## Thème et Design

### Palette de Couleurs

L'application utilise un thème **futuriste nébuleux espace** :

- **Cosmic** (bleus/indigo) : Couleur principale
- **Nebula** (violets/roses) : Couleur secondaire
- Mode sombre par défaut
- Effets de verre (glassmorphism)
- Animations subtiles

### Classes Utilitaires Personnalisées

- `.cosmic-bg` : Fond cosmique animé avec étoiles
- `.glass-card` : Effet de verre avec backdrop blur
- `.cosmic-gradient` : Dégradé cosmic
- `.nebula-gradient` : Dégradé nebula
- `.glow-text` : Texte avec effet de lueur
- `.glow-border` : Bordure lumineuse

## API Routes

### POST /api/download

Génère un fichier ZIP à partir des fichiers sélectionnés.

**Body** :
```json
{
  "files": [...],  // Arbre de fichiers avec sélections
  "basePath": "..." // Chemin de base
}
```

**Response** : Fichier ZIP en téléchargement

## Points d'Extension

### Fonctionnalités à Ajouter

1. **Recherche** : Barre de recherche globale pour les ressources
2. **Filtres** : Filtrage des présentations par catégorie/tag
3. **Favoris** : Système de favoris (localStorage)
4. **Partage** : Boutons de partage social
5. **Analytics** : Tracking des téléchargements et vues
6. **Commentaires** : Système de commentaires sur les ressources
7. **Multi-langue** : Internationalisation (i18n)
8. **Dark/Light Mode** : Toggle manuel pour le thème
9. **PWA** : Progressive Web App avec offline support
10. **RSS** : Flux RSS pour les nouvelles ressources

### Améliorations Techniques

1. **Tests** : Jest + React Testing Library
2. **E2E Tests** : Playwright ou Cypress
3. **CI/CD** : GitHub Actions pour déploiement automatique
4. **Performance** : Lazy loading, code splitting optimisé
5. **SEO** : Sitemap XML, robots.txt, Open Graph amélioré
6. **Accessibilité** : Audit WCAG complet
7. **Cache** : Stratégies de cache optimisées
8. **API** : API RESTful ou GraphQL pour les données

## Déploiement

### Vercel (Recommandé)

```bash
# Installer Vercel CLI
pnpm add -g vercel

# Déployer
vercel
```

### Autres Plateformes

- **Netlify** : Compatible Next.js
- **Cloudflare Pages** : Avec Next.js runtime
- **AWS Amplify** : Support Next.js SSR
- **Docker** : Dockerfile disponible

## Contribution

Ce projet est conçu pour être facilement extensible. Pour contribuer :

1. Forkez le projet
2. Créez une branche (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add AmazingFeature'`)
4. Pushez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## Licence

ISC

## Support

Pour toute question ou problème :
- Email : contact@example.com
- GitHub Issues : <url-du-repo>/issues

## Remerciements

- **Anthropic** pour Claude Code
- **Reveal.js** pour le framework de présentation
- **shadcn/ui** pour les composants UI
- **Vercel** pour Next.js

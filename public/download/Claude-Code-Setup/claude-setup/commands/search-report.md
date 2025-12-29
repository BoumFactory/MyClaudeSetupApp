---
description: Recherche approfondie sur un sujet et génération d'un rapport HTML complet
tags: [recherche, web, rapport, documentation, enquête]
---

# Recherche et Rapport Web

Cette commande effectue une recherche approfondie sur Internet concernant le sujet demandé et génère un rapport HTML complet, informatif et bien structuré.

## Argument requis

$ARGUMENTS = Le sujet de recherche (ex: "WebSocket vs Server-Sent Events", "HTMX framework", "DuckDB database")

## Instructions

### 1. Comprendre le sujet

Analyse le sujet fourni pour identifier :
- Le domaine principal (technologie, pédagogie, outil, concept...)
- Les questions clés à investiguer
- Les angles d'approche possibles

### 2. Mener l'enquête web

Utilise `WebSearch` de manière extensive pour couvrir :

**A. Informations fondamentales**
- Qu'est-ce que c'est ? Définition précise
- Qui l'a créé ? Historique et contexte d'émergence
- À quel problème ça répond ?
- Comment ça fonctionne (architecture, principes)

**B. Aspects pratiques**
- Cas d'usage principaux et exemples concrets
- Avantages et inconvénients documentés
- Limitations connues et pièges à éviter
- Courbe d'apprentissage

**C. Écosystème et alternatives**
- Solutions concurrentes ou complémentaires
- Comparaison objective avec les alternatives
- Ce qui distingue cette solution (USP)
- Tendances d'adoption et popularité

**D. Aspects non évidents**
- Critiques et controverses
- Retours d'expérience réels (success stories ET échecs)
- Évolutions récentes et roadmap
- Communauté et support

**E. Ressources utiles**
- Documentation officielle
- Tutoriels recommandés
- Outils et extensions associés

### 3. Utiliser WebFetch pour approfondir

Pour les sources importantes trouvées, utilise `WebFetch` pour extraire :
- Détails techniques précis
- Exemples de code ou configurations
- Benchmarks et comparatifs
- Témoignages d'utilisateurs

### 4. Générer le rapport HTML

Crée un fichier HTML complet dans :
```
C:\Users\Utilisateur\Documents\Professionnel\1. Reims 2025 - 2026\3. Ressources\6.search-reports\
```

**Nom du fichier** : `[sujet-slug]-[YYYY-MM-DD].html` (ex: `htmx-framework-2025-01-15.html`)

**Structure du rapport** :

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapport : [SUJET]</title>
    <style>
        :root {
            --primary: #2563eb;
            --secondary: #64748b;
            --success: #22c55e;
            --warning: #f59e0b;
            --danger: #ef4444;
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --text: #1e293b;
            --text-muted: #64748b;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
            padding: 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }

        header {
            background: linear-gradient(135deg, var(--primary), #1d4ed8);
            color: white;
            padding: 3rem 2rem;
            border-radius: 1rem;
            margin-bottom: 2rem;
            box-shadow: 0 10px 40px rgba(37, 99, 235, 0.2);
        }

        header h1 { font-size: 2.5rem; margin-bottom: 0.5rem; }
        header .meta { opacity: 0.9; font-size: 0.95rem; }

        nav.toc {
            background: var(--card-bg);
            padding: 1.5rem 2rem;
            border-radius: 0.75rem;
            margin-bottom: 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }

        nav.toc h2 { font-size: 1.1rem; color: var(--secondary); margin-bottom: 1rem; }
        nav.toc ul { list-style: none; display: flex; flex-wrap: wrap; gap: 0.5rem 1rem; }
        nav.toc a { color: var(--primary); text-decoration: none; }
        nav.toc a:hover { text-decoration: underline; }

        section {
            background: var(--card-bg);
            padding: 2rem;
            border-radius: 0.75rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }

        section h2 {
            color: var(--primary);
            font-size: 1.5rem;
            margin-bottom: 1.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid var(--primary);
        }

        section h3 {
            color: var(--text);
            font-size: 1.2rem;
            margin: 1.5rem 0 1rem;
        }

        p { margin-bottom: 1rem; }

        ul, ol { margin: 1rem 0 1rem 1.5rem; }
        li { margin-bottom: 0.5rem; }

        .highlight {
            background: linear-gradient(135deg, #fef3c7, #fde68a);
            border-left: 4px solid var(--warning);
            padding: 1rem 1.5rem;
            border-radius: 0 0.5rem 0.5rem 0;
            margin: 1rem 0;
        }

        .info-box {
            background: #eff6ff;
            border-left: 4px solid var(--primary);
            padding: 1rem 1.5rem;
            border-radius: 0 0.5rem 0.5rem 0;
            margin: 1rem 0;
        }

        .warning-box {
            background: #fef2f2;
            border-left: 4px solid var(--danger);
            padding: 1rem 1.5rem;
            border-radius: 0 0.5rem 0.5rem 0;
            margin: 1rem 0;
        }

        .success-box {
            background: #f0fdf4;
            border-left: 4px solid var(--success);
            padding: 1rem 1.5rem;
            border-radius: 0 0.5rem 0.5rem 0;
            margin: 1rem 0;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
        }

        th, td {
            padding: 0.75rem 1rem;
            text-align: left;
            border-bottom: 1px solid #e2e8f0;
        }

        th { background: var(--bg); font-weight: 600; }
        tr:hover { background: var(--bg); }

        code {
            background: #f1f5f9;
            padding: 0.2rem 0.4rem;
            border-radius: 0.25rem;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 0.9em;
        }

        pre {
            background: #1e293b;
            color: #e2e8f0;
            padding: 1.5rem;
            border-radius: 0.5rem;
            overflow-x: auto;
            margin: 1rem 0;
        }

        pre code { background: none; color: inherit; padding: 0; }

        .badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 1rem;
            font-size: 0.85rem;
            font-weight: 500;
        }

        .badge-primary { background: #dbeafe; color: #1d4ed8; }
        .badge-success { background: #dcfce7; color: #166534; }
        .badge-warning { background: #fef3c7; color: #92400e; }
        .badge-danger { background: #fee2e2; color: #991b1b; }

        .comparison-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1rem;
            margin: 1rem 0;
        }

        .comparison-card {
            background: var(--bg);
            padding: 1.5rem;
            border-radius: 0.5rem;
            border: 1px solid #e2e8f0;
        }

        .comparison-card h4 {
            color: var(--primary);
            margin-bottom: 1rem;
        }

        .pros-cons {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
            margin: 1rem 0;
        }

        .pros { background: #f0fdf4; padding: 1rem; border-radius: 0.5rem; }
        .cons { background: #fef2f2; padding: 1rem; border-radius: 0.5rem; }
        .pros h4 { color: var(--success); }
        .cons h4 { color: var(--danger); }

        footer {
            text-align: center;
            padding: 2rem;
            color: var(--text-muted);
            font-size: 0.9rem;
        }

        a { color: var(--primary); }

        .sources {
            background: var(--bg);
            padding: 1rem;
            border-radius: 0.5rem;
            margin-top: 1rem;
        }

        .sources h4 { margin-bottom: 0.5rem; color: var(--secondary); }
        .sources ul { margin: 0; font-size: 0.9rem; }

        @media (max-width: 768px) {
            body { padding: 1rem; }
            header { padding: 2rem 1.5rem; }
            header h1 { font-size: 1.75rem; }
            .pros-cons { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <header>
        <h1>📊 [TITRE DU RAPPORT]</h1>
        <p class="meta">
            📅 Généré le [DATE] | 🔍 Recherche approfondie | ⏱️ [NOMBRE] sources analysées
        </p>
    </header>

    <nav class="toc">
        <h2>📑 Sommaire</h2>
        <ul>
            <!-- Liens vers les sections -->
        </ul>
    </nav>

    <!-- SECTIONS DU RAPPORT -->

    <footer>
        <p>Rapport généré par Claude Code | Recherche web automatisée</p>
    </footer>
</body>
</html>
```

### 5. Sections obligatoires du rapport

1. **🎯 Résumé exécutif** - L'essentiel en 3-5 points clés
2. **📖 Introduction et contexte** - Qu'est-ce que c'est, pourquoi ça existe
3. **⚙️ Fonctionnement** - Comment ça marche techniquement
4. **✅ Avantages et points forts** - Avec exemples concrets
5. **⚠️ Limites et inconvénients** - Honnêteté sur les faiblesses
6. **🔄 Alternatives et comparaison** - Tableau comparatif avec concurrents
7. **💡 Ce qui le rend unique** - La proposition de valeur distinctive
8. **📚 Cas d'usage** - Exemples réels d'utilisation
9. **🚀 Pour aller plus loin** - Ressources, documentation, communauté
10. **📋 Sources** - Liste des sources consultées avec liens

### 6. Qualité attendue

- **Objectivité** : Présenter les faits, pas de promotion
- **Exhaustivité** : Couvrir tous les angles importants
- **Clarté** : Accessible même pour un novice du sujet
- **Actualité** : Privilégier les informations récentes
- **Utilité** : Le lecteur doit pouvoir prendre une décision éclairée

### 7. Après génération

Informe l'utilisateur :
- Chemin complet du fichier généré
- Nombre de sources consultées
- Proposition d'ouvrir le rapport dans le navigateur

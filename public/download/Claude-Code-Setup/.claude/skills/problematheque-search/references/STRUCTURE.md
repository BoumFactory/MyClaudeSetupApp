# Structure du Skill Problémathèque CSEN

**Version :** 1.0
**Date :** 27 octobre 2025

---

## 📁 Arborescence

```
.claude/skills/problematheque-search/
│
├── skill.md                        # ⭐ Prompt système pour Claude Code
├── README.md                       # 📖 Documentation utilisateur complète
├── QUICKSTART.md                   # 🚀 Guide de démarrage rapide
├── TESTS.md                        # ✅ Résultats des tests et validation
├── STRUCTURE.md                    # 📋 Ce fichier - Structure du projet
│
└── scripts/                        # 🐍 Scripts Python du skill
    ├── requirements.txt            # 📦 Dépendances Python
    ├── scraper_config.json         # ⚙️  Configuration (API, sélecteurs CSS, cache)
    │
    ├── api_client.py               # 🔌 Client API REST WordPress
    ├── html_scraper.py             # 🕷️  Scraper HTML pour téléchargements
    ├── problematheque.py           # 🎯 Script principal (CLI)
    ├── utils.py                    # 🛠️  Utilitaires (encodage Windows)
    │
    ├── cache_problematheque.json   # 💾 Cache API (généré automatiquement)
    └── download_links_cache.json   # 💾 Cache téléchargements (généré automatiquement)
```

---

## 📄 Description des Fichiers

### Documentation

| Fichier | Rôle | Audience |
|---------|------|----------|
| **skill.md** | Prompt système pour Claude Code. Explique comment utiliser le skill, les workflows, la configuration du scraper. | Claude Code |
| **README.md** | Documentation complète : installation, utilisation, exemples, dépannage, maintenance du scraper. | Utilisateur final |
| **QUICKSTART.md** | Guide de démarrage rapide avec exemples les plus courants. | Utilisateur pressé |
| **TESTS.md** | Résultats des tests de validation, problèmes résolus, limitations connues. | Développeur / Maintenance |
| **STRUCTURE.md** | Ce fichier - Vue d'ensemble de la structure du projet. | Développeur / Documentation |

### Scripts Python

| Fichier | Rôle | Taille (lignes) | Statut |
|---------|------|-----------------|--------|
| **api_client.py** | Client pour l'API REST WordPress. Gère les requêtes vers `/wp-json/wp/v2/`, le cache, le rate limiting. | ~300 | ✅ Stable |
| **html_scraper.py** | Scraper HTML pour extraire les liens de téléchargement depuis les pages HTML des fiches. | ~250 | ✅ Stable |
| **problematheque.py** | Script principal (CLI) qui combine API + scraper. Point d'entrée pour l'utilisateur. | ~310 | ✅ Stable |
| **utils.py** | Fonctions utilitaires (encodage UTF-8 Windows, affichage emojis). | ~50 | ✅ Stable |

### Configuration

| Fichier | Rôle | Modifiable | Critique |
|---------|------|------------|----------|
| **requirements.txt** | Liste des dépendances Python à installer avec pip. | ❌ Non | ⭐ Oui |
| **scraper_config.json** | Configuration complète : endpoints API, sélecteurs CSS, rate limiting, cache. | ✅ Oui | ⭐⭐⭐ Très critique |

### Cache (Générés Automatiquement)

| Fichier | Contenu | Durée de vie | Supprimable |
|---------|---------|--------------|-------------|
| **cache_problematheque.json** | Métadonnées API (cycles, domaines, résultats de recherche) | 24 heures | ✅ Oui |
| **download_links_cache.json** | URLs de téléchargement extraites du HTML | Permanent | ✅ Oui |

---

## 🔗 Dépendances Externes

### API REST

| Service | URL | Documentation |
|---------|-----|---------------|
| API WordPress Problémathèque CSEN | `https://www.problematheque-csen.fr/wp-json/wp/v2/` | [WordPress REST API](https://developer.wordpress.org/rest-api/) |
| Endpoint fiches problème | `/fiche-probleme` | Custom post type |
| Endpoint cycles | `/cycle` | Taxonomie |
| Endpoint domaines | `/domaine` | Taxonomie |
| Endpoint mots-clés | `/mot-cle` | Taxonomie |

### Bibliothèques Python

| Bibliothèque | Version | Usage |
|--------------|---------|-------|
| **requests** | ≥ 2.31.0 | Requêtes HTTP (API + HTML) |
| **beautifulsoup4** | ≥ 4.12.0 | Parsing HTML |
| **lxml** | ≥ 5.0.0 | Parser XML/HTML performant |
| **python-dateutil** | ≥ 2.8.2 | Manipulation des dates |

---

## 🔧 Points de Configuration

### scraper_config.json

#### Sélecteurs CSS (Critiques)

```json
"html_selectors": {
  "download_links": {
    "pdf_enseignant": {
      "selector": "a.format__download-link[href*='.pdf'], ...",
      "attribute": "href"
    }
  }
}
```

**⚠️ À mettre à jour si la structure HTML du site change.**

#### Rate Limiting

```json
"rate_limiting": {
  "requests_per_second": 1
}
```

**Respect du serveur CSEN : 1 requête/seconde max.**

#### Cache

```json
"cache": {
  "enabled": true,
  "ttl_seconds": 86400
}
```

**Durée de validité du cache API : 24 heures.**

---

## 🎯 Workflows Principaux

### Workflow 1 : Recherche Simple

```
Utilisateur → problematheque.py → api_client.py → API REST WordPress
                                                  ↓
                                            Résultats JSON
                                                  ↓
                                        Formatage et affichage
```

### Workflow 2 : Recherche avec Liens

```
Utilisateur → problematheque.py → api_client.py → API REST (métadonnées)
                                         ↓
                                  html_scraper.py → Pages HTML (liens)
                                         ↓
                                  Cache téléchargements
                                         ↓
                                  Affichage avec liens
```

### Workflow 3 : Téléchargement

```
Utilisateur → problematheque.py → api_client.py → Récupération fiche (slug → URL)
                                         ↓
                                  html_scraper.py → Extraction URL téléchargement
                                         ↓
                                  Téléchargement fichier → Sauvegarde locale
```

---

## 📊 Statistiques du Code

| Métrique | Valeur |
|----------|--------|
| **Lignes de code Python** | ~900 |
| **Fichiers Python** | 4 |
| **Fichiers de documentation** | 5 |
| **Taille totale** | ~150 KB |
| **Dépendances externes** | 4 bibliothèques |
| **Endpoints API utilisés** | 5 |

---

## 🔒 Sécurité et Respect du Site

### Rate Limiting

- **1 requête par seconde max** (configurable)
- Respect automatique des délais entre requêtes

### User-Agent

```
ProblemathequeSkill/1.0 (Educational Purpose; Claude Code Integration)
```

Identifie clairement le skill pour les logs du serveur CSEN.

### Gestion des Erreurs

- Tous les `try/except` catchent les erreurs réseau
- Timeout configuré (10 secondes par défaut)
- Messages d'erreur explicites pour l'utilisateur

---

## 🚀 Évolution Future

### Améliorations Prioritaires

1. **Résolution des mots-clés** : Afficher les vrais noms au lieu de "Tag XXX"
2. **Investigation fiches sans liens** : Comprendre pourquoi certaines fiches n'ont pas de téléchargements
3. **Téléchargement batch** : Télécharger plusieurs fiches d'un coup

### Idées Avancées

- Serveur MCP dédié pour intégration plus profonde avec Claude Code
- Agent spécialisé `problematheque-searcher`
- Export des résultats en CSV/Excel
- Interface web locale (Flask)

---

## 📞 Maintenance

### Vérifications Régulières (Tous les 3 Mois)

1. **Tester le scraper :**
   ```bash
   python .claude/skills/problematheque-search/scripts/problematheque.py \
     --download "la-cigale-et-la-fourmi"
   ```

2. **Si échec, inspecter la structure HTML du site**

3. **Mettre à jour `scraper_config.json`** si nécessaire

4. **Vider le cache :**
   ```bash
   rm .claude/skills/problematheque-search/scripts/*.json
   ```

---

## 📝 Changelog

### Version 1.0 (27 octobre 2025)

- ✅ Client API REST fonctionnel
- ✅ Scraper HTML avec configuration modulaire
- ✅ Cache local (API + téléchargements)
- ✅ CLI complet avec tous les filtres
- ✅ Documentation complète
- ✅ Tests validés
- ✅ Gestion encodage Windows (UTF-8)
- ✅ Rate limiting automatique

---

**Auteur :** Claude Code (Sonnet 4.5)
**Date de création :** 27 octobre 2025
**Dernière mise à jour :** 27 octobre 2025
**Statut :** ✅ Stable et prêt à l'emploi

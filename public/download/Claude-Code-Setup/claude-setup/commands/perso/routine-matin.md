# /routine-matin - Journal d'actualités quotidien

## Description

Génère un rapport d'actualités structuré en JSON pour chaque domaine suivi (Code & IA, Géopolitique, Mathématiques). Les rapports sont consultables via l'application de gestion.

## Usage

```bash
/routine-matin                    # Tous les domaines
/routine-matin --domain code      # Uniquement Code & IA
/routine-matin --domain geo       # Uniquement Géopolitique
/routine-matin --domain maths     # Uniquement Mathématiques
```

## Protocole d'exécution

### Étape 1 : Déterminer les domaines

Lire les arguments :
- Si `--domain` spécifié → un seul domaine
- Sinon → tous les domaines (`code`, `geopolithique`, `mathematiques`)

### Étape 2 : Pour chaque domaine, effectuer les recherches

Utiliser `WebSearch` avec des requêtes adaptées :

**Code & IA :**
```
- "Claude Anthropic news January 2025"
- "AI coding tools updates"
- "LLM education applications"
- "EdTech AI innovations"
```

**Géopolitique :**
```
- "actualité internationale janvier 2025"
- "France politique économie"
- "world news analysis"
```

**Mathématiques :**
```
- "mathematics research discoveries"
- "mathématiques actualités recherche"
- "math olympiad news"
```

### Étape 3 : Analyser et structurer

Pour chaque résultat pertinent :
1. Extraire titre, source, URL
2. Générer un résumé concis (2-3 phrases)
3. Identifier les points clés
4. Attribuer des tags
5. Évaluer la pertinence (high/medium/low)

### Étape 4 : Produire la synthèse

Pour chaque domaine :
- Identifier les tendances principales
- Relever les faits notables
- Formuler des recommandations de suivi

### Étape 5 : Sauvegarder les rapports JSON

Structure de fichier : `rapport_YYYY-MM-DD.json`

Emplacements :
- `C:\Users\Utilisateur\Documents\Professionnel\1. Reims 2025 - 2026\7. Routine\code\`
- `C:\Users\Utilisateur\Documents\Professionnel\1. Reims 2025 - 2026\7. Routine\geopolithique\`
- `C:\Users\Utilisateur\Documents\Professionnel\1. Reims 2025 - 2026\7. Routine\mathematiques\`

### Étape 6 : Afficher le résumé

```markdown
## 📰 Journal du [DATE]

### Code & IA
- [N] articles trouvés
- Tendance : [résumé]

### Géopolitique
- [N] articles trouvés
- Tendance : [résumé]

### Mathématiques
- [N] articles trouvés
- Tendance : [résumé]

📁 Rapports sauvegardés dans `7. Routine/[domaine]/`
🌐 Consultez l'application : http://localhost:5000
```

## Schéma JSON

```json
{
  "metadata": {
    "date": "YYYY-MM-DD",
    "domain": "code|geopolithique|mathematiques",
    "generated_at": "ISO8601",
    "sources_count": N
  },
  "articles": [
    {
      "id": "domain_YYYYMMDD_NNN",
      "title": "...",
      "summary": "...",
      "source": "...",
      "url": "...",
      "relevance": "high|medium|low",
      "tags": [],
      "key_points": []
    }
  ],
  "synthesis": {
    "main_trends": [],
    "notable_facts": [],
    "recommendations": []
  }
}
```

## Dépendances

- Skill : `routine-matin`
- Application : `7. Routine/app/` (Flask)

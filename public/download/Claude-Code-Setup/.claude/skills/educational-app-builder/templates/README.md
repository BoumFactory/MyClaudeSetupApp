# Templates d'Applications Éducatives

Ce dossier contient les templates d'applications que l'agent `app-creator-agent` peut utiliser pour générer rapidement des applications complètes.

## Structure

Chaque template est dans son propre dossier et contient :
- Tous les fichiers source (Python, HTML, CSS, JS)
- Un fichier `template.json` décrivant le template
- Des placeholders à remplacer lors de la génération

## Templates Disponibles

### 1. revision-app

**Type** : Application de révision interactive
**Description** : Application Flask complète pour réviser par questions-réponses avec :
- Système de thèmes avancé (8 thèmes dont dyslexique)
- Statistiques détaillées
- Algorithme de répétition espacée
- Sauvegarde locale de la progression
- Rendu mathématique (MathJax)

**Utilisation** :
Pour des ressources de type cours, exercices, séquences complètes.

## Comment Utiliser un Template

L'agent `app-creator-agent` :
1. Lit le fichier `template.json` du template choisi
2. Copie tous les fichiers du template vers la destination
3. Remplace les placeholders par les valeurs réelles
4. Génère le fichier `data/questions.json` basé sur le contenu analysé
5. Teste l'application
6. Construit l'exécutable si demandé

## Placeholders Standards

Les templates utilisent des placeholders qui seront remplacés :
- `{{APP_NAME}}` : Nom de l'application
- `{{APP_VERSION}}` : Version
- `{{APP_AUTHOR}}` : Auteur
- `{{THEME}}` : Thème du cours
- `{{LEVEL}}` : Niveau (6ème, 5ème, 1ère, Terminale, etc.)
- `{{CREATED_DATE}}` : Date de création
- `{{TOTAL_QUESTIONS}}` : Nombre total de questions

## Ajouter un Nouveau Template

1. Créer un dossier `nom-template/` dans `templates/`
2. Créer la structure de l'application
3. Créer un fichier `template.json` :

```json
{
    "name": "Nom du Template",
    "type": "revision|exerciseur|visualiseur|mixte",
    "description": "Description du template",
    "placeholders": {
        "APP_NAME": "Nom par défaut",
        "APP_VERSION": "1.0.0",
        ...
    },
    "files": {
        "required": ["app.py", "config.py", "templates/base.html", ...],
        "optional": ["build/build_exe.py", ...]
    },
    "features": [
        "Thèmes multiples",
        "Statistiques",
        "Export PDF",
        ...
    ]
}
```

4. Utiliser les placeholders dans les fichiers du template
5. Tester le template manuellement
6. Documenter dans ce README

## Maintenance

- Mettre à jour les templates régulièrement
- Corriger les bugs dans les templates sources
- Ajouter de nouvelles fonctionnalités
- Versionner les templates si besoin

---

**Dernière mise à jour** : 2025-10-20
**Nombre de templates** : 1
**Mainteneur** : Educational App Builder Skill

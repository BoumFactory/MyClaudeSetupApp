# Capsules vidéo animées : mode d'emploi du dossier

Ce dossier (`{{BASE}}`) sert à fabriquer des capsules vidéo (MP4) de correction d'exercices, d'explication de cours ou de vulgarisation, avec le skill **capsule-video**. Il a été préparé par l'installeur. Ce fichier existe en deux exemplaires identiques : `CLAUDE.md` (Claude Code) et `AGENTS.md` (Codex, Antigravity et autres agents).

## Où sont les choses

| Quoi | Où |
|---|---|
| Le skill : à lire en premier | `.claude/skills/capsule-video/SKILL.md` |
| Chemins des outils et réglages | `.claude/skills/capsule-video/config.json` (écrit par l'installeur) |
| Préférences de l'utilisateur | `.claude/skills/capsule-video/references/preferences.md` |
| Outils lourds (Python, modèles, navigateur, MFA) | `outils/` : ne rien y modifier à la main |
| Les capsules | `capsules/<nom-court-sans-accents>/`, une par dossier |

Un agent qui ne charge pas les skills tout seul ouvre lui-même `SKILL.md` et suit ses renvois vers `references/`.

## Première utilisation

Si `premier_usage_fait` vaut `false` dans `config.json`, lire et suivre `.claude/skills/capsule-video/references/first_check.md` **avant** la première capsule.

## Lancer les scripts

Depuis ce dossier :

```bash
PY={{PYTHON}}      # clé python_rendu de config.json
S=.claude/skills/capsule-video/scripts
PYTHONIOENCODING=utf-8 $PY $S/rendre_canvas.py "capsules/<nom>" --images 5,12
```

Chaque script trouve seul le Python de son moteur (Pocket, Parakeet, Whisper, MFA) grâce à `config.json`.

## Règles clés

- **Tout reste local et gratuit.** Aucun outil ne s'installe hors de `outils/`. Un outil manque ou ne répond pas : relancer `.claude/skills/capsule-video/installation/installer.ps1` (il saute ce qui est fait et refait l'essai).
- **Une capsule = un dossier** dans `capsules/`, nom court sans accents ni espaces. Essais, planches et extraits restent dans ce dossier (jamais dans un dossier temporaire) ; les rendus d'essai s'appellent `essai-*.mp4`, jamais `capsule*.mp4`.
- **Après validation de la vidéo**, supprimer `planches/`, les extraits, les essais et les `*.bak.js` de la capsule.
- **Un seul rendu à la fois.**
- **Chromium** est lancé et fermé par Playwright. Ne jamais tuer de processus Chrome ou Chromium par leur nom : cela fermerait aussi le navigateur de l'utilisateur.
- **Voix de synthèse** : toujours l'annoncer à l'écran (`mention: 'Voix de synthèse'`). Une voix clonée est personnelle : `voix_clonees` de `config.json` et l'échantillon ne se partagent jamais.
- **Français soigné** (accents compris) dans tout ce qui est affiché ou dit ; chemins et noms de fichiers sans accents.
- **Rigueur** : une capsule est une copie modèle que les élèves recopient (`references/rigueur.md`).

## Préférences

Lues au cadrage de chaque capsule : ce qui y figure n'est pas redemandé, seulement annoncé. L'utilisateur peut les changer à tout moment (« je préfère… ») : mettre alors `references/preferences.md` à jour (une ligne datée).

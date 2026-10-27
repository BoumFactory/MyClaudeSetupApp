# Installer « Capsules vidéo animées »

Gratuit, tout tourne sur votre ordinateur. Il faut un PC Windows 64 bits (Linux et macOS : voir plus bas), ≈ 6 Go libres (≈ 8 à 11 Go pour animer vos propres enregistrements) et un agent capable d'utiliser un skill (Claude Code, Codex…). Une carte graphique NVIDIA n'est **pas** nécessaire.

## Installer

1. Clic droit sur `installer.ps1` (dossier `capsule-video\installation\` du kit) > **Exécuter avec PowerShell**.
2. Donnez le **dossier de base**, par exemple `D:\Capsules` (sans espace ni accent). Tout s'y installe ; rien ailleurs.
3. Le script inspecte le PC, puis pose **deux questions**. D'abord, l'agent que vous utilisez (1 = Claude Code, 2 = Codex) : le skill est copié et configuré en **une seule copie**, dans `.claude\skills\capsule-video\` pour Claude Code (avec `CLAUDE.md`) ou dans `.agents\skills\capsule-video\` pour Codex (avec `AGENTS.md`, qui pointe sur cette copie). Ensuite, voulez-vous travailler avec vos propres enregistrements ? Répondez « non » si vous ne comptez utiliser que la voix de synthèse.
4. Comptez 20 à 40 minutes (surtout du téléchargement). À la fin, chaque brique est essayée sur une phrase : le bilan dit OK, ou le problème et sa solution.

Il manque Python ou ffmpeg ? Le script le dit et propose de l'installer.

## Linux et macOS

**Statut : Linux et macOS ne sont pas testés** (le script transpose `installer.ps1` étape par étape). Retours bienvenus.

Dans un terminal, depuis le dossier du kit :

```
bash installer.sh
```

(ou `chmod +x installer.sh` puis `./installer.sh`). Mêmes étapes, même question, même bilan que sous Windows ; compatible avec le bash 3.2 de macOS. Tout s'installe dans le dossier de base (par exemple `~/Capsules`, sans espace ni accent) : aucun fichier de démarrage du shell (`.bashrc`, `.zshrc`) n'est modifié.

- **Prérequis** : Python 3.10 à 3.13 avec le module `venv`, ffmpeg (sous Linux x86-64 ou ARM, le script peut le télécharger en version portable), ≈ 6 Go libres. S'il manque quelque chose, le script affiche la commande à lancer (`apt`, `dnf`, `pacman`, `zypper` ou Homebrew) et ne l'exécute avec `sudo` que si vous répondez « o ».
- **Linux** : si Chromium signale des bibliothèques manquantes, lancer la commande `playwright install-deps chromium` que le script indique. Rendu graphique : Vulkan, puis logiciel.
- **macOS** : pas de carte NVIDIA, donc Whisper tourne sur le processeur (nettement plus lent). Rendu graphique : Metal, puis logiciel. Sur un Mac Intel, les versions récentes de PyTorch n'existent plus : la voix Pocket TTS peut échouer (voix de secours Piper).
- Options : `bash installer.sh --base ~/Capsules --enregistrements non --agent claude --silencieux` (sans question ; `--agent codex` pour Codex) ; `--reutiliser <config.json>` ; `--version-python 3.12` ; `--aide`.

## Ensuite

Ouvrez votre agent dans le dossier de base (PowerShell : `cd D:\Capsules` puis `claude` ou `codex`) et demandez : « Fais-moi une capsule vidéo de correction de l'exercice suivant : … ». La première fois, l'agent vous propose quelques questions sur vos goûts ; tout se change ensuite d'une phrase (« je préfère les formules plus petites »).

## Ce qui est installé

| Brique | Rôle | Poids |
|---|---|---|
| Rendu (Python + Chromium) | dessine l'animation et fabrique la vidéo | ≈ 0,8 Go |
| Pocket TTS | voix de synthèse française, sur processeur | ≈ 1,8 Go |
| Parakeet | réécoute la voix pour vérifier qu'aucun mot n'est sauté | ≈ 0,8 Go |
| MFA | cale chaque mot sur la voix, pour synchroniser les animations | ≈ 2,5 Go |
| Piper | voix de secours | ≈ 0,2 Go |
| Whisper (si « oui ») | transcrit vos enregistrements | ≈ 1,9 Go sans carte NVIDIA, ≈ 4,6 Go avec |

## Bon à savoir

- **Relancer** le script ne refait pas ce qui est fait : il complète (par exemple, répondre « oui » plus tard ajoute Whisper), met le skill à jour et refait l'essai. Vos réglages, préférences et voix clonées sont gardés.
- **Désinstaller** : supprimer le dossier de base (vos capsules sont dans `capsules\` : les sauvegarder avant).
- **Votre propre voix** (facultatif) : demande un compte Hugging Face gratuit. Marche à suivre : `references/cloner-sa-voix.md`. Une voix clonée est personnelle : ne la partagez jamais avec le skill.
- **Réseau d'établissement** qui bloque les téléchargements (erreur SSL) : le script réessaie seul sans vérification ; sinon, lancez l'installation depuis un autre réseau.
- **Journal** : `outils\installation.log` ; bilan de l'essai : `outils\bilan-installation.json`.

## Options (sans question)

```
powershell -ExecutionPolicy Bypass -File installer.ps1 -DossierBase D:\Capsules -Enregistrements non -Agent claude -Silencieux
```

`-Agent codex` installe et configure le skill dans `.agents\skills\capsule-video\` (emplacement des skills de Codex) au lieu de `.claude\skills\`. Sans `-Agent` ni question, le choix est Claude Code, sauf si seule la copie `.agents` existe déjà. Si une copie de l'autre agent existe, le script le signale : elle n'est pas configurée, la supprimer évite la confusion.

`-Caches <dossier>` réutilise les téléchargements d'une installation existante (copiés, jamais liés) ; `-VersionPython 3.13` impose une version de Python.

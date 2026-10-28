#!/usr/bin/env bash
# Installation de la configuration bfcours.dev (Claude Code / Codex) - macOS / Linux
#
#   curl -fsSL https://bfcours.dev/installer/claude.sh | bash     -> ./.claude  + CLAUDE.md
#   curl -fsSL https://bfcours.dev/installer/codex.sh  | bash     -> ./.agents  + AGENTS.md
#
# Version allégée (sans les skills les plus lourds) :
#   curl -fsSL https://bfcours.dev/installer/claude.sh | BFCOURS_LEGER=1 bash
#
# Fichiers jumeaux : claude.sh et codex.sh sont identiques, sauf la ligne AGENT=...
# Tout le script est dans une fonction appelée à la fin : un téléchargement
# interrompu n'exécute rien.
#
# Rien de destructif : un dossier existant est sauvegardé (copie) avant la fusion, jamais supprimé.

AGENT=codex

principal() {
  set -eu

  DEPOT="https://github.com/BoumFactory/MyClaudeSetupApp.git"
  BRANCHE="main"
  SOURCE="public/download/Claude-Code-Setup"
  LOURDS="h5p-branching-scenario programmes-officiels"
  TUTO_GIT="https://bfcours.dev/claude-code/tutorials/git-install"

  if [ "$AGENT" = "codex" ]; then
    OUTIL="Codex"; NOM_CIBLE=".agents"; FICHIER_RACINE="AGENTS.md"
  else
    OUTIL="Claude Code"; NOM_CIBLE=".claude"; FICHIER_RACINE="CLAUDE.md"
  fi
  LEGER="${BFCOURS_LEGER:-0}"

  if [ -t 1 ]; then VERT=$(printf '\033[32m'); ROUGE=$(printf '\033[31m'); JAUNE=$(printf '\033[33m'); GRIS=$(printf '\033[90m'); NORMAL=$(printf '\033[0m')
  else VERT=""; ROUGE=""; JAUNE=""; GRIS=""; NORMAL=""; fi

  ok() { printf '  %s[ok]%s %s\n' "$VERT" "$NORMAL" "$1"; }
  attention() { printf '  %s[!]%s %s\n' "$JAUNE" "$NORMAL" "$1"; }

  PROJET="$(pwd)"
  CIBLE="$PROJET/$NOM_CIBLE"
  DEBUT=$(date +%s)
  SAUVEGARDE=""
  COPIE_COMMENCEE=0
  TMP=""

  nettoyer() { if [ -n "$TMP" ] && [ -d "$TMP" ]; then rm -rf "$TMP"; fi; }

  echec() {
    printf '\n%sERREUR : %s%s\n' "$ROUGE" "$1" "$NORMAL" >&2
    if [ "$COPIE_COMMENCEE" = 0 ]; then
      printf '%sRien n'"'"'a été modifié dans votre projet.%s\n' "$ROUGE" "$NORMAL" >&2
    elif [ -n "$SAUVEGARDE" ]; then
      printf '%sCopie incomplète. Votre ancien dossier est intact dans %s.%s\n' "$ROUGE" "$(basename "$SAUVEGARDE")" "$NORMAL" >&2
    else
      printf '%sCopie incomplète : relancez la commande.%s\n' "$ROUGE" "$NORMAL" >&2
    fi
    nettoyer
    exit 1
  }

  git_run() { git "$@" 2>&1 | sed "s/^/    $GRIS/;s/\$/$NORMAL/" ; return "${PIPESTATUS[0]}"; }

  trap nettoyer EXIT
  trap 'echec "installation interrompue."' INT TERM

  echo ""
  echo "Installation de la configuration bfcours.dev pour $OUTIL"
  echo "Projet : $PROJET"
  echo "Destination : $CIBLE"
  if [ "$LEGER" = 1 ]; then echo "Version allégée : sans les skills $LOURDS."; fi
  echo ""

  # 1. Garde-fous
  command -v git >/dev/null 2>&1 || echec "Git n'est pas installé. Installez-le d'abord : $TUTO_GIT"
  if [ "$PROJET" = "$HOME" ]; then
    attention "Vous êtes dans votre dossier personnel : la configuration servira à tous vos projets."
  fi

  # 2. Téléchargement : clone partiel, seuls les fichiers de la configuration sont récupérés
  echo "1/4 Téléchargement de la configuration (Git)..."
  TMP="$(mktemp -d "${TMPDIR:-/tmp}/bfcours-config-XXXXXXXX")" || echec "impossible de créer un dossier temporaire."
  git_run clone --quiet --depth 1 --filter=blob:none --no-checkout --branch "$BRANCHE" "$DEPOT" "$TMP/depot" \
    || echec "le téléchargement a échoué (connexion internet ? proxy ?)."

  # Motifs sans « / » initial : Git Bash (Windows) le réécrirait en chemin Windows.
  # Un « / » interne suffit à ancrer le motif à la racine du dépôt (règles gitignore).
  set -- "$SOURCE/"
  if [ "$LEGER" = 1 ]; then for l in $LOURDS; do set -- "$@" "!$SOURCE/claude-setup/skills/$l/"; done; fi
  git_run -C "$TMP/depot" sparse-checkout set --no-cone "$@" \
    || echec "votre version de Git est trop ancienne (2.35 au minimum). Mettez-la à jour : $TUTO_GIT"
  git_run -C "$TMP/depot" checkout --quiet "$BRANCHE" || echec "l'extraction des fichiers a échoué."

  SRC="$TMP/depot/$SOURCE"
  [ -d "$SRC/claude-setup/skills" ] || echec "la configuration téléchargée est incomplète."
  VOLUME=$(du -sk "$TMP/depot/.git" | awk '{ printf "%.1f", $1 / 1024 }')
  ok "configuration récupérée ($VOLUME Mo téléchargés)"

  # 3. Sauvegarde du dossier existant (copie : l'original reste en place)
  echo "2/4 Sauvegarde..."
  if [ -e "$CIBLE" ]; then
    NOM="$NOM_CIBLE.sauvegarde-$(date +%Y%m%d-%H%M)"
    SAUVEGARDE="$PROJET/$NOM"
    i=2
    while [ -e "$SAUVEGARDE" ]; do SAUVEGARDE="$PROJET/$NOM-$i"; i=$((i + 1)); done
    cp -R "$CIBLE" "$SAUVEGARDE" || echec "la sauvegarde de $NOM_CIBLE a échoué."
    ok "dossier $NOM_CIBLE existant sauvegardé dans $(basename "$SAUVEGARDE")"
  else
    ok "aucun dossier $NOM_CIBLE existant : rien à sauvegarder"
  fi

  # 4. Copie par fusion : les fichiers de la configuration remplacent ceux de même nom,
  #    les autres fichiers du dossier sont conservés.
  echo "3/4 Copie des fichiers dans $NOM_CIBLE..."
  COPIE_COMMENCEE=1
  mkdir -p "$CIBLE"
  cp -R "$SRC/claude-setup/." "$CIBLE/" || echec "la copie a échoué."
  NB_SKILLS=$(find "$CIBLE/skills" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')
  ok "$NB_SKILLS skills dans $NOM_CIBLE/skills"

  # 5. Fichier d'instructions à la racine du projet (seulement s'il n'existe pas)
  echo "4/4 Fichier $FICHIER_RACINE..."
  RACINE="$PROJET/$FICHIER_RACINE"
  if [ -e "$RACINE" ]; then
    ok "$FICHIER_RACINE existe déjà : il n'est pas modifié"
  else
    if [ "$AGENT" = "codex" ]; then
      {
        printf '%s\n\n' '> Configuration installée dans `.agents/`. Les chemins `.claude/...` cités dans les skills et ci-dessous désignent `.agents/...`.'
        cat "$SRC/CLAUDE-simple.md"
      } > "$RACINE"
    else
      cp "$SRC/CLAUDE-simple.md" "$RACINE"
    fi
    ok "$FICHIER_RACINE créé à partir de CLAUDE-simple.md"
  fi
  if [ "$AGENT" != "codex" ]; then
    # Exemple seulement : ses permissions sont larges et ses sons passent par PowerShell (Windows).
    cp "$SRC/settings.json" "$CIBLE/settings.exemple.json"
  fi

  DUREE=$(( $(date +%s) - DEBUT ))
  echo ""
  printf '%sInstallation terminée en %s s.%s\n' "$VERT" "$DUREE" "$NORMAL"
  echo ""
  echo "Étapes suivantes (facultatives, selon les skills utilisés) :"
  echo "  - Python 3 et Node.js servent à plusieurs skills."
  echo "  - Serveurs MCP : python3 -m pip install -r $NOM_CIBLE/mcp_servers/requirements.txt"
  echo "  - Skill latex-visual-review : python3 -m pip install -r $NOM_CIBLE/skills/latex-visual-review/scripts/requirements.txt"
  if [ "$AGENT" != "codex" ]; then
    echo "  - $NOM_CIBLE/settings.exemple.json : exemple de réglages (sons sous Windows, permissions larges). Non activé ; à relire avant de le renommer en settings.json."
  else
    echo "  - Codex lit les skills dans .agents/skills. Les chemins .claude/... cités dans les skills désignent .agents/..."
  fi
  echo "  - Pour mettre à jour : relancez la même commande."
  if [ -n "$SAUVEGARDE" ]; then echo "  - Sauvegarde : $(basename "$SAUVEGARDE") (supprimez-la quand tout fonctionne)."; fi
  echo ""
}

principal "$@"

#!/usr/bin/env bash
# Installeur « Capsules vidéo animées » (skill capsule-video) pour Linux et macOS : gratuit, 100 % local, relançable.
# Équivalent de installer.ps1 (Windows). Compatible bash 3.2 (macOS).
#
# Ce que fait le script :
#   1. demande le DOSSIER DE BASE (ex. ~/Capsules) et y prépare :
#        .claude/skills/capsule-video/   le skill, UNE seule copie, configurée (agent Claude Code)
#        .agents/skills/capsule-video/   idem à la place de la précédente si l'agent est Codex (--agent codex)
#        CLAUDE.md ou AGENTS.md          le mode d'emploi du dossier ; il pointe sur cette copie (Codex : AGENTS.md seul)
#        outils/                         tout le lourd : Python, modèles, navigateur, MFA… (rien ailleurs)
#        capsules/                       vos capsules, une par dossier
#   2. inspecte l'ordinateur (système, carte NVIDIA, mémoire, place libre, Python, ffmpeg, Git) ;
#   3. pose UNE question : travaillerez-vous avec vos propres enregistrements ?
#   4. installe la base (≈ 6 Go, processeur seul) : rendu, voix Pocket TTS, contrôle Parakeet, horodatage MFA,
#      voix de secours Piper ; et, si oui à la question, Whisper ;
#   5. écrit config.json et essaie chaque brique sur une phrase (bilan OK / problème + solution).
#
# Rien n'est modifié hors du dossier de base : ni le PATH, ni ~/.bashrc, ~/.zshrc ou autre fichier de démarrage.
# Jamais Anaconda. Journal : <base>/outils/installation.log. Relancer le script saute ce qui est déjà fait.
# Statut : Linux et macOS NON TESTÉS (écrit par transposition de installer.ps1) : retours bienvenus.
#
# Lancement :   bash installer.sh      (ou : chmod +x installer.sh puis ./installer.sh)
# Sans question (tests, déploiement) :
#   bash installer.sh --base ~/Capsules --enregistrements non --silencieux
# Options :
#   --base <dossier>            dossier de base (chemin sans espace ni accent)
#   --enregistrements oui|non   ajouter (oui) ou non la transcription Whisper de vos propres enregistrements
#   --agent claude|codex        agent utilisé (question posée si absent ; sans question : claude, ou codex si seule
#                               la copie .agents existe déjà) : détermine où le skill est copié et configuré
#   --silencieux                aucune question : valeurs proposées
#   --reutiliser <config.json>  reprendre les outils d'une installation existante par leurs chemins (python_pocket,
#                               python_parakeet, python_asr, mfa, cache_modeles, voix_piper), sans rien copier
#                               ni retélécharger ; seul l'environnement de rendu est créé
#   --version-python 3.12       imposer une version de Python (3.10 à 3.13, 64 bits)
#   --aide                      affiche cette aide

DEBUT=$SECONDS
BASE=""
ENREGISTREMENTS=""
SILENCIEUX=0
REUTILISER=""
VERSION_PYTHON=""
AGENT=""

while [ $# -gt 0 ]; do
  case "$1" in
    --base) BASE="${2:-}"; shift 2 ;;
    --enregistrements) ENREGISTREMENTS="${2:-}"; shift 2 ;;
    --agent) AGENT="${2:-}"; shift 2 ;;
    --silencieux) SILENCIEUX=1; shift ;;
    --reutiliser) REUTILISER="${2:-}"; shift 2 ;;
    --version-python) VERSION_PYTHON="${2:-}"; shift 2 ;;
    --aide|-h|--help) sed -n '2,/^$/p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "Option inconnue : $1 (voir --aide)"; exit 1 ;;
  esac
done
case "$ENREGISTREMENTS" in ""|oui|non) ;; *) echo "--enregistrements : oui ou non"; exit 1 ;; esac
case "$AGENT" in ""|claude|codex) ;; *) echo "--agent : claude ou codex"; exit 1 ;; esac

# ------------------------------------------------------------------ affichage et journal
if [ -t 1 ]; then
  C_CYAN=$(printf '\033[36m'); C_VERT=$(printf '\033[32m'); C_JAUNE=$(printf '\033[33m')
  C_ROUGE=$(printf '\033[31m'); C_GRIS=$(printf '\033[90m'); C_RAZ=$(printf '\033[0m')
else
  C_CYAN=""; C_VERT=""; C_JAUNE=""; C_ROUGE=""; C_GRIS=""; C_RAZ=""
fi
LOG=""
journal() { [ -n "$LOG" ] && printf '[%s] %s\n' "$(date +%H:%M:%S)" "$1" >> "$LOG"; return 0; }
NUM_ETAPE=0
titre() {
  NUM_ETAPE=$((NUM_ETAPE + 1))
  printf '\n%s=== %s. %s ===%s\n' "$C_CYAN" "$NUM_ETAPE" "$1" "$C_RAZ"
  [ -n "${2:-}" ] && printf '%s    %s%s\n' "$C_GRIS" "$2" "$C_RAZ"
  journal "=== $NUM_ETAPE. $1"
}
ok() { printf '%s    OK  %s%s\n' "$C_VERT" "$1" "$C_RAZ"; journal "OK $1"; }
info() { printf '    ... %s\n' "$1"; journal "$1"; }
alerte() { printf '%s    !!  %s%s\n' "$C_JAUNE" "$1" "$C_RAZ"; journal "ALERTE $1"; }
duree_depuis() {  # secondes de départ -> « 2 min 05 s » ou « 40 s »
  local s=$((SECONDS - $1))
  if [ "$s" -ge 60 ]; then printf '%d min %02d s' $((s / 60)) $((s % 60)); else printf '%d s' "$s"; fi
}
demander() {  # question, défaut -> réponse (la question va sur la sortie d'erreur)
  local r=""
  if [ "$SILENCIEUX" = 1 ]; then printf '%s' "$2"; return; fi
  printf '%s [%s] ' "$1" "$2" >&2
  read -r r || r=""
  [ -z "$r" ] && r="$2"
  printf '%s' "$r"
}
oui() { case "$(demander "$1" "$2")" in o*|O*|y*|Y*) return 0 ;; *) return 1 ;; esac; }

PROBLEMES=""
NB_PROBLEMES=0
probleme() {  # brique, solution
  PROBLEMES="${PROBLEMES}   - $1 : $2
"
  NB_PROBLEMES=$((NB_PROBLEMES + 1))
  printf '%s    ÉCHEC  %s%s\n' "$C_ROUGE" "$1" "$C_RAZ"
  printf '%s           -> %s%s\n' "$C_ROUGE" "$2" "$C_RAZ"
  journal "ECHEC $1 -> $2"
}
CHRONO=""
chrono() { CHRONO="${CHRONO}$1|$(duree_depuis "$T_ETAPE")
"; }

# Lance un programme ; sa sortie va dans le journal ; renvoie son code de sortie.
executer() {
  journal "> $*"
  if [ -n "$LOG" ]; then "$@" >> "$LOG" 2>&1; else "$@" > /dev/null 2>&1; fi
}

# pip avec repli SSL (réseau d'établissement qui intercepte les certificats)
pip_installer() {  # python, paquets...
  local py="$1"; shift
  executer "$py" -m pip install --disable-pip-version-check --no-input "$@" && return 0
  info "nouvel essai de pip sans vérification SSL (réseau filtrant)"
  executer "$py" -m pip install --disable-pip-version-check --no-input "$@" \
    --trusted-host pypi.org --trusted-host files.pythonhosted.org --trusted-host download.pytorch.org
}

telecharger() {  # url, destination
  local url="$1" dest="$2"
  if command -v curl > /dev/null 2>&1; then
    curl -fL --retry 3 -s -o "$dest.part" "$url" && mv -f "$dest.part" "$dest" && return 0
  fi
  if command -v wget > /dev/null 2>&1; then
    wget -q -O "$dest.part" "$url" && mv -f "$dest.part" "$dest" && return 0
  fi
  rm -f "$dest.part"
  journal "téléchargement échoué : $url"
  return 1
}

# Étapes faites (idempotence) : un fichier témoin par étape
fait() { [ -f "$ETAPES/$1.ok" ]; }
marquer() { date +%Y-%m-%dT%H:%M:%S > "$ETAPES/$1.ok"; }

commande() { command -v "$1" > /dev/null 2>&1; }
vers_go() { awk -v k="$1" 'BEGIN { printf "%.1f", k / 1048576 }'; }

# ------------------------------------------------------------------ 0. Source du skill
ICI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL="$(cd "$ICI/.." && pwd)"
if [ ! -f "$SKILL/SKILL.md" ]; then SKILL="$ICI/capsule-video"; fi
if [ ! -f "$SKILL/SKILL.md" ]; then
  echo "${C_ROUGE}Le dossier du skill « capsule-video » est introuvable.${C_RAZ}"
  echo "Placez installer.sh dans le dossier capsule-video/installation/ du kit, ou à côté du dossier capsule-video, puis relancez."
  exit 1
fi
SKILL="$(cd "$SKILL" && pwd)"

printf '%sCapsules vidéo animées : installation (Linux / macOS)%s\n' "$C_JAUNE" "$C_RAZ"
printf '%sTout est gratuit et tourne sur votre ordinateur. Entrée = valeur proposée.%s\n' "$C_GRIS" "$C_RAZ"

SYSTEME="$(uname -s)"
ARCH="$(uname -m)"
case "$SYSTEME" in
  Linux|Darwin) ;;
  *) echo "Système non pris en charge par ce script ($SYSTEME). Sous Windows : installer.ps1."; exit 1 ;;
esac
case "$ARCH" in
  x86_64|amd64|arm64|aarch64) ;;
  *) echo "Architecture non prise en charge ($ARCH) : 64 bits x86 ou ARM requis."; exit 1 ;;
esac

# ------------------------------------------------------------------ 1. Dossier de base
DEFAUT="$HOME/Capsules"
VALIDE_RE='^/[A-Za-z0-9_./-]+$'
if ! printf '%s' "$DEFAUT" | grep -Eq "$VALIDE_RE"; then DEFAUT="/opt/Capsules"; fi
while true; do
  if [ -z "$BASE" ]; then BASE="$(demander "Dossier de base (outils lourds + capsules, ≈ 6 à 11 Go)" "$DEFAUT")"; fi
  case "$BASE" in "~"|"~/"*) BASE="$HOME${BASE#\~}" ;; esac
  case "$BASE" in /*) ;; *) BASE="$PWD/$BASE" ;; esac
  BASE="${BASE%/}"
  if printf '%s' "$BASE" | grep -Eq "$VALIDE_RE"; then break; fi
  echo "${C_ROUGE}  Chemin refusé : lettres, chiffres, - _ . / seulement (ni espace ni accent : plusieurs outils les supportent mal). Exemple : $HOME/Capsules${C_RAZ}"
  [ "$SILENCIEUX" = 1 ] && exit 1
  BASE=""
done
# Agent utilisé : UNE seule copie du skill est installée et configurée, là où cet agent la cherche
# (Claude Code : .claude/skills ; Codex : .agents/skills)
if [ -z "$AGENT" ]; then
  DEF_AGENT="1"
  if [ -d "$BASE/.agents/skills/capsule-video" ] && [ ! -d "$BASE/.claude/skills/capsule-video" ]; then DEF_AGENT="2"; fi
  case "$(demander "Agent utilisé : 1 = Claude Code, 2 = Codex" "$DEF_AGENT")" in 2*|codex*|Codex*) AGENT="codex" ;; *) AGENT="claude" ;; esac
fi
if [ "$AGENT" = "codex" ]; then SKILLS_REL=".agents/skills"; AUTRE_REL=".claude/skills"; else SKILLS_REL=".claude/skills"; AUTRE_REL=".agents/skills"; fi
OUTILS="$BASE/outils"
ETAPES="$OUTILS/.etapes"
mkdir -p "$OUTILS" "$ETAPES" "$BASE/capsules" "$OUTILS/tmp" || { echo "Impossible de créer $BASE"; exit 1; }
LOG="$OUTILS/installation.log"
journal "===== Installation lancée le $(date '+%Y-%m-%d %H:%M') ; base = $BASE ; skill source = $SKILL ; agent = $AGENT ; $SYSTEME $ARCH"

# ------------------------------------------------------------------ 2. Inspection de l'ordinateur
titre "Votre ordinateur" "Inspection automatique : rien n'est modifié."
EN_WSL=0
DISTRIB=""
BREW=0
GESTIONNAIRE=""
if [ "$SYSTEME" = "Linux" ]; then
  grep -qi microsoft /proc/version 2> /dev/null && EN_WSL=1
  DISTRIB="$( ( . /etc/os-release 2> /dev/null && printf '%s' "${PRETTY_NAME:-Linux}" ) )"
  [ -z "$DISTRIB" ] && DISTRIB="Linux"
  CPU="$(awk -F': ' '/model name/ {print $2; exit}' /proc/cpuinfo 2> /dev/null)"
  FILS="$(nproc 2> /dev/null || echo '?')"
  RAM_GO="$(awk '/MemTotal/ {printf "%d", $2 / 1048576 + 0.5}' /proc/meminfo 2> /dev/null)"
  if commande apt-get; then GESTIONNAIRE="apt"
  elif commande dnf; then GESTIONNAIRE="dnf"
  elif commande pacman; then GESTIONNAIRE="pacman"
  elif commande zypper; then GESTIONNAIRE="zypper"
  fi
else
  DISTRIB="macOS $(sw_vers -productVersion 2> /dev/null)"
  CPU="$(sysctl -n machdep.cpu.brand_string 2> /dev/null)"
  FILS="$(sysctl -n hw.ncpu 2> /dev/null || echo '?')"
  RAM_GO="$(sysctl -n hw.memsize 2> /dev/null | awk '{printf "%d", $1 / 1073741824 + 0.5}')"
  # Homebrew : emplacements habituels (le PATH du terminal peut ne pas les contenir)
  for d in /opt/homebrew/bin /usr/local/bin; do
    case ":$PATH:" in *":$d:"*) ;; *) [ -d "$d" ] && PATH="$PATH:$d" ;; esac
  done
  commande brew && { BREW=1; GESTIONNAIRE="brew"; }
fi
[ -z "${RAM_GO:-}" ] && RAM_GO=0
LIBRE_GO="$(df -Pk "$BASE" 2> /dev/null | awk 'NR == 2 {printf "%.1f", $4 / 1048576}')"
[ -z "$LIBRE_GO" ] && LIBRE_GO=0

NVIDIA=0; NOM_NVIDIA=""; VRAM_MO=0; VRAM_GO="0"
if [ "$SYSTEME" = "Linux" ] && commande nvidia-smi; then
  Q="$(nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits 2> /dev/null | head -n 1)"
  if printf '%s' "$Q" | grep -Eq ',[[:space:]]*[0-9]+'; then
    NVIDIA=1
    NOM_NVIDIA="$(printf '%s' "$Q" | cut -d, -f1 | sed 's/^ *//;s/ *$//')"
    VRAM_MO="$(printf '%s' "$Q" | cut -d, -f2 | tr -dc '0-9')"
    VRAM_GO="$(awk -v m="$VRAM_MO" 'BEGIN { printf "%.1f", m / 1024 }')"
  fi
fi
CARTE="$(command -v lspci > /dev/null 2>&1 && lspci 2> /dev/null | grep -Ei 'vga|3d|display' | head -n 2 | cut -d: -f3- | sed 's/^ *//' | tr '\n' ';')"
[ -z "$CARTE" ] && [ "$SYSTEME" = "Darwin" ] && CARTE="$(system_profiler SPDisplaysDataType 2> /dev/null | awk -F': ' '/Chipset Model/ {print $2}' | tr '\n' ';')"
[ -z "$CARTE" ] && CARTE="non détectée"

# Python 64 bits 3.10 à 3.13 (ordre de préférence : 3.12, 3.13, 3.11, 3.10)
version_python() {  # exécutable -> « 3.12 » si 64 bits et 3.10 à 3.13, sinon rien
  local v
  v="$("$1" -c "import sys,struct;print('%d.%d %d' % (sys.version_info[0], sys.version_info[1], struct.calcsize('P')*8))" 2> /dev/null)" || return 1
  case "$v" in 3.10\ 64|3.11\ 64|3.12\ 64|3.13\ 64) printf '%s' "${v% 64}" ;; *) return 1 ;; esac
}
venv_possible() {  # un venv se crée-t-il avec cet exécutable ? (Debian/Ubuntu : paquet python3-venv à part)
  local t="$OUTILS/tmp/essai-venv"
  rm -rf "$t"
  "$1" -m venv "$t" > /dev/null 2>&1 && [ -x "$t/bin/python" ]
  local r=$?
  rm -rf "$t"
  return $r
}
trouver_python() {  # -> « version chemin » sur la sortie standard
  local cands="" nom exe v ordre
  for nom in python3.12 python3.13 python3.11 python3.10 python3 python; do
    exe="$(command -v "$nom" 2> /dev/null)" || continue
    v="$(version_python "$exe")" || continue
    cands="${cands}${v} ${exe}
"
  done
  ordre="3.12 3.13 3.11 3.10"
  [ -n "$VERSION_PYTHON" ] && ordre="$VERSION_PYTHON"
  for v in $ordre; do
    exe="$(printf '%s' "$cands" | awk -v v="$v" '$1 == v {print $2; exit}')"
    if [ -n "$exe" ] && venv_possible "$exe"; then printf '%s %s' "$v" "$exe"; return 0; fi
  done
  return 1
}
PYTHON_SANS_VENV=""
for n in python3.12 python3.13 python3.11 python3.10 python3 python; do
  e="$(command -v "$n" 2> /dev/null)" && version_python "$e" > /dev/null && { PYTHON_SANS_VENV="$e"; break; }
done
PY_INFO="$(trouver_python)"
PY_VERSION="${PY_INFO%% *}"
PY_BASE=""
[ -n "$PY_INFO" ] && PY_BASE="${PY_INFO#* }"

# ffmpeg portable déjà installé ?
FFMPEG_PORTABLE="$OUTILS/ffmpeg/bin"
[ -x "$FFMPEG_PORTABLE/ffmpeg" ] && PATH="$FFMPEG_PORTABLE:$PATH"
FFMPEG=0; commande ffmpeg && commande ffprobe && FFMPEG=1
GIT=0; commande git && GIT=1

printf '  Système         : %s (%s)%s\n' "$DISTRIB" "$ARCH" "$([ "$EN_WSL" = 1 ] && printf ' sous WSL')"
printf '  Processeur      : %s (%s fils)\n' "${CPU:-inconnu}" "$FILS"
printf '  Mémoire vive    : %s Go%s\n' "$RAM_GO" "$([ "$RAM_GO" -lt 8 ] && printf '  (juste : fermez les autres logiciels pendant la voix et le rendu)')"
printf '  Carte graphique : %s\n' "$CARTE"
if [ "$NVIDIA" = 1 ]; then
  printf '  Carte NVIDIA    : oui, %s (%s Go) : Whisper rapide\n' "$NOM_NVIDIA" "$VRAM_GO"
elif [ "$SYSTEME" = "Darwin" ]; then
  printf '  Carte NVIDIA    : sans objet sur Mac : tout tourne sur le processeur (Whisper plus lent)\n'
else
  printf '  Carte NVIDIA    : non : tout tourne sur le processeur (Whisper plus lent)\n'
fi
printf '  Place libre     : %s Go (là où est %s)\n' "$LIBRE_GO" "$BASE"
if [ -n "$PY_BASE" ]; then printf '  Python 64 bits  : %s (%s)\n' "$PY_VERSION" "$PY_BASE"
else printf '  Python 64 bits  : ABSENT (3.10 à 3.13 requis, avec le module venv)\n'; fi
printf '  ffmpeg          : %s\n' "$([ "$FFMPEG" = 1 ] && printf 'présent' || printf 'ABSENT')"
printf '  Git             : %s\n' "$([ "$GIT" = 1 ] && printf 'présent' || printf 'absent (facultatif ici ; utile à votre agent)')"
journal "Ordinateur : RAM $RAM_GO Go ; NVIDIA $NVIDIA $NOM_NVIDIA $VRAM_GO Go ; libre $LIBRE_GO Go ; Python $PY_INFO ; ffmpeg $FFMPEG ; Git $GIT ; WSL $EN_WSL"
if [ "$SYSTEME" = "Darwin" ] && [ "$ARCH" = "x86_64" ]; then
  alerte "Mac Intel : les versions récentes de PyTorch n'existent plus pour ce processeur ; la voix Pocket TTS peut échouer (voix de secours Piper disponible)."
fi

# Commande à proposer pour un prérequis (jamais lancée d'office avec sudo)
commande_installation() {  # paquet logique : python | ffmpeg | git | venv
  case "$GESTIONNAIRE:$1" in
    apt:python) echo "sudo apt update && sudo apt install -y python3 python3-venv python3-pip" ;;
    apt:venv) echo "sudo apt install -y python3-venv" ;;
    apt:ffmpeg) echo "sudo apt update && sudo apt install -y ffmpeg" ;;
    apt:git) echo "sudo apt install -y git" ;;
    dnf:python) echo "sudo dnf install -y python3.12" ;;
    dnf:venv) echo "sudo dnf install -y python3.12" ;;
    dnf:ffmpeg) echo "sudo dnf install -y ffmpeg-free   (ou ffmpeg après avoir activé RPM Fusion)" ;;
    dnf:git) echo "sudo dnf install -y git" ;;
    pacman:python|pacman:venv) echo "sudo pacman -S --needed python" ;;
    pacman:ffmpeg) echo "sudo pacman -S --needed ffmpeg" ;;
    pacman:git) echo "sudo pacman -S --needed git" ;;
    zypper:python|zypper:venv) echo "sudo zypper install python312" ;;
    zypper:ffmpeg) echo "sudo zypper install ffmpeg" ;;
    zypper:git) echo "sudo zypper install git" ;;
    brew:python|brew:venv) echo "brew install python@3.12" ;;
    brew:ffmpeg) echo "brew install ffmpeg" ;;
    brew:git) echo "brew install git" ;;
    *:python) if [ "$SYSTEME" = "Darwin" ]; then echo "installer Homebrew (https://brew.sh) puis : brew install python@3.12"; else echo "installez Python 3.10 à 3.13 (avec venv) par le gestionnaire de paquets de votre distribution"; fi ;;
    *:ffmpeg) if [ "$SYSTEME" = "Darwin" ]; then echo "installer Homebrew (https://brew.sh) puis : brew install ffmpeg"; else echo "installez ffmpeg par le gestionnaire de paquets de votre distribution"; fi ;;
    *) echo "installez-le par le gestionnaire de paquets de votre système" ;;
  esac
}

# Python absent : proposer la commande (sans sudo d'office)
if [ -z "$PY_BASE" ]; then
  CMD="$(commande_installation python)"
  [ -n "$PYTHON_SANS_VENV" ] && CMD="$(commande_installation venv)"
  [ -n "$PYTHON_SANS_VENV" ] && echo "${C_JAUNE}  Python $PYTHON_SANS_VENV est présent mais sans le module « venv ».${C_RAZ}"
  echo "  Commande proposée : $CMD"
  if [ "$SILENCIEUX" != 1 ] && { [ "$BREW" = 1 ] || [ -n "$GESTIONNAIRE" ]; } && oui "Lancer cette commande maintenant ? (sudo demandera votre mot de passe) (o/n)" "n"; then
    info "installation de Python : $CMD"
    sh -c "$CMD"
    PY_INFO="$(trouver_python)"
    PY_VERSION="${PY_INFO%% *}"
    [ -n "$PY_INFO" ] && PY_BASE="${PY_INFO#* }"
  fi
  if [ -z "$PY_BASE" ]; then
    echo "${C_ROUGE}  Python 64 bits (3.10 à 3.13, avec venv) est nécessaire. Lancez la commande ci-dessus, puis relancez ce script.${C_RAZ}"
    exit 1
  fi
  ok "Python $PY_VERSION : $PY_BASE"
fi

# -- reutiliser : outils d'une installation existante, repris par leurs chemins (rien n'est copié ni lié)
if [ -n "$REUTILISER" ] && [ ! -f "$REUTILISER" ]; then echo "${C_ROUGE}Fichier introuvable : $REUTILISER${C_RAZ}"; exit 1; fi
ancien_chemin() {  # clé (pointée : mfa.env) -> chemin s'il existe, sinon rien
  [ -n "$REUTILISER" ] || return 0
  "$PY_BASE" -c "
import json, os, sys
v = json.load(open(sys.argv[1], encoding='utf-8-sig'))
for k in sys.argv[2].split('.'):
    v = v.get(k) if isinstance(v, dict) else None
print(v if v and os.path.exists(str(v)) else '')
" "$REUTILISER" "$1"
}
ancien_mfa_json() {  # objet « mfa » de l'ancien config.json si son environnement existe
  [ -n "$REUTILISER" ] || return 0
  "$PY_BASE" -c "
import json, os, sys
d = json.load(open(sys.argv[1], encoding='utf-8-sig')).get('mfa') or {}
env = d.get('env') or ''
print(json.dumps(d) if env and os.path.exists(os.path.join(env, 'bin', 'mfa')) else '')
" "$REUTILISER"
}
a_sec() {  # brique, commande
  ok "$1 : repris de l'installation existante (--reutiliser)"
  info "à sec, commande qui aurait été lancée : $2"
}

# ------------------------------------------------------------------ 3. La question
if [ "$NVIDIA" = 1 ]; then POIDS_WHISPER="4.6"; else POIDS_WHISPER="1.9"; fi
fait whisper && ENREGISTREMENTS="oui"
if [ -z "$ENREGISTREMENTS" ]; then
  echo ""
  printf '%s  La voix de synthèse (texte rédigé puis lu par l'"'"'ordinateur) fonctionne sans rien de plus.%s\n' "$C_GRIS" "$C_RAZ"
  if [ "$NVIDIA" = 1 ]; then SUITE=" (avec votre carte NVIDIA : rapide)"
  else SUITE=" (sans carte NVIDIA : sur le processeur, plusieurs fois plus lent)"; fi
  printf '%s  Pour vos PROPRES enregistrements, il faut en plus la transcription Whisper : ≈ %s Go%s.%s\n' "$C_GRIS" "$POIDS_WHISPER" "$SUITE" "$C_RAZ"
  if oui "Voulez-vous travailler avec vos propres enregistrements (les nettoyer, les animer) ? (o/n)" "n"; then ENREGISTREMENTS="oui"; else ENREGISTREMENTS="non"; fi
fi
AVEC_WHISPER=0; [ "$ENREGISTREMENTS" = "oui" ] && AVEC_WHISPER=1
if [ "$AVEC_WHISPER" = 1 ]; then BESOIN="$(awk -v w="$POIDS_WHISPER" 'BEGIN { printf "%.1f", 6 + w }')"; else BESOIN="6.0"; fi
printf '  À installer : ≈ %s Go dans %s ; durée ≈ 20 à 40 min (surtout du téléchargement).\n' "$BESOIN" "$OUTILS"
if awk -v l="$LIBRE_GO" -v b="$BESOIN" 'BEGIN { exit !(l < b + 2) }'; then
  echo "${C_ROUGE}  Place insuffisante (il faut ≈ $(awk -v b="$BESOIN" 'BEGIN { printf "%.0f", b + 2 }') Go libres là où est $BASE). Choisissez un autre dossier de base.${C_RAZ}"
  exit 1
fi
oui "Lancer l'installation ? (o/n)" "o" || exit 0
journal "Enregistrements : $ENREGISTREMENTS ; Python $PY_INFO"

# Environnement du processus (et de ses enfants) : tout sous outils/
ANCIEN_HF="$(ancien_chemin cache_modeles)"
ANCIEN_PIP=""
[ -n "$ANCIEN_HF" ] && ANCIEN_PIP="$(dirname "$ANCIEN_HF")/cache-pip"
if [ -n "$ANCIEN_PIP" ] && [ -d "$ANCIEN_PIP" ]; then export PIP_CACHE_DIR="$ANCIEN_PIP"; else export PIP_CACHE_DIR="$OUTILS/cache-pip"; fi
if [ -n "$ANCIEN_HF" ]; then export HF_HOME="$ANCIEN_HF"; else export HF_HOME="$OUTILS/cache-hf"; fi
export PLAYWRIGHT_BROWSERS_PATH="$OUTILS/navigateurs"
export XDG_CACHE_HOME="$OUTILS/cache-xdg"
export TMPDIR="$OUTILS/tmp"
export HF_HUB_DISABLE_SYMLINKS_WARNING=1
export PYTHONUTF8=1 PYTHONIOENCODING=utf-8
export PIP_REQUIRE_VIRTUALENV=0
mkdir -p "$PIP_CACHE_DIR" "$HF_HOME" "$XDG_CACHE_HOME" "$TMPDIR"

PY_RENDU="$OUTILS/venv-rendu/bin/python"
REUT_POCKET="$(ancien_chemin python_pocket)"
REUT_PARAKEET="$(ancien_chemin python_parakeet)"
REUT_WHISPER="$(ancien_chemin python_asr)"
REUT_PIPER="$(ancien_chemin voix_piper)"
REUT_MFA="$(ancien_mfa_json)"
PY_POCKET="${REUT_POCKET:-$OUTILS/venv-pocket/bin/python}"
PY_PARAKEET="${REUT_PARAKEET:-$OUTILS/venv-parakeet/bin/python}"
PY_WHISPER="${REUT_WHISPER:-$OUTILS/venv-whisper/bin/python}"
VOIX_PIPER="${REUT_PIPER:-$OUTILS/voix-piper}"
[ -n "$REUTILISER" ] && journal "Réutilisation : HF $ANCIEN_HF ; pocket $REUT_POCKET ; parakeet $REUT_PARAKEET ; whisper $REUT_WHISPER ; piper $REUT_PIPER ; mfa $REUT_MFA"
CIBLE="$BASE/$SKILLS_REL/capsule-video"
AIDE="$CIBLE/installation/aide_installation.py"

creer_venv() {  # dossier -> 0 si le venv existe et fonctionne
  local py="$1/bin/python"
  if [ ! -x "$py" ]; then
    executer "$PY_BASE" -m venv "$1" || return 1
    executer "$py" -m pip install -q --upgrade pip --disable-pip-version-check
  fi
  [ -x "$py" ]
}

# ------------------------------------------------------------------ 4. Skill, CLAUDE.md, AGENTS.md
titre "Dossier de base" "Le skill (instructions et scripts de l'agent), le mode d'emploi du dossier et le dossier des capsules."
T_ETAPE=$SECONDS
mkdir -p "$BASE/$SKILLS_REL"
if [ -d "$BASE/$AUTRE_REL/capsule-video" ]; then alerte "une autre copie du skill existe dans $BASE/$AUTRE_REL/capsule-video : elle n'est pas configurée et plus utilisée (la supprimer évite la confusion)"; fi
if [ "$SKILL" != "$CIBLE" ]; then
  # config.json et preferences.md ne sont jamais copiés : ils sont propres à chaque utilisateur
  if executer "$PY_BASE" "$SKILL/installation/aide_installation.py" copier --source "$SKILL" --cible "$CIBLE"; then
    ok "skill copié (ou mis à jour) dans $CIBLE"
  else echo "${C_ROUGE}  Copie du skill impossible (voir $LOG).${C_RAZ}"; exit 1; fi
else ok "skill déjà en place"; fi
chmod +x "$CIBLE/installation/installer.sh" 2> /dev/null
PREF="$CIBLE/references/preferences.md"
if [ ! -f "$PREF" ]; then cp "$CIBLE/installation/preferences-vierge.md" "$PREF"; ok "préférences vierges : references/preferences.md"; fi
FICHIER_AGENT="CLAUDE.md"; [ "$AGENT" = "codex" ] && FICHIER_AGENT="AGENTS.md"
sed -e "s|{{BASE}}|$BASE|g" -e "s|{{PYTHON}}|outils/venv-rendu/bin/python|g" -e "s|{{SKILLS}}|$SKILLS_REL|g" -e "s|installer\\.ps1|installer.sh|g" \
  "$CIBLE/installation/modele-CLAUDE.md" > "$BASE/$FICHIER_AGENT"
if [ "$AGENT" = "claude" ]; then cp "$BASE/CLAUDE.md" "$BASE/AGENTS.md"; ok "CLAUDE.md et AGENTS.md écrits (mode d'emploi pour l'agent, pointant sur $SKILLS_REL/capsule-video)"
else ok "AGENTS.md écrit (mode d'emploi pour l'agent, pointant sur $SKILLS_REL/capsule-video)"; fi

# config.json : chemins sous outils/, valeurs selon l'ordinateur (references/outils-audio.md)
json_chaine() { if [ -n "$1" ]; then printf '"%s"' "$1"; else printf 'null'; fi; }
ecrire_config() {
  local tmp="$OUTILS/config-valeurs.json" asr arbitre enreg device modele ffdir
  if [ "$AVEC_WHISPER" = 1 ]; then asr="$PY_WHISPER"; enreg="whisper"; else asr=""; enreg="parakeet"; fi
  if [ "$AVEC_WHISPER" = 1 ] && [ "$NVIDIA" = 1 ]; then arbitre="whisper"; else arbitre=""; fi
  if [ "$NVIDIA" = 1 ]; then device="auto"; else device="cpu"; fi
  if [ "$NVIDIA" = 1 ] && [ "$VRAM_MO" -ge 6144 ]; then modele="large-v3"; else modele="medium"; fi
  if [ -x "$FFMPEG_PORTABLE/ffmpeg" ]; then ffdir="$FFMPEG_PORTABLE"; else ffdir=""; fi
  {
    printf '{\n'
    printf '  "python_rendu": "%s",\n  "python_tts": "%s",\n  "python_voix": "%s",\n' "$PY_RENDU" "$PY_RENDU" "$PY_RENDU"
    printf '  "python_pocket": "%s",\n  "python_parakeet": "%s",\n' "$PY_POCKET" "$PY_PARAKEET"
    printf '  "python_asr": %s,\n' "$(json_chaine "$asr")"
    printf '  "asr_fidelite": "parakeet",\n'
    printf '  "arbitre_fidelite": %s,\n' "$(json_chaine "$arbitre")"
    printf '  "asr_enregistrements": "%s",\n' "$enreg"
    printf '  "horodatage": "mfa",\n'
    printf '  "whisper_device": "%s",\n  "modele_asr": "%s",\n' "$device" "$modele"
    printf '  "modele_pocket": "french_24l",\n  "voix_pocket_defaut": "estelle",\n  "voix_clonees": {},\n'
    printf '  "cache_modeles": "%s",\n  "navigateurs": "%s",\n' "$HF_HOME" "$PLAYWRIGHT_BROWSERS_PATH"
    printf '  "voix_piper": "%s",\n' "$VOIX_PIPER"
    printf '  "dossier_ffmpeg": %s,\n' "$(json_chaine "$ffdir")"
    printf '  "dossier_capsules": "%s",\n' "$BASE/capsules"
    printf '  "qualite_rendu": "envoi",\n  "premier_usage_fait": false,\n'
    [ -n "$REUT_MFA" ] && printf '  "mfa": %s,\n' "$REUT_MFA"
    printf '  "_note": "Écrit par installation/installer.sh. PERSONNEL : voix_clonees (jamais partagé). Clés audio : references/outils-audio.md. premier_usage_fait=false : l agent lit references/first_check.md."\n'
    printf '}\n'
  } > "$tmp"
  local py="$PY_BASE"; [ -x "$PY_RENDU" ] && py="$PY_RENDU"
  executer "$py" "$AIDE" config --skill "$CIBLE" --valeurs "$tmp" || probleme "écriture de config.json" "voir $LOG"
}
ecrire_config
ok "config.json écrit ($(duree_depuis "$T_ETAPE"))"
chrono "Dossier de base"

# ------------------------------------------------------------------ 5. ffmpeg
if [ "$FFMPEG" != 1 ]; then
  titre "ffmpeg" "Assemble les images et la voix en vidéo."
  T_ETAPE=$SECONDS
  CMD_FF="$(commande_installation ffmpeg)"
  ff_ok=0
  if [ "$SYSTEME" = "Linux" ] && { [ "$ARCH" = "x86_64" ] || [ "$ARCH" = "amd64" ] || [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; }; then
    if oui "Télécharger ffmpeg portable dans outils/ffmpeg (≈ 40 Mo, sans rien modifier d'autre) ? (o/n)" "o"; then
      case "$ARCH" in x86_64|amd64) VARIANTE="amd64"; BTBN="linux64" ;; *) VARIANTE="arm64"; BTBN="linuxarm64" ;; esac
      ARCHIVE="$OUTILS/ffmpeg.tar.xz"
      if telecharger "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-$VARIANTE-static.tar.xz" "$ARCHIVE" \
         || telecharger "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-$BTBN-gpl.tar.xz" "$ARCHIVE"; then
        if executer "$PY_BASE" "$AIDE" ffmpeg --archive "$ARCHIVE" --dest "$FFMPEG_PORTABLE"; then
          rm -f "$ARCHIVE"
          PATH="$FFMPEG_PORTABLE:$PATH"; ff_ok=1
          ok "ffmpeg portable : $FFMPEG_PORTABLE ($(duree_depuis "$T_ETAPE"))"
        fi
      fi
    fi
  elif [ "$BREW" = 1 ] && oui "Installer ffmpeg avec Homebrew ($CMD_FF) ? (o/n)" "o"; then
    info "installation de ffmpeg (Homebrew)"
    executer brew install ffmpeg && commande ffmpeg && ff_ok=1 && ok "ffmpeg installé par Homebrew"
  fi
  if [ "$ff_ok" != 1 ]; then probleme "ffmpeg" "installez-le (« $CMD_FF »), puis relancez ce script"; fi
  chrono "ffmpeg"
fi

# ------------------------------------------------------------------ 6. Rendu + voix de secours
titre "Rendu des vidéos" "Python dédié + Chromium (navigateur invisible qui dessine l'animation) + voix de secours Piper. ≈ 0,8 Go."
T_ETAPE=$SECONDS
if fait rendu; then ok "déjà installé"; else
  info "environnement Python et bibliothèques (≈ 2 min)"
  if creer_venv "$OUTILS/venv-rendu" && pip_installer "$PY_RENDU" playwright psutil numpy scipy num2words piper-tts; then
    info "Chromium (≈ 1 min)"
    if executer "$PY_RENDU" -m playwright install --only-shell chromium; then marquer rendu; ok "rendu prêt"
    else probleme "Chromium" "relancez l'installeur ; derrière un proxy : voir $LOG"; fi
  else probleme "environnement de rendu" "relancez l'installeur ; détail dans $LOG"; fi
fi
if [ -n "$REUT_PIPER" ]; then a_sec "voix Piper" "téléchargement de fr_FR-{siwis,tom,upmc}-medium.onnx dans outils/voix-piper"
elif ! fait piper; then
  mkdir -p "$VOIX_PIPER"
  tout=1
  for v in siwis tom upmc; do
    for ext in onnx onnx.json; do
      dest="$VOIX_PIPER/fr_FR-$v-medium.$ext"
      if [ ! -f "$dest" ]; then
        telecharger "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/$v/medium/fr_FR-$v-medium.$ext" "$dest" || tout=0
      fi
    done
  done
  if [ "$tout" = 1 ]; then marquer piper; ok "voix de secours Piper (siwis, tom, upmc)"; else alerte "voix Piper incomplètes (secours seulement : sans gravité)"; fi
fi
chrono "Rendu + Piper"
ecrire_config

# ------------------------------------------------------------------ 7. Pocket TTS
titre "Voix de synthèse Pocket TTS" "La voix par défaut (française, naturelle), sur processeur. ≈ 1,8 Go (PyTorch processeur + modèle)."
T_ETAPE=$SECONDS
if [ -n "$REUT_POCKET" ]; then a_sec "Pocket TTS" "venv-pocket + pip install pocket-tts num2words --extra-index-url https://download.pytorch.org/whl/cpu + aide_installation.py precharger pocket"
elif fait pocket; then ok "déjà installé"; else
  info "PyTorch processeur et Pocket TTS (≈ 3 min)"
  if creer_venv "$OUTILS/venv-pocket" && pip_installer "$PY_POCKET" pocket-tts num2words --extra-index-url https://download.pytorch.org/whl/cpu; then
    info "modèle french_24l et voix estelle (≈ 2 min la première fois)"
    if executer "$PY_POCKET" -X utf8 "$AIDE" precharger pocket; then marquer pocket; ok "Pocket TTS prêt"
    else probleme "modèle Pocket TTS" "relancez l'installeur (téléchargement interrompu ?) ; détail dans $LOG"; fi
  else probleme "Pocket TTS" "relancez l'installeur ; détail dans $LOG. Secours en attendant : voix Piper"; fi
fi
chrono "Pocket TTS"

# ------------------------------------------------------------------ 8. Parakeet
titre "Contrôle de la voix : Parakeet" "Réécoute chaque phrase générée pour vérifier qu'aucun mot n'a été sauté. ≈ 0,8 Go."
T_ETAPE=$SECONDS
if [ -n "$REUT_PARAKEET" ]; then a_sec "Parakeet" "venv-parakeet + pip install onnx-asr[cpu,hub] soundfile num2words + aide_installation.py precharger parakeet"
elif fait parakeet; then ok "déjà installé"; else
  if creer_venv "$OUTILS/venv-parakeet" && pip_installer "$PY_PARAKEET" "onnx-asr[cpu,hub]" soundfile num2words; then
    info "modèle Parakeet (640 Mo, ≈ 5 min la première fois)"
    if executer "$PY_PARAKEET" -X utf8 "$AIDE" precharger parakeet; then marquer parakeet; ok "Parakeet prêt"
    else probleme "modèle Parakeet" "relancez l'installeur ; détail dans $LOG"; fi
  else probleme "Parakeet" "relancez l'installeur ; détail dans $LOG"; fi
fi
chrono "Parakeet"

# ------------------------------------------------------------------ 9. MFA
titre "Horodatage au mot : MFA" "Pose chaque mot du texte sur la voix (à 20 ms près) pour caler les animations. ≈ 2,5 Go, ≈ 7 min."
T_ETAPE=$SECONDS
RACINE_MFA="$OUTILS/mfa"
if [ -n "$REUT_MFA" ]; then a_sec "MFA" "$PY_RENDU $CIBLE/scripts/installer_mfa.py --racine $RACINE_MFA --config $CIBLE/config.json --maj-config"
elif [ -x "$RACINE_MFA/env-mfa/bin/mfa" ] && [ -f "$RACINE_MFA/mfa-modeles/pretrained_models/acoustic/french_mfa.zip" ]; then ok "déjà installé"
elif executer "$PY_RENDU" "$CIBLE/scripts/installer_mfa.py" --racine "$RACINE_MFA" --config "$CIBLE/config.json" --maj-config; then
  ok "MFA prêt ($(duree_depuis "$T_ETAPE"))"
else probleme "MFA" "relancez l'installeur ; si l'erreur parle de SSL : voir $LOG. Sans MFA, l'horodatage passe par Whisper (si installé)"; fi
chrono "MFA"

# ------------------------------------------------------------------ 10. Whisper (facultatif)
if [ "$AVEC_WHISPER" = 1 ]; then
  if [ "$NVIDIA" = 1 ] && [ "$VRAM_MO" -ge 6144 ]; then MODELE_W="large-v3"; else MODELE_W="medium"; fi
  if [ "$NVIDIA" = 1 ]; then OU=" sur la carte NVIDIA"; else OU=" sur le processeur (plus lent)"; fi
  titre "Transcription de vos enregistrements : Whisper" "Modèle $MODELE_W$OU, ≈ $POIDS_WHISPER Go."
  T_ETAPE=$SECONDS
  if [ "$NVIDIA" = 1 ]; then PAQ_W="faster-whisper num2words nvidia-cublas-cu12 nvidia-cudnn-cu12==9.*"; else PAQ_W="faster-whisper num2words"; fi
  if [ -n "$REUT_WHISPER" ]; then a_sec "Whisper" "venv-whisper + pip install $PAQ_W + aide_installation.py precharger whisper $MODELE_W"; marquer whisper
  elif fait whisper; then ok "déjà installé"; else
    # shellcheck disable=SC2086
    if creer_venv "$OUTILS/venv-whisper" && pip_installer "$PY_WHISPER" $PAQ_W; then
      info "modèle $MODELE_W (≈ 5 à 10 min la première fois)"
      if executer "$PY_WHISPER" -X utf8 "$AIDE" precharger whisper "$MODELE_W"; then marquer whisper; ok "Whisper prêt"
      else probleme "modèle Whisper" "relancez l'installeur ; détail dans $LOG"; fi
    else probleme "Whisper" "relancez l'installeur ; détail dans $LOG"; fi
  fi
  chrono "Whisper"
fi
ecrire_config

# ------------------------------------------------------------------ 11. Essai de chaque brique
titre "Essai" "Une phrase dite par Pocket, contrôlée par Parakeet, horodatée par MFA, puis une image rendue (≈ 2 min)."
T_ETAPE=$SECONDS
BILAN="$OUTILS/bilan-installation.json"
if [ -x "$PY_RENDU" ]; then
  "$PY_RENDU" "$AIDE" essai --skill "$CIBLE" --travail "$OUTILS/essai-installation" --bilan "$BILAN" 2>&1 | tee -a "$LOG"
  if [ "${PIPESTATUS[0]}" -ne 0 ]; then
    alerte "au moins une brique ne répond pas : voir les solutions ci-dessus"
    if [ "$SYSTEME" = "Linux" ] && grep -qE "error while loading shared libraries|libnss3|libatk|Host system is missing dependencies" "$OUTILS/essai-installation"/journal-rendu.txt 2> /dev/null; then
      alerte "Chromium manque de bibliothèques système : sudo \"$PY_RENDU\" -m playwright install-deps chromium"
    fi
  fi
else probleme "essai" "environnement de rendu absent : relancez l'installeur"; fi
chrono "Essai"

# ------------------------------------------------------------------ 12. Bilan
titre "Bilan" ""
DOSSIERS=""
for d in venv-rendu navigateurs voix-piper venv-pocket venv-parakeet mfa venv-whisper cache-hf cache-xdg ffmpeg; do
  [ -e "$OUTILS/$d" ] && DOSSIERS="$DOSSIERS $d"
done
TOTAL="0"
# shellcheck disable=SC2086
for d in $DOSSIERS; do
  g="$("$PY_RENDU" "$AIDE" poids "$OUTILS/$d" 2> /dev/null | head -n 1)"
  [ -z "$g" ] && g="0"
  TOTAL="$(awk -v a="$TOTAL" -v b="$g" 'BEGIN { printf "%.2f", a + b }')"
  printf '  %-15s %6.2f Go\n' "$d" "$g"
done
printf '  %-15s %6.2f Go   (cache pip non compté : supprimable, outils/cache-pip)\n' "TOTAL" "$TOTAL"
echo ""
printf '%s' "$CHRONO" | while IFS='|' read -r k v; do
  [ -n "$k" ] && printf '%s  %-16s %s%s\n' "$C_GRIS" "$k" "$v" "$C_RAZ"
done
MIN="$(awk -v s=$((SECONDS - DEBUT)) 'BEGIN { printf "%.0f", s / 60 }')"
printf '  Durée totale : %s min\n' "$MIN"
journal "Poids total $TOTAL Go ; durée $MIN min"

if [ "$NB_PROBLEMES" -gt 0 ]; then
  echo ""
  printf '%s  À corriger :%s\n' "$C_ROUGE" "$C_RAZ"
  printf '%s%s%s' "$C_ROUGE" "$PROBLEMES" "$C_RAZ"
fi
echo ""
printf '%sInstallation terminée. Pour votre première capsule :%s\n' "$C_JAUNE" "$C_RAZ"
echo "  1. Ouvrez votre agent (Claude Code, Codex…) dans le dossier $BASE"
echo "     (terminal : cd $BASE  puis  $([ "$AGENT" = "codex" ] && printf codex || printf claude))"
echo "  2. Dites : « Fais-moi une capsule vidéo de correction de l'exercice suivant : … »"
echo "     La première fois, l'agent vous propose quelques questions sur vos goûts (facultatives)."
echo "  Vos capsules arriveront dans $BASE/capsules"
echo ""
printf '%s  Parler avec VOTRE voix (facultatif) : il faut un compte Hugging Face gratuit et accepter les conditions%s\n' "$C_GRIS" "$C_RAZ"
printf '%s  du modèle de clonage. Marche à suivre : %s/capsule-video/references/cloner-sa-voix.md%s\n' "$C_GRIS" "$SKILLS_REL" "$C_RAZ"
if [ "$AVEC_WHISPER" != 1 ]; then
  printf '%s  Travailler plus tard avec vos enregistrements : relancez ce script et répondez « oui ».%s\n' "$C_GRIS" "$C_RAZ"
fi
printf '%s  Journal complet : %s%s\n' "$C_GRIS" "$LOG" "$C_RAZ"
[ "$NB_PROBLEMES" -eq 0 ]

<#
  Installeur « Capsules vidéo animées » (skill capsule-video) : gratuit, 100 % local, relançable.

  Ce que fait le script :
    1. demande le DOSSIER DE BASE (ex. D:\Capsules) et y prépare :
         .claude\skills\capsule-video\   le skill (instructions et scripts suivis par l'agent)
         CLAUDE.md et AGENTS.md          le mode d'emploi du dossier, pour tout agent (Claude Code, Codex…)
         outils\                         tout le lourd : Python, modèles, navigateur, MFA… (rien ailleurs)
         capsules\                       vos capsules, une par dossier
    2. inspecte le PC (carte NVIDIA, mémoire, place libre, Python, ffmpeg, Git) ;
    3. pose UNE question : travaillerez-vous avec vos propres enregistrements ?
    4. installe la base (≈ 6 Go, processeur seul) : rendu, voix Pocket TTS, contrôle Parakeet, horodatage MFA,
       voix de secours Piper ; et, si oui à la question, Whisper ;
    5. écrit config.json et essaie chaque brique sur une phrase (bilan OK / problème + solution).

  Rien n'est modifié hors du dossier de base : ni le PATH, ni le profil du terminal. Jamais Anaconda.
  Journal : <base>\outils\installation.log. Relancer le script saute ce qui est déjà fait.

  Lancement : clic droit > « Exécuter avec PowerShell », ou :
    powershell -ExecutionPolicy Bypass -File .\installer.ps1
  Sans question (tests, déploiement) :
    powershell -ExecutionPolicy Bypass -File .\installer.ps1 -DossierBase D:\Capsules -Enregistrements non -Silencieux
  Options :
    -Reutiliser <config.json>  reprendre les outils d'une installation existante (python_pocket, python_parakeet,
                        python_asr, mfa, cache_modeles, voix_piper) par leurs chemins, sans rien copier ni
                        retélécharger ; seul l'environnement de rendu est créé. Les installations sautées sont
                        affichées « à sec » (commande qui aurait été lancée). Sert aux essais et à un changement
                        de dossier de base.
    -VersionPython 3.12 imposer une version de Python (3.10 à 3.13, 64 bits)
#>
param(
  [string]$DossierBase = "",
  [ValidateSet("", "oui", "non")][string]$Enregistrements = "",
  [switch]$Silencieux,
  [string]$Reutiliser = "",
  [string]$VersionPython = ""
)
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"
[Console]::OutputEncoding = [Text.Encoding]::UTF8
try { [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12 } catch {}
$Debut = Get-Date

# ------------------------------------------------------------------ affichage et journal
$Log = $null
# Écriture tolérante : un journal ouvert ailleurs (éditeur, antivirus) ne doit jamais arrêter l'installation
function Ajouter-Journal($texte) {
  if (-not $Log) { return }
  for ($i = 0; $i -lt 5; $i++) {
    try { [IO.File]::AppendAllText($Log, $texte + "`r`n", (New-Object Text.UTF8Encoding $false)); return }
    catch { Start-Sleep -Milliseconds 300 }
  }
}
function Journal($t) { Ajouter-Journal ("[{0:HH:mm:ss}] {1}" -f (Get-Date), $t) }
$NumEtape = 0
function Titre($n, $texte, $explication) {
  $script:NumEtape++; $n = $script:NumEtape   # numérotation continue (ffmpeg et Whisper sont facultatifs)
  Write-Host ""
  Write-Host "=== $n. $texte ===" -ForegroundColor Cyan
  if ($explication) { Write-Host "    $explication" -ForegroundColor DarkGray }
  Journal "=== $n. $texte"
}
function Ok($t) { Write-Host "    OK  $t" -ForegroundColor Green; Journal "OK $t" }
function Info($t) { Write-Host "    ... $t"; Journal $t }
function Alerte($t) { Write-Host "    !!  $t" -ForegroundColor Yellow; Journal "ALERTE $t" }
function Duree($sw) { $s = [int]$sw.Elapsed.TotalSeconds; if ($s -ge 60) { "{0} min {1:00} s" -f [int][math]::Floor($s / 60), ($s % 60) } else { "$s s" } }
function Demander($question, $defaut) {
  if ($Silencieux) { return $defaut }
  $r = Read-Host "$question [$defaut]"
  if ([string]::IsNullOrWhiteSpace($r)) { return $defaut } else { return $r.Trim().Trim('"') }
}
function Oui($question, $defaut) { return (Demander $question $defaut) -match "^[oOyY]" }

$Problemes = New-Object System.Collections.ArrayList
function Probleme($brique, $solution) {
  [void]$Problemes.Add([pscustomobject]@{ Brique = $brique; Solution = $solution })
  Write-Host "    ÉCHEC  $brique" -ForegroundColor Red
  Write-Host "           → $solution" -ForegroundColor Red
  Journal "ECHEC $brique -> $solution"
}

# Lance un programme, sa sortie va dans le journal ; renvoie le code de sortie.
function Executer([string]$Exe, [string[]]$Arguments) {
  $out = [IO.Path]::GetTempFileName(); $err = [IO.Path]::GetTempFileName()
  $ligne = ($Arguments | ForEach-Object { if ($_ -match '[\s"]') { '"' + ($_ -replace '"', '\"') + '"' } else { $_ } }) -join ' '
  Journal "> $Exe $ligne"
  $p = Start-Process -FilePath $Exe -ArgumentList $ligne -NoNewWindow -Wait -PassThru `
         -RedirectStandardOutput $out -RedirectStandardError $err
  foreach ($f in @($out, $err)) {
    $c = Get-Content $f -Raw -Encoding UTF8 -ErrorAction SilentlyContinue
    if ($c) { Ajouter-Journal $c.TrimEnd() }
    Remove-Item $f -Force -ErrorAction SilentlyContinue
  }
  return $p.ExitCode
}

# pip avec repli SSL (réseau d'établissement qui intercepte les certificats)
function Pip([string]$Py, [string[]]$Paquets) {
  $base = @("-m", "pip", "install", "--disable-pip-version-check", "--no-input") + $Paquets
  if ((Executer $Py $base) -eq 0) { return $true }
  Info "nouvel essai de pip sans vérification SSL (réseau filtrant)"
  $hotes = @("--trusted-host", "pypi.org", "--trusted-host", "files.pythonhosted.org", "--trusted-host", "download.pytorch.org")
  return ((Executer $Py ($base + $hotes)) -eq 0)
}

function Telecharger($url, $dest) {
  try { Invoke-WebRequest -UseBasicParsing -Uri $url -OutFile "$dest.part"; Move-Item "$dest.part" $dest -Force; return $true }
  catch {
    Journal "téléchargement Invoke-WebRequest échoué ($url) : $_"
    if (Get-Command curl.exe -ErrorAction SilentlyContinue) {
      & curl.exe -L --ssl-no-revoke -s -o "$dest.part" $url
      if ($LASTEXITCODE -eq 0 -and (Test-Path "$dest.part")) { Move-Item "$dest.part" $dest -Force; return $true }
    }
    return $false
  }
}

# Étapes faites (idempotence) : un fichier témoin par étape
function Fait($cle) { return (Test-Path (Join-Path $Etapes "$cle.ok")) }
function Marquer($cle) { Set-Content -Path (Join-Path $Etapes "$cle.ok") -Value (Get-Date -Format s) -Encoding ASCII }

# -Reutiliser : outils d'une installation existante, repris par leurs chemins (rien n'est copié ni lié)
$Ancien = $null
if ($Reutiliser) {
  if (-not (Test-Path $Reutiliser)) { Write-Host "Fichier introuvable : $Reutiliser" -ForegroundColor Red; exit 1 }
  $Ancien = Get-Content $Reutiliser -Raw -Encoding UTF8 | ConvertFrom-Json
}
function Ancien-Chemin($cle) {
  if (-not $Ancien) { return $null }
  $v = $Ancien.$cle
  if ($v -and (Test-Path $v)) { return ($v -replace "/", "\") }
  return $null
}
function A-Sec($brique, $commande) {
  Ok "$brique : repris de l'installation existante (-Reutiliser)"
  Info "à sec, commande qui aurait été lancée : $commande"
}

function Commande($nom) { return [bool](Get-Command $nom -ErrorAction SilentlyContinue) }

# ------------------------------------------------------------------ 0. Source du skill
$Skill = Split-Path -Parent $PSScriptRoot
if (-not (Test-Path (Join-Path $Skill "SKILL.md"))) { $Skill = Join-Path $PSScriptRoot "capsule-video" }
if (-not (Test-Path (Join-Path $Skill "SKILL.md"))) {
  Write-Host "Le dossier du skill « capsule-video » est introuvable." -ForegroundColor Red
  Write-Host "Placez installer.ps1 dans le dossier capsule-video\installation\ du kit, ou à côté du dossier capsule-video, puis relancez."
  exit 1
}
$Skill = (Resolve-Path $Skill).Path

Write-Host "Capsules vidéo animées : installation" -ForegroundColor Yellow
Write-Host "Tout est gratuit et tourne sur votre ordinateur. Entrée = valeur proposée." -ForegroundColor DarkGray

# ------------------------------------------------------------------ 1. Dossier de base
$defaut = if (Test-Path "D:\") { "D:\Capsules" } else { Join-Path $env:USERPROFILE "Capsules" }
$ValideRe = '^[A-Za-z]:\\[A-Za-z0-9_.\-\\]+$'
if ($defaut -notmatch $ValideRe) { $defaut = "C:\Capsules" }
while ($true) {
  if (-not $DossierBase) { $DossierBase = Demander "Dossier de base (outils lourds + capsules, ≈ 6 à 11 Go)" $defaut }
  $DossierBase = $DossierBase.Replace("/", "\").TrimEnd("\")
  if ($DossierBase -match $ValideRe) { break }
  Write-Host "  Chemin refusé : lettres, chiffres, - _ . seulement (ni espace ni accent : plusieurs outils les supportent mal). Exemple : D:\Capsules" -ForegroundColor Red
  if ($Silencieux) { exit 1 }
  $DossierBase = ""
}
$Base = $DossierBase
$Outils = Join-Path $Base "outils"
$Etapes = Join-Path $Outils ".etapes"
New-Item -ItemType Directory -Force -Path $Outils, $Etapes, (Join-Path $Base "capsules") | Out-Null
$Log = Join-Path $Outils "installation.log"
Journal "===== Installation lancée le $(Get-Date -Format 'yyyy-MM-dd HH:mm') ; base = $Base ; skill source = $Skill"

# ------------------------------------------------------------------ 2. Inspection du PC
Titre 1 "Votre ordinateur" "Inspection automatique : rien n'est modifié."
$Cpu = Get-CimInstance Win32_Processor | Select-Object -First 1
$RamGo = [math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB)
$Cartes = @(Get-CimInstance Win32_VideoController | ForEach-Object { $_.Name })
$Nvidia = $false; $VramGo = 0; $NomNvidia = ""
if (Commande "nvidia-smi") {
  # pas de « | Select-Object -First 1 » : il coupe nvidia-smi en cours de route (code de sortie -1)
  $q = @(& nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits 2>$null)[0]
  if ($LASTEXITCODE -eq 0 -and $q -match ',\s*\d+') { $Nvidia = $true; $NomNvidia = ($q -split ",")[0].Trim(); $VramGo = [math]::Round([double](($q -split ",")[1].Trim()) / 1024, 1) }
}
if (-not $Nvidia -and ($Cartes -match "NVIDIA")) { $NomNvidia = ($Cartes -match "NVIDIA")[0]; Alerte "carte NVIDIA vue mais nvidia-smi ne répond pas : pilote à mettre à jour (Whisper restera sur processeur)" }
$Lecteur = $Base.Substring(0, 1)
$LibreGo = [math]::Round((Get-PSDrive $Lecteur).Free / 1GB, 1)

# Python 64 bits 3.10 à 3.13 (ordre de préférence : 3.12, 3.13, 3.11, 3.10)
function Version-Python($exe) {
  try {
    $v = & $exe -c "import sys,struct;print('%d.%d %d' % (sys.version_info[0], sys.version_info[1], struct.calcsize('P')*8))" 2>$null
    if ($LASTEXITCODE -eq 0 -and $v -match '^(3\.\d+) 64$') { return $matches[1] }
  } catch {}
  return $null
}
function Trouver-Python {
  $cands = @{}
  if (Commande "py") {
    foreach ($l in (& py -0p 2>$null)) {
      if ($l -match '-V:(3\.1[0-3])\s+\*?\s*(\S.*python\.exe)\s*$') { if (-not $cands[$matches[1]]) { $cands[$matches[1]] = $matches[2].Trim() } }
    }
  }
  foreach ($nom in @("python", "python3")) {
    $c = Get-Command $nom -ErrorAction SilentlyContinue
    if ($c -and $c.Source -notmatch "WindowsApps") { $v = Version-Python $c.Source; if ($v -and -not $cands[$v]) { $cands[$v] = $c.Source } }
  }
  $ordre = @("3.12", "3.13", "3.11", "3.10")
  if ($VersionPython) { $ordre = @($VersionPython) }
  foreach ($v in $ordre) { if ($cands[$v] -and (Version-Python $cands[$v]) -eq $v) { return @($v, $cands[$v]) } }
  return $null
}
$Py = Trouver-Python
$FfmpegPortable = Join-Path $Outils "ffmpeg\bin"
if (Test-Path (Join-Path $FfmpegPortable "ffmpeg.exe")) { $env:Path = "$FfmpegPortable;$env:Path" }
$Ffmpeg = (Commande "ffmpeg") -and (Commande "ffprobe")
$Git = Commande "git"
$Winget = Commande "winget"

Write-Host ("  Processeur      : {0} ({1} fils)" -f $Cpu.Name.Trim(), $Cpu.NumberOfLogicalProcessors)
Write-Host ("  Mémoire vive    : {0} Go{1}" -f $RamGo, $(if ($RamGo -lt 8) { "  (juste : fermez les autres logiciels pendant la voix et le rendu)" } else { "" }))
Write-Host ("  Carte graphique : {0}" -f ($Cartes -join " ; "))
Write-Host ("  Carte NVIDIA    : {0}" -f $(if ($Nvidia) { "oui, $NomNvidia ($VramGo Go) : Whisper rapide" } else { "non : tout tourne sur le processeur (Whisper plus lent)" }))
Write-Host ("  Place libre {0}: : {1} Go" -f $Lecteur, $LibreGo)
Write-Host ("  Python 64 bits  : {0}" -f $(if ($Py) { "$($Py[0]) ($($Py[1]))" } else { "ABSENT (3.10 à 3.13 requis)" }))
Write-Host ("  ffmpeg          : {0}" -f $(if ($Ffmpeg) { "présent" } else { "ABSENT" }))
Write-Host ("  Git             : {0}" -f $(if ($Git) { "présent" } else { "absent (Claude Code en a besoin sous Windows : winget install Git.Git)" }))
Journal "PC : RAM $RamGo Go ; cartes $($Cartes -join ' ; ') ; NVIDIA $Nvidia $NomNvidia $VramGo Go ; libre $LibreGo Go ; Python $($Py -join ' ') ; ffmpeg $Ffmpeg ; Git $Git"

# Python absent : proposer winget (installation pour l'utilisateur seul, sans toucher au PATH)
if (-not $Py) {
  if ($Winget -and (Oui "Python 3.12 manque. L'installer maintenant avec winget (≈ 100 Mo, pour vous seul) ? (o/n)" "o")) {
    Info "installation de Python 3.12 (winget)"
    & winget install -e --id Python.Python.3.12 --scope user --accept-source-agreements --accept-package-agreements `
      --override "/quiet InstallAllUsers=0 PrependPath=0 Include_launcher=1 InstallLauncherAllUsers=0 Include_test=0" | Out-Null
    $p312 = Join-Path $env:LOCALAPPDATA "Programs\Python\Python312\python.exe"
    if (Test-Path $p312) { $Py = @("3.12", $p312) } else { $Py = Trouver-Python }
  }
  if (-not $Py) {
    Write-Host "  Python 64 bits (3.10 à 3.13) est nécessaire. Installez-le depuis https://www.python.org/downloads/windows/" -ForegroundColor Red
    Write-Host "  (« Windows installer (64-bit) », version 3.12), puis relancez ce script." -ForegroundColor Red
    exit 1
  }
  Ok "Python $($Py[0]) : $($Py[1])"
}
$PyBase = $Py[1]

# ------------------------------------------------------------------ 3. La question
$PoidsWhisper = if ($Nvidia) { 4.6 } else { 1.9 }
$DejaWhisper = Fait "whisper"
if ($DejaWhisper) { $Enregistrements = "oui" }
if (-not $Enregistrements) {
  Write-Host ""
  Write-Host "  La voix de synthèse (texte rédigé puis lu par l'ordinateur) fonctionne sans rien de plus." -ForegroundColor DarkGray
  Write-Host ("  Pour vos PROPRES enregistrements, il faut en plus la transcription Whisper : ≈ {0} Go{1}." -f $PoidsWhisper,
    $(if ($Nvidia) { " (avec votre carte NVIDIA : rapide)" } else { " (sans carte NVIDIA : sur le processeur, plusieurs fois plus lent)" })) -ForegroundColor DarkGray
  $Enregistrements = if (Oui "Voulez-vous travailler avec vos propres enregistrements (les nettoyer, les animer) ? (o/n)" "n") { "oui" } else { "non" }
}
$AvecWhisper = $Enregistrements -eq "oui"
$Besoin = 6 + $(if ($AvecWhisper) { $PoidsWhisper } else { 0 })
Write-Host ("  À installer : ≈ {0} Go dans {1} ; durée ≈ 20 à 40 min (surtout du téléchargement)." -f $Besoin, $Outils)
if ($LibreGo -lt $Besoin + 2) {
  Write-Host "  Place insuffisante sur ${Lecteur}: (il faut ≈ $($Besoin + 2) Go libres). Choisissez un autre dossier de base." -ForegroundColor Red
  exit 1
}
if (-not (Oui "Lancer l'installation ? (o/n)" "o")) { exit 0 }
Journal "Enregistrements : $Enregistrements ; Python $($Py -join ' ')"

# Environnement du processus (et de ses enfants) : tout sous outils\
$AncienHf = Ancien-Chemin "cache_modeles"
$AncienPip = if ($AncienHf) { Join-Path (Split-Path $AncienHf) "cache-pip" } else { $null }
$env:PIP_CACHE_DIR = if ($AncienPip -and (Test-Path $AncienPip)) { $AncienPip } else { Join-Path $Outils "cache-pip" }
$env:HF_HOME = if ($AncienHf) { $AncienHf } else { Join-Path $Outils "cache-hf" }
$env:PLAYWRIGHT_BROWSERS_PATH = Join-Path $Outils "navigateurs"
$env:HF_HUB_DISABLE_SYMLINKS_WARNING = "1"
$env:PYTHONUTF8 = "1"; $env:PYTHONIOENCODING = "utf-8"

$PyRendu = Join-Path $Outils "venv-rendu\Scripts\python.exe"
$ReutPocket = Ancien-Chemin "python_pocket"
$ReutParakeet = Ancien-Chemin "python_parakeet"
$ReutWhisper = Ancien-Chemin "python_asr"
$ReutPiper = Ancien-Chemin "voix_piper"
$ReutMfa = $null
if ($Ancien -and $Ancien.mfa -and $Ancien.mfa.env -and (Test-Path (Join-Path $Ancien.mfa.env "Scripts\mfa.exe"))) { $ReutMfa = $Ancien.mfa }
$PyPocket = if ($ReutPocket) { $ReutPocket } else { Join-Path $Outils "venv-pocket\Scripts\python.exe" }
$PyParakeet = if ($ReutParakeet) { $ReutParakeet } else { Join-Path $Outils "venv-parakeet\Scripts\python.exe" }
$PyWhisper = if ($ReutWhisper) { $ReutWhisper } else { Join-Path $Outils "venv-whisper\Scripts\python.exe" }
$VoixPiper = if ($ReutPiper) { $ReutPiper } else { Join-Path $Outils "voix-piper" }
if ($Ancien) { Journal "Réutilisation : HF $AncienHf ; pocket $ReutPocket ; parakeet $ReutParakeet ; whisper $ReutWhisper ; piper $ReutPiper ; mfa $($ReutMfa.env)" }
$Cible = Join-Path $Base ".claude\skills\capsule-video"
$Aide = Join-Path $Cible "installation\aide_installation.py"
$Chrono = @{}

function Venv($dossier) {
  $py = Join-Path $dossier "Scripts\python.exe"
  if (-not (Test-Path $py)) {
    if ((Executer $PyBase @("-m", "venv", $dossier)) -ne 0) { return $false }
    [void](Executer $py @("-m", "pip", "install", "-q", "--upgrade", "pip", "--disable-pip-version-check"))
  }
  return (Test-Path $py)
}

# ------------------------------------------------------------------ 4. Skill, CLAUDE.md, AGENTS.md
Titre 2 "Dossier de base" "Le skill (instructions et scripts de l'agent), le mode d'emploi du dossier et le dossier des capsules."
$sw = [Diagnostics.Stopwatch]::StartNew()
if ((Resolve-Path $Skill).Path -ne [IO.Path]::GetFullPath($Cible)) {
  # config.json et preferences.md ne sont jamais copiés : ils sont propres à chaque utilisateur
  & robocopy $Skill $Cible /E /XF config.json preferences.md *.bak.js /XD __pycache__ /NFL /NDL /NJH /NJS /NP | Out-Null
  if ($LASTEXITCODE -ge 8) { Write-Host "  Copie du skill impossible (voir $Log)." -ForegroundColor Red; exit 1 }
  Ok "skill copié (ou mis à jour) dans $Cible"
} else { Ok "skill déjà en place" }
$Pref = Join-Path $Cible "references\preferences.md"
if (-not (Test-Path $Pref)) { Copy-Item (Join-Path $Cible "installation\preferences-vierge.md") $Pref; Ok "préférences vierges : references\preferences.md" }
$Modele = Get-Content (Join-Path $Cible "installation\modele-CLAUDE.md") -Raw -Encoding UTF8
$Modele = $Modele.Replace("{{BASE}}", $Base).Replace("{{PYTHON}}", "outils/venv-rendu/Scripts/python.exe")
foreach ($f in @("CLAUDE.md", "AGENTS.md")) {
  [IO.File]::WriteAllText((Join-Path $Base $f), $Modele, (New-Object Text.UTF8Encoding $false))
}
Ok "CLAUDE.md et AGENTS.md écrits (mode d'emploi pour l'agent)"

# config.json : chemins sous outils\, valeurs selon le poste (references/outils-audio.md)
function Chemin($p) { return $p.Replace("\", "/") }
function Ecrire-Config {
  $v = [ordered]@{
    python_rendu = Chemin $PyRendu; python_tts = Chemin $PyRendu; python_voix = Chemin $PyRendu
    python_pocket = Chemin $PyPocket; python_parakeet = Chemin $PyParakeet
    python_asr = $(if ($AvecWhisper) { Chemin $PyWhisper } else { $null })
    asr_fidelite = "parakeet"
    arbitre_fidelite = $(if ($AvecWhisper -and $Nvidia) { "whisper" } else { $null })
    asr_enregistrements = $(if ($AvecWhisper) { "whisper" } else { "parakeet" })
    horodatage = "mfa"
    whisper_device = $(if ($Nvidia) { "auto" } else { "cpu" })
    modele_asr = $(if ($Nvidia -and $VramGo -ge 6) { "large-v3" } else { "medium" })
    modele_pocket = "french_24l"; voix_pocket_defaut = "estelle"; voix_clonees = @{}
    cache_modeles = Chemin $env:HF_HOME; navigateurs = Chemin $env:PLAYWRIGHT_BROWSERS_PATH
    voix_piper = Chemin $VoixPiper
    dossier_ffmpeg = $(if (Test-Path (Join-Path $FfmpegPortable "ffmpeg.exe")) { Chemin $FfmpegPortable } else { $null })
    dossier_capsules = Chemin (Join-Path $Base "capsules")
    qualite_rendu = "envoi"; premier_usage_fait = $false
    _note = "Écrit par installation/installer.ps1. PERSONNEL : voix_clonees (jamais partagé). Clés audio : references/outils-audio.md. premier_usage_fait=false : l'agent lit references/first_check.md."
  }
  if ($ReutMfa) { $v["mfa"] = $ReutMfa }
  $tmp = Join-Path $Outils "config-valeurs.json"
  [IO.File]::WriteAllText($tmp, ($v | ConvertTo-Json -Depth 4), (New-Object Text.UTF8Encoding $false))
  $py = if (Test-Path $PyRendu) { $PyRendu } else { $PyBase }
  if ((Executer $py @($Aide, "config", "--skill", $Cible, "--valeurs", $tmp)) -ne 0) { Probleme "écriture de config.json" "voir $Log" }
}
Ecrire-Config
Ok "config.json écrit ($(Duree $sw))"
$Chrono["Dossier de base"] = Duree $sw

# ------------------------------------------------------------------ 5. ffmpeg
if (-not $Ffmpeg) {
  Titre 3 "ffmpeg" "Assemble les images et la voix en vidéo."
  $sw = [Diagnostics.Stopwatch]::StartNew()
  if (Oui "Télécharger ffmpeg portable dans outils\ffmpeg (≈ 100 Mo, sans rien modifier d'autre) ? (o/n)" "o") {
    $zip = Join-Path $Outils "ffmpeg.zip"
    $ok = (Telecharger "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip" $zip) -or
          (Telecharger "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip" $zip)
    if ($ok) {
      $tmpz = Join-Path $Outils "ffmpeg-tmp"
      Expand-Archive $zip $tmpz -Force
      $bin = Get-ChildItem $tmpz -Recurse -Filter ffmpeg.exe | Select-Object -First 1
      New-Item -ItemType Directory -Force -Path $FfmpegPortable | Out-Null
      Copy-Item (Join-Path $bin.DirectoryName "*.exe") $FfmpegPortable
      Remove-Item $tmpz, $zip -Recurse -Force
      $env:Path = "$FfmpegPortable;$env:Path"
      Ok "ffmpeg portable : $FfmpegPortable ($(Duree $sw))"
    } else { Probleme "ffmpeg" "téléchargement impossible : installez-le avec « winget install Gyan.FFmpeg », puis relancez" }
  } else { Probleme "ffmpeg" "installez-le (winget install Gyan.FFmpeg), puis relancez ce script" }
  $Chrono["ffmpeg"] = Duree $sw
}

# ------------------------------------------------------------------ 6. Rendu + voix de secours
Titre 4 "Rendu des vidéos" "Python dédié + Chromium (navigateur invisible qui dessine l'animation) + voix de secours Piper. ≈ 0,8 Go."
$sw = [Diagnostics.Stopwatch]::StartNew()
if (Fait "rendu") { Ok "déjà installé" } else {
  Info "environnement Python et bibliothèques (≈ 2 min)"
  if ((Venv (Join-Path $Outils "venv-rendu")) -and (Pip $PyRendu @("playwright", "psutil", "numpy", "scipy", "num2words", "piper-tts"))) {
    Info "Chromium (≈ 1 min)"
    if ((Executer $PyRendu @("-m", "playwright", "install", "--only-shell", "chromium")) -eq 0) { Marquer "rendu"; Ok "rendu prêt" }
    else { Probleme "Chromium" "relancez l'installeur ; derrière un proxy : voir $Log" }
  } else { Probleme "environnement de rendu" "relancez l'installeur ; détail dans $Log" }
}
if ($ReutPiper) { A-Sec "voix Piper" "téléchargement de fr_FR-{siwis,tom,upmc}-medium.onnx dans outils\voix-piper" }
elseif (-not (Fait "piper")) {
  New-Item -ItemType Directory -Force -Path $VoixPiper | Out-Null
  $tout = $true
  foreach ($v in @("siwis", "tom", "upmc")) {
    foreach ($ext in @("onnx", "onnx.json")) {
      $dest = Join-Path $VoixPiper "fr_FR-$v-medium.$ext"
      if (-not (Test-Path $dest)) {
        if (-not (Telecharger "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/$v/medium/fr_FR-$v-medium.$ext" $dest)) { $tout = $false }
      }
    }
  }
  if ($tout) { Marquer "piper"; Ok "voix de secours Piper (siwis, tom, upmc)" } else { Alerte "voix Piper incomplètes (secours seulement : sans gravité)" }
}
$Chrono["Rendu + Piper"] = Duree $sw
Ecrire-Config

# ------------------------------------------------------------------ 7. Pocket TTS
Titre 5 "Voix de synthèse Pocket TTS" "La voix par défaut (française, naturelle), sur processeur. ≈ 1,8 Go (PyTorch processeur + modèle)."
$sw = [Diagnostics.Stopwatch]::StartNew()
if ($ReutPocket) { A-Sec "Pocket TTS" "venv-pocket + pip install pocket-tts num2words --extra-index-url https://download.pytorch.org/whl/cpu + aide_installation.py precharger pocket" }
elseif (Fait "pocket") { Ok "déjà installé" } else {
  Info "PyTorch processeur et Pocket TTS (≈ 3 min)"
  if ((Venv (Join-Path $Outils "venv-pocket")) -and (Pip $PyPocket @("pocket-tts", "num2words", "--extra-index-url", "https://download.pytorch.org/whl/cpu"))) {
    Info "modèle french_24l et voix estelle (≈ 2 min la première fois)"
    if ((Executer $PyPocket @("-X", "utf8", $Aide, "precharger", "pocket")) -eq 0) { Marquer "pocket"; Ok "Pocket TTS prêt" }
    else { Probleme "modèle Pocket TTS" "relancez l'installeur (téléchargement interrompu ?) ; détail dans $Log" }
  } else { Probleme "Pocket TTS" "relancez l'installeur ; détail dans $Log. Secours en attendant : voix Piper" }
}
$Chrono["Pocket TTS"] = Duree $sw

# ------------------------------------------------------------------ 8. Parakeet
Titre 6 "Contrôle de la voix : Parakeet" "Réécoute chaque phrase générée pour vérifier qu'aucun mot n'a été sauté. ≈ 0,8 Go."
$sw = [Diagnostics.Stopwatch]::StartNew()
if ($ReutParakeet) { A-Sec "Parakeet" "venv-parakeet + pip install onnx-asr[cpu,hub] soundfile num2words + aide_installation.py precharger parakeet" }
elseif (Fait "parakeet") { Ok "déjà installé" } else {
  if ((Venv (Join-Path $Outils "venv-parakeet")) -and (Pip $PyParakeet @("onnx-asr[cpu,hub]", "soundfile", "num2words"))) {
    Info "modèle Parakeet (640 Mo, ≈ 5 min la première fois)"
    if ((Executer $PyParakeet @("-X", "utf8", $Aide, "precharger", "parakeet")) -eq 0) { Marquer "parakeet"; Ok "Parakeet prêt" }
    else { Probleme "modèle Parakeet" "relancez l'installeur ; détail dans $Log" }
  } else { Probleme "Parakeet" "relancez l'installeur ; détail dans $Log" }
}
$Chrono["Parakeet"] = Duree $sw

# ------------------------------------------------------------------ 9. MFA
Titre 7 "Horodatage au mot : MFA" "Pose chaque mot du texte sur la voix (à 20 ms près) pour caler les animations. ≈ 2,5 Go, ≈ 7 min."
$sw = [Diagnostics.Stopwatch]::StartNew()
$RacineMfa = Join-Path $Outils "mfa"
$CmdMfa = @((Join-Path $Cible "scripts\installer_mfa.py"), "--racine", $RacineMfa, "--config", (Join-Path $Cible "config.json"), "--maj-config")
if ($ReutMfa) { A-Sec "MFA" ("$PyRendu " + ($CmdMfa -join " ")) }
elseif ((Executer $PyRendu @((Join-Path $Cible "scripts\installer_mfa.py"), "--racine", $RacineMfa, "--config", (Join-Path $Cible "config.json"), "--maj-config")) -eq 0) {
  Ok "MFA prêt ($(Duree $sw))"
} else { Probleme "MFA" "relancez l'installeur ; si l'erreur parle de SSL : voir $Log. Sans MFA, l'horodatage passe par Whisper (si installé)" }
$Chrono["MFA"] = Duree $sw

# ------------------------------------------------------------------ 10. Whisper (facultatif)
if ($AvecWhisper) {
  $ModeleW = if ($Nvidia -and $VramGo -ge 6) { "large-v3" } else { "medium" }
  Titre 8 "Transcription de vos enregistrements : Whisper" ("Modèle $ModeleW" + $(if ($Nvidia) { " sur la carte NVIDIA" } else { " sur le processeur (plus lent)" }) + (", ≈ {0} Go." -f $PoidsWhisper))
  $sw = [Diagnostics.Stopwatch]::StartNew()
  $paq = @("faster-whisper", "num2words")
  if ($Nvidia) { $paq += @("nvidia-cublas-cu12", "nvidia-cudnn-cu12==9.*") }
  if ($ReutWhisper) { A-Sec "Whisper" ("venv-whisper + pip install " + ($paq -join " ") + " + aide_installation.py precharger whisper $ModeleW"); Marquer "whisper" }
  elseif (Fait "whisper") { Ok "déjà installé" } else {
    $paq = @("faster-whisper", "num2words")
    if ($Nvidia) { $paq += @("nvidia-cublas-cu12", "nvidia-cudnn-cu12==9.*") }
    if ((Venv (Join-Path $Outils "venv-whisper")) -and (Pip $PyWhisper $paq)) {
      Info "modèle $ModeleW (≈ 5 à 10 min la première fois)"
      if ((Executer $PyWhisper @("-X", "utf8", $Aide, "precharger", "whisper", $ModeleW)) -eq 0) { Marquer "whisper"; Ok "Whisper prêt" }
      else { Probleme "modèle Whisper" "relancez l'installeur ; détail dans $Log" }
    } else { Probleme "Whisper" "relancez l'installeur ; détail dans $Log" }
  }
  $Chrono["Whisper"] = Duree $sw
}
Ecrire-Config

# ------------------------------------------------------------------ 11. Essai de chaque brique
Titre 9 "Essai" "Une phrase dite par Pocket, contrôlée par Parakeet, horodatée par MFA, puis une image rendue (≈ 2 min)."
$sw = [Diagnostics.Stopwatch]::StartNew()
$Bilan = Join-Path $Outils "bilan-installation.json"
if (Test-Path $PyRendu) {
  $out = Join-Path $Outils "essai-sortie.txt"
  $p = Start-Process -FilePath $PyRendu -ArgumentList ('"' + $Aide + '" essai --skill "' + $Cible + '" --travail "' + (Join-Path $Outils "essai-installation") + '" --bilan "' + $Bilan + '"') `
         -NoNewWindow -Wait -PassThru -RedirectStandardOutput $out -RedirectStandardError "$out.err"
  Get-Content $out -Encoding UTF8 | ForEach-Object { Write-Host $_ }
  Get-Content $out, "$out.err" -Raw -Encoding UTF8 -ErrorAction SilentlyContinue | ForEach-Object { Ajouter-Journal $_ }
  Remove-Item $out, "$out.err" -Force -ErrorAction SilentlyContinue
  if ($p.ExitCode -ne 0) { Alerte "au moins une brique ne répond pas : voir les solutions ci-dessus" }
} else { Probleme "essai" "environnement de rendu absent : relancez l'installeur" }
$Chrono["Essai"] = Duree $sw

# ------------------------------------------------------------------ 12. Bilan
Titre 10 "Bilan" ""
$PoidsLignes = @()
$dossiers = @("venv-rendu", "navigateurs", "voix-piper", "venv-pocket", "venv-parakeet", "mfa", "venv-whisper", "cache-hf", "ffmpeg") |
  Where-Object { Test-Path (Join-Path $Outils $_) }
$poids = & $PyRendu $Aide poids @($dossiers | ForEach-Object { Join-Path $Outils $_ }) 2>$null
$total = 0
for ($i = 0; $i -lt $dossiers.Count; $i++) {
  $g = [double]::Parse(@($poids)[$i], [Globalization.CultureInfo]::InvariantCulture); $total += $g
  Write-Host ("  {0,-15} {1,6:N2} Go" -f $dossiers[$i], $g)
}
Write-Host ("  {0,-15} {1,6:N2} Go   (cache pip non compté : supprimable, outils\cache-pip)" -f "TOTAL", $total)
Write-Host ""
foreach ($k in $Chrono.Keys) { Write-Host ("  {0,-16} {1}" -f $k, $Chrono[$k]) -ForegroundColor DarkGray }
Write-Host ("  Durée totale : {0:N0} min" -f ((Get-Date) - $Debut).TotalMinutes)
Journal ("Poids total {0:N2} Go ; durée {1:N1} min" -f $total, ((Get-Date) - $Debut).TotalMinutes)

if ($Problemes.Count -gt 0) {
  Write-Host ""
  Write-Host "  À corriger :" -ForegroundColor Red
  foreach ($p in $Problemes) { Write-Host "   - $($p.Brique) : $($p.Solution)" -ForegroundColor Red }
}
Write-Host ""
Write-Host "Installation terminée. Pour votre première capsule :" -ForegroundColor Yellow
Write-Host "  1. Ouvrez votre agent (Claude Code, Codex…) dans le dossier $Base"
Write-Host "     (PowerShell : cd $Base  puis  claude)"
Write-Host "  2. Dites : « Fais-moi une capsule vidéo de correction de l'exercice suivant : … »"
Write-Host "     La première fois, l'agent vous propose quelques questions sur vos goûts (facultatives)."
Write-Host "  Vos capsules arriveront dans $Base\capsules"
Write-Host ""
Write-Host "  Parler avec VOTRE voix (facultatif) : il faut un compte Hugging Face gratuit et accepter les conditions" -ForegroundColor DarkGray
Write-Host "  du modèle de clonage. Marche à suivre : .claude\skills\capsule-video\references\cloner-sa-voix.md" -ForegroundColor DarkGray
if (-not $AvecWhisper) {
  Write-Host "  Travailler plus tard avec vos enregistrements : relancez ce script et répondez « oui »." -ForegroundColor DarkGray
}
Write-Host "  Journal complet : $Log" -ForegroundColor DarkGray
if (-not $Silencieux) { Read-Host "Entrée pour fermer" | Out-Null }

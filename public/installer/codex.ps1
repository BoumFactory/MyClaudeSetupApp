# Installation de la configuration bfcours.dev (Claude Code / Codex) - Windows PowerShell
#
#   irm https://bfcours.dev/installer/claude.ps1 | iex     -> ./.claude  + CLAUDE.md
#   irm https://bfcours.dev/installer/codex.ps1  | iex     -> ./.agents  + AGENTS.md
#
# Version allegee (sans les skills les plus lourds) : $env:BFCOURS_LEGER = "1" avant la commande.
#
# Fichiers jumeaux : claude.ps1 et codex.ps1 sont identiques, sauf la ligne "$Agent = ...".
# Le fichier est volontairement en ASCII pur : "irm | iex" casse sur un BOM UTF-8, et
# PowerShell 5.1 lit un fichier UTF-8 sans BOM comme de l'ANSI. Les accents des messages
# sont donc construits a l'execution ($ea = e accent aigu, etc.).
#
# Rien de destructif : un dossier existant est sauvegarde (copie) avant la fusion, jamais supprime.

& {
  $Agent = 'codex'

  $ErrorActionPreference = 'Stop'
  $ea = [char]0xE9; $eg = [char]0xE8; $ec = [char]0xEA; $ag = [char]0xE0; $Emaj = [char]0xC9

  $Depot = 'https://github.com/BoumFactory/MyClaudeSetupApp.git'
  $Branche = 'main'
  $Source = 'public/download/Claude-Code-Setup'
  $Lourds = @('h5p-branching-scenario', 'programmes-officiels')
  $TutoGit = 'https://bfcours.dev/claude-code/tutorials/git-install'
  # Lance par -File : $PSCommandPath est renseigne. Lance par "irm | iex" : il est vide.
  $ModeFichier = [bool]$PSCommandPath

  if ($Agent -eq 'codex') {
    $Outil = 'Codex'; $NomCible = '.agents'; $FichierRacine = 'AGENTS.md'
  } else {
    $Outil = 'Claude Code'; $NomCible = '.claude'; $FichierRacine = 'CLAUDE.md'
  }
  $Leger = ($env:BFCOURS_LEGER -eq '1')

  function Info([string]$m) { Write-Host $m }
  function Ok([string]$m) { Write-Host "  [ok] $m" -ForegroundColor Green }
  function Attention([string]$m) { Write-Host "  [!] $m" -ForegroundColor Yellow }

  # Echec prevu : message deja clair, on interrompt sans trace d'erreur PowerShell.
  function Echec([string]$m) { throw [System.OperationCanceledException]::new($m) }

  # Git ecrit sa progression sur stderr : on neutralise ErrorActionPreference le temps de l'appel.
  function Git-Run {
    $EAP = $ErrorActionPreference; $ErrorActionPreference = 'Continue'
    try { & git @args 2>&1 | ForEach-Object { "$_" } | Where-Object { $_ -ne '' } | ForEach-Object { Write-Host "    $_" -ForegroundColor DarkGray } }
    finally { $ErrorActionPreference = $EAP }
    return $LASTEXITCODE
  }

  function Taille-Mo([string]$chemin) {
    $s = (Get-ChildItem -LiteralPath $chemin -Recurse -Force -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    if (-not $s) { $s = 0 }
    return [math]::Round($s / 1MB, 1)
  }

  $Projet = (Get-Location).ProviderPath
  $Cible = Join-Path $Projet $NomCible
  $Debut = Get-Date
  $Sauvegarde = $null
  $CopieCommencee = $false
  $Reussi = $false
  $Tmp = Join-Path ([IO.Path]::GetTempPath()) ('bfcours-config-' + [guid]::NewGuid().ToString('N').Substring(0, 8))

  Info ""
  Info "Installation de la configuration bfcours.dev pour $Outil"
  Info "Projet : $Projet"
  Info "Destination : $Cible"
  if ($Leger) { Info "Version all${ea}g${ea}e : sans les skills $($Lourds -join ', ')." }
  Info ""

  try {
    # 1. Garde-fous
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
      Echec "Git n'est pas install${ea}. Installez-le d'abord : $TutoGit"
    }
    if ($Projet -eq [Environment]::GetFolderPath('UserProfile')) {
      Attention "Vous ${ea}tes dans votre dossier personnel : la configuration servira ${ag} tous vos projets."
    }

    # 2. Telechargement : clone partiel, seuls les fichiers de la configuration sont recuperes
    Info "1/4 T${ea}l${ea}chargement de la configuration (Git)..."
    $code = Git-Run clone --quiet --depth 1 --filter=blob:none --no-checkout --branch $Branche -c core.longpaths=true $Depot $Tmp
    if ($code -ne 0) { Echec "le t${ea}l${ea}chargement a ${ea}chou${ea} (connexion internet ? proxy ?)." }

    # Un "/" interne suffit a ancrer le motif a la racine du depot (regles gitignore).
    $motifs = @("$Source/")
    if ($Leger) { foreach ($l in $Lourds) { $motifs += "!$Source/claude-setup/skills/$l/" } }
    $code = Git-Run -C $Tmp sparse-checkout set --no-cone @motifs
    if ($code -ne 0) { Echec "votre version de Git est trop ancienne (2.35 au minimum). Mettez-la ${ag} jour : $TutoGit" }
    $code = Git-Run -C $Tmp checkout --quiet $Branche
    if ($code -ne 0) { Echec "l'extraction des fichiers a ${ea}chou${ea}." }

    $Src = Join-Path $Tmp ($Source -replace '/', '\')
    $SrcSetup = Join-Path $Src 'claude-setup'
    if (-not (Test-Path -LiteralPath (Join-Path $SrcSetup 'skills'))) { Echec "la configuration t${ea}l${ea}charg${ea}e est incompl${eg}te." }
    $Volume = Taille-Mo (Join-Path $Tmp '.git')
    Ok "configuration r${ea}cup${ea}r${ea}e ($Volume Mo t${ea}l${ea}charg${ea}s)"

    # 3. Sauvegarde du dossier existant (copie : l'original reste en place)
    Info "2/4 Sauvegarde..."
    if (Test-Path -LiteralPath $Cible) {
      $nom = "$NomCible.sauvegarde-" + (Get-Date -Format 'yyyyMMdd-HHmm')
      $Sauvegarde = Join-Path $Projet $nom
      $i = 2
      while (Test-Path -LiteralPath $Sauvegarde) { $Sauvegarde = Join-Path $Projet "$nom-$i"; $i++ }
      Copy-Item -LiteralPath $Cible -Destination $Sauvegarde -Recurse -Force
      Ok "dossier $NomCible existant sauvegard${ea} dans $(Split-Path $Sauvegarde -Leaf)"
    } else {
      Ok "aucun dossier $NomCible existant : rien ${ag} sauvegarder"
    }

    # 4. Copie par fusion : les fichiers de la configuration remplacent ceux de meme nom,
    #    les autres fichiers du dossier sont conserves.
    Info "3/4 Copie des fichiers dans $NomCible..."
    $CopieCommencee = $true
    if (-not (Test-Path -LiteralPath $Cible)) { New-Item -ItemType Directory -Path $Cible | Out-Null }
    Get-ChildItem -LiteralPath $SrcSetup -Force | Copy-Item -Destination $Cible -Recurse -Force
    $nbSkills = @(Get-ChildItem -LiteralPath (Join-Path $Cible 'skills') -Directory).Count
    Ok "$nbSkills skills dans $NomCible\skills"

    # 5. Fichier d'instructions a la racine du projet (seulement s'il n'existe pas)
    Info "4/4 Fichier $FichierRacine..."
    $Racine = Join-Path $Projet $FichierRacine
    if (Test-Path -LiteralPath $Racine) {
      Ok "$FichierRacine existe d${ea}j${ag} : il n'est pas modifi${ea}"
    } else {
      $texte = [IO.File]::ReadAllText((Join-Path $Src 'CLAUDE-simple.md'), [Text.Encoding]::UTF8)
      if ($Agent -eq 'codex') {
        $note = "> Configuration install${ea}e dans ``.agents/``. Les chemins ``.claude/...`` cit${ea}s dans les skills et ci-dessous d${ea}signent ``.agents/...``.`n`n"
        $texte = $note + $texte
      }
      [IO.File]::WriteAllText($Racine, $texte, (New-Object Text.UTF8Encoding $false))
      Ok "$FichierRacine cr${ea}${ea} ${ag} partir de CLAUDE-simple.md"
    }
    if ($Agent -ne 'codex') {
      # Exemple seulement : ses permissions sont larges, l'utilisateur decide de l'activer.
      Copy-Item -LiteralPath (Join-Path $Src 'settings.json') -Destination (Join-Path $Cible 'settings.exemple.json') -Force
    }

    $Duree = [math]::Round(((Get-Date) - $Debut).TotalSeconds)
    Info ""
    Write-Host "Installation termin${ea}e en $Duree s." -ForegroundColor Green
    Info ""
    Info "${Emaj}tapes suivantes (facultatives, selon les skills utilis${ea}s) :"
    Info "  - Python 3 et Node.js servent ${ag} plusieurs skills."
    Info "  - Serveurs MCP : python -m pip install -r $NomCible\mcp_servers\requirements.txt"
    Info "  - Skill latex-visual-review : python -m pip install -r $NomCible\skills\latex-visual-review\scripts\requirements.txt"
    if ($Agent -ne 'codex') {
      Info "  - $NomCible\settings.exemple.json : exemple de r${ea}glages (sons, permissions larges). Non activ${ea} ; ${ag} relire avant de le renommer en settings.json."
    } else {
      Info "  - Codex lit les skills dans .agents\skills. Les chemins .claude\... cit${ea}s dans les skills d${ea}signent .agents\..."
    }
    Info "  - Pour mettre ${ag} jour : relancez la m${ec}me commande."
    if ($Sauvegarde) { Info "  - Sauvegarde : $(Split-Path $Sauvegarde -Leaf) (supprimez-la quand tout fonctionne)." }
    Info ""
    $Reussi = $true
  }
  catch {
    $m = $_.Exception.Message
    if (-not ($_.Exception -is [System.OperationCanceledException])) { $m = "erreur inattendue : $m" }
    Write-Host ""
    Write-Host "ERREUR : $m" -ForegroundColor Red
    if (-not $CopieCommencee) {
      Write-Host "Rien n'a ${ea}t${ea} modifi${ea} dans votre projet." -ForegroundColor Red
    } elseif ($Sauvegarde) {
      Write-Host "Copie incompl${eg}te. Votre ancien dossier est intact dans $(Split-Path $Sauvegarde -Leaf)." -ForegroundColor Red
    } else {
      Write-Host "Copie incompl${eg}te : relancez la commande." -ForegroundColor Red
    }
  }
  finally {
    if (Test-Path -LiteralPath $Tmp) { Remove-Item -LiteralPath $Tmp -Recurse -Force -ErrorAction SilentlyContinue }
  }

  if ($Reussi) {
    $global:LASTEXITCODE = 0
  } else {
    $global:LASTEXITCODE = 1
    # En mode "irm | iex", exit fermerait la fenetre de l'utilisateur : on se contente du code.
    if ($ModeFichier) { exit 1 }
  }
}

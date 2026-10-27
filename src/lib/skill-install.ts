/**
 * Commandes d'installation d'un pack de skill (archive téléchargée via le panier).
 *
 * L'archive d'un pack de skill (`claude-setup-<id>.zip`) contient uniquement un dossier
 * `.claude/` : `skills/`, `mcp_servers/`, `datas/` et un LISEZMOI. Les scripts des skills
 * retrouvent `mcp_servers/` et `datas/` par chemin relatif (`../../../mcp_servers`), il faut
 * donc copier le contenu de `.claude/` d'un seul bloc, quel que soit le dossier d'arrivée.
 *
 * Emplacements des skills :
 * - Claude Code : `.claude/skills/` (projet) ou `~/.claude/skills/` (global).
 * - Codex : `.agents/skills/` (projet) ou `~/.agents/skills/` (global), d'après
 *   https://learn.chatgpt.com/docs/build-skills (ex-developers.openai.com/codex/skills).
 *
 * Ce module ne dépend ni de React ni de Node : il sert à la page web ET au LISEZMOI du ZIP.
 */

export interface InstallVariant {
  id: 'claude-projet' | 'claude-global' | 'codex-projet' | 'codex-global'
  outil: 'Claude Code' | 'Codex'
  portee: 'projet' | 'global'
  recommande: boolean
  /** Dossier où arrivent les skills */
  dossier: string
  /** Phrase courte affichée sous le titre */
  explication: string
  windows: string
  unix: string
}

export function archiveName(packId: string): string {
  return `claude-setup-${packId}.zip`
}

export function skillPackInstallVariants(packId: string): InstallVariant[] {
  const zip = archiveName(packId)
  const winZip = `"$HOME\\Downloads\\${zip}"`
  const unixZip = `~/Downloads/${zip}`
  const tmpWin = `"$env:TEMP\\${packId}"`
  const tmpUnix = `/tmp/${packId}`

  return [
    {
      id: 'claude-projet',
      outil: 'Claude Code',
      portee: 'projet',
      recommande: true,
      dossier: '.claude/skills/',
      explication: 'Les skills ne servent que dans ce projet. À lancer depuis le dossier du projet.',
      windows: `Expand-Archive ${winZip} -DestinationPath . -Force`,
      unix: `unzip -o ${unixZip} -d .`,
    },
    {
      id: 'claude-global',
      outil: 'Claude Code',
      portee: 'global',
      recommande: false,
      dossier: '~/.claude/skills/',
      explication: 'Déconseillé : les skills se chargent dans tous vos projets, même ceux qui n\'en ont pas l\'usage.',
      windows: `Expand-Archive ${winZip} -DestinationPath $HOME -Force`,
      unix: `unzip -o ${unixZip} -d ~`,
    },
    {
      id: 'codex-projet',
      outil: 'Codex',
      portee: 'projet',
      recommande: true,
      dossier: '.agents/skills/',
      explication: 'Codex lit les skills du projet dans .agents/skills/. À lancer depuis le dossier du projet.',
      windows: [
        `Expand-Archive ${winZip} -DestinationPath ${tmpWin} -Force`,
        `New-Item -ItemType Directory -Force .agents | Out-Null`,
        `Copy-Item "$env:TEMP\\${packId}\\.claude\\*" .agents -Recurse -Force`,
      ].join('\n'),
      unix: [
        `unzip -o ${unixZip} -d ${tmpUnix}`,
        `mkdir -p .agents && cp -R ${tmpUnix}/.claude/. .agents/`,
      ].join('\n'),
    },
    {
      id: 'codex-global',
      outil: 'Codex',
      portee: 'global',
      recommande: false,
      dossier: '~/.agents/skills/',
      explication: 'Déconseillé, pour la même raison que l\'installation globale de Claude Code.',
      windows: [
        `Expand-Archive ${winZip} -DestinationPath ${tmpWin} -Force`,
        `New-Item -ItemType Directory -Force "$HOME\\.agents" | Out-Null`,
        `Copy-Item "$env:TEMP\\${packId}\\.claude\\*" "$HOME\\.agents" -Recurse -Force`,
      ].join('\n'),
      unix: [
        `unzip -o ${unixZip} -d ${tmpUnix}`,
        `mkdir -p ~/.agents && cp -R ${tmpUnix}/.claude/. ~/.agents/`,
      ].join('\n'),
    },
  ]
}

export function pythonDepsCommands(deps: string): { windows: string; unix: string } {
  return {
    windows: `python -m pip install ${deps}`,
    unix: `python3 -m pip install ${deps}`,
  }
}

/** Texte Markdown d'installation, glissé dans le LISEZMOI de l'archive */
export function installMarkdown(packId: string, pythonDeps?: string): string {
  const lignes: string[] = []
  lignes.push('## Installation')
  lignes.push('')
  lignes.push('Les commandes supposent que l\'archive est dans le dossier Téléchargements ; adaptez le chemin sinon.')
  lignes.push('')
  for (const v of skillPackInstallVariants(packId)) {
    const titre = `### ${v.outil}, ${v.portee === 'projet' ? 'dans le projet' : 'global'}${v.recommande ? ' (recommandé)' : ' (déconseillé)'}`
    lignes.push(titre, '', `Les skills arrivent dans \`${v.dossier}\`. ${v.explication}`, '')
    lignes.push('Windows (PowerShell) :', '', '```powershell', v.windows, '```', '')
    lignes.push('macOS / Linux :', '', '```bash', v.unix, '```', '')
  }
  if (pythonDeps) {
    const deps = pythonDepsCommands(pythonDeps)
    lignes.push('### Modules Python', '', '```powershell', deps.windows, '```', '', '```bash', deps.unix, '```', '')
  }
  lignes.push('### Codex : chemins cités dans les skills', '')
  lignes.push('Les fiches des skills citent leurs scripts sous `.claude/skills/…`. Avec Codex, précisez-lui (ou écrivez dans votre `AGENTS.md`) : « les skills sont installés dans `.agents/skills/` ».')
  lignes.push('')
  return lignes.join('\n')
}

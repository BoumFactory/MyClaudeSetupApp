import { SHARED_FOLDERS } from '@/data/ai-packages'
import type { AIPackage, PackageId } from '@/data/ai-packages'
import { installMarkdown } from '@/lib/skill-install'
import { SKILL_PAGES } from '@/data/skill-pages'
import { addPresentationToZip } from '@/lib/presentation-zip'
import JSZip from 'jszip'
import fs from 'fs/promises'
import path from 'path'

/**
 * Construction des archives des bundles et des packs de skill (côté serveur uniquement).
 * Utilisée par /api/download-package ; isolée ici pour pouvoir vérifier le contenu
 * d'un pack sans lancer le serveur (un route.ts ne peut exporter que GET, POST…).
 */

const SETUP_BASE = path.join(process.cwd(), 'public', 'download', 'Claude-Code-Setup')
const CLAUDE_SETUP = path.join(SETUP_BASE, 'claude-setup')
const PRESENTATION_DIR = '.claude/diaporama'

/** Slug du diaporama (public/render/Reveals/<slug>.html) de la page de skill liée à ce pack */
function presentationSlug(packId: string): string | undefined {
  return Object.entries(SKILL_PAGES).find(([, page]) => page.packId === packId)?.[0]
}

export async function buildPackageZip(pkg: AIPackage<PackageId>): Promise<JSZip> {
  const zip = new JSZip()

  // Pack d'un skill : seulement .claude/ (skills, mcp_servers, datas) + LISEZMOI dans .claude/,
  // pour pouvoir décompresser l'archive telle quelle dans un projet existant.
  if (pkg.skillOnly) {
    await addSkills(zip, pkg.skills)
    await addSelectivePaths(zip, path.join(CLAUDE_SETUP, 'mcp_servers'), '.claude/mcp_servers', pkg.mcpServerPaths ?? [])
    await addSelectivePaths(zip, path.join(CLAUDE_SETUP, 'datas'), '.claude/datas', pkg.dataPaths)
    // Commandes slash propres au skill (fichiers listés un à un, sans l'ARCHITECTURE.md de tout le dossier)
    for (const cmd of pkg.commandPaths) {
      const cmdPath = path.join(CLAUDE_SETUP, 'commands', cmd)
      if (await exists(cmdPath)) zip.file(`.claude/commands/${cmd}`, await fs.readFile(cmdPath))
    }
    // Le diaporama de présentation du skill voyage avec son pack : .claude/diaporama/<slug>.html
    // (+ assets/ reveal.js), à ouvrir directement dans le navigateur.
    const slug = presentationSlug(pkg.id)
    const withPresentation = slug
      ? await addPresentationToZip(zip, `${slug}.html`, PRESENTATION_DIR)
      : false
    zip.file(`.claude/LISEZMOI-${pkg.id}.md`, generateSkillPackReadme(pkg, withPresentation ? `${slug}.html` : undefined))
    return zip
  }

  // 1. Add shared folders (hooks, scripts, base-scripts, assets)
  for (const folder of SHARED_FOLDERS) {
    const folderPath = path.join(CLAUDE_SETUP, folder)
    await addDirectoryToZip(zip, folderPath, `.claude/${folder}`)
  }

  // 2. Add skills
  await addSkills(zip, pkg.skills)

  // 3. Add agents
  await addSelectivePaths(zip, path.join(CLAUDE_SETUP, 'agents'), '.claude/agents', pkg.agentPaths)

  // 4. Add commands
  await addSelectivePaths(zip, path.join(CLAUDE_SETUP, 'commands'), '.claude/commands', pkg.commandPaths)

  // 5. Add datas
  await addSelectivePaths(zip, path.join(CLAUDE_SETUP, 'datas'), '.claude/datas', pkg.dataPaths)

  // 6. Add agents-data
  await addSelectivePaths(zip, path.join(CLAUDE_SETUP, 'agents-data'), '.claude/agents-data', pkg.agentsDataPaths)

  // 7. Add mcp_servers (serveurs Python importés par les scripts des skills LaTeX)
  await addSelectivePaths(zip, path.join(CLAUDE_SETUP, 'mcp_servers'), '.claude/mcp_servers', pkg.mcpServerPaths ?? [])

  // 8. Add CLAUDE.md at root
  if (pkg.claudeMdFile) {
    const claudeMdPath = path.join(SETUP_BASE, pkg.claudeMdFile)
    if (await exists(claudeMdPath)) {
      const content = await fs.readFile(claudeMdPath)
      zip.file('CLAUDE.md', content)
    }
  }

  // 9. Add settings.json at root
  const settingsPath = path.join(SETUP_BASE, 'settings.json')
  if (await exists(settingsPath)) {
    const content = await fs.readFile(settingsPath)
    zip.file('settings.json', content)
  }

  // 10. Add README
  zip.file('README.md', generateReadme(pkg))

  return zip
}

async function addSkills(zip: JSZip, skills: string[]): Promise<void> {
  for (const skill of skills) {
    const skillPath = path.join(CLAUDE_SETUP, 'skills', skill)
    if (await exists(skillPath)) {
      await addDirectoryToZip(zip, skillPath, `.claude/skills/${skill}`)
    }
  }
}

async function exists(p: string): Promise<boolean> {
  try { await fs.access(p); return true } catch { return false }
}

async function addDirectoryToZip(zip: JSZip, dirPath: string, zipPrefix: string): Promise<void> {
  try {
    const entries = await fs.readdir(dirPath, { withFileTypes: true })
    for (const entry of entries) {
      // Caches Python : jamais dans une archive
      if (entry.name === '__pycache__') continue
      const entryPath = path.join(dirPath, entry.name)
      const zipPath = `${zipPrefix}/${entry.name}`
      if (entry.isDirectory()) {
        await addDirectoryToZip(zip, entryPath, zipPath)
      } else {
        const content = await fs.readFile(entryPath)
        zip.file(zipPath, content)
      }
    }
  } catch {
    // Dossier inexistant, on skip
  }
}

/**
 * Add paths selectively. If paths contains '*', add everything.
 * Otherwise, add only the specified paths (files or directories).
 */
async function addSelectivePaths(
  zip: JSZip,
  basePath: string,
  zipPrefix: string,
  paths: string[]
): Promise<void> {
  if (paths.length === 0) return

  if (paths.includes('*')) {
    // Add everything
    await addDirectoryToZip(zip, basePath, zipPrefix)
    return
  }

  // Also add ARCHITECTURE.md if it exists at basePath root
  const archPath = path.join(basePath, 'ARCHITECTURE.md')
  if (await exists(archPath)) {
    const content = await fs.readFile(archPath)
    zip.file(`${zipPrefix}/ARCHITECTURE.md`, content)
  }

  for (const p of paths) {
    const fullPath = path.join(basePath, p)
    if (!(await exists(fullPath))) continue

    const stat = await fs.stat(fullPath)
    if (stat.isDirectory()) {
      await addDirectoryToZip(zip, fullPath, `${zipPrefix}/${p}`)
    } else {
      const content = await fs.readFile(fullPath)
      zip.file(`${zipPrefix}/${p}`, content)
    }
  }
}

function generateReadme(pkg: { name: string; id: string; description: string; highlights: string[] }): string {
  return `# Claude Code Setup — ${pkg.name}

${pkg.description}

## Installation

1. Copiez le dossier \`.claude\` a la racine de votre projet
2. Copiez \`CLAUDE.md\` a la racine de votre projet
3. Copiez \`settings.json\` dans \`.claude/settings.json\` (ou fusionnez avec l'existant)
4. Lancez Claude Code dans votre projet

## Contenu

${pkg.highlights.map(h => `- ${h}`).join('\n')}

---
Genere depuis bfcours.dev
`
}

function generateSkillPackReadme(pkg: AIPackage<PackageId>, presentationFile?: string): string {
  return `# Pack ${pkg.name}

${pkg.description}

## Contenu

${pkg.highlights.map(h => `- ${h}`).join('\n')}
${presentationFile ? `- diaporama/${presentationFile} : le diaporama de présentation du skill (à ouvrir dans le navigateur ; reveal.js et les icônes se chargent en ligne)\n` : ''}${pkg.mcpServerPaths?.length ? '- mcp_servers/ : serveurs Python appelés par les scripts de création et de compilation\n' : ''}${pkg.dataPaths.length ? '- datas/ : modèles de documents et préférences par défaut\n' : ''}
${installMarkdown(pkg.id, pkg.pythonDeps)}
## Prérequis

${skillPackPrerequis(pkg)}

---
Généré depuis bfcours.dev
`
}

/**
 * Prérequis du LISEZMOI : ceux de la page du skill (SKILL_PAGES), sinon ceux déclarés
 * dans le pack (pack sans page, téléchargé depuis un tutoriel), sinon ceux du pack LaTeX.
 */
function skillPackPrerequis(pkg: AIPackage<PackageId>): string {
  const page = Object.values(SKILL_PAGES).find(p => p.packId === pkg.id)
  if (page) return page.prerequis.map(p => `- ${p.texte}`).join('\n')
  if (pkg.prerequis?.length) return pkg.prerequis.map(p => `- ${p}`).join('\n')
  return '- Une distribution LaTeX avec LuaLaTeX (MiKTeX ou TeX Live) et le paquet bfcours.\n- Python 3.'
}

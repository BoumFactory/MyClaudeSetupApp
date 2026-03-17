import { NextRequest, NextResponse } from 'next/server'
import { AI_PACKAGES, SHARED_FOLDERS } from '@/data/ai-packages'
import type { PackageTier } from '@/data/ai-packages'
import JSZip from 'jszip'
import fs from 'fs/promises'
import path from 'path'

const SETUP_BASE = path.join(process.cwd(), 'public', 'download', 'Claude-Code-Setup')
const CLAUDE_SETUP = path.join(SETUP_BASE, 'claude-setup')

export async function POST(request: NextRequest) {
  try {
    const { packageId } = (await request.json()) as { packageId: PackageTier }

    const pkg = AI_PACKAGES.find(p => p.id === packageId)
    if (!pkg) {
      return NextResponse.json({ error: 'Package inconnu' }, { status: 400 })
    }

    const zip = new JSZip()

    // 1. Add shared folders (hooks, scripts, base-scripts, assets)
    for (const folder of SHARED_FOLDERS) {
      const folderPath = path.join(CLAUDE_SETUP, folder)
      await addDirectoryToZip(zip, folderPath, `.claude/${folder}`)
    }

    // 2. Add skills
    for (const skill of pkg.skills) {
      const skillPath = path.join(CLAUDE_SETUP, 'skills', skill)
      if (await exists(skillPath)) {
        await addDirectoryToZip(zip, skillPath, `.claude/skills/${skill}`)
      }
    }

    // 3. Add agents
    await addSelectivePaths(zip, path.join(CLAUDE_SETUP, 'agents'), '.claude/agents', pkg.agentPaths)

    // 4. Add commands
    await addSelectivePaths(zip, path.join(CLAUDE_SETUP, 'commands'), '.claude/commands', pkg.commandPaths)

    // 5. Add datas
    await addSelectivePaths(zip, path.join(CLAUDE_SETUP, 'datas'), '.claude/datas', pkg.dataPaths)

    // 6. Add agents-data
    await addSelectivePaths(zip, path.join(CLAUDE_SETUP, 'agents-data'), '.claude/agents-data', pkg.agentsDataPaths)

    // 7. Add CLAUDE.md at root
    const claudeMdPath = path.join(SETUP_BASE, pkg.claudeMdFile)
    if (await exists(claudeMdPath)) {
      const content = await fs.readFile(claudeMdPath)
      zip.file('CLAUDE.md', content)
    }

    // 8. Add settings.json at root
    const settingsPath = path.join(SETUP_BASE, 'settings.json')
    if (await exists(settingsPath)) {
      const content = await fs.readFile(settingsPath)
      zip.file('settings.json', content)
    }

    // 9. Add README
    zip.file('README.md', generateReadme(pkg))

    const zipBuffer = await zip.generateAsync({
      type: 'nodebuffer',
      compression: 'DEFLATE',
      compressionOptions: { level: 9 },
    })

    return new NextResponse(new Uint8Array(zipBuffer), {
      headers: {
        'Content-Type': 'application/zip',
        'Content-Disposition': `attachment; filename="claude-setup-${pkg.id}.zip"`,
      },
    })
  } catch (error) {
    console.error('[PACKAGE-ZIP] Erreur:', error)
    return NextResponse.json({ error: 'Erreur lors de la generation du ZIP' }, { status: 500 })
  }
}

async function exists(p: string): Promise<boolean> {
  try { await fs.access(p); return true } catch { return false }
}

async function addDirectoryToZip(zip: JSZip, dirPath: string, zipPrefix: string): Promise<void> {
  try {
    const entries = await fs.readdir(dirPath, { withFileTypes: true })
    for (const entry of entries) {
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

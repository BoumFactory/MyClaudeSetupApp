import { NextRequest, NextResponse } from 'next/server'
import { generateZip } from '@/lib/zip-generator-server'
import { DownloadableItem } from '@/types'
import { generateDownloadReport } from '@/lib/download-report-generator'
import { createDownloadRateLimiter } from '@/lib/rate-limiter'
import type { CartItem } from '@/types/cart-theme'
import JSZip from 'jszip'
import fs from 'fs/promises'
import path from 'path'

/**
 * API route pour generer et telecharger un ZIP
 * Supporte deux modes :
 * - { files: DownloadableItem[] } : mode classique (FileExplorer)
 * - { cartItems: CartItem[], themeName: string } : mode panier allegorique
 */
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const basePath = path.join(process.cwd(), 'public', 'download')

    // Mode panier allegorique
    if (body.cartItems) {
      const { cartItems, themeName } = body as {
        cartItems: CartItem[]
        themeName: string
      }

      if (!cartItems || cartItems.length === 0) {
        return NextResponse.json(
          { error: 'Panier vide' },
          { status: 400 }
        )
      }

      // Rate limiting pour le panier (meme limites que FileExplorer)
      try {
        const forwarded = request.headers.get('x-forwarded-for')
        const ip = forwarded ? forwarded.split(',')[0] : 'unknown'
        const rateLimiter = createDownloadRateLimiter()
        const check = await rateLimiter.canDownload(ip)

        if (!check.allowed) {
          return NextResponse.json(
            {
              error: 'Rate limit dépassé',
              message: 'Vous avez atteint votre limite de téléchargements pour aujourd\'hui. Réessayez demain !',
              remaining: 0,
            },
            { status: 429 }
          )
        }

        // Enregistrer le telechargement
        await rateLimiter.recordDownload(ip)
      } catch {
        // Redis non disponible (dev local) — on laisse passer
      }

      const zip = new JSZip()
      const publicRoot = path.join(process.cwd(), 'public')
      const resolvedPublicRoot = path.resolve(publicRoot)

      // Ajouter chaque item du panier
      for (const item of cartItems) {
        // Securite : empecher le path traversal
        const sanitized = item.path.replace(/\.\./g, '').replace(/^\//, '')

        // Resoudre depuis public/ (couvre download/, render/, etc.)
        let resolved: string
        if (sanitized.startsWith('download/') || sanitized.startsWith('render/') || sanitized.startsWith('images/')) {
          // Path deja relatif a public/
          resolved = path.resolve(path.join(publicRoot, sanitized))
        } else {
          // Fallback : chercher dans public/download/ (ancien comportement)
          resolved = path.resolve(path.join(basePath, sanitized))
        }

        // Verifier qu'on reste dans public/
        if (!resolved.startsWith(resolvedPublicRoot)) {
          console.warn(`[CART-ZIP] Path traversal bloque: ${item.path}`)
          continue
        }

        try {
          const stat = await fs.stat(resolved)
          if (stat.isDirectory()) {
            await addDirectoryToZip(zip, resolved, item.name || path.basename(resolved))
          } else {
            // Pour les presentations HTML, inclure aussi les assets reveal.js references
            if (resolved.includes('Reveals') && resolved.endsWith('.html')) {
              const htmlContent = await fs.readFile(resolved, 'utf-8')
              const presFolder = `presentations/${path.basename(resolved, '.html')}`
              zip.file(`${presFolder}/${path.basename(resolved)}`, htmlContent)

              // Extraire les references aux assets locaux
              const assetRegex = /(?:src|href)=["']assets\/([^"']+)["']/g
              const assetsDir = path.join(path.dirname(resolved), 'assets')
              let assetMatch
              while ((assetMatch = assetRegex.exec(htmlContent)) !== null) {
                const assetFile = assetMatch[1]
                const assetFullPath = path.join(assetsDir, assetFile)
                try {
                  const assetContent = await fs.readFile(assetFullPath)
                  zip.file(`${presFolder}/assets/${assetFile}`, assetContent)
                } catch {
                  // Asset manquant, on continue
                }
              }
            } else {
              const content = await fs.readFile(resolved)
              zip.file(path.basename(resolved), content)
            }
          }
        } catch (err) {
          console.warn(`[CART-ZIP] Fichier introuvable: ${resolved}`)
        }
      }

      // Ajouter le rapport HTML
      const report = generateDownloadReport(cartItems, themeName)
      zip.file('rapport-telechargement.html', report)

      const zipBuffer = await zip.generateAsync({
        type: 'nodebuffer',
        compression: 'DEFLATE',
        compressionOptions: { level: 9 },
      })

      return new NextResponse(new Uint8Array(zipBuffer), {
        headers: {
          'Content-Type': 'application/zip',
          'Content-Disposition': `attachment; filename="bfcours-${Date.now()}.zip"`,
        },
      })
    }

    // Mode classique (FileExplorer)
    const { files } = body as { files: DownloadableItem[] }

    if (!files) {
      return NextResponse.json(
        { error: 'Donnees manquantes' },
        { status: 400 }
      )
    }

    const zipBuffer = await generateZip(files, basePath, true)

    return new NextResponse(new Uint8Array(zipBuffer), {
      headers: {
        'Content-Type': 'application/zip',
        'Content-Disposition': `attachment; filename="claude-code-${Date.now()}.zip"`,
      },
    })
  } catch (error) {
    console.error('Erreur lors de la generation du ZIP :', error)
    return NextResponse.json(
      { error: 'Erreur lors de la generation du ZIP' },
      { status: 500 }
    )
  }
}

/**
 * Ajoute recursivement un repertoire au ZIP
 */
async function addDirectoryToZip(
  zip: JSZip,
  dirPath: string,
  zipPrefix: string
): Promise<void> {
  const entries = await fs.readdir(dirPath, { withFileTypes: true })
  for (const entry of entries) {
    const entryPath = path.join(dirPath, entry.name)
    const zipPath = `${zipPrefix}/${entry.name}`
    if (entry.isDirectory()) {
      zip.folder(zipPath)
      await addDirectoryToZip(zip, entryPath, zipPath)
    } else {
      const content = await fs.readFile(entryPath)
      zip.file(zipPath, content)
    }
  }
}

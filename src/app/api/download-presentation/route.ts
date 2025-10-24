import { NextRequest, NextResponse } from 'next/server'
import path from 'path'
import fs from 'fs/promises'
import JSZip from 'jszip'

/**
 * API Route pour télécharger une présentation avec tous ses assets
 * GET /api/download-presentation?filename=presentation.html
 */
export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const filename = searchParams.get('filename')

    if (!filename) {
      return NextResponse.json(
        { error: 'Le paramètre filename est requis' },
        { status: 400 }
      )
    }

    // Vérifier que le fichier est bien dans le dossier Reveals
    if (!filename.endsWith('.html') || filename.includes('..')) {
      return NextResponse.json(
        { error: 'Nom de fichier invalide' },
        { status: 400 }
      )
    }

    const revealsPath = path.join(process.cwd(), 'src', 'public', 'render', 'Reveals')
    const htmlPath = path.join(revealsPath, filename)

    // Vérifier que le fichier existe
    try {
      await fs.access(htmlPath)
    } catch {
      return NextResponse.json(
        { error: 'Présentation non trouvée' },
        { status: 404 }
      )
    }

    // Lire le contenu HTML
    const htmlContent = await fs.readFile(htmlPath, 'utf-8')

    // Créer un ZIP
    const zip = new JSZip()

    // Ajouter le fichier HTML
    zip.file(filename, htmlContent)

    // Extraire toutes les références aux assets locaux
    const assetRegex = /(?:src|href)=["']assets\/([^"']+)["']/g
    const assets = new Set<string>()
    let match

    while ((match = assetRegex.exec(htmlContent)) !== null) {
      assets.add(match[1])
    }

    // Ajouter les assets au ZIP
    const assetsPath = path.join(revealsPath, 'assets')

    for (const assetPath of assets) {
      const fullAssetPath = path.join(assetsPath, assetPath)

      try {
        const assetContent = await fs.readFile(fullAssetPath)
        zip.file(`assets/${assetPath}`, assetContent)
        console.log(`[Download] Asset ajouté: assets/${assetPath}`)
      } catch (error) {
        console.warn(`[Download] Asset non trouvé: ${assetPath}`, error)
        // Continuer même si un asset n'est pas trouvé
      }
    }

    // Générer le ZIP
    const zipBuffer = await zip.generateAsync({
      type: 'nodebuffer',
      compression: 'DEFLATE',
      compressionOptions: { level: 6 }
    })

    // Créer le nom du fichier ZIP
    const zipFilename = filename.replace('.html', '.zip')

    // Retourner le ZIP (conversion en Uint8Array pour Next.js 15)
    return new NextResponse(new Uint8Array(zipBuffer), {
      headers: {
        'Content-Type': 'application/zip',
        'Content-Disposition': `attachment; filename="${zipFilename}"`,
        'Content-Length': zipBuffer.length.toString(),
      },
    })
  } catch (error) {
    console.error('[Download] Erreur lors de la génération du ZIP:', error)
    return NextResponse.json(
      { error: 'Erreur lors de la génération du package' },
      { status: 500 }
    )
  }
}

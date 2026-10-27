import { NextRequest, NextResponse } from 'next/server'
import JSZip from 'jszip'
import { addPresentationToZip, isValidPresentationFilename } from '@/lib/presentation-zip'

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
    if (!isValidPresentationFilename(filename)) {
      return NextResponse.json(
        { error: 'Nom de fichier invalide' },
        { status: 400 }
      )
    }

    // ZIP : le HTML et les assets locaux qu'il référence
    const zip = new JSZip()
    const found = await addPresentationToZip(zip, filename)
    if (!found) {
      return NextResponse.json(
        { error: 'Présentation non trouvée' },
        { status: 404 }
      )
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

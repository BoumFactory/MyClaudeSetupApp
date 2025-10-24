import { NextRequest, NextResponse } from 'next/server'
import { generateZip } from '@/lib/zip-generator-server'
import { DownloadableItem } from '@/types'
import path from 'path'

/**
 * API route pour générer et télécharger un ZIP
 */
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { files } = body as {
      files: DownloadableItem[]
    }

    // Valider les données
    if (!files) {
      return NextResponse.json(
        { error: 'Données manquantes' },
        { status: 400 }
      )
    }

    // Recalculer le basePath côté serveur au runtime
    // Cela garantit que le chemin est correct sur Vercel
    const basePath = path.join(process.cwd(), 'public', 'download')

    // Générer le ZIP
    const zipBuffer = await generateZip(files, basePath, true)

    // Retourner le ZIP en tant que Uint8Array
    return new NextResponse(new Uint8Array(zipBuffer), {
      headers: {
        'Content-Type': 'application/zip',
        'Content-Disposition': `attachment; filename="claude-code-${Date.now()}.zip"`,
      },
    })
  } catch (error) {
    console.error('Erreur lors de la génération du ZIP :', error)
    return NextResponse.json(
      { error: 'Erreur lors de la génération du ZIP' },
      { status: 500 }
    )
  }
}

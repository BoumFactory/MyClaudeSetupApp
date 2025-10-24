import { NextRequest, NextResponse } from 'next/server'
import { generateZip } from '@/lib/zip-generator-server'
import { DownloadableItem } from '@/types'

/**
 * API route pour générer et télécharger un ZIP
 */
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { files, basePath } = body as {
      files: DownloadableItem[]
      basePath: string
    }

    // Valider les données
    if (!files || !basePath) {
      return NextResponse.json(
        { error: 'Données manquantes' },
        { status: 400 }
      )
    }

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

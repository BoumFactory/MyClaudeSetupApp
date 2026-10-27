import { NextRequest, NextResponse } from 'next/server'
import { ALL_PACKAGES } from '@/data/ai-packages'
import type { PackageId } from '@/data/ai-packages'
import { buildPackageZip } from '@/lib/package-zip'

/**
 * Télécharge un bundle (Généraliste, LaTeX Enseignant, Power User)
 * ou un pack de skill (ex. skill-latex) sous forme de ZIP.
 */
export async function POST(request: NextRequest) {
  try {
    const { packageId } = (await request.json()) as { packageId: PackageId }

    const pkg = ALL_PACKAGES.find(p => p.id === packageId)
    if (!pkg) {
      return NextResponse.json({ error: 'Package inconnu' }, { status: 400 })
    }

    const zip = await buildPackageZip(pkg)

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

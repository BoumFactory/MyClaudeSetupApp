import { NextRequest, NextResponse } from 'next/server'
import path from 'path'
import fs from 'fs'

/**
 * Route API pour servir les fichiers depuis src/public/
 * Accessible via /api/serve-public/render/Reveals/fichier.html
 */
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> }
) {
  try {
    const { path: pathSegments } = await params

    // Construire le chemin vers le fichier
    const publicDir = path.join(process.cwd(), 'src', 'public')
    const filePath = path.join(publicDir, ...pathSegments)

    // Protection contre path traversal : vérifier que le chemin résolu reste dans src/public
    const resolvedPath = path.resolve(filePath)
    const resolvedPublicDir = path.resolve(publicDir)
    if (!resolvedPath.startsWith(resolvedPublicDir)) {
      return new NextResponse('Forbidden', { status: 403 })
    }

    // Vérifier que le fichier existe
    if (!fs.existsSync(filePath)) {
      return new NextResponse('File not found', { status: 404 })
    }

    // Vérifier que c'est bien un fichier (pas un dossier)
    const stats = fs.statSync(filePath)
    if (!stats.isFile()) {
      return new NextResponse('Not a file', { status: 400 })
    }

    // Lire le fichier
    const fileBuffer = fs.readFileSync(filePath)

    // Déterminer le Content-Type selon l'extension
    const ext = path.extname(filePath).toLowerCase()
    const contentTypes: Record<string, string> = {
      '.html': 'text/html',
      '.css': 'text/css',
      '.js': 'application/javascript',
      '.json': 'application/json',
      '.png': 'image/png',
      '.jpg': 'image/jpeg',
      '.jpeg': 'image/jpeg',
      '.gif': 'image/gif',
      '.svg': 'image/svg+xml',
      '.pdf': 'application/pdf',
      '.txt': 'text/plain',
      '.md': 'text/markdown',
    }

    const contentType = contentTypes[ext] || 'application/octet-stream'

    // Retourner le fichier avec cache agressif
    // Pas de rate limiting car ce sont des fichiers statiques
    // (contrairement aux téléchargements ZIP qui sont rate-limitées)
    return new NextResponse(fileBuffer, {
      headers: {
        'Content-Type': contentType,
        // Cache pendant 1 an pour les assets statiques
        'Cache-Control': 'public, max-age=31536000, immutable',
        // Permettre l'accès depuis l'iframe
        'X-Frame-Options': 'SAMEORIGIN',
      },
    })
  } catch (error) {
    console.error('Error serving file:', error)
    return new NextResponse('Internal server error', { status: 500 })
  }
}

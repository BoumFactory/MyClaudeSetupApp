import { NextRequest, NextResponse } from 'next/server'
import { createHash, timingSafeEqual } from 'node:crypto'

/**
 * Ingestion des feedbacks de l'application desktop QF-Studio.
 *
 * URL GELEE : POST https://bfcours.dev/7gOdepBMu5OY2QBKBcd7mGyA/qfstudio/feedback
 * (gravee dans le binaire via feedback.rs — ne jamais changer).
 *
 * Source de verite = depot GitHub BoumFactory/qfstudio-feedback.
 * Chaque item est commite sous inbox/AAAA-MM/<id>.json via l'API Contents.
 * Chemin unique par item => aucun conflit de SHA. Idempotent : si le fichier
 * existe deja, on renvoie 200 sans recommit.
 *
 * Garde-fous :
 *  - kill-switch  : QF_FEEDBACK_KILL truthy => 503 (coupe l'ingestion).
 *  - app-key      : header X-QF-Key compare a QF_FEEDBACK_APP_KEY (anti-spam de base).
 *  - cap de taille: corps de requete plafonne (MAX_BODY_BYTES).
 *
 * Secrets Vercel attendus :
 *  - QF_FEEDBACK_APP_KEY  : la cle partagee avec l'app (header X-QF-Key).
 *  - QF_FEEDBACK_GH_TOKEN : PAT fine-grained (repo qfstudio-feedback, Contents: write).
 *  - QF_FEEDBACK_KILL     : (optionnel) "1" pour couper l'ingestion.
 */

export const runtime = 'nodejs'
export const dynamic = 'force-dynamic'

const GH_REPO = 'BoumFactory/qfstudio-feedback'
// Doit rester IDENTIQUE a max_payload_kb de feedback-config.json (32 Ko). Si la
// route capait plus bas, l'app re-essaierait indefiniment un item accepte cote app.
const MAX_BODY_BYTES = 32 * 1024

function unauthorized() {
  return NextResponse.json({ error: 'unauthorized' }, { status: 401 })
}

/** Comparaison a temps constant (evite de fuiter la cle par timing). */
function keyMatches(provided: string | null, expected: string): boolean {
  if (!provided) return false
  const a = Buffer.from(provided)
  const b = Buffer.from(expected)
  if (a.length !== b.length) return false
  return timingSafeEqual(a, b)
}

/** Identifiant de fichier sur : id fourni par l'app, sinon empreinte du contenu. */
function deriveId(body: Record<string, unknown>, raw: string): string {
  const candidate = typeof body.id === 'string' ? body.id : ''
  const safe = candidate.replace(/[^a-zA-Z0-9_-]/g, '').slice(0, 64)
  if (safe.length >= 8) return safe
  return createHash('sha256').update(raw).digest('hex').slice(0, 40)
}

export async function POST(request: NextRequest) {
  // 1. Kill-switch
  if (process.env.QF_FEEDBACK_KILL && process.env.QF_FEEDBACK_KILL !== '0') {
    return NextResponse.json({ error: 'feedback temporairement desactive' }, { status: 503 })
  }

  // 2. Config serveur presente ?
  const appKey = process.env.QF_FEEDBACK_APP_KEY
  const ghToken = process.env.QF_FEEDBACK_GH_TOKEN
  if (!appKey || !ghToken) {
    console.error('[qf-feedback] secret manquant (QF_FEEDBACK_APP_KEY / QF_FEEDBACK_GH_TOKEN)')
    return NextResponse.json({ error: 'configuration serveur' }, { status: 500 })
  }

  // 3. App-key
  if (!keyMatches(request.headers.get('x-qf-key'), appKey)) {
    return unauthorized()
  }

  // 4. Cap de taille + parsing
  const raw = await request.text()
  if (raw.length > MAX_BODY_BYTES) {
    return NextResponse.json({ error: 'feedback trop volumineux' }, { status: 413 })
  }
  let body: Record<string, unknown>
  try {
    const parsed = JSON.parse(raw)
    if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) throw new Error('not an object')
    body = parsed as Record<string, unknown>
  } catch {
    return NextResponse.json({ error: 'JSON invalide' }, { status: 400 })
  }

  // 5. Identifiant + chemin. feedback.rs fournit un id (uuid v4) => idempotence
  // parfaite ; deriveId retombe sur une empreinte du contenu si absent.
  const now = new Date()
  const yyyymm = `${now.getUTCFullYear()}-${String(now.getUTCMonth() + 1).padStart(2, '0')}`
  const id = deriveId(body, raw)

  // On archive l'enveloppe ENTIERE telle quelle (l'outillage de lecture s'attend
  // exactement a ce schema). Aucune transformation, aucun wrapper serveur.
  const item = body

  const path = `inbox/${yyyymm}/${id}.json`
  const apiUrl = `https://api.github.com/repos/${GH_REPO}/contents/${path}`
  const ghHeaders = {
    Authorization: `Bearer ${ghToken}`,
    Accept: 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28',
    'User-Agent': 'qfstudio-feedback-ingest',
  }

  try {
    // 6. Idempotence : si le fichier existe deja, ne pas recommit
    const head = await fetch(apiUrl, { headers: ghHeaders, cache: 'no-store' })
    if (head.status === 200) {
      return NextResponse.json({ ok: true, id, status: 'deja_recu' }, { status: 200 })
    }
    if (head.status !== 404) {
      const txt = await head.text()
      console.error(`[qf-feedback] GitHub GET ${head.status}: ${txt.slice(0, 200)}`)
      return NextResponse.json({ error: 'amont indisponible' }, { status: 502 })
    }

    // 7. Creation du fichier (chemin neuf => pas besoin de SHA, pas de conflit)
    const content = Buffer.from(JSON.stringify(item, null, 2) + '\n', 'utf-8').toString('base64')
    const kind = typeof body.type === 'string' ? body.type : 'feedback'
    const put = await fetch(apiUrl, {
      method: 'PUT',
      headers: { ...ghHeaders, 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: `${kind}: ${id} (${yyyymm})`, content }),
    })

    if (put.status === 201) {
      return NextResponse.json({ ok: true, id, status: 'enregistre' }, { status: 201 })
    }
    // 422 = course : un autre process a cree le meme chemin entre-temps => idempotent OK
    if (put.status === 422) {
      return NextResponse.json({ ok: true, id, status: 'deja_recu' }, { status: 200 })
    }
    const txt = await put.text()
    console.error(`[qf-feedback] GitHub PUT ${put.status}: ${txt.slice(0, 200)}`)
    return NextResponse.json({ error: 'echec enregistrement' }, { status: 502 })
  } catch (e) {
    console.error('[qf-feedback] erreur reseau GitHub:', e)
    return NextResponse.json({ error: 'amont injoignable' }, { status: 502 })
  }
}

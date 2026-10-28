// Essai à vide d'Exos Lombards : exe + kit de départ seuls dans un dossier vierge.
// Un exercice libre, ajouté au panier, puis « Produire le document » : on attend
// un PDF dans .exoslombards/fiches et on lit son texte.
//   node essai_kit.mjs <bac> <captures>
import { execFileSync } from 'node:child_process'
import { existsSync, readFileSync, readdirSync, statSync } from 'node:fs'
import { join, resolve } from 'node:path'
import { Bilan, attendre, lancerApplication } from 'file:///D:/Applications/Exos_lombards/tools/essai_webview/cdp.mjs'

const bac = resolve(process.argv[2])
const captures = resolve(process.argv[3])
const donnees = join(bac, '.exoslombards')
const bilan = new Bilan()

const LIBRE = String.raw`\begin{EXO}{Essai du kit}{KIT}
Calculer $2+3$.
\exocorrection
$2+3=5$.
\end{EXO}
`
const LIGNES = `document.querySelectorAll('[data-indice]').length`
const MESSAGES = `[...document.querySelectorAll('[role=status], [role=alert]')].map((e) => e.textContent).join(' | ')`

function pdfProduit(debut) {
  const fiches = join(donnees, 'fiches')
  if (!existsSync(fiches)) return null
  for (const d of readdirSync(fiches)) {
    const dossier = join(fiches, d)
    if (!statSync(dossier).isDirectory()) continue
    for (const f of readdirSync(dossier)) {
      if (f.endsWith('.pdf') && statSync(join(dossier, f)).mtimeMs > debut) return join(dossier, f)
    }
  }
  return null
}

const app = await lancerApplication({ bac, captures, env: { EXOS_ONGLET: 'fiche' } })
try {
  const { evaluer, jusqua, capture } = app
  await jusqua(`!!document.querySelector('[data-bouton-libre]')`, 120000, 'Composer affiché')
  await attendre(1500)
  await evaluer(`window.confirm = () => true; true`)
  await capture('01-composer-vide')
  bilan.noter('Composer ouvert sur une installation vide', true, 'lignes : ' + (await evaluer(LIGNES)))

  await evaluer(`document.querySelector('[data-bouton-libre]').click(); true`)
  await jusqua(`!!window.__t.modele()`, 60000, 'éditeur de l’exercice libre (Monaco)')
  await evaluer(`window.__t.modele().setValue(${JSON.stringify(LIBRE)}); true`)
  await attendre(800)
  await evaluer(`window.__t.cliquer('Ajouter au panier'); true`)
  await jusqua(`${MESSAGES}.includes('ajouté au panier')`, 15000, 'ajout au panier')
  await evaluer(`window.__t.cliquer('Retour au Composer'); true`)
  await jusqua(`${LIGNES} === 1`, 15000, 'exercice libre au panier')
  bilan.noter('exercice libre ajouté au panier', true)
  await capture('02-panier')

  const debut = Date.now()
  await evaluer(`window.__t.cliquer('Produire le document'); true`)
  const vivant = () => {
    try {
      process.kill(app.pid, 0)
      return true
    } catch {
      return false
    }
  }
  let pdf = null
  for (let t = Date.now(); !pdf && Date.now() - t < 420000; ) {
    await attendre(2000)
    pdf = pdfProduit(debut)
    if (!vivant()) {
      bilan.noter('application toujours ouverte pendant la production', false, `arrêtée après ${Math.round((Date.now() - debut) / 1000)} s`)
      throw new Error('application arrêtée')
    }
  }
  // Le PDF apparaît dès que LuaLaTeX commence à l'écrire : attendre la fin des
  // deux compilations (énoncé, puis corrigé) dans les .log.
  const fini = (log) => existsSync(log) && readFileSync(log, 'latin1').includes('Output written')
  if (pdf) {
    const log = pdf.replace(/\.pdf$/, '.log')
    const logCorr = pdf.replace(/\.pdf$/, '-correction.log')
    for (let t = Date.now(); !(fini(log) && fini(logCorr)) && Date.now() - t < 420000; ) {
      await attendre(2000)
      if (!vivant()) throw new Error('application arrêtée pendant la compilation')
    }
    bilan.noter('énoncé et corrigé compilés jusqu’au bout (« Output written »)', fini(log) && fini(logCorr))
  }
  await attendre(4000)
  await capture('03-production')
  const erreurs = await evaluer(`[...document.querySelectorAll('.bg-red-50')].map((e) => e.textContent).join(' | ')`)
  bilan.noter('PDF produit', !!pdf, pdf ?? erreurs.slice(0, 600))
  if (pdf) {
    const texte = execFileSync('python', ['-c', 'import sys,fitz; print("".join(p.get_text() for p in fitz.open(sys.argv[1])))', pdf], {
      encoding: 'utf8',
      env: { ...process.env, PYTHONIOENCODING: 'utf-8' },
    })
    bilan.noter('PDF : énoncé de l’exercice libre présent', texte.includes('Essai du kit') || texte.includes('Calculer'), texte.slice(0, 200).replace(/\n/g, ' '))
  }
  bilan.noter('aucune erreur affichée', erreurs === '', erreurs.slice(0, 300))
} catch (e) {
  bilan.noter('scénario', false, e.message)
  await app.capture('erreur').catch(() => undefined)
} finally {
  console.log('PID arrêté :', app.pid)
  await app.fermer()
}
process.exit(bilan.terminer(captures))

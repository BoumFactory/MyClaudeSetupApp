"""Joue réellement les activités de l'exemple dans le lecteur H5P (h5p-standalone).

Propre à CET exemple (textes des étiquettes et des affirmations écrits en dur) :
Summary (une erreur puis les bonnes réponses), glisser-déposer à la souris
(zones surlignées en rouge pour contrôler leur position, deux étiquettes
inversées exprès), cartes retournées, textes à trous remplis avec « 0,19 »,
points de l'image ouverts (centres mesurés en % de l'image). Mode « m4 » :
mesure de la tolérance aux fautes sur mesure_m4/mesure_m4.json.

Règles Chrome : profil temporaire dédié (render_h5p._new_profile), fermeture du
contexte Playwright, puis nettoyage des orphelins FILTRÉ sur ce profil
(render_h5p._kill_orphans). Jamais de fermeture par nom d'image.

Usage (Playwright, avec le python du venv du projet) :
  python <ce_dossier>/jouer_activites.py example <archive.h5p> <dossier_captures>
  python <ce_dossier>/jouer_activites.py m4      <archive.h5p> <dossier_captures>
"""
import json, shutil, sys, tempfile, time
from pathlib import Path

SKILL = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILL / "scripts"))
import render_h5p as rh
from playwright.sync_api import sync_playwright

mode, h5p_path, out_dir = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
out_dir.mkdir(parents=True, exist_ok=True)
report = {'mode': mode, 'steps': [], 'errors': []}

staging = Path(tempfile.mkdtemp(prefix='h5pplay_'))
render_dir = staging / 'work'
rh._extract_h5p(h5p_path, render_dir / 'package')
shutil.copytree(rh.STANDALONE_DIR, render_dir / 'h5p-standalone')
httpd, port = rh._start_http_server(render_dir)
base_url = f"http://127.0.0.1:{port}"
rh._build_index_html(render_dir, base_url)
chrome = rh._find_chrome()
profile = rh._new_profile()
n_shot = [0]

CUR = "(document.querySelector('.h5p-current-screen') || document)"
SLIDE = CUR + ".querySelector('.h5p-slide.h5p-current')"


def log(msg, **kw):
    print(msg, kw if kw else '')
    report['steps'].append(dict(msg=msg, **kw))


try:
    with sync_playwright() as pw:
        ctx = pw.chromium.launch_persistent_context(
            user_data_dir=profile, executable_path=chrome, headless=True,
            viewport={'width': 1200, 'height': 900},
            args=['--no-first-run', '--no-default-browser-check'], timeout=60000)
        try:
            page = ctx.new_page()
            page.set_default_timeout(20000)
            page.on('pageerror', lambda e: report['errors'].append(f'pageerror: {e}'))

            def settle(fr, pause=1.0):
                time.sleep(pause)
                t0 = time.time()
                while time.time() - t0 < 8:
                    try:
                        if fr.evaluate(rh._JS_MATHJAX_IDLE):
                            break
                    except Exception:
                        pass
                    time.sleep(0.3)
                time.sleep(0.3)

            def shot(fr, label):
                settle(fr, 0.3)
                n_shot[0] += 1
                tmp = staging / f"s{n_shot[0]:02d}.png"
                page.screenshot(path=str(tmp), full_page=True)
                dest = out_dir / f"jeu_{n_shot[0]:02d}_{label}.png"
                shutil.move(str(tmp), str(dest))
                log(f"capture {dest.name}")

            def click(fr, sel):
                if not fr.evaluate(rh._JS_CLICK, sel):
                    raise RuntimeError(f"introuvable : {sel}")

            def next_slide(fr):
                # CP 1.25 : .h5p-footer-next-slide ; CP 1.27 (Logiquiz) : barre
                # .h5p-cp-footer-navigation, bouton désigné par son aria-label.
                if not fr.evaluate(rh._JS_CLICK, '.h5p-footer-next-slide'):
                    click(fr, '.h5p-cp-footer-navigation button[aria-label="Suivant"]')
                settle(fr, 1.0)

            page.goto(f"{base_url}/index.html?steps=0")
            fr = page.wait_for_selector('iframe.h5p-iframe', timeout=20000).content_frame()
            fr.wait_for_selector('.h5p-start-button', state='visible', timeout=30000)
            settle(fr)
            click(fr, '.h5p-start-button')
            settle(fr)

            if mode == 'm4':
                values = ["0,1", "0,26", "1600", "12,57", "0,19", "paralèle"]
                expected = ["0,4", "0,25", "1500", "12,75", "0,18/0.18", "parallèle"]
                blanks = fr.locator('.h5p-slide.h5p-current .h5p-blanks')
                table = []
                for k in range(blanks.count()):
                    b = blanks.nth(k)
                    inputs = b.locator('input')
                    for i, v in enumerate(values):
                        inputs.nth(i).fill(v)
                    b.locator('.h5p-question-check-answer').click()
                    settle(fr, 0.8)
                    classes = [inputs.nth(i).evaluate("e => e.parentElement.className + ' ' + e.className")
                               for i in range(len(values))]
                    for i, v in enumerate(values):
                        verdict = 'JUSTE' if 'h5p-correct' in classes[i] else (
                            'FAUX' if 'h5p-wrong' in classes[i] else '?')
                        table.append({'interaction': ['numeric true', 'défaut'][k],
                                      'attendu': expected[i], 'saisi': v, 'verdict': verdict})
                shot(fr, 'm4_tolerance')
                for row in table:
                    print(f"  {row['interaction']:13s} attendu {row['attendu']:10s} saisi {row['saisi']:9s} -> {row['verdict']}")
                report['m4'] = table

            else:
                # --- nœud 0 : texte
                click(fr, '.h5p-proceed-button')
                settle(fr)

                # --- diapo 1 : Summary
                for step in range(3):
                    texts = fr.evaluate("() => Array.from(" + SLIDE + ".querySelectorAll('.summary-options li'))"
                                        ".filter(li => li.offsetParent !== null).map(li => li.textContent)")
                    if not texts:
                        raise RuntimeError('Summary : aucune affirmation visible')
                    def is_correct(t):
                        return ("même nœud" in t) or ("produit" in t) or ("on lit" in t and "∩" not in t)
                    good = next(i for i, t in enumerate(texts) if is_correct(t))
                    if step == 0:
                        bad = next(i for i, t in enumerate(texts) if not is_correct(t))
                        fr.evaluate("(k) => Array.from(" + SLIDE + ".querySelectorAll('.summary-options li'))"
                                    ".filter(li => li.offsetParent !== null)[k].click()", bad)
                        settle(fr, 0.6)
                        shot(fr, 'summary_erreur')
                        texts = fr.evaluate("() => Array.from(" + SLIDE + ".querySelectorAll('.summary-options li'))"
                                            ".filter(li => li.offsetParent !== null).map(li => li.textContent)")
                        good = next(i for i, t in enumerate(texts) if is_correct(t))
                    if step == 1:
                        shot(fr, 'summary_etape2_mathjax')
                    fr.evaluate("(k) => Array.from(" + SLIDE + ".querySelectorAll('.summary-options li'))"
                                ".filter(li => li.offsetParent !== null)[k].click()", good)
                    settle(fr, 0.8)
                shot(fr, 'summary_termine')
                log('summary', score=fr.evaluate("() => (" + SLIDE + ".querySelector('.summary-evaluation') || {}).textContent || ''"))

                # --- diapo 2 : DragQuestion
                next_slide(fr)
                fr.evaluate("""() => { const s = document.createElement('style');
                   s.id = 'zones-debug';
                   s.textContent = '.h5p-dropzone{outline:3px solid rgba(220,0,0,.85)!important}';
                   document.head.appendChild(s); }""")
                shot(fr, 'dragquestion_zones_en_rouge')
                fr.evaluate("() => document.getElementById('zones-debug').remove()")
                drags = fr.locator('.h5p-slide.h5p-current .h5p-draggable')
                zones = fr.locator('.h5p-slide.h5p-current .h5p-dropzone')
                log('dragquestion', draggables=drags.count(), zones=zones.count())
                # H5P déplace dans le DOM l'étiquette déposée : on la vise par son TEXTE.
                labels = ['0,3', '0,7', '0,6', '0,4', '0,2', '0,8']
                plan = {0: 0, 1: 1, 2: 2, 3: 3, 4: 5, 5: 4}     # 4 et 5 inversées exprès
                overflow = "() => { const el = " + SLIDE + ".querySelector('.h5p-dragquestion').closest('.h5p-element-inner') || " + SLIDE + ".querySelector('.h5p-dragquestion').parentElement; return {scroll: el.scrollHeight, client: el.clientHeight}; }"
                log('hauteur élément avant vérification', **fr.evaluate(overflow))
                for d_idx, z_idx in plan.items():
                    db = fr.locator('.h5p-slide.h5p-current .h5p-draggable', has_text=labels[d_idx]).bounding_box()
                    zb = zones.nth(z_idx).bounding_box()
                    page.mouse.move(db['x'] + db['width'] / 2, db['y'] + db['height'] / 2)
                    page.mouse.down()
                    page.mouse.move(zb['x'] + zb['width'] / 2, zb['y'] + zb['height'] / 2, steps=12)
                    page.mouse.up()
                    time.sleep(0.3)
                shot(fr, 'dragquestion_deposees')
                fr.locator('.h5p-slide.h5p-current .h5p-question-check-answer').click()
                settle(fr, 1.0)
                shot(fr, 'dragquestion_verifiee')
                log('hauteur élément après vérification', **fr.evaluate(overflow))
                log('dragquestion verifiee',
                    corrects=fr.locator('.h5p-slide.h5p-current .h5p-draggable.h5p-correct').count(),
                    fausses=fr.locator('.h5p-slide.h5p-current .h5p-draggable.h5p-wrong').count(),
                    score=fr.evaluate("() => { const e = " + SLIDE + ".querySelector('.h5p-joubelui-score-bar-star, .h5p-joubelui-score-numeric'); return e ? e.textContent : ''; }"))

                # --- diapo 3 : Dialogcards
                next_slide(fr)
                shot(fr, 'dialogcards_recto')
                fr.locator('.h5p-slide.h5p-current .h5p-dialogcards-turn').first.click()
                settle(fr, 1.2)
                shot(fr, 'dialogcards_verso_mathjax')

                # --- diapo 4 : Blanks (0,19 au lieu de 0,18)
                next_slide(fr)
                blanks = fr.locator('.h5p-slide.h5p-current .h5p-blanks')
                verdicts = []
                for k in range(blanks.count()):
                    b = blanks.nth(k)
                    b.locator('input').first.fill('0,19')
                    b.locator('.h5p-question-check-answer').click()
                    settle(fr, 0.6)
                    cls = b.locator('input').first.evaluate("e => e.parentElement.className")
                    verdicts.append('JUSTE' if 'h5p-correct' in cls else 'FAUX')
                shot(fr, 'blanks_0-19')
                log('blanks 0,19 (numeric / défaut)', verdicts=verdicts)

                # --- nœud 2 : image à zones
                click(fr, '.h5p-proceed-button')
                settle(fr, 1.5)
                spots = fr.locator('.h5p-image-hotspot')
                log('imagehotspots', points=spots.count())
                boxes = [spots.nth(i).bounding_box() for i in range(spots.count())]
                img = fr.locator('.h5p-image-hotspots-background').bounding_box()
                if img:
                    rel = [(round((b['x'] + b['width'] / 2 - img['x']) / img['width'] * 100, 1),
                            round((b['y'] + b['height'] / 2 - img['y']) / img['height'] * 100, 1)) for b in boxes]
                    log('centres des points mesurés en % de l image', centres=rel)
                # le point du nœud A (y le plus proche de 27 %)
                target = min(range(len(boxes)), key=lambda i: abs(rel[i][1] - 27) + abs(rel[i][0] - 40)) if img else 0
                spots.nth(target).click()
                settle(fr, 1.2)
                shot(fr, 'imagehotspots_bulle_noeud_A')
                fr.locator('.h5p-image-hotspot-close-popup-button').first.click()
                settle(fr, 0.8)
                spots.nth(0).click()
                settle(fr, 1.2)
                shot(fr, 'imagehotspots_bulle_2')
        finally:
            ctx.close()
except Exception as exc:
    report['errors'].append(f'pilotage interrompu : {exc}')
finally:
    httpd.shutdown()
    rh._kill_orphans(profile, Path(chrome).name)
    shutil.rmtree(profile, ignore_errors=True)
    shutil.rmtree(staging, ignore_errors=True)

(out_dir / f'jeu_{mode}.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print('ERREURS :', report['errors'])
sys.exit(1 if report['errors'] else 0)

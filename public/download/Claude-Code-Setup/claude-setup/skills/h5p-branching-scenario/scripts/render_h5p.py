#!/usr/bin/env python3
"""
Rendu fidele d'un .h5p via le VRAI player H5P (h5p-standalone), en Chrome
headless. Sert a l'AUTO-VISUALISATION : l'agent (ou l'enseignant) voit
directement le rendu reel et les erreurs eventuelles, sans passer par Moodle.

Ce que ca prouve :
  - Le package s'ouvre dans un vrai player H5P (donc importable Moodle sans friction)
  - Les librairies sont bien resolues (pas de 'missing library')
  - Le contenu, les maths (MathJax) et les boutons s'affichent reellement

Usage :
  python render_h5p.py --input scenario.h5p --output renders/
  python render_h5p.py --input scenario.h5p --output renders/ --screens 6
  # TOUS les écrans de TOUS les chemins (Playwright : python du venv du projet)
  python render_h5p.py --input scenario.h5p --output captures/ --parcours

Sortie :
  renders/screen_00.png ... screen_NN.png  (ecran titre puis ecrans suivants)
  renders/console.log                       (messages console, erreurs en tete)
  --parcours : captures/NN_<noeud>-<etat>.png dans l'ordre de l'organigramme
               + captures/captures.json (clés, chemins parcourus, erreurs)
  Code de sortie != 0 si une erreur H5P bloquante est detectee.

Chrome : chaque lancement a son --user-data-dir temporaire dédié, un timeout,
et s'arrête par PID ; les orphelins sont filtrés sur le profil temporaire.
Jamais de fermeture par nom d'image (la fenêtre de l'utilisateur est ouverte).
"""
import argparse
import functools
import http.server
import json
import os
import re
import shutil
import socketserver
import subprocess
import sys
import tempfile
import threading
import zipfile
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
STANDALONE_DIR = SKILL_DIR / 'assets' / 'h5p-standalone'

# Erreurs console qui signalent un package casse.
BLOCKING_PATTERNS = [
    r'missing library',
    r'no library selected',
    r'Failed to load',
    r'Uncaught (?!.*ResizeObserver)',  # ignore le bruit ResizeObserver
    r'is not a function',
    r'Cannot read propert',
    r'library file not found',
    r'Failed to fetch',
    r'404',
]


def _start_http_server(docroot: Path):
    """Sert docroot sur un port libre (h5p-standalone utilise fetch(), qui ne
    marche pas en file://). Retourne (httpd, port)."""
    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=str(docroot), **k)

        def log_message(self, *a, **k):
            pass

    class Server(socketserver.ThreadingTCPServer):
        allow_reuse_address = True
        daemon_threads = True

    httpd = Server(('127.0.0.1', 0), QuietHandler)
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, port


def _find_chrome() -> str:
    candidates = [
        os.environ.get('CHROME_PATH', ''),
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        '/usr/bin/google-chrome',
        '/usr/bin/chromium',
    ]
    for c in candidates:
        if c and Path(c).exists():
            return c
    raise FileNotFoundError("Chrome/Edge introuvable. Definir CHROME_PATH.")


def _extract_h5p(h5p_path: Path, dest: Path):
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    with zipfile.ZipFile(h5p_path) as z:
        z.extractall(dest)


def _file_url(p: Path) -> str:
    return p.resolve().as_uri()


def _build_index_html(render_dir: Path, base_url: str) -> Path:
    """Page qui charge le .h5p extrait avec h5p-standalone via HTTP local,
    puis tente automatiquement de passer l'ecran titre."""
    main_js = f"{base_url}/h5p-standalone/main.bundle.js"
    frame_js = f"{base_url}/h5p-standalone/frame.bundle.js"
    frame_css = f"{base_url}/h5p-standalone/styles/h5p.css"
    h5p_path = f"{base_url}/package"

    html = f'''<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8">
<title>Rendu H5P</title>
<link rel="stylesheet" href="{frame_css}">
<style>
  body {{ margin:0; background:#fff; font-family:Arial,sans-serif; }}
  #h5p-container {{ max-width:1100px; margin:0 auto; }}
  #render-status {{ position:fixed; top:4px; right:8px; font:11px monospace; color:#888; z-index:9999; }}
</style>
</head><body>
<div id="render-status">chargement...</div>
<pre id="render-result" style="display:none">{{"state":"loading"}}</pre>
<div id="h5p-container"></div>
<script src="{main_js}"></script>
<script>
  window.__H5P_ERRORS__ = [];
  window.addEventListener('error', function(e) {{
    window.__H5P_ERRORS__.push('window.onerror: ' + (e.message||e));
  }});
  const opts = {{
    h5pJsonPath: "{h5p_path}",
    frameJs: "{frame_js}",
    frameCss: "{frame_css}",
    frame: true
  }};
  // Nombre d'avances (clics) a effectuer avant capture : ?steps=N
  const STEPS = parseInt(new URLSearchParams(location.search).get('steps') || '0', 10);

  function h5pDoc() {{
    const ifr = document.querySelector('#h5p-container iframe.h5p-iframe, #h5p-container iframe');
    return (ifr && ifr.contentDocument) ? ifr.contentDocument : document;
  }}

  // Renvoie le prochain bouton a cliquer : bouton Demarrer, OU une reponse de
  // BranchingQuestion (la 1ere), OU un bouton Continuer/Proceed.
  function nextButton() {{
    const d = h5pDoc();
    const order = [
      '.h5p-branching-scenario-start-button',
      '.h5p-branching-question .h5p-branching-question-answer',
      '.h5p-branching-question button',
      '.h5p-nav-button:not([disabled])',
      '.h5p-branching-scenario-proceed-button',
      '.h5p-joubelui-button:not([disabled])'
    ];
    for (const s of order) {{
      const el = d.querySelector(s);
      if (el && el.offsetParent !== null) return el;
    }}
    return null;
  }}

  function writeResult(state) {{
    document.getElementById('render-result').textContent = JSON.stringify({{
      state: state, errors: window.__H5P_ERRORS__
    }});
  }}

  new H5PStandalone.H5P(document.getElementById('h5p-container'), opts)
    .then(function() {{
      document.getElementById('render-status').textContent = 'rendu OK';
      writeResult('ok');
      // Avances best-effort dans le Branching Scenario.
      for (let i = 0; i < STEPS; i++) {{
        setTimeout(function() {{
          try {{ const b = nextButton(); if (b) b.click(); }} catch(e) {{}}
          writeResult('ok');
        }}, 1200 + i * 1600);
      }}
    }})
    .catch(function(err) {{
      document.getElementById('render-status').textContent = 'ERREUR: ' + err;
      window.__H5P_ERRORS__.push('H5P init: ' + err);
      writeResult('error');
    }});
</script>
</body></html>'''
    index = render_dir / 'index.html'
    index.write_text(html, encoding='utf-8')
    return index


# ---------------------------------------------------------------------------
# LANCEMENT DE CHROME — règle absolue du poste (CLAUDE.md utilisateur)
#   1. un --user-data-dir TEMPORAIRE dédié à chaque lancement, jamais le
#      profil par défaut (sinon Chrome travaille dans le profil de
#      l'utilisateur, dont la fenêtre est ouverte en permanence) ;
#   2. un timeout sur chaque lancement ;
#   3. arrêt PAR PID uniquement (proc.kill(), ou taskkill /F /PID sans /T),
#      et nettoyage des orphelins filtré sur le profil temporaire.
# JAMAIS de taskkill /IM chrome.exe, Stop-Process -Name chrome, ni /T.
# ---------------------------------------------------------------------------

def _new_profile() -> str:
    """Crée un profil Chrome temporaire dédié (supprimé après usage)."""
    return tempfile.mkdtemp(prefix='chrome-agent-h5p-')


def _kill_orphans(profile: str, exe_name: str = 'chrome.exe'):
    """Arrête, par PID, les seuls processus dont la ligne de commande contient
    le profil temporaire. Ce filtre ne peut pas atteindre la fenêtre de
    l'utilisateur, qui tourne sur son profil par défaut."""
    if os.name != 'nt' or not profile:
        return
    prof = profile.replace("'", "''")
    exe = exe_name.replace("'", "''")
    ps = (
        f"Get-CimInstance Win32_Process -Filter \"Name='{exe}'\" | "
        f"Where-Object {{ $_.CommandLine -and $_.CommandLine.Contains('{prof}') }} | "
        "ForEach-Object { taskkill /F /PID $_.ProcessId | Out-Null }"
    )
    try:
        subprocess.run(['powershell', '-NoProfile', '-NonInteractive', '-Command', ps],
                       capture_output=True, timeout=30)
    except (subprocess.TimeoutExpired, OSError):
        pass


def _run_chrome(chrome: str, args: list, timeout: int = 90) -> subprocess.CompletedProcess:
    """Lance Chrome headless sur un profil temporaire dédié, avec timeout.
    En cas de dépassement : proc.kill() (arrêt par PID, sans arbre), puis
    nettoyage des orphelins filtré sur le profil, puis suppression du profil."""
    profile = _new_profile()
    cmd = [chrome, '--headless', f'--user-data-dir={profile}',
           '--no-first-run', '--no-default-browser-check'] + list(args)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=True, encoding='utf-8', errors='replace')
    try:
        out, err = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        out, err = proc.communicate()
    finally:
        _kill_orphans(profile, Path(chrome).name)
        shutil.rmtree(profile, ignore_errors=True)
    return subprocess.CompletedProcess(cmd, proc.returncode, out, err)


def _screenshot(chrome: str, url: str, out_png: Path, budget_ms: int = 6000,
                width: int = 1200, height: int = 900) -> str:
    """Capture une PNG + retourne les logs console (stderr)."""
    args = [
        '--disable-gpu', '--no-sandbox',
        '--hide-scrollbars', '--allow-file-access-from-files',
        f'--virtual-time-budget={budget_ms}',
        '--run-all-compositor-stages-before-draw',
        '--enable-logging=stderr', '--v=1',
        f'--window-size={width},{height}',
        f'--screenshot={out_png}', url,
    ]
    proc = _run_chrome(chrome, args, timeout=90)
    return proc.stderr or ''


def _probe_result(chrome: str, url: str, budget_ms: int = 8000) -> dict:
    """Lit l'etat final du rendu via --dump-dom (fiable, contrairement au
    parsing console). Retourne {'state': 'ok'|'error'|..., 'errors': [...]}"""
    args = [
        '--disable-gpu', '--no-sandbox',
        f'--virtual-time-budget={budget_ms}', '--dump-dom', url,
    ]
    proc = _run_chrome(chrome, args, timeout=90)
    dom = proc.stdout or ''
    m = re.search(r'<pre id="render-result"[^>]*>(.*?)</pre>', dom, re.S)
    if not m:
        return {'state': 'unknown', 'errors': ['render-result introuvable']}
    raw = (m.group(1).replace('&quot;', '"').replace('&amp;', '&')
           .replace('&lt;', '<').replace('&gt;', '>'))
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        return {'state': 'unknown', 'errors': ['resultat illisible: ' + raw[:120]]}


def _extract_console(stderr: str) -> list:
    lines = []
    for line in stderr.splitlines():
        m = re.search(r'CONSOLE\(\d+\)\] "?(.*)', line)
        if m:
            lines.append(m.group(1).rstrip('"'))
        elif 'ERROR:' in line and 'CONSOLE' not in line:
            continue
    return lines


def render(h5p_path: Path, out_dir: Path, screens: int = 1,
           width: int = 1200, height: int = 900) -> int:
    chrome = _find_chrome()
    out_dir.mkdir(parents=True, exist_ok=True)
    # IMPORTANT : Chrome (Windows) n'ecrit pas --screenshot= vers un chemin
    # contenant des espaces. On travaille dans un staging temporaire SANS
    # espaces (tempfile), puis on deplace les PNG vers out_dir.
    staging = Path(tempfile.mkdtemp(prefix='h5prender_'))
    render_dir = staging / 'work'
    content_dir = render_dir / 'package'
    _extract_h5p(h5p_path, content_dir)
    # Copier h5p-standalone dans le docroot (servi via HTTP)
    shutil.copytree(STANDALONE_DIR, render_dir / 'h5p-standalone')

    httpd, port = _start_http_server(render_dir)
    base_url = f"http://127.0.0.1:{port}"
    result = {'state': 'unknown', 'errors': []}
    try:
        _build_index_html(render_dir, base_url)

        # 1) GATE FIABLE : etat final lu dans le DOM (pas le parsing console)
        result = _probe_result(chrome, f"{base_url}/index.html?steps=0", budget_ms=9000)

        # 2) Captures visuelles : 1 par ecran (best-effort pour steps>0).
        #    Ecrites dans le staging (sans espaces) puis deplacees vers out_dir.
        for k in range(max(1, screens)):
            staged = staging / f'screen_{k:02d}.png'
            shot = out_dir / f'screen_{k:02d}.png'
            budget = 5000 + (k + 1) * 1700
            url = f"{base_url}/index.html?steps={k}"
            _screenshot(chrome, url, staged, budget_ms=budget, width=width, height=height)
            if staged.exists():
                shutil.move(str(staged), str(shot))
                print(f"  capture : {shot.name} (steps={k})")
            else:
                print(f"  ! capture manquee (steps={k})")
    finally:
        httpd.shutdown()

    # Journal d'erreurs
    errors = result.get('errors', []) or []
    blocking = [e for e in errors
                if any(re.search(p, e, re.I) for p in BLOCKING_PATTERNS)]
    log_path = out_dir / 'render.log'
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write(f"state: {result.get('state')}\n")
        f.write(f"errors ({len(errors)}):\n")
        for e in errors:
            f.write("  " + e + "\n")

    # Nettoyage du staging temporaire
    try:
        shutil.rmtree(staging)
    except OSError:
        pass

    state = result.get('state')
    if state == 'ok' and not blocking:
        print(f"  OK Le package s'ouvre dans un vrai player H5P (state={state}, "
              f"{len(errors)} erreur(s) non bloquante(s)).")
        return 0

    print(f"  X Rendu problematique (state={state}, {len(blocking)} erreur(s) bloquante(s)) :")
    for e in (blocking or errors)[:5]:
        print(f"     - {e[:140]}")
    return 1


# ---------------------------------------------------------------------------
# MODE PARCOURS : une capture par écran, sur TOUS les chemins du parcours
# ---------------------------------------------------------------------------
# Pilote le vrai lecteur avec Playwright (python du venv du projet).
# Énumère tous les chemins racine -> fin d'après content.json, les rejoue un
# par un, et capture chaque écran une seule fois : écran d'accueil, chaque
# diapositive d'une Course Presentation (question vierge, puis question
# corrigée avec un distracteur pour montrer le retour), chaque question
# d'embranchement, chaque écran de retour d'une proposition, chaque écran de
# texte et chaque écran de fin. Les fichiers sont numérotés dans l'ordre de
# l'organigramme (indice de nœud, puis diapositive, puis proposition).

_JS_VISIBLE = """
(sel) => {
  const vis = (el) => {
    if (!el) return false;
    const r = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none';
  };
  const cur = document.querySelector('.h5p-current-screen') || document;
  for (const root of [cur, document]) {
    for (const el of root.querySelectorAll(sel)) { if (vis(el)) return true; }
  }
  return false;
}
"""

_JS_CLICK = """
(sel) => {
  const vis = (el) => {
    if (!el) return false;
    const r = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none';
  };
  const cur = document.querySelector('.h5p-current-screen') || document;
  for (const root of [cur, document]) {
    for (const el of root.querySelectorAll(sel)) {
      if (vis(el) && !el.disabled) { el.click(); return true; }
    }
  }
  return false;
}
"""

_JS_MATHJAX_IDLE = """
() => {
  const MJ = window.MathJax;
  if (!MJ || !MJ.Hub || !MJ.Hub.queue) return true;
  return MJ.Hub.queue.pending === 0 && !MJ.Hub.queue.running
         && document.querySelectorAll('.MathJax_Processing').length === 0;
}
"""


def _enumerate_paths(content: list) -> list:
    """Tous les chemins racine -> fin : listes de (indice_noeud, alternative|None)."""
    paths = []

    def walk(i, acc, seen):
        if i is None or i < 0 or i >= len(content) or i in seen:
            paths.append(acc)
            return
        node = content[i]
        lib = node['type']['library'].split(' ')[0]
        if lib == 'H5P.BranchingQuestion':
            alts = node['type']['params']['branchingQuestion']['alternatives']
            for k, alt in enumerate(alts):
                walk(alt.get('nextContentId', -1), acc + [(i, k)], seen | {i})
        else:
            walk(node.get('nextContentId', -1), acc + [(i, None)], seen | {i})

    walk(0, [], frozenset())
    return paths


def render_parcours(h5p_path: Path, out_dir: Path, timeout_s: int = 900,
                    width: int = 1200, height: int = 900) -> int:
    """Capture tous les écrans de tous les chemins du parcours."""
    import time
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERREUR : Playwright absent. Lancer ce mode avec le python du venv du projet.")
        return 1

    chrome = _find_chrome()
    out_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(h5p_path) as z:
        content = json.loads(z.read('content/content.json').decode('utf-8'))
    bs = content['branchingScenario']
    nodes = bs['content']
    paths = _enumerate_paths(nodes)
    print(f"  {len(nodes)} nœuds, {len(paths)} chemin(s) à parcourir")

    staging = Path(tempfile.mkdtemp(prefix='h5prender_'))
    render_dir = staging / 'work'
    _extract_h5p(h5p_path, render_dir / 'package')
    shutil.copytree(STANDALONE_DIR, render_dir / 'h5p-standalone')
    httpd, port = _start_http_server(render_dir)
    base_url = f"http://127.0.0.1:{port}"
    _build_index_html(render_dir, base_url)

    deadline = time.time() + timeout_s
    shots = {}      # clé de tri -> (nom lisible, png temporaire)
    errors = []
    profile = _new_profile()

    def check_deadline():
        if time.time() > deadline:
            raise TimeoutError(f"délai global de {timeout_s} s dépassé")

    try:
        with sync_playwright() as pw:
            ctx = pw.chromium.launch_persistent_context(
                user_data_dir=profile, executable_path=chrome, headless=True,
                viewport={'width': width, 'height': height},
                args=['--no-first-run', '--no-default-browser-check'],
                timeout=60000)
            try:
                page = ctx.new_page()
                page.set_default_timeout(20000)
                page.on('pageerror', lambda e: errors.append(f'pageerror: {e}'))

                def frame():
                    el = page.wait_for_selector('iframe.h5p-iframe', timeout=20000)
                    return el.content_frame()

                def settle(fr, pause=1.2):
                    time.sleep(pause)
                    t0 = time.time()
                    while time.time() - t0 < 10:
                        try:
                            if fr.evaluate(_JS_MATHJAX_IDLE):
                                break
                        except Exception:
                            pass
                        time.sleep(0.3)
                    time.sleep(0.4)

                def shoot(key, label, fr):
                    if key in shots:
                        return
                    settle(fr, pause=0.2)
                    tmp = staging / f"shot_{len(shots):03d}.png"
                    page.screenshot(path=str(tmp), full_page=True)
                    shots[key] = (label, tmp)
                    print(f"  capture : {label}")

                def click(fr, sel, what):
                    if not fr.evaluate(_JS_CLICK, sel):
                        raise RuntimeError(f"bouton introuvable : {what} ({sel})")

                for p_idx, path in enumerate(paths):
                    check_deadline()
                    page.goto(f"{base_url}/index.html?steps=0")
                    fr = frame()
                    fr.wait_for_selector('.h5p-start-button', state='visible', timeout=30000)
                    settle(fr)
                    shoot((-1, 0, 0, 0), '00-accueil', fr)
                    click(fr, '.h5p-start-button', 'Commencer')
                    settle(fr)

                    for step, (i, alt) in enumerate(path):
                        check_deadline()
                        node = nodes[i]
                        lib = node['type']['library'].split(' ')[0]
                        tag = f"n{i}"
                        if lib == 'H5P.CoursePresentation':
                            slides = node['type']['params']['presentation']['slides']
                            for s, slide in enumerate(slides):
                                shoot((i, s, 0, 0), f"{tag}-diapo{s + 1}", fr)
                                # Question de la diapositive : réponse fausse + vérifier
                                mc = [e for e in slide['elements'][1:]
                                      if e['action']['library'].startswith('H5P.MultiChoice')]
                                if mc and (i, s, 1, 0) not in shots:
                                    answers = mc[0]['action']['params']['answers']
                                    wrong = next((k for k, a in enumerate(answers)
                                                  if not a['correct']), 0)
                                    ok = fr.evaluate(
                                        """(k) => {
                                          const cur = document.querySelector('.h5p-current-screen') || document;
                                          const sl = cur.querySelector('.h5p-slide.h5p-current');
                                          if (!sl) return false;
                                          const ans = sl.querySelectorAll('.h5p-answer');
                                          if (!ans[k]) return false;
                                          ans[k].click();
                                          const btn = sl.querySelector('.h5p-question-check-answer');
                                          if (btn) btn.click();
                                          return true;
                                        }""", wrong)
                                    if ok:
                                        settle(fr)
                                        shoot((i, s, 1, 0), f"{tag}-diapo{s + 1}-corrigee", fr)
                                    else:
                                        errors.append(f"{tag} diapo {s + 1} : question non pilotable")
                                if s < len(slides) - 1:
                                    click(fr, '.h5p-slide.h5p-current ~ * .h5p-footer-next-slide, '
                                              '.h5p-footer-next-slide', 'diapositive suivante')
                                    settle(fr, pause=0.9)
                            click(fr, '.h5p-proceed-button', 'Continuer')
                            settle(fr)
                        elif lib == 'H5P.BranchingQuestion':
                            shoot((i, 0, 0, 0), f"{tag}-question", fr)
                            ok = fr.evaluate(
                                """(k) => {
                                  const cur = document.querySelector('.h5p-current-screen') || document;
                                  const b = cur.querySelector('.h5p-branching-question-alternative[data-id="' + k + '"]')
                                         || document.querySelector('.h5p-branching-question-alternative[data-id="' + k + '"]');
                                  if (!b) return false; b.click(); return true;
                                }""", alt)
                            if not ok:
                                raise RuntimeError(f"{tag} : proposition {alt} introuvable")
                            settle(fr)
                            if fr.evaluate(_JS_VISIBLE, '.h5p-feedback-content'):
                                shoot((i, 1, alt, 0), f"{tag}-retour-proposition{alt + 1}", fr)
                                if not fr.evaluate(_JS_CLICK, '.h5p-feedback-content ~ button, '
                                                   '.h5p-branching-question button:not(.h5p-branching-question-alternative)'):
                                    raise RuntimeError(f"{tag} : bouton du retour introuvable")
                                settle(fr)
                        else:
                            shoot((i, 0, 0, 0), f"{tag}-texte", fr)
                            click(fr, '.h5p-proceed-button', 'Continuer')
                            settle(fr)

                    # Écran de fin atteint par ce chemin
                    last_i, last_alt = path[-1]
                    fr.wait_for_selector('.h5p-end-screen.h5p-current-screen', timeout=15000)
                    settle(fr)
                    end_key = (last_i, 9, last_alt if last_alt is not None else 0, 0)
                    shoot(end_key, f"n{last_i}-ecran-de-fin"
                          + (f"-proposition{last_alt + 1}" if last_alt is not None else ''), fr)
            finally:
                ctx.close()
    except Exception as exc:
        errors.append(f"pilotage interrompu : {exc}")
    finally:
        httpd.shutdown()
        _kill_orphans(profile, Path(chrome).name)
        shutil.rmtree(profile, ignore_errors=True)

    # Numérotation dans l'ordre de l'organigramme
    for old in out_dir.glob('[0-9][0-9]_*.png'):
        old.unlink()
    manifest = []
    for n, key in enumerate(sorted(shots), start=1):
        label, tmp = shots[key]
        name = f"{n:02d}_{label}.png"
        shutil.move(str(tmp), str(out_dir / name))
        manifest.append({'fichier': name, 'cle': list(key)})
    (out_dir / 'captures.json').write_text(
        json.dumps({'captures': manifest, 'chemins': [[list(x) for x in p] for p in paths],
                    'erreurs': errors}, ensure_ascii=False, indent=2), encoding='utf-8')
    shutil.rmtree(staging, ignore_errors=True)

    print(f"  {len(manifest)} capture(s) écrite(s) dans {out_dir}")
    blocking = [e for e in errors if any(re.search(p, e, re.I) for p in BLOCKING_PATTERNS)
                or e.startswith('pilotage')]
    for e in errors:
        print(f"  ! {e[:160]}")
    return 1 if blocking else 0


def main():
    ap = argparse.ArgumentParser(description="Rendu fidele d'un .h5p (vrai player H5P)")
    ap.add_argument('--input', '-i', required=True, help='Fichier .h5p')
    ap.add_argument('--output', '-o', required=True, help='Dossier de sortie (PNG + console.log)')
    ap.add_argument('--screens', '-n', type=int, default=1, help='Nb d ecrans (defaut 1 : ecran titre)')
    ap.add_argument('--parcours', action='store_true',
                    help='Capture TOUS les écrans de TOUS les chemins (Playwright, python du venv du projet)')
    ap.add_argument('--timeout', type=int, default=900,
                    help='Délai global du mode --parcours, en secondes (défaut 900)')
    ap.add_argument('--width', type=int, default=1200,
                    help='Largeur de la fenêtre en pixels (défaut 1200 ; 1366 = PC élève)')
    ap.add_argument('--height', type=int, default=900,
                    help='Hauteur de la fenêtre en pixels (défaut 900 ; 768 = PC élève)')
    args = ap.parse_args()

    h5p_path = Path(args.input)
    if not h5p_path.exists():
        print(f"ERREUR: introuvable : {args.input}")
        return 1
    if not STANDALONE_DIR.is_dir():
        print(f"ERREUR: h5p-standalone absent : {STANDALONE_DIR}")
        return 1
    if args.parcours:
        return render_parcours(h5p_path, Path(args.output), args.timeout,
                               args.width, args.height)
    return render(h5p_path, Path(args.output), args.screens, args.width, args.height)


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script CLI pour une compilation rapide avec LuaLaTeX (profil Reims).
Contient la logique complete de compilation, la verification post-compilation
(analyse exhaustive du .log, fraicheur reelle du PDF) et un verrou par dossier
pour eviter que deux maitres du meme dossier ne compilent en meme temps.
"""

import sys
import os
import json
import time
import argparse
import subprocess
import re
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

# Configuration LuaLaTeX recommandee Reims
LUALATEX_ARGS = ["-synctex=1", "-interaction=nonstopmode", "-file-line-error", "-shell-escape"]
PASS_TIMEOUT_SECONDS = 120

# Verrouillage par dossier (Friction 2 : deux maitres du meme dossier qui
# compilent en meme temps ecrasent leurs fichiers auxiliaires bfcours partages)
LOCK_FILENAME = ".quick_compile.lock"
LOCK_STALE_SECONDS = 900       # au-dela : verrou considere orphelin (processus mort ou trop ancien)
LOCK_MAX_WAIT_SECONDS = 300    # delai maximal d'attente avant abandon
LOCK_POLL_SECONDS = 2

# Erreurs "fichier:ligne: message" produites par -file-line-error, quel que
# soit le fichier en cause (.tex, .sty, .cls)
FILE_LINE_ERROR_RE = re.compile(
    r'^(?P<file>[^\s:][^:\n]*\.(?:tex|sty|cls)):(?P<line>\d+):[ \t]*(?P<msg>.+)$',
    re.MULTILINE
)
# Toutes les lignes d'erreur LaTeX generiques "! message"
BANG_ERROR_RE = re.compile(r'^! (?P<msg>.+)$', re.MULTILINE)

# Motifs d'echec muet : aucune erreur fatale, mais du contenu disparait du PDF
# sans avertissement explicite (tableaux/boites tcolorbox rognes, arrets brutaux...)
SILENT_FAILURE_PATTERNS = [
    (re.compile(r'\\vsplit needs a \\vbox'),
     "Bloc non secable rogne (\\vsplit needs a \\vbox) : du contenu peut avoir disparu du PDF"),
    (re.compile(r"Incompatible list can't be unboxed"),
     "Bloc non secable rogne (Incompatible list can't be unboxed) : du contenu peut avoir disparu du PDF"),
    (re.compile(r'upper box part has become overfull'),
     "tcolorbox : la partie superieure d'une boite non secable deborde : des items peuvent avoir disparu du PDF"),
    (re.compile(r'Emergency stop'),
     "Emergency stop : la compilation s'est interrompue brutalement"),
    (re.compile(r'Missing \$ inserted'),
     "Missing $ inserted : mode mathematique mal ferme"),
    (re.compile(r'Undefined control sequence'),
     "Undefined control sequence : commande LaTeX inconnue"),
    (re.compile(r'Paragraph ended before'),
     "Paragraph ended before ... : environnement ou groupe mal ferme"),
]


class LockTimeoutError(Exception):
    """Levee quand le verrou d'un dossier reste actif au-dela du delai maximal."""


# ---------------------------------------------------------------------------
# Verrouillage par dossier
# ---------------------------------------------------------------------------

def _pid_alive(pid: Optional[int]) -> bool:
    """Verifie (lecture seule, aucune action sur le processus) si un PID existe encore."""
    if not isinstance(pid, int) or pid <= 0:
        return False
    try:
        if sys.platform == "win32":
            result = subprocess.run(
                ["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"],
                capture_output=True, encoding="utf-8", errors="replace", timeout=10
            )
            return str(pid) in (result.stdout or "")
        os.kill(pid, 0)
        return True
    except Exception:
        return False


def _read_lock(lock_path: Path) -> Optional[Dict[str, Any]]:
    try:
        return json.loads(lock_path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _lock_is_stale(data: Optional[Dict[str, Any]]) -> bool:
    """Un verrou est perime s'il est trop ancien ou si son PID n'existe plus."""
    if not data:
        return True
    started_ts = data.get("started_ts")
    if not isinstance(started_ts, (int, float)):
        return True
    if time.time() - started_ts > LOCK_STALE_SECONDS:
        return True
    if not _pid_alive(data.get("pid")):
        return True
    return False


def _try_create_lock(lock_path: Path, payload: Dict[str, Any]) -> bool:
    """Creation atomique du verrou (O_EXCL) pour limiter les conditions de course."""
    try:
        fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False))
        return True
    except FileExistsError:
        return False


def acquire_lock(directory: Path, tex_file_name: str) -> Path:
    """
    Acquiert le verrou `.quick_compile.lock` du dossier avant de compiler.
    Attend la fin d'une compilation en cours dans le meme dossier (delai
    maximal LOCK_MAX_WAIT_SECONDS) et nettoie automatiquement un verrou
    orphelin (processus mort ou trop ancien) sans jamais toucher au processus
    lui-meme.
    """
    lock_path = directory / LOCK_FILENAME
    payload = {
        "pid": os.getpid(),
        "started_ts": time.time(),
        "started_human": datetime.now().isoformat(timespec="seconds"),
        "file": tex_file_name,
    }

    waited = 0.0
    last_report = -10.0
    while True:
        if _try_create_lock(lock_path, payload):
            return lock_path

        data = _read_lock(lock_path)
        if _lock_is_stale(data):
            owner_pid = data.get("pid") if data else "?"
            print(f"⚠️  Verrou perime dans {directory} (PID {owner_pid}), nettoyage", file=sys.stderr)
            try:
                lock_path.unlink()
            except FileNotFoundError:
                pass
            continue

        if waited >= LOCK_MAX_WAIT_SECONDS:
            owner_pid = data.get("pid") if data else "?"
            owner_file = data.get("file") if data else "?"
            raise LockTimeoutError(
                f"Verrou actif depuis plus de {LOCK_MAX_WAIT_SECONDS}s dans {directory} "
                f"(PID {owner_pid}, fichier {owner_file}) : une autre compilation du meme "
                f"dossier est en cours. Compiler sequentiellement les maitres d'un meme dossier."
            )

        if waited - last_report >= 10.0:
            print(
                f"⏳ En attente du verrou de compilation ({directory.name}) : "
                f"{waited:.0f}s/{LOCK_MAX_WAIT_SECONDS}s",
                file=sys.stderr
            )
            last_report = waited

        time.sleep(LOCK_POLL_SECONDS)
        waited += LOCK_POLL_SECONDS


def release_lock(lock_path: Path) -> None:
    try:
        lock_path.unlink()
    except FileNotFoundError:
        pass
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Compilation
# ---------------------------------------------------------------------------

def run_lualatex(file_path: Path, pass_number: int) -> Tuple[bool, int, str, str]:
    """
    Execute une passe de compilation LuaLaTeX.

    Returns:
        (ran_ok, returncode, stdout, stderr) - ran_ok=False uniquement si le
        processus n'a pas pu etre lance/termine (timeout, executable absent,
        erreur de decodage...). Ne fait AUCUNE hypothese de tolerance : le
        returncode brut est retourne tel quel.
    """
    cmd = ["lualatex"] + LUALATEX_ARGS + [str(file_path.name)]
    cwd = file_path.parent

    try:
        print(f"⚙️  Passe {pass_number}: {' '.join(cmd)}", file=sys.stderr)
        result = subprocess.run(
            cmd,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            cwd=str(cwd),
            timeout=PASS_TIMEOUT_SECONDS
        )
        return True, result.returncode, result.stdout or "", result.stderr or ""
    except subprocess.TimeoutExpired:
        return False, -1, "", f"Timeout apres {PASS_TIMEOUT_SECONDS} secondes"
    except FileNotFoundError:
        return False, -1, "", "lualatex non trouve - verifiez votre installation LaTeX"
    except Exception as e:
        return False, -1, "", str(e)


def analyze_latex_log(log_file_path: Path) -> Dict[str, Any]:
    """
    Analyse complete du .log : toutes les erreurs "fichier:ligne:" (tex/sty/cls)
    produites par -file-line-error, toutes les lignes "! ...", et les motifs
    d'echec muet connus (perte de contenu sans erreur fatale).
    """
    if not log_file_path.exists():
        return {"errors": [], "warnings": [], "log_found": False}

    try:
        log_content = log_file_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return {"errors": [], "warnings": [f"Impossible de lire le .log : {e}"], "log_found": False}

    errors: List[Dict[str, Any]] = []
    seen_messages = set()

    for match in FILE_LINE_ERROR_RE.finditer(log_content):
        msg = match.group("msg").strip()
        errors.append({
            "file": match.group("file"),
            "line": int(match.group("line")),
            "message": msg
        })
        seen_messages.add(msg)

    for match in BANG_ERROR_RE.finditer(log_content):
        msg = match.group("msg").strip()
        if msg in seen_messages:
            continue
        errors.append({"file": None, "line": None, "message": msg})
        seen_messages.add(msg)

    warnings: List[str] = []
    for pattern, description in SILENT_FAILURE_PATTERNS:
        count = len(pattern.findall(log_content))
        if count:
            suffix = f" ({count} occurrence{'s' if count > 1 else ''})"
            warnings.append(description + suffix)

    return {"errors": errors, "warnings": warnings, "log_found": True}


def verify_text_content(pdf_path: Path) -> Dict[str, Any]:
    """Verifie via pymupdf que le PDF contient du texte (nombre de pages/caracteres)."""
    try:
        import fitz  # pymupdf
    except ImportError:
        return {
            "available": False,
            "error": "pymupdf (fitz) non installe. Installer avec : pip install pymupdf"
        }

    try:
        doc = fitz.open(str(pdf_path))
        total_chars = 0
        for page in doc:
            total_chars += len(page.get_text())
        pages = doc.page_count
        doc.close()
        return {
            "available": True,
            "pages": pages,
            "chars": total_chars,
            "has_text": total_chars > 0
        }
    except Exception as e:
        return {"available": False, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(
        description="Compilation rapide avec LuaLaTeX (profil Reims recommande)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python quick_compile.py --file "mon_cours.tex"
  python quick_compile.py --file "devoir.tex" --passes 2
  python quick_compile.py --file "devoir.tex" --verifier-texte
        """
    )

    parser.add_argument(
        "--file",
        required=True,
        help="Chemin du fichier .tex a compiler"
    )

    parser.add_argument(
        "--passes",
        type=int,
        default=1,
        help="Nombre de passes de compilation (defaut: 1)"
    )

    parser.add_argument(
        "--verifier-texte",
        action="store_true",
        help="Verifie via pymupdf que le PDF genere contient du texte (pages, nombre de caracteres)"
    )

    args = parser.parse_args()

    if args.passes < 1:
        print("⚠️  Nombre de passes < 1, utilisation de 1 passe", file=sys.stderr)
        args.passes = 1

    tex_file = Path(args.file)
    if not tex_file.exists():
        print(f"❌ Fichier non trouve: {args.file}", file=sys.stderr)
        print(json.dumps({
            "status": "error",
            "message": f"Fichier non trouve: {args.file}",
            "pdf_generated": False
        }, ensure_ascii=False))
        sys.exit(1)

    directory = tex_file.parent
    pdf_file = tex_file.with_suffix(".pdf")
    log_file = tex_file.with_suffix(".log")

    # Etat du PDF AVANT compilation (mtime + taille), pour detecter s'il a
    # reellement ete reecrit par CETTE compilation (Friction 1 : ne jamais
    # supprimer le PDF avant compilation, l'utilisateur peut etre en train
    # de le lire).
    pdf_before = pdf_file.stat() if pdf_file.exists() else None

    print(f"⚡ Compilation rapide (LuaLaTeX): {args.file}", file=sys.stderr)
    print(f"   Nombre de passes: {args.passes}", file=sys.stderr)

    try:
        lock_path = acquire_lock(directory, tex_file.name)
    except LockTimeoutError as e:
        print(f"❌ {e}", file=sys.stderr)
        print(json.dumps({
            "status": "error",
            "message": str(e),
            "pdf_generated": pdf_file.exists()
        }, ensure_ascii=False))
        sys.exit(1)

    try:
        return_codes: List[int] = []
        launch_ok = True
        for i in range(args.passes):
            ran_ok, returncode, stdout, stderr = run_lualatex(tex_file, i + 1)
            if not ran_ok:
                launch_ok = False
                print(f"❌ Echec du lancement a la passe {i + 1} : {stderr}", file=sys.stderr)
                break
            return_codes.append(returncode)
            if returncode != 0:
                print(f"⚠️  Code retour {returncode} a la passe {i + 1} (peut se resoudre aux passes suivantes)", file=sys.stderr)

        # Analyse du log systematiquement apres la derniere passe (plus jamais
        # conditionnee a un echec de returncode : c'est le .log qui fait foi)
        log_analysis = analyze_latex_log(log_file)

        pdf_exists_after = pdf_file.exists()
        pdf_fresh = False
        if pdf_exists_after:
            pdf_after = pdf_file.stat()
            if pdf_before is None:
                pdf_fresh = True
            else:
                pdf_fresh = (
                    pdf_after.st_mtime != pdf_before.st_mtime
                    or pdf_after.st_size != pdf_before.st_size
                )

        last_returncode = return_codes[-1] if return_codes else None
        final_pass_ok = launch_ok and last_returncode == 0
        has_log_errors = bool(log_analysis["errors"])

        text_check = None
        if args.verifier_texte and pdf_exists_after:
            text_check = verify_text_content(pdf_file)

        result: Dict[str, Any] = {
            "pdf_generated": pdf_exists_after,
            "pdf_fresh": pdf_fresh,
            "pdf_path": str(pdf_file),
            "passes_run": len(return_codes),
            "return_codes": return_codes,
            "errors": log_analysis["errors"],
            "warnings": log_analysis["warnings"],
        }
        if text_check is not None:
            result["text_check"] = text_check

        if final_pass_ok and not has_log_errors and pdf_fresh:
            result["status"] = "success"
            result["message"] = "Compilation reussie"
            print("\n✅ Compilation reussie", file=sys.stderr)
            print(f"📄 PDF: {pdf_file}", file=sys.stderr)
            exit_code = 0
        elif pdf_fresh:
            result["status"] = "success_with_errors"
            result["message"] = (
                "PDF produit malgre des erreurs signalees dans le .log : "
                "du contenu peut manquer, verifier le rendu avant de considerer le document termine"
            )
            print("\n⚠️  PDF produit malgre des erreurs (voir 'errors'/'warnings' dans le JSON)", file=sys.stderr)
            print(f"📄 PDF: {pdf_file}", file=sys.stderr)
            exit_code = 0
        else:
            result["status"] = "error"
            if not launch_ok:
                result["message"] = "Compilation echouee : lualatex n'a pas pu etre execute"
            elif not pdf_exists_after:
                result["message"] = "Compilation echouee : aucun PDF genere"
            else:
                result["message"] = "Compilation echouee : le PDF existant n'a pas ete reecrit par cette compilation"
            print("\n❌ Compilation echouee", file=sys.stderr)
            exit_code = 1

        if log_analysis["errors"]:
            print("\n📋 Erreurs (fichier:ligne quand disponible):", file=sys.stderr)
            for error in log_analysis["errors"][:10]:
                loc = f"{error['file']}:{error['line']}" if error.get("line") else "?"
                print(f"   {loc}: {error['message']}", file=sys.stderr)
            if len(log_analysis["errors"]) > 10:
                print(f"   ... et {len(log_analysis['errors']) - 10} de plus (voir le champ 'errors' du JSON)", file=sys.stderr)

        if log_analysis["warnings"]:
            print("\n⚠️  Avertissements (echecs muets potentiels) :", file=sys.stderr)
            for warning in log_analysis["warnings"]:
                print(f"   {warning}", file=sys.stderr)

        if result["status"] != "success":
            print("\n💡 Pour deboguer, lancez:", file=sys.stderr)
            print(f'   python ".claude/skills/tex-compiling-skill/scripts/analyze_latex_log.py" --log "{log_file}"', file=sys.stderr)

        print(json.dumps(result, ensure_ascii=False))
        sys.exit(exit_code)

    finally:
        release_lock(lock_path)


if __name__ == "__main__":
    main()

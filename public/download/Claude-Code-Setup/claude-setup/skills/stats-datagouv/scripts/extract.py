#!/usr/bin/env python3
"""Filtre et extrait un sous-ensemble d'un fichier CSV/XLSX brut.

Usage:
    python extract.py \
        --input _data/raw_file.csv \
        --output _data/extract.csv \
        --columns "federation,nb_licences,pct_femmes" \
        --filter "annee==2024" \
        --filter "region==Grand Est" \
        --limit 20 \
        --sort "nb_licences desc"

Produit :
    - _data/extract.csv         (sous-ensemble filtre, separateur ;)
    - _data/extract.json        (meme contenu en JSON)
    - _data/extract_params.json (parametres de filtrage pour reproductibilite)
"""

import argparse
import csv
import json
from pathlib import Path


def detect_separator(filepath: Path) -> str:
    """Detecte le separateur CSV (virgule, point-virgule, tab)."""
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        sample = f.read(4096)
    for sep in [";", ",", "\t"]:
        if sep in sample:
            return sep
    return ","


def read_csv(filepath: Path) -> list[dict]:
    """Lit un CSV et retourne une liste de dicts."""
    sep = detect_separator(filepath)
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f, delimiter=sep)
        return list(reader)


def read_xlsx(filepath: Path) -> list[dict]:
    """Lit un XLSX (necessite openpyxl)."""
    try:
        import openpyxl
    except ImportError:
        print("ERREUR: pip install openpyxl pour lire les fichiers XLSX")
        raise SystemExit(1)
    wb = openpyxl.load_workbook(filepath, read_only=True, data_only=True)
    ws = wb.active
    rows_iter = ws.iter_rows(values_only=True)
    headers = [str(h) for h in next(rows_iter)]
    return [{h: v for h, v in zip(headers, row)} for row in rows_iter]


def load_data(filepath: Path) -> list[dict]:
    """Charge CSV ou XLSX."""
    ext = filepath.suffix.lower()
    if ext in (".xlsx", ".xls"):
        return read_xlsx(filepath)
    return read_csv(filepath)


def apply_filter(rows: list[dict], filter_expr: str) -> list[dict]:
    """Applique un filtre 'colonne==valeur' ou 'colonne!=valeur'."""
    if "!=" in filter_expr:
        col, val = filter_expr.split("!=", 1)
        return [r for r in rows if str(r.get(col.strip(), "")).strip() != val.strip()]
    elif "==" in filter_expr:
        col, val = filter_expr.split("==", 1)
        return [r for r in rows if str(r.get(col.strip(), "")).strip() == val.strip()]
    elif ">=" in filter_expr:
        col, val = filter_expr.split(">=", 1)
        return [r for r in rows if to_num(r.get(col.strip())) >= to_num(val)]
    elif "<=" in filter_expr:
        col, val = filter_expr.split("<=", 1)
        return [r for r in rows if to_num(r.get(col.strip())) <= to_num(val)]
    elif ">" in filter_expr:
        col, val = filter_expr.split(">", 1)
        return [r for r in rows if to_num(r.get(col.strip())) > to_num(val)]
    elif "<" in filter_expr:
        col, val = filter_expr.split("<", 1)
        return [r for r in rows if to_num(r.get(col.strip())) < to_num(val)]
    return rows


def to_num(val):
    """Convertit en nombre si possible."""
    if val is None:
        return 0
    try:
        return float(str(val).replace(",", ".").replace(" ", ""))
    except (ValueError, TypeError):
        return 0


def auto_type(val):
    """Convertit les valeurs en int/float si possible, sinon str."""
    if val is None:
        return None
    s = str(val).strip()
    if not s:
        return None
    # Tenter int
    try:
        return int(s)
    except ValueError:
        pass
    # Tenter float (virgule francaise)
    try:
        return float(s.replace(",", ".").replace(" ", ""))
    except ValueError:
        pass
    return s


def main():
    parser = argparse.ArgumentParser(description="Extrait un sous-ensemble filtre")
    parser.add_argument("--input", required=True, help="Fichier brut (CSV/XLSX)")
    parser.add_argument("--output", required=True, help="Fichier de sortie (.csv)")
    parser.add_argument("--columns", default="", help="Colonnes a garder (virgule)")
    parser.add_argument("--filter", action="append", default=[], help="Filtre col==val (repeatable)")
    parser.add_argument("--limit", type=int, default=0, help="Nombre max de lignes")
    parser.add_argument("--sort", default="", help="Tri: 'colonne asc|desc'")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Charger
    print(f"Lecture: {input_path}")
    rows = load_data(input_path)
    print(f"  {len(rows)} lignes chargees")

    # Filtrer
    for f in args.filter:
        before = len(rows)
        rows = apply_filter(rows, f)
        print(f"  Filtre '{f}': {before} -> {len(rows)} lignes")

    # Selectionner colonnes
    if args.columns:
        cols = [c.strip() for c in args.columns.split(",")]
        rows = [{c: r.get(c) for c in cols} for r in rows]
    else:
        cols = list(rows[0].keys()) if rows else []

    # Trier
    if args.sort:
        parts = args.sort.strip().split()
        sort_col = parts[0]
        reverse = len(parts) > 1 and parts[1].lower() == "desc"
        rows.sort(key=lambda r: to_num(r.get(sort_col, 0)), reverse=reverse)
        print(f"  Tri par '{sort_col}' {'desc' if reverse else 'asc'}")

    # Limiter
    if args.limit > 0:
        rows = rows[:args.limit]
        print(f"  Limite: {args.limit} lignes")

    # Typer les valeurs
    rows = [{k: auto_type(v) for k, v in r.items()} for r in rows]

    # Ecrire CSV (separateur ;)
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=cols, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Sortie CSV: {output_path} ({len(rows)} lignes)")

    # Ecrire JSON
    json_path = output_path.with_suffix(".json")
    json_data = {"columns": cols, "rows": rows}
    json_path.write_text(json.dumps(json_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Sortie JSON: {json_path}")

    # Ecrire params
    params_path = output_path.parent / "extract_params.json"
    params = {
        "input_file": input_path.name,
        "columns": cols,
        "filters": args.filter,
        "sort": args.sort or None,
        "limit": args.limit or None,
        "rows_extracted": len(rows),
        "command": f"python extract.py --input {input_path.name} --output {output_path.name}"
                   + (f" --columns \"{args.columns}\"" if args.columns else "")
                   + "".join(f" --filter \"{f}\"" for f in args.filter)
                   + (f" --limit {args.limit}" if args.limit else "")
                   + (f" --sort \"{args.sort}\"" if args.sort else ""),
    }
    params_path.write_text(json.dumps(params, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Params: {params_path}")


if __name__ == "__main__":
    main()

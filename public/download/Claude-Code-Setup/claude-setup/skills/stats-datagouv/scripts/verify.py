#!/usr/bin/env python3
"""Verifie la chaine de verite : extract.csv + computed.json → OK/FAIL.

Usage:
    python verify.py _data/

Lit _data/extract.json et _data/computed.json, recalcule chaque operation
et compare aux resultats declares.
"""

import json
import sys
from pathlib import Path
from statistics import mean, median, stdev, variance


def load(data_dir: Path):
    """Charge extract.json, computed.json et source.json."""
    extract = json.loads((data_dir / "extract.json").read_text(encoding="utf-8"))
    computed = json.loads((data_dir / "computed.json").read_text(encoding="utf-8"))
    source = json.loads((data_dir / "source.json").read_text(encoding="utf-8"))
    return extract, computed, source


def col_values(rows: list[dict], col: str) -> list[float]:
    """Extrait les valeurs numeriques d'une colonne."""
    vals = []
    for r in rows:
        v = r.get(col)
        if v is not None:
            try:
                vals.append(float(v))
            except (ValueError, TypeError):
                pass
    return vals


def approx_equal(a, b, tol=1e-6):
    """Comparaison avec tolerance."""
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        if a == b:
            return True
        denom = max(abs(a), abs(b), 1)
        return abs(a - b) / denom < tol
    return a == b


# --- Operations ---

def op_sum(values, **kw):
    return sum(values)

def op_mean(values, **kw):
    return mean(values)

def op_median(values, **kw):
    return median(sorted(values))

def op_min(values, **kw):
    return min(values)

def op_max(values, **kw):
    return max(values)

def op_range(values, **kw):
    return max(values) - min(values)

def op_count(values, **kw):
    return len(values)

def op_ratio(values, **kw):
    return values[0] / values[1]

def op_percentage(values, **kw):
    return (values[0] / values[1]) * 100

def op_frequency(values, **kw):
    return values[0] / values[1]

def op_complement(values, **kw):
    return 1 - values[0]

def op_variance(values, **kw):
    return variance(values)

def op_stdev(values, **kw):
    return stdev(values)

def op_q1(values, **kw):
    s = sorted(values)
    n = len(s)
    return median(s[:n // 2])

def op_q3(values, **kw):
    s = sorted(values)
    n = len(s)
    return median(s[(n + 1) // 2:])

def op_iqr(values, **kw):
    return op_q3(values) - op_q1(values)

def op_product(values, **kw):
    r = 1
    for v in values:
        r *= v
    return r

def op_subtract(values, **kw):
    return values[0] - values[1]

def op_add(values, **kw):
    return values[0] + values[1]


OPERATIONS = {
    "sum": op_sum, "mean": op_mean, "median": op_median,
    "min": op_min, "max": op_max, "range": op_range, "count": op_count,
    "ratio": op_ratio, "percentage": op_percentage, "frequency": op_frequency,
    "complement": op_complement, "variance": op_variance, "stdev": op_stdev,
    "q1": op_q1, "q3": op_q3, "iqr": op_iqr,
    "product": op_product, "subtract": op_subtract, "add": op_add,
}


def resolve_values(calc: dict, rows: list[dict]) -> list[float]:
    """Determine les valeurs d'entree pour un calcul.

    Priorite :
    1. 'input_values' explicites dans computed.json
    2. 'column' → extraire toutes les valeurs de cette colonne depuis extract
    """
    if "input_values" in calc:
        return [float(v) for v in calc["input_values"]]
    if "column" in calc:
        return col_values(rows, calc["column"])
    return []


def main():
    if len(sys.argv) < 2:
        print("Usage: python verify.py <data_dir>")
        sys.exit(1)

    data_dir = Path(sys.argv[1])
    extract, computed, source = load(data_dir)
    rows = extract["rows"]

    print(f"Dataset : {source.get('dataset_title', '?')}")
    print(f"Source  : {source.get('datagouv_url', source.get('download_url', '?'))}")
    print(f"Date    : {source.get('download_date', '?')}")
    print(f"Lignes  : {len(rows)}")
    print(f"Colonnes: {extract.get('columns', [])}")
    print("-" * 60)

    passed = 0
    failed = 0
    errors = []

    for calc in computed["calculs"]:
        q = calc["question"]
        op_name = calc["operation"].split("(")[0].strip()
        expected = calc["result"]
        values = resolve_values(calc, rows)

        if op_name not in OPERATIONS:
            print(f"  ???  {q}: operation inconnue '{op_name}'")
            failed += 1
            errors.append(q)
            continue

        try:
            actual = OPERATIONS[op_name](values)
            if approx_equal(actual, expected):
                print(f"  OK   {q}: {calc['operation']} = {actual}")
                passed += 1
            else:
                print(f"  FAIL {q}: {calc['operation']} attendu={expected} obtenu={actual}")
                failed += 1
                errors.append(q)
        except Exception as e:
            print(f"  ERR  {q}: {calc['operation']} -- {e}")
            failed += 1
            errors.append(q)

    print("-" * 60)
    total = passed + failed
    print(f"Resultat : {passed}/{total} OK")
    if errors:
        print(f"Echecs   : {', '.join(errors)}")
        sys.exit(1)
    else:
        print("Chaine de verite : VALIDEE")
        sys.exit(0)


if __name__ == "__main__":
    main()

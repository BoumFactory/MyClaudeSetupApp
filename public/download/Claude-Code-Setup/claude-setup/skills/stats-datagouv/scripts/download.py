#!/usr/bin/env python3
"""Telecharge un fichier brut depuis data.gouv.fr et genere source.json.

Usage:
    python download.py \
        --url "https://www.data.gouv.fr/fr/datasets/r/RESOURCE_ID" \
        --output _data/raw_file.csv \
        --source-json _data/source.json \
        --dataset-id "DATASET_ID" \
        --dataset-title "Titre du dataset" \
        --resource-id "RESOURCE_ID" \
        --producer "Producteur"
"""

import argparse
import json
import urllib.request
import ssl
from datetime import datetime
from pathlib import Path


def download(url: str, output: Path) -> int:
    """Telecharge l'URL vers output. Retourne la taille en octets."""
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent": "stats-datagouv-skill/0.3"})
    with urllib.request.urlopen(req, context=ctx) as resp:
        data = resp.read()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(data)
    return len(data)


def write_source(path: Path, **kwargs) -> None:
    """Ecrit source.json avec les metadonnees de provenance."""
    source = {
        "dataset_id": kwargs.get("dataset_id", ""),
        "dataset_title": kwargs.get("dataset_title", ""),
        "resource_id": kwargs.get("resource_id", ""),
        "producer": kwargs.get("producer", ""),
        "download_url": kwargs.get("url", ""),
        "datagouv_url": f"https://www.data.gouv.fr/fr/datasets/{kwargs.get('dataset_id', '')}",
        "download_date": datetime.now().isoformat(timespec="seconds"),
        "raw_file": kwargs.get("raw_filename", ""),
        "raw_file_size_bytes": kwargs.get("size", 0),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(source, indent=2, ensure_ascii=False), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Telecharge un fichier data.gouv.fr")
    parser.add_argument("--url", required=True, help="URL directe du fichier")
    parser.add_argument("--output", required=True, help="Chemin de sortie du fichier brut")
    parser.add_argument("--source-json", required=True, help="Chemin de sortie de source.json")
    parser.add_argument("--dataset-id", default="", help="ID du dataset")
    parser.add_argument("--dataset-title", default="", help="Titre du dataset")
    parser.add_argument("--resource-id", default="", help="ID de la ressource")
    parser.add_argument("--producer", default="", help="Producteur des donnees")
    args = parser.parse_args()

    output = Path(args.output)
    print(f"Telechargement: {args.url}")
    size = download(args.url, output)
    print(f"Fichier sauvegarde: {output} ({size:,} octets)")

    write_source(
        Path(args.source_json),
        url=args.url,
        dataset_id=args.dataset_id,
        dataset_title=args.dataset_title,
        resource_id=args.resource_id,
        producer=args.producer,
        raw_filename=output.name,
        size=size,
    )
    print(f"Source: {args.source_json}")


if __name__ == "__main__":
    main()

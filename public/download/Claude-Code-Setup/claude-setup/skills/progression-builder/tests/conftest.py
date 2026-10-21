"""Configuration pytest commune.

Ajoute le dossier `scripts/` au sys.path pour que les tests puissent
importer `generate_vierge`, `apply_progression`, `validate_progression`
et `_utils` directement.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

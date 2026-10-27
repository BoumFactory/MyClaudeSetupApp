#!/usr/bin/env python3
"""
MCP Server pour la création de documents LaTeX à partir de modèles.
Version simplifiée avec 3 fonctions principales : list, info, create
Gestion des préférences utilisateur et remplacement intelligent des balises.
"""

import json
import logging
import sys
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger("document-creator-server")

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    logger.error("Erreur: Le package 'mcp' n'est pas installé. Installez-le avec: pip install mcp")
    sys.exit(1)

# Créer l'instance du serveur MCP
mcp = FastMCP("document-creator-server")

# Configuration des chemins
TEMPLATES_PATH = Path(__file__).parent.parent / "datas" / "latex-modeles"
USER_PREFERENCES_PATH = Path(__file__).parent.parent / "datas" / "create-document-user-preferences.json"

# Configuration du workspace depuis mcp.json
def get_workspace_path() -> Path:
    """Charge le workspace path depuis mcp.json."""
    config_path = Path(__file__).parent / "mcp.json"
    try:
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                workspace_str = config.get('document_creator_server', {}).get('workspace_path', '')
                if workspace_str:
                    return Path(workspace_str)
    except Exception as e:
        logger.warning(f"Erreur lors du chargement de mcp.json: {e}")
    
    # Fallback vers chemin relatif
    return Path(__file__).parent.parent.parent

WORKSPACE_PATH = get_workspace_path()

# Cache pour les remplacements choisis
_field_choices_cache = {}

def load_user_preferences() -> Dict[str, Any]:
    """Charge les préférences utilisateur par défaut."""
    if USER_PREFERENCES_PATH.exists():
        try:
            with open(USER_PREFERENCES_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Erreur lors du chargement des préférences: {e}")
    
    return {
        "default_values": {},
        "favorite_options": {},
        "create_folder": True,
        "create_images_folder": False,
        "create_annexes_folder": False,
        "create_sections_folder": False,
        "create_figures_file": True
    }

def save_user_preferences(preferences: Dict[str, Any]) -> bool:
    """Sauvegarde les préférences utilisateur."""
    try:
        USER_PREFERENCES_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(USER_PREFERENCES_PATH, 'w', encoding='utf-8') as f:
            json.dump(preferences, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde des préférences: {e}")
        return False

def analyze_template_fields(template_path: Path) -> Dict[str, Any]:
    """
    Analyse un modèle pour extraire les champs paramétrables.
    Retourne un dictionnaire avec les champs et leurs options par défaut.
    """
    if not template_path.exists():
        return {"error": f"Modèle non trouvé: {template_path}"}
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Convention des templates : un champ s'écrit « % nom_champ » ou
        # « % nom_champ : option1, option2 », avec un espace après le %.
        # Un commentaire LaTeX ordinaire s'écrit collé (« %commentaire ») pour
        # ne pas être pris pour un champ — d'où le \s+ et non \s*.
        # Pattern pour détecter les champs avec options : % nom_champ : option1, option2, ...
        pattern_with_options = r'%\s+(\w+)\s*:\s*([^%\n]+)'
        # Pattern pour détecter tous les champs (avec ou sans :)
        pattern_all_fields = r'%\s+(\w+)'
        
        fields = {}
        
        # D'abord, trouver tous les champs avec leurs définitions d'options
        for match in re.finditer(pattern_with_options, content):
            field_name = match.group(1)
            options_str = match.group(2).strip()
            
            # Si le champ contient des virgules, c'est une liste d'options
            if ',' in options_str:
                options = [opt.strip() for opt in options_str.split(',')]
                fields[field_name] = {
                    "type": "choice",
                    "options": options,
                    "default": options[0] if options else ""
                }
            else:
                # Sinon c'est une valeur par défaut simple
                fields[field_name] = {
                    "type": "text",
                    "default": options_str
                }
        
        # Ensuite, trouver tous les champs utilisés (même sans définition)
        all_field_names = set(re.findall(pattern_all_fields, content))
        
        # Ajouter les champs sans définition explicite
        for field_name in all_field_names:
            if field_name not in fields:
                fields[field_name] = {
                    "type": "text",
                    "default": ""
                }
        
        return fields
        
    except Exception as e:
        return {"error": f"Erreur lors de l'analyse du modèle: {str(e)}"}

def compute_field_requirements(fields: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fonction UNIQUE de calcul du caractère requis/optionnel de chaque champ.
    Partagée par get_template_info() et create_document() pour garantir que
    les deux commandes détectent exactement les mêmes champs (même liste,
    même définition de « requis »).

    Règle de décision :
    - Un champ « choice » n'est jamais bloquant : sa première option sert de
      valeur par défaut, même si cette option est une chaîne vide (ex.
      `% supplement : ,\\tableofcontents` → défaut `""`).
    - Un champ « text » est requis seulement si son défaut est une chaîne
      vide (aucune valeur exploitable sans intervention de l'appelant).

    Returns:
        Dict avec :
        - "fields" : les champs enrichis d'une clé "required" (bool)
        - "required_fields" : liste des noms de champs réellement obligatoires
        - "example_fields_file" : dict prêt à écrire dans un fields-file JSON
          (valeurs par défaut quand elles existent, placeholder sinon)
    """
    enriched: Dict[str, Any] = {}
    required_fields: List[str] = []
    example_fields_file: Dict[str, str] = {}

    for field_name, field_info in fields.items():
        info = dict(field_info)
        if info.get("type") == "choice":
            options = info.get("options", [])
            info["required"] = False
            non_empty_options = [opt for opt in options if opt.strip()]
            example_fields_file[field_name] = non_empty_options[0] if non_empty_options else (options[0] if options else "")
        else:
            default = info.get("default", "")
            if default:
                info["required"] = False
                example_fields_file[field_name] = default
            else:
                info["required"] = True
                required_fields.append(field_name)
                example_fields_file[field_name] = f"<A_COMPLETER:{field_name}>"
        enriched[field_name] = info

    return {
        "fields": enriched,
        "required_fields": required_fields,
        "example_fields_file": example_fields_file,
    }


# Largeur mesurée de la boîte de niveau (bfcours-exoplus.sty, \chapitre/\chapEval) :
# tcolorbox de 1,5 cm de large (42,68 pt), contenu en \Large. Mesure empirique
# (pdflatex, \settowidth) : "STI2D" (5 caractères) tient (40,9 pt < 42,7 pt),
# "Techno" (6 caractères) déborde déjà légèrement (43,9 pt > 42,7 pt). Seuil
# fixé à 5 caractères rendus : au-delà, avertissement non bloquant.
NIVEAU_BOX_CHAR_THRESHOLD = 5


def estimate_rendered_length(value: str) -> int:
    """
    Estime grossièrement le nombre de caractères RENDUS d'une valeur LaTeX
    (ex: "$\\mathbf{2^{\\text{nde}}}$" -> "2nde", 4 caractères), en retirant
    le mode math et les commandes de mise en forme usuelles. Approximation
    volontairement prudente (elle surestime plutôt que sous-estime).
    """
    text = value.replace('$', '')
    text = re.sub(r'\\[a-zA-Z]+', '', text)
    text = re.sub(r'[{}\^_\\]', '', text)
    return len(text.strip())


def _consume_balanced_groups(content: str, start: int, n_groups: int) -> int:
    """
    À partir de `start`, avance de `n_groups` groupes équilibrés consécutifs
    (`[...]` ou `{...}`, espaces/sauts de ligne ignorés entre eux). Renvoie
    l'indice juste après le dernier groupe consommé, ou `start` si la
    structure attendue n'est pas trouvée (par prudence, aucune modification
    n'est alors appliquée par l'appelant).
    """
    i = start
    n = len(content)
    consumed = 0

    while consumed < n_groups:
        while i < n and content[i] in ' \t\r\n':
            i += 1
        if i >= n or content[i] not in '{[':
            break
        opener = content[i]
        closer = '}' if opener == '{' else ']'
        depth = 1
        i += 1
        while i < n and depth > 0:
            if content[i] == opener:
                depth += 1
            elif content[i] == closer:
                depth -= 1
            i += 1
        consumed += 1

    return i if consumed == n_groups else start


def protect_chapitre_blank_lines(content: str, macro_names=('chapitre', 'chapEval')) -> str:
    """
    Filet de sécurité : \\chapitre et \\chapEval sont déclarées avec des
    arguments xparse de type "m" (NON "+m"), donc NON longs — une ligne
    totalement vide à l'intérieur d'un de leurs 6 groupes
    ([niveau]{thème}{établissement}{nom}{supplément}{type}) devient un \\par
    et casse la compilation : « Paragraph ended before \\chapitre was
    complete ». Repère chaque appel et protège les lignes vides qu'il
    contient en leur ajoutant un simple '%' (qui absorbe la fin de ligne sans
    déclencher de paragraphe), sans toucher au reste du contenu.
    """
    macro_pattern = re.compile(r'\\(?:' + '|'.join(macro_names) + r')\b')
    out = []
    last_end = 0

    for match in macro_pattern.finditer(content):
        call_end = _consume_balanced_groups(content, match.end(), n_groups=6)
        out.append(content[last_end:match.start()])
        segment = content[match.start():call_end]
        segment = re.sub(r'(?m)^([ \t]*)$', r'\1%', segment)
        out.append(segment)
        last_end = call_end

    out.append(content[last_end:])
    return ''.join(out)


def replace_fields_in_template(content: str, field_values: Dict[str, str]) -> str:
    """
    Remplace TOUTES les occurrences des balises % nom_champ par les valeurs fournies.
    Important: remplace aussi les champs sans : après leur première définition.
    """
    # Pour chaque champ fourni, remplacer toutes ses occurrences
    for field_name, value in field_values.items():
        # Utiliser une fonction lambda pour éviter les problèmes d'échappement
        replacement_value = f'{value}%'
        
        # Pattern pour remplacer % field_name (avec ou sans : et ce qui suit)
        # \s+ et non \s* : un commentaire collé (%mot) n'est pas un champ.
        # Remplace d'abord les définitions avec :
        pattern_with_colon = rf'%\s+{re.escape(field_name)}\s*:[^%\n]*'
        content = re.sub(pattern_with_colon, lambda m: replacement_value, content)

        # Puis remplace toutes les autres occurrences sans :
        pattern_without_colon = rf'%\s+{re.escape(field_name)}(?!\s*:)'
        content = re.sub(pattern_without_colon, lambda m: replacement_value, content)
    
    return content

def create_folder_structure(base_path: Path, document_name: str, options: Dict[str, bool]) -> Path:
    """Crée la structure de dossiers pour le document."""
    if options.get("create_folder", True):
        doc_path = base_path / document_name
    else:
        doc_path = base_path
    
    doc_path.mkdir(parents=True, exist_ok=True)
    
    # Créer les sous-dossiers optionnels
    if options.get("create_images_folder", False):
        (doc_path / "images").mkdir(exist_ok=True)
    
    if options.get("create_annexes_folder", False):
        (doc_path / "annexes").mkdir(exist_ok=True)
    
    if options.get("create_sections_folder", False):
        (doc_path / "sections").mkdir(exist_ok=True)
    
    return doc_path

def detect_input_files(content: str) -> List[str]:
    """Détecte les fichiers inclus via \\input{} ou \\include{}."""
    input_files = []
    pattern = r"\\(?:input|include|inputImprim)\{(.+?)\}"
    matches = re.findall(pattern, content)
    
    for match in matches:
        # Ignorer les commandes spéciales
        if match not in [r'\impressFileName', r'\enonce', r'\solution']:
            # Nettoyer le nom de fichier
            file_name = match.replace('.tex', '')
            if file_name not in input_files:
                input_files.append(file_name)
    
    return input_files

def create_auxiliary_files(doc_path: Path, input_files: List[str], create_figures: bool = True):
    """Crée les fichiers auxiliaires détectés."""
    for file_name in input_files:
        file_path = doc_path / f"{file_name}.tex"
        if not file_path.exists():
            file_path.touch()
            logger.info(f"Fichier créé: {file_path}")
    
    # Créer le fichier de figures si demandé
    if create_figures:
        figures_file = doc_path / "enonce_figures.tex"
        if not figures_file.exists():
            figures_file.write_text("% Fichier pour les figures de l'énoncé\n", encoding='utf-8')

def create_claude_instructions(doc_path: Path, template_name: str, fields: Dict[str, str]):
    """Crée un fichier CLAUDE.md avec les instructions pour Claude."""
    instructions = f"""# Instructions pour Claude - Document {doc_path.name}

## Modèle utilisé
- **Modèle**: {template_name}
- **Date de création**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Paramètres du document
"""
    
    for field, value in fields.items():
        instructions += f"- **{field}**: {value}\n"
    
    instructions += """

## Structure du document
Ce document a été créé automatiquement à partir d'un modèle LaTeX.
Les fichiers suivants peuvent nécessiter votre attention:

1. **Fichier principal**: `{}.tex`
2. **Fichiers inclus**: Vérifiez les fichiers créés via \\input{{}}
3. **Images**: Placez les images dans le dossier `images/` si créé
4. **Annexes**: Placez les annexes dans le dossier `annexes/` si créé

## Compilation
Pour compiler ce document:
```bash
pdflatex {}.tex
```

## Notes supplémentaires
- Respectez la structure bfcours si applicable
- Utilisez les environnements didactiques appropriés
- Vérifiez la cohérence pédagogique du contenu
""".format(doc_path.name, doc_path.name)
    
    claude_file = doc_path / "CLAUDE.md"
    claude_file.write_text(instructions, encoding='utf-8')

# ============================================================================
# FONCTIONS MCP PRINCIPALES
# ============================================================================

@mcp.tool()
async def list_templates() -> str:
    """
    Liste tous les modèles disponibles.
    
    Returns:
        JSON string avec la liste des modèles disponibles
    """
    try:
        if not TEMPLATES_PATH.exists():
            return json.dumps({
                "status": "error",
                "message": f"Le dossier des modèles n'existe pas: {TEMPLATES_PATH}"
            }, ensure_ascii=False)
        
        templates = []
        for template_file in TEMPLATES_PATH.glob("*.tex"):
            templates.append({
                "name": template_file.stem,
                "file": template_file.name,
                "size": template_file.stat().st_size
            })
        
        return json.dumps({
            "status": "success",
            "templates": templates,
            "total": len(templates),
            "path": str(TEMPLATES_PATH)
        }, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": str(e)
        }, ensure_ascii=False)

@mcp.tool()
async def get_template_info(template_name: str) -> str:
    """
    Obtient les informations détaillées d'un modèle, incluant tous les champs paramétrables.
    
    Args:
        template_name: Nom du modèle à analyser (sans extension .tex)
    
    Returns:
        JSON string avec la structure des champs à remplir
    """
    try:
        template_path = TEMPLATES_PATH / f"{template_name}.tex"
        
        if not template_path.exists():
            return json.dumps({
                "status": "error",
                "message": f"Modèle '{template_name}' non trouvé"
            }, ensure_ascii=False)
        
        # Analyser les champs du modèle (fonction UNIQUE, partagée avec create_document)
        fields = analyze_template_fields(template_path)

        if "error" in fields:
            return json.dumps({
                "status": "error",
                "message": fields["error"]
            }, ensure_ascii=False)

        # Calcul requis/optionnel + exemple de fields-file : même fonction que create_document,
        # pour que get_template_info annonce TOUJOURS les mêmes champs manquants.
        requirements = compute_field_requirements(fields)
        fields = requirements["fields"]
        example_fields_file = requirements["example_fields_file"]

        # Charger les préférences utilisateur
        user_prefs = load_user_preferences()

        # Fusionner avec les préférences utilisateur
        for field_name, field_info in fields.items():
            # Si l'utilisateur a une valeur par défaut pour ce champ
            if field_name in user_prefs.get("default_values", {}):
                field_info["user_default"] = user_prefs["default_values"][field_name]
                example_fields_file[field_name] = user_prefs["default_values"][field_name]

            # Si c'est un champ à choix multiple et que l'utilisateur a un favori
            if field_info["type"] == "choice" and field_name in user_prefs.get("favorite_options", {}):
                favorite = user_prefs["favorite_options"][field_name]
                if favorite in field_info["options"]:
                    field_info["user_favorite"] = favorite
                    example_fields_file[field_name] = favorite

        return json.dumps({
            "status": "success",
            "template": template_name,
            "fields": fields,
            "required_fields": requirements["required_fields"],
            "example_fields_file": example_fields_file,
            "structure_options": {
                "create_folder": user_prefs.get("create_folder", True),
                "create_images_folder": user_prefs.get("create_images_folder", False),
                "create_annexes_folder": user_prefs.get("create_annexes_folder", False),
                "create_sections_folder": user_prefs.get("create_sections_folder", False),
                "create_figures_file": user_prefs.get("create_figures_file", True),
                "include_claude_instructions": False
            },
            "instructions": (
                "Les champs listés dans 'required_fields' sont obligatoires (aucun défaut "
                "exploitable) : create_document échoue si l'un d'eux manque. Copier "
                "'example_fields_file' dans un fichier JSON (outil Write), compléter les "
                "valeurs <A_COMPLETER:...>, puis lancer create_document.py --fields-file <chemin> "
                "(évite les problèmes d'échappement des antislashs LaTeX en Bash)."
            )
        }, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": str(e)
        }, ensure_ascii=False)

@mcp.tool()
async def create_document(
    destination_path: str,
    document_name: str,
    template_name: str,
    field_values: Dict[str, str],
    create_folder: bool = True,
    create_images_folder: bool = False,
    create_annexes_folder: bool = False,
    create_sections_folder: bool = False,
    create_figures_file: bool = True,
    include_claude_instructions: bool = False
) -> str:
    """
    Crée un document à partir d'un modèle avec les paramètres fournis.
    
    Args:
        destination_path: Chemin où créer le document
        document_name: Nom du document (sans extension)
        template_name: Nom du modèle à utiliser
        field_values: Dictionnaire des valeurs pour chaque champ du modèle
        create_folder: Créer un dossier pour le document
        create_images_folder: Créer le dossier images
        create_annexes_folder: Créer le dossier annexes
        create_sections_folder: Créer le dossier sections
        create_figures_file: Créer le fichier enonce_figures.tex
        include_claude_instructions: Inclure un fichier CLAUDE.md
    
    Returns:
        JSON string avec le résultat de la création
    """
    try:
        # Vérifier que le modèle existe
        template_path = TEMPLATES_PATH / f"{template_name}.tex"
        if not template_path.exists():
            return json.dumps({
                "status": "error",
                "message": f"Modèle '{template_name}' non trouvé",
                "available_templates": [f.stem for f in TEMPLATES_PATH.glob("*.tex")]
            }, ensure_ascii=False)
        
        # Analyser les champs requis du modèle (fonction UNIQUE, partagée avec get_template_info)
        template_fields = analyze_template_fields(template_path)
        if "error" in template_fields:
            return json.dumps({
                "status": "error",
                "message": template_fields["error"]
            }, ensure_ascii=False)

        requirements = compute_field_requirements(template_fields)

        # Vérifier que tous les champs requis sont fournis AVANT toute écriture sur le disque
        # (ni dossier, ni fichier ne doit exister si la création échoue ici).
        missing_fields = [
            field_name for field_name in requirements["required_fields"]
            if field_name not in field_values
        ]

        if missing_fields:
            return json.dumps({
                "status": "error",
                "message": "Champs manquants : aucun fichier n'a été créé",
                "missing_fields": missing_fields,
                "example_fields_file": requirements["example_fields_file"],
                "hint": (
                    "Compléter les valeurs <A_COMPLETER:...> ci-dessus dans un fichier JSON "
                    "(outil Write), puis relancer create_document.py --fields-file <chemin>. "
                    "Ne jamais écrire le document ou le fichier maître à la main à la place du script."
                )
            }, ensure_ascii=False, indent=2)

        # Compléter les champs optionnels non fournis (valeur par défaut / première option)
        for field_name, field_info in template_fields.items():
            if field_name not in field_values:
                if field_info["type"] == "choice":
                    field_values[field_name] = field_info["options"][0] if field_info.get("options") else ""
                else:
                    field_values[field_name] = field_info.get("default", "")

        # Avertissement non bloquant : le niveau risque de déborder de sa boîte (1,5 cm, \Large)
        warnings: List[str] = []
        if "niveau" in field_values:
            rendered_len = estimate_rendered_length(field_values["niveau"])
            if rendered_len > NIVEAU_BOX_CHAR_THRESHOLD:
                warnings.append(
                    f"Niveau '{field_values['niveau']}' : environ {rendered_len} caractères rendus, "
                    f"au-delà du seuil de {NIVEAU_BOX_CHAR_THRESHOLD} caractères mesuré sur la boîte "
                    f"de niveau de \\chapitre/\\chapEval (largeur fixe 1,5 cm, police \\Large). Le "
                    f"texte risque de déborder silencieusement dans le bandeau : vérifier le PDF, "
                    f"envisager \\shortstack sur deux lignes (voir bfcours-conventions.md)."
                )

        # Créer le chemin de destination
        # Logique adaptative : gère 3 cas
        #   1. Chemin absolu (ex: "C:\...\1. Cours\Tle\...") → utilisé tel quel
        #   2. Chemin relatif commençant par le nom du workspace (ex: "1. Cours/Tle/...")
        #      → on retire ce préfixe pour éviter le doublon ("1. Cours/1. Cours/...")
        #   3. Chemin relatif simple (ex: "Tle_math_comp/Tests/...")
        #      → résolu relativement à WORKSPACE_PATH
        dest_path = Path(destination_path)
        if not dest_path.is_absolute():
            workspace_name = WORKSPACE_PATH.name  # "1. Cours" en pratique
            parts = dest_path.parts
            # Si le premier segment du chemin relatif correspond au nom du workspace,
            # on le retire pour éviter le doublon.
            if parts and parts[0] == workspace_name:
                logger.info(
                    f"Chemin relatif normalisé : préfixe '{workspace_name}/' retiré "
                    f"de '{destination_path}' (workspace_path contient déjà ce dossier)"
                )
                dest_path = Path(*parts[1:]) if len(parts) > 1 else Path('.')
            dest_path = WORKSPACE_PATH / dest_path
        
        # Créer la structure de dossiers
        options = {
            "create_folder": create_folder,
            "create_images_folder": create_images_folder,
            "create_annexes_folder": create_annexes_folder,
            "create_sections_folder": create_sections_folder
        }
        doc_path = create_folder_structure(dest_path, document_name, options)
        
        # Lire le contenu du modèle
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remplacer TOUS les champs par leurs valeurs
        content = replace_fields_in_template(content, field_values)

        # Filet de sécurité : neutraliser toute ligne vide à l'intérieur des appels
        # \chapitre[...]/\chapEval[...] (arguments xparse non longs -> \par y est fatal :
        # "Paragraph ended before \chapitre was complete").
        content = protect_chapitre_blank_lines(content)

        # Détecter les fichiers à créer
        input_files = detect_input_files(content)
        
        # Créer le fichier principal
        main_file = doc_path / f"{document_name}.tex"
        with open(main_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Créer les fichiers auxiliaires
        create_auxiliary_files(doc_path, input_files, create_figures_file)
        
        # Créer les instructions Claude si demandé
        if include_claude_instructions:
            create_claude_instructions(doc_path, template_name, field_values)
        
        # Préparer le résumé
        created_files = [f"{document_name}.tex"]
        created_files.extend([f"{f}.tex" for f in input_files])
        if create_figures_file:
            created_files.append("enonce_figures.tex")
        if include_claude_instructions:
            created_files.append("CLAUDE.md")
        
        created_folders = []
        if create_folder:
            created_folders.append(document_name)
        if create_images_folder:
            created_folders.append("images")
        if create_annexes_folder:
            created_folders.append("annexes")
        if create_sections_folder:
            created_folders.append("sections")
        
        return json.dumps({
            "status": "success",
            "message": "Document créé avec succès",
            "path": str(doc_path),
            "main_file": str(main_file),
            "created_files": created_files,
            "created_folders": created_folders,
            "field_replacements": field_values,
            "warnings": warnings,
            "next_steps": [
                "Éditez les fichiers créés pour ajouter le contenu",
                "Compilez avec pdflatex pour générer le PDF",
                "Vérifiez que tous les \\input{} pointent vers des fichiers existants"
            ]
        }, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": str(e),
            "type": type(e).__name__
        }, ensure_ascii=False)

# ============================================================================
# FONCTIONS DE GESTION DES PRÉFÉRENCES
# ============================================================================

@mcp.tool()
async def get_user_preferences() -> str:
    """
    Récupère les préférences utilisateur actuelles.
    
    Returns:
        JSON string avec les préférences utilisateur
    """
    try:
        prefs = load_user_preferences()
        return json.dumps({
            "status": "success",
            "preferences": prefs,
            "file_path": str(USER_PREFERENCES_PATH)
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": str(e)
        }, ensure_ascii=False)

@mcp.tool()
async def update_user_preferences(
    default_values: Optional[Dict[str, str]] = None,
    favorite_options: Optional[Dict[str, str]] = None,
    structure_options: Optional[Dict[str, bool]] = None
) -> str:
    """
    Met à jour les préférences utilisateur.
    
    Args:
        default_values: Valeurs par défaut pour les champs texte
        favorite_options: Options favorites pour les champs à choix
        structure_options: Options de structure (create_folder, etc.)
    
    Returns:
        JSON string avec le résultat de la mise à jour
    """
    try:
        # Charger les préférences actuelles
        prefs = load_user_preferences()
        
        # Mettre à jour les valeurs par défaut
        if default_values:
            prefs["default_values"].update(default_values)
        
        # Mettre à jour les options favorites
        if favorite_options:
            prefs["favorite_options"].update(favorite_options)
        
        # Mettre à jour les options de structure
        if structure_options:
            for key, value in structure_options.items():
                if key in ["create_folder", "create_images_folder", "create_annexes_folder", 
                          "create_sections_folder", "create_figures_file"]:
                    prefs[key] = value
        
        # Sauvegarder
        if save_user_preferences(prefs):
            return json.dumps({
                "status": "success",
                "message": "Préférences mises à jour",
                "preferences": prefs
            }, ensure_ascii=False, indent=2)
        else:
            return json.dumps({
                "status": "error",
                "message": "Erreur lors de la sauvegarde"
            }, ensure_ascii=False)
            
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": str(e)
        }, ensure_ascii=False)

@mcp.tool()
async def add_user_habit(field_name: str, value: str, is_choice: bool = False) -> str:
    """
    Ajoute une habitude utilisateur (valeur par défaut ou option favorite).
    
    Args:
        field_name: Nom du champ
        value: Valeur à enregistrer
        is_choice: True si c'est un champ à choix multiple, False pour un champ texte
    
    Returns:
        JSON string avec le résultat
    """
    try:
        prefs = load_user_preferences()
        
        if is_choice:
            prefs["favorite_options"][field_name] = value
            message = f"Option favorite '{value}' enregistrée pour le champ '{field_name}'"
        else:
            prefs["default_values"][field_name] = value
            message = f"Valeur par défaut '{value}' enregistrée pour le champ '{field_name}'"
        
        if save_user_preferences(prefs):
            return json.dumps({
                "status": "success",
                "message": message,
                "field": field_name,
                "value": value
            }, ensure_ascii=False)
        else:
            return json.dumps({
                "status": "error",
                "message": "Erreur lors de la sauvegarde"
            }, ensure_ascii=False)
            
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": str(e)
        }, ensure_ascii=False)

@mcp.tool()
async def remove_user_habit(field_name: str, habit_type: str = "auto") -> str:
    """
    Supprime une habitude utilisateur spécifique.
    
    Args:
        field_name: Nom du champ dont supprimer l'habitude
        habit_type: Type d'habitude ("default", "favorite", "auto" pour détecter automatiquement)
    
    Returns:
        JSON string avec le résultat
    """
    try:
        prefs = load_user_preferences()
        removed = []
        
        # Auto-détection du type si "auto"
        if habit_type == "auto":
            if field_name in prefs.get("default_values", {}):
                del prefs["default_values"][field_name]
                removed.append("valeur par défaut")
            
            if field_name in prefs.get("favorite_options", {}):
                del prefs["favorite_options"][field_name]
                removed.append("option favorite")
                
        elif habit_type == "default":
            if field_name in prefs.get("default_values", {}):
                del prefs["default_values"][field_name]
                removed.append("valeur par défaut")
                
        elif habit_type == "favorite":
            if field_name in prefs.get("favorite_options", {}):
                del prefs["favorite_options"][field_name]
                removed.append("option favorite")
        else:
            return json.dumps({
                "status": "error",
                "message": f"Type d'habitude invalide: {habit_type}. Utilisez 'default', 'favorite' ou 'auto'"
            }, ensure_ascii=False)
        
        if not removed:
            return json.dumps({
                "status": "warning",
                "message": f"Aucune habitude trouvée pour le champ '{field_name}'"
            }, ensure_ascii=False)
        
        # Sauvegarder les modifications
        if save_user_preferences(prefs):
            message = f"Supprimé pour le champ '{field_name}': {', '.join(removed)}"
            return json.dumps({
                "status": "success",
                "message": message,
                "field": field_name,
                "removed": removed
            }, ensure_ascii=False)
        else:
            return json.dumps({
                "status": "error",
                "message": "Erreur lors de la sauvegarde"
            }, ensure_ascii=False)
            
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": str(e)
        }, ensure_ascii=False)

@mcp.tool()
async def reset_user_preferences() -> str:
    """
    Réinitialise les préférences utilisateur aux valeurs par défaut.
    
    Returns:
        JSON string avec le résultat
    """
    try:
        default_prefs = {
            "default_values": {},
            "favorite_options": {},
            "create_folder": True,
            "create_images_folder": False,
            "create_annexes_folder": False,
            "create_sections_folder": False,
            "create_figures_file": True
        }
        
        if save_user_preferences(default_prefs):
            return json.dumps({
                "status": "success",
                "message": "Préférences réinitialisées",
                "preferences": default_prefs
            }, ensure_ascii=False)
        else:
            return json.dumps({
                "status": "error",
                "message": "Erreur lors de la réinitialisation"
            }, ensure_ascii=False)
            
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": str(e)
        }, ensure_ascii=False)

# ============================================================================
# FONCTION D'AIDE
# ============================================================================

@mcp.tool()
async def get_help() -> str:
    """
    Retourne l'aide complète du serveur MCP.
    
    Returns:
        JSON string avec la documentation
    """
    help_text = """
# Document Creator Server - Guide d'utilisation

## Workflow simplifié en 3 étapes

### 1. list_templates()
Liste tous les modèles disponibles.

### 2. get_template_info(template_name)
Obtient la structure JSON des champs à remplir pour un modèle.
- Affiche les champs requis avec leurs types (text/choice)
- Montre les options disponibles pour les champs à choix
- Intègre les préférences utilisateur si configurées

### 3. create_document(...)
Crée le document avec les paramètres fournis.
- Remplace TOUTES les occurrences des balises % nom_champ
- Crée la structure de dossiers configurée
- Génère les fichiers auxiliaires détectés

## Gestion des préférences utilisateur

- **get_user_preferences()**: Voir les préférences actuelles
- **update_user_preferences()**: Modifier les préférences globales
- **add_user_habit()**: Ajouter une habitude spécifique
- **remove_user_habit()**: Supprimer une habitude spécifique
- **reset_user_preferences()**: Réinitialiser aux valeurs par défaut

## Exemple d'utilisation

```python
# 1. Lister les modèles
templates = await list_templates()

# 2. Obtenir les infos d'un modèle
info = await get_template_info("Exercices_light")

# 3. Créer le document
result = await create_document(
    destination_path="./Test",
    document_name="Mon_Exercice",
    template_name="Exercices_light",
    field_values={
        "classe": "Seconde",
        "chapitre": "Fonctions",
        "titre": "Exercices sur les fonctions"
    }
)
```

## Comportement du remplacement

Quand vous définissez `field_values["nom_etab"] = "Claudel"`:
- Remplace `% nom_etab : claudel, romilly...` par `Claudel%`
- Remplace AUSSI tous les `% nom_etab` ailleurs dans le document par `Claudel%`

## Messages d'erreur

Le serveur retourne toujours un JSON avec:
- `status`: "success" ou "error"
- `message`: Description claire du problème
- Informations supplémentaires pour aider à corriger
"""
    
    return json.dumps({
        "status": "success",
        "help": help_text,
        "available_functions": [
            "list_templates",
            "get_template_info",
            "create_document",
            "get_user_preferences",
            "update_user_preferences",
            "add_user_habit",
            "remove_user_habit",
            "reset_user_preferences",
            "get_help"
        ]
    }, ensure_ascii=False, indent=2)

# Point d'entrée principal
if __name__ == "__main__":
    try:
        import asyncio
        logger.info("Démarrage du Document Creator Server (version simplifiée)")
        logger.info(f"Dossier des modèles: {TEMPLATES_PATH}")
        logger.info(f"Workspace: {WORKSPACE_PATH}")
        
        # Vérifier que le dossier des modèles existe
        if not TEMPLATES_PATH.exists():
            logger.warning(f"Le dossier des modèles n'existe pas: {TEMPLATES_PATH}")
            logger.info("Création du dossier...")
            TEMPLATES_PATH.mkdir(parents=True, exist_ok=True)
        
        # Lancer le serveur
        asyncio.run(mcp.run())
    except KeyboardInterrupt:
        logger.info("Arrêt du serveur")
    except Exception as e:
        logger.error(f"Erreur fatale: {e}")
        sys.exit(1)
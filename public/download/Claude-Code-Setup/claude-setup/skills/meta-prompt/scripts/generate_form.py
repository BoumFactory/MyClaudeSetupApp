#!/usr/bin/env python3
"""
Generateur de formulaire HTML interactif pour specifier un prompt.
Usage:
    python generate_form.py --context education-math --output /tmp/prompt-workshop.html
    python generate_form.py --context software --output /tmp/prompt-workshop.html
    python generate_form.py --context custom --output /tmp/prompt-workshop.html

Contextes: education-math, software, agent, analysis, creative, custom
"""

import argparse
import sys
import os
from pathlib import Path


# Configurations par contexte
CONTEXTS = {
    "education-math": {
        "title": "Prompt Workshop — Education Mathematique",
        "color": "#6c5ce7",
        "sections": [
            {
                "id": "role",
                "title": "Role / Persona",
                "description": "Definir l'expert qui va executer ce prompt",
                "default_checked": True,
                "fields": [
                    {"id": "role_type", "type": "select", "label": "Type de role",
                     "options": ["Professeur de mathematiques college", "Professeur de mathematiques lycee",
                                 "Formateur/Tuteur", "Concepteur de QCM", "Redacteur de manuels", "Autre"],
                     "suggestion": "Professeur de mathematiques college"},
                    {"id": "role_level", "type": "select", "label": "Niveau d'expertise",
                     "options": ["Debutant (1-3 ans)", "Confirme (3-10 ans)", "Expert (10+ ans)", "Inspecteur/Formateur"],
                     "suggestion": "Expert (10+ ans)"},
                    {"id": "role_traits", "type": "textarea", "label": "Traits specifiques",
                     "placeholder": "Ex: Approche progressive, bienveillant, axe sur la comprehension...",
                     "suggestion": "Approche progressive et bienveillante. Privilegier la comprehension sur le par-coeur. Connaissance parfaite des programmes officiels."},
                ],
                "code_example": "## Role\n\nProfesseur de mathematiques experimente en college (6eme-3eme).\nSpecialiste du programme officiel Education Nationale.\nApproche progressive, bienveillante, centree comprehension."
            },
            {
                "id": "context",
                "title": "Contexte pedagogique",
                "description": "Situation d'enseignement et public cible",
                "default_checked": True,
                "fields": [
                    {"id": "ctx_level", "type": "select", "label": "Niveau scolaire",
                     "options": ["6eme", "5eme", "4eme", "3eme", "2nde", "1ere Spe", "Terminale Spe", "Autre"],
                     "suggestion": "3eme"},
                    {"id": "ctx_theme", "type": "text", "label": "Theme mathematique",
                     "placeholder": "Ex: Theoreme de Thales, Fractions, Equations...",
                     "suggestion": "Theoreme de Pythagore"},
                    {"id": "ctx_domain", "type": "select", "label": "Domaine du programme",
                     "options": ["Nombres et calculs", "Geometrie", "Grandeurs et mesures",
                                 "Organisation et gestion de donnees", "Algorithmique et programmation"],
                     "suggestion": "Geometrie"},
                    {"id": "ctx_situation", "type": "select", "label": "Type de seance",
                     "options": ["Cours / Decouverte", "Exercices / Application", "Evaluation",
                                 "Revision / Remise a niveau", "Questions Flash", "Activite / Investigation"],
                     "suggestion": "Questions Flash"},
                    {"id": "ctx_prereqs", "type": "textarea", "label": "Prerequis des eleves",
                     "placeholder": "Ce que les eleves savent deja...",
                     "suggestion": "Les eleves connaissent les triangles rectangles et le carre d'un nombre."},
                ],
                "code_example": "<context>\nNiveau : 3eme\nTheme : Theoreme de Pythagore\nDomaine : Geometrie\nSeance : Questions Flash\nPrerequis : Triangles rectangles, carre d'un nombre\n</context>"
            },
            {
                "id": "instructions",
                "title": "Instructions de generation",
                "description": "Ce que le prompt doit produire, etape par etape",
                "default_checked": True,
                "fields": [
                    {"id": "instr_type", "type": "select", "label": "Type de contenu a generer",
                     "options": ["Questions Flash (3 questions)", "Exercices progressifs", "Fiche de cours",
                                 "Evaluation / Devoir", "Activite de decouverte", "Correction detaillee"],
                     "suggestion": "Questions Flash (3 questions)"},
                    {"id": "instr_count", "type": "number", "label": "Nombre d'elements", "min": 1, "max": 20,
                     "suggestion": "3"},
                    {"id": "instr_difficulty", "type": "select", "label": "Progression de difficulte",
                     "options": ["Homogene (meme niveau)", "Progressive (facile → difficile)",
                                 "Mixte (varier aleatoirement)"],
                     "suggestion": "Progressive (facile → difficile)"},
                    {"id": "instr_details", "type": "textarea", "label": "Instructions supplementaires",
                     "placeholder": "Instructions specifiques pour la generation...",
                     "suggestion": "Varier les configurations (calcul d'hypotenuse, calcul d'un cote de l'angle droit, verification si triangle rectangle). Utiliser des valeurs entieres."},
                ],
                "code_example": "## Instructions\n\n### Etape 1 : Identifier les configurations\nLister 3 configurations differentes du theoreme.\n\n### Etape 2 : Generer les questions\nPour chaque configuration, creer une question flash.\nDifficulte progressive.\n\n### Etape 3 : Verifier\nS'assurer que toutes les reponses sont des entiers."
            },
            {
                "id": "constraints",
                "title": "Contraintes",
                "description": "Limites et regles a respecter",
                "default_checked": True,
                "fields": [
                    {"id": "cstr_positive", "type": "textarea", "label": "Contraintes positives (DOIT)",
                     "placeholder": "Ce qui doit etre fait...",
                     "suggestion": "- Conformite programme officiel du niveau\n- Valeurs distinctes entre elles\n- Enonces clairs et courts (1-2 lignes max)"},
                    {"id": "cstr_negative", "type": "textarea", "label": "Contraintes negatives (NE DOIT PAS)",
                     "placeholder": "Ce qui ne doit pas etre fait...",
                     "suggestion": "- Ne pas utiliser de nombres decimaux complexes\n- Ne pas depasser le programme du niveau\n- Ne pas repeter la meme configuration"},
                ],
                "code_example": "## Contraintes\n\n### Obligatoire\n- Conformite programme officiel 3eme\n- Valeurs distinctes dans chaque question\n- Enonces 1-2 lignes max\n\n### Interdit\n- Nombres decimaux complexes\n- Notions hors programme\n- Configurations repetees"
            },
            {
                "id": "format",
                "title": "Format de sortie",
                "description": "Structure et format du resultat attendu",
                "default_checked": True,
                "fields": [
                    {"id": "fmt_type", "type": "select", "label": "Format",
                     "options": ["JSON (Questions Flash)", "LaTeX bfcours", "Markdown", "Texte brut"],
                     "suggestion": "JSON (Questions Flash)"},
                    {"id": "fmt_details", "type": "textarea", "label": "Details du format",
                     "placeholder": "Structure exacte attendue...",
                     "suggestion": ""},
                ],
                "code_example": "## Format de sortie\n\n```json\n{\n  \"enonce\": \"texte de la question\",\n  \"reponse\": \"reponse attendue\",\n  \"details\": \"explication courte\",\n  \"theme\": \"theoreme_pythagore\",\n  \"prompt\": \"prompt utilise\"\n}\n```"
            },
            {
                "id": "examples",
                "title": "Exemples (Few-Shot)",
                "description": "Exemples concrets d'entree/sortie pour calibrer le modele",
                "default_checked": True,
                "fields": [
                    {"id": "ex_input", "type": "textarea", "label": "Exemple d'entree",
                     "placeholder": "Entree de l'exemple...",
                     "suggestion": "Niveau = 3eme, Theme = Pythagore, Config = Calcul hypotenuse"},
                    {"id": "ex_output", "type": "textarea", "label": "Exemple de sortie attendue",
                     "placeholder": "Sortie attendue...",
                     "suggestion": "{\n  \"enonce\": \"ABC est un triangle rectangle en A avec AB = 3 cm et AC = 4 cm. Calculer BC.\",\n  \"reponse\": \"BC = 5 cm\",\n  \"details\": \"BC² = AB² + AC² = 9 + 16 = 25, donc BC = 5 cm\",\n  \"theme\": \"theoreme_pythagore\",\n  \"prompt\": \"...\"\n}"},
                ],
                "code_example": "## Exemples\n\n### Exemple 1\n**Entree** : Niveau=3eme, Theme=Pythagore, Config=hypotenuse\n**Sortie** :\n```json\n{\"enonce\": \"ABC rectangle en A, AB=3, AC=4. Calculer BC.\", ...}\n```"
            },
            {
                "id": "verification",
                "title": "Criteres d'auto-verification",
                "description": "Checklist que le modele doit verifier avant de finaliser",
                "default_checked": True,
                "fields": [
                    {"id": "verif_items", "type": "textarea", "label": "Items de verification",
                     "placeholder": "Liste des criteres...",
                     "suggestion": "- [ ] Conforme au programme officiel de 3eme\n- [ ] Valeurs toutes distinctes dans chaque question\n- [ ] Reponses correctes mathematiquement\n- [ ] Progression de difficulte respectee\n- [ ] Format JSON valide"},
                ],
                "code_example": "## Criteres de qualite\n\n- [ ] Conforme programme officiel 3eme\n- [ ] Valeurs distinctes\n- [ ] Reponses correctes\n- [ ] Progression respectee\n- [ ] JSON valide"
            },
            {
                "id": "variables",
                "title": "Variables parametriques",
                "description": "Variables pour rendre le prompt reutilisable",
                "default_checked": False,
                "fields": [
                    {"id": "vars_list", "type": "textarea", "label": "Variables et defauts",
                     "placeholder": "NOM_VARIABLE = defaut\n...",
                     "suggestion": "NIVEAU = 3eme\nTHEME = obligatoire\nNB_QUESTIONS = 3\nDIFFICULTE = progressive\nFORMAT = JSON"},
                ],
                "code_example": "## Variables\n\n| Variable | Description | Defaut |\n|----------|-------------|--------|\n| `{{NIVEAU}}` | Niveau scolaire | 3eme |\n| `{{THEME}}` | Theme math | obligatoire |\n| `{{NB_QUESTIONS}}` | Nombre | 3 |"
            },
        ]
    },
    "software": {
        "title": "Prompt Workshop — Developpement Logiciel",
        "color": "#00b894",
        "sections": [
            {
                "id": "role",
                "title": "Role / Expertise",
                "description": "Profil technique de l'agent",
                "default_checked": True,
                "fields": [
                    {"id": "role_stack", "type": "text", "label": "Stack technique",
                     "placeholder": "Ex: Rust, TypeScript, Python...",
                     "suggestion": "Rust + TypeScript (Tauri v2)"},
                    {"id": "role_specialty", "type": "text", "label": "Specialite",
                     "placeholder": "Ex: Backend API, Frontend UI, DevOps...",
                     "suggestion": "Full-stack desktop application"},
                ],
                "code_example": "## Role\n\nIngenieur logiciel expert en Rust et TypeScript.\nSpecialiste des architectures Tauri v2 et des patterns async."
            },
            {
                "id": "task",
                "title": "Tache a accomplir",
                "description": "Description precise de ce qu'il faut faire",
                "default_checked": True,
                "fields": [
                    {"id": "task_type", "type": "select", "label": "Type de tache",
                     "options": ["Nouvelle fonctionnalite", "Bug fix", "Refactoring", "Optimisation performance",
                                 "Migration / Upgrade", "Tests", "Documentation"],
                     "suggestion": "Nouvelle fonctionnalite"},
                    {"id": "task_desc", "type": "textarea", "label": "Description detaillee",
                     "placeholder": "Decrire ce qu'il faut implementer...",
                     "suggestion": ""},
                    {"id": "task_files", "type": "textarea", "label": "Fichiers impactes",
                     "placeholder": "Lister les fichiers concernes...",
                     "suggestion": ""},
                ],
                "code_example": "## Instructions\n\n### Etape 1 : Analyse\nLire les fichiers impactes.\n\n### Etape 2 : Implementation\nImplementer selon les conventions.\n\n### Etape 3 : Tests\nEcrire et executer les tests."
            },
            {
                "id": "constraints",
                "title": "Contraintes techniques",
                "description": "Regles et conventions a respecter",
                "default_checked": True,
                "fields": [
                    {"id": "cstr_patterns", "type": "textarea", "label": "Patterns obligatoires",
                     "placeholder": "Conventions de code, derives, error handling...",
                     "suggestion": "- anyhow::Context, jamais unwrap()\n- #[derive(Debug, Clone, Serialize, Deserialize)]\n- BTreeMap pour cles triees\n- cargo clippy sans warnings"},
                ],
                "code_example": "## Contraintes\n\n- anyhow::Context pour toute erreur\n- Derives : Debug, Clone, Serialize, Deserialize\n- cargo clippy sans warnings\n- Tests pour chaque nouveau chemin"
            },
            {
                "id": "format",
                "title": "Format de sortie",
                "description": "Ce que le prompt doit produire",
                "default_checked": True,
                "fields": [
                    {"id": "fmt_output", "type": "select", "label": "Type de sortie",
                     "options": ["Code Rust", "Code TypeScript/JS", "Fichier de config", "Rapport d'analyse",
                                 "Plan d'implementation", "Code + Tests"],
                     "suggestion": "Code + Tests"},
                ],
                "code_example": "## Format\n\nProduire :\n1. Code Rust avec commentaires\n2. Tests unitaires\n3. Mise a jour des exports si necessaire"
            },
            {
                "id": "verification",
                "title": "Verification",
                "description": "Comment valider le resultat",
                "default_checked": True,
                "fields": [
                    {"id": "verif_items", "type": "textarea", "label": "Criteres de validation",
                     "placeholder": "Tests, build, lint...",
                     "suggestion": "- [ ] cargo build sans erreur\n- [ ] cargo clippy sans warning\n- [ ] cargo test passe\n- [ ] Pas de regression sur les tests existants"},
                ],
                "code_example": "## Verification\n\n- [ ] cargo build OK\n- [ ] cargo clippy OK\n- [ ] cargo test OK\n- [ ] Pas de regression"
            },
        ]
    },
    "agent": {
        "title": "Prompt Workshop — Agent Autonome",
        "color": "#e17055",
        "sections": [
            {
                "id": "identity",
                "title": "Identite de l'agent",
                "description": "Nom, role et mission",
                "default_checked": True,
                "fields": [
                    {"id": "agent_name", "type": "text", "label": "Nom de l'agent",
                     "placeholder": "Ex: data-analyzer, code-reviewer...",
                     "suggestion": ""},
                    {"id": "agent_mission", "type": "textarea", "label": "Mission principale",
                     "placeholder": "Que doit faire cet agent ?",
                     "suggestion": ""},
                    {"id": "agent_tools", "type": "textarea", "label": "Outils necessaires",
                     "placeholder": "Read, Write, Bash, Grep, Glob, WebFetch...",
                     "suggestion": "Read, Write, Edit, Bash, Grep, Glob"},
                ],
                "code_example": "# Agent: data-analyzer\n\n## Role\nAgent specialise dans l'analyse de donnees.\nMission : extraire, analyser et synthetiser."
            },
            {
                "id": "workflow",
                "title": "Workflow",
                "description": "Processus etape par etape",
                "default_checked": True,
                "fields": [
                    {"id": "wf_steps", "type": "textarea", "label": "Etapes du workflow",
                     "placeholder": "1. Reconnaissance\n2. Planification\n3. Execution\n4. Validation",
                     "suggestion": "1. Reconnaissance : lire les fichiers pertinents\n2. Planification : lister les actions dans <thinking>\n3. Execution : implementer les changements\n4. Validation : tester et verifier"},
                ],
                "code_example": "## Processus\n\n### Etape 1 : Reconnaissance\nLire les fichiers. Ne JAMAIS deviner.\n\n### Etape 2 : Planification\nReflechir dans <thinking>.\n\n### Etape 3 : Execution\nImplementer. Un fichier a la fois.\n\n### Etape 4 : Validation\nTester."
            },
            {
                "id": "rules",
                "title": "Regles critiques",
                "description": "Les 3 rappels agentiques + regles specifiques",
                "default_checked": True,
                "fields": [
                    {"id": "rules_list", "type": "textarea", "label": "Regles",
                     "placeholder": "Regles obligatoires...",
                     "suggestion": "- PERSISTENCE : continuer jusqu'a resolution complete\n- ANTI-HALLUCINATION : utiliser les outils, ne pas deviner\n- PLANIFICATION : reflechir avant chaque action"},
                ],
                "code_example": "## Regles critiques\n\n1. PERSISTENCE : ne pas s'arreter avant resolution complete\n2. ANTI-HALLUCINATION : toujours lire avant d'agir\n3. PLANIFICATION : <thinking> avant chaque action"
            },
        ]
    },
}

# Ajouter les contextes manquants comme alias de custom
for ctx in ["analysis", "creative", "custom"]:
    if ctx not in CONTEXTS:
        CONTEXTS[ctx] = {
            "title": f"Prompt Workshop — {ctx.title()}",
            "color": "#636e72",
            "sections": [
                {
                    "id": "role", "title": "Role", "description": "Definir l'expert",
                    "default_checked": True,
                    "fields": [
                        {"id": "role_desc", "type": "textarea", "label": "Description du role",
                         "placeholder": "Decrire le role...", "suggestion": ""},
                    ],
                    "code_example": "## Role\n\n[Decrire le role ici]"
                },
                {
                    "id": "context", "title": "Contexte", "description": "Cadre d'utilisation",
                    "default_checked": True,
                    "fields": [
                        {"id": "ctx_desc", "type": "textarea", "label": "Contexte",
                         "placeholder": "Decrire le contexte...", "suggestion": ""},
                    ],
                    "code_example": "## Contexte\n\n[Decrire le contexte ici]"
                },
                {
                    "id": "instructions", "title": "Instructions", "description": "Ce qu'il faut faire",
                    "default_checked": True,
                    "fields": [
                        {"id": "instr_desc", "type": "textarea", "label": "Instructions",
                         "placeholder": "Decrire les instructions...", "suggestion": ""},
                    ],
                    "code_example": "## Instructions\n\n[Decrire les instructions ici]"
                },
                {
                    "id": "format", "title": "Format de sortie", "description": "Resultat attendu",
                    "default_checked": True,
                    "fields": [
                        {"id": "fmt_desc", "type": "textarea", "label": "Format",
                         "placeholder": "Decrire le format...", "suggestion": ""},
                    ],
                    "code_example": "## Format\n\n[Decrire le format ici]"
                },
            ]
        }


def generate_html(context_key: str) -> str:
    """Genere le HTML complet du formulaire."""
    ctx = CONTEXTS.get(context_key, CONTEXTS["custom"])
    title = ctx["title"]
    color = ctx["color"]
    sections = ctx["sections"]

    # Build sections HTML
    sections_html = ""
    for section in sections:
        checked = "checked" if section["default_checked"] else ""
        fields_html = ""
        for field in section["fields"]:
            fid = field["id"]
            suggestion = field.get("suggestion", "")
            suggestion_html = ""
            if suggestion:
                suggestion_html = f'''
                <div class="suggestion" id="sug-{fid}">
                    <span class="suggestion-label">Suggestion :</span>
                    <span class="suggestion-text">{suggestion}</span>
                    <button type="button" class="btn-apply" onclick="applySuggestion('{fid}')">Appliquer</button>
                </div>'''

            if field["type"] == "select":
                opts = "".join(f'<option value="{o}">{o}</option>' for o in field["options"])
                fields_html += f'''
                <div class="field-group">
                    <label for="{fid}">{field["label"]}</label>
                    <select id="{fid}" name="{fid}">{opts}</select>
                    {suggestion_html}
                </div>'''
            elif field["type"] == "textarea":
                ph = field.get("placeholder", "")
                fields_html += f'''
                <div class="field-group">
                    <label for="{fid}">{field["label"]}</label>
                    <textarea id="{fid}" name="{fid}" rows="4" placeholder="{ph}"></textarea>
                    {suggestion_html}
                </div>'''
            elif field["type"] == "text":
                ph = field.get("placeholder", "")
                fields_html += f'''
                <div class="field-group">
                    <label for="{fid}">{field["label"]}</label>
                    <input type="text" id="{fid}" name="{fid}" placeholder="{ph}">
                    {suggestion_html}
                </div>'''
            elif field["type"] == "number":
                fields_html += f'''
                <div class="field-group">
                    <label for="{fid}">{field["label"]}</label>
                    <input type="number" id="{fid}" name="{fid}" min="{field.get('min',1)}" max="{field.get('max',100)}" value="{suggestion}">
                </div>'''

        code_ex = section.get("code_example", "")
        code_html = ""
        if code_ex:
            # Escape HTML
            code_ex_escaped = code_ex.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            code_html = f'''
            <details class="code-preview">
                <summary>Apercu du pattern genere</summary>
                <pre><code>{code_ex_escaped}</code></pre>
            </details>'''

        sections_html += f'''
        <div class="section" id="section-{section['id']}">
            <div class="section-header">
                <label class="toggle-label">
                    <input type="checkbox" class="section-toggle" data-section="{section['id']}" {checked}>
                    <span class="section-title">{section['title']}</span>
                </label>
                <span class="section-desc">{section['description']}</span>
            </div>
            <div class="section-body" id="body-{section['id']}">
                {fields_html}
                <div class="field-group">
                    <label for="comment-{section['id']}">Commentaire / Modification suggeree</label>
                    <textarea id="comment-{section['id']}" name="comment-{section['id']}" rows="2"
                        placeholder="Vos notes ou modifications pour cette section..." class="comment-field"></textarea>
                </div>
                {code_html}
            </div>
        </div>'''

    html = f'''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background: #1a1a2e;
            color: #e0e0e0;
            line-height: 1.6;
            padding: 20px;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}
        h1 {{
            text-align: center;
            color: {color};
            margin-bottom: 8px;
            font-size: 1.8rem;
        }}
        .subtitle {{
            text-align: center;
            color: #888;
            margin-bottom: 30px;
            font-size: 0.9rem;
        }}
        .section {{
            background: #16213e;
            border: 1px solid #2a2a4a;
            border-radius: 12px;
            margin-bottom: 16px;
            overflow: hidden;
            transition: opacity 0.3s;
        }}
        .section.disabled {{
            opacity: 0.4;
        }}
        .section.disabled .section-body {{
            display: none;
        }}
        .section-header {{
            padding: 16px 20px;
            background: #1a1a3e;
            border-bottom: 1px solid #2a2a4a;
            display: flex;
            align-items: center;
            gap: 16px;
            flex-wrap: wrap;
        }}
        .toggle-label {{
            display: flex;
            align-items: center;
            gap: 10px;
            cursor: pointer;
            flex-shrink: 0;
        }}
        .section-toggle {{
            width: 18px;
            height: 18px;
            accent-color: {color};
        }}
        .section-title {{
            font-weight: 700;
            font-size: 1.1rem;
            color: {color};
        }}
        .section-desc {{
            color: #888;
            font-size: 0.85rem;
        }}
        .section-body {{
            padding: 16px 20px;
        }}
        .field-group {{
            margin-bottom: 14px;
        }}
        .field-group label {{
            display: block;
            font-weight: 600;
            margin-bottom: 4px;
            color: #b0b0d0;
            font-size: 0.9rem;
        }}
        input[type="text"], input[type="number"], textarea, select {{
            width: 100%;
            padding: 10px 14px;
            background: #0f0f23;
            border: 1px solid #3a3a5a;
            border-radius: 8px;
            color: #e0e0e0;
            font-size: 0.95rem;
            font-family: inherit;
            transition: border-color 0.2s;
        }}
        input:focus, textarea:focus, select:focus {{
            outline: none;
            border-color: {color};
            box-shadow: 0 0 0 2px {color}33;
        }}
        textarea {{ resize: vertical; }}
        .comment-field {{
            border-color: #5a4a2a;
            background: #1a1a10;
            font-style: italic;
            font-size: 0.85rem;
        }}
        .suggestion {{
            margin-top: 4px;
            padding: 8px 12px;
            background: #1a2a1a;
            border: 1px solid #2a4a2a;
            border-radius: 6px;
            font-size: 0.85rem;
            display: flex;
            align-items: flex-start;
            gap: 8px;
            flex-wrap: wrap;
        }}
        .suggestion-label {{
            color: #4aaf4a;
            font-weight: 600;
            white-space: nowrap;
        }}
        .suggestion-text {{
            flex: 1;
            color: #8adf8a;
            min-width: 200px;
            white-space: pre-wrap;
        }}
        .btn-apply {{
            background: #2a5a2a;
            color: #8adf8a;
            border: 1px solid #4a7a4a;
            padding: 4px 12px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.8rem;
            white-space: nowrap;
            transition: background 0.2s;
        }}
        .btn-apply:hover {{ background: #3a7a3a; }}
        .code-preview {{
            margin-top: 10px;
            padding: 10px;
            background: #0f0f1f;
            border: 1px solid #2a2a3a;
            border-radius: 8px;
        }}
        .code-preview summary {{
            cursor: pointer;
            color: #8888cc;
            font-size: 0.85rem;
            font-weight: 600;
        }}
        .code-preview pre {{
            margin-top: 8px;
            padding: 12px;
            background: #0a0a18;
            border-radius: 6px;
            overflow-x: auto;
            font-size: 0.82rem;
            line-height: 1.5;
        }}
        .code-preview code {{ color: #a0d0a0; }}
        .actions {{
            display: flex;
            gap: 12px;
            margin-top: 24px;
            justify-content: center;
            flex-wrap: wrap;
        }}
        .btn {{
            padding: 12px 28px;
            border: none;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .btn-primary {{
            background: {color};
            color: white;
        }}
        .btn-primary:hover {{ filter: brightness(1.2); }}
        .btn-secondary {{
            background: #2a2a4a;
            color: #b0b0d0;
            border: 1px solid #4a4a6a;
        }}
        .btn-secondary:hover {{ background: #3a3a5a; }}
        .btn-danger {{
            background: #4a1a1a;
            color: #df8a8a;
            border: 1px solid #6a2a2a;
        }}
        .btn-danger:hover {{ background: #5a2a2a; }}
        #output-area {{
            margin-top: 24px;
            padding: 16px;
            background: #0f0f23;
            border: 1px solid #3a3a5a;
            border-radius: 12px;
            display: none;
        }}
        #output-area h3 {{
            color: {color};
            margin-bottom: 12px;
        }}
        #output-json {{
            width: 100%;
            min-height: 300px;
            background: #0a0a18;
            border: 1px solid #2a2a3a;
            color: #a0d0a0;
            font-family: 'Cascadia Code', 'Fira Code', monospace;
            font-size: 0.85rem;
            padding: 12px;
            border-radius: 8px;
            resize: vertical;
        }}
        .apply-all-bar {{
            text-align: center;
            margin-bottom: 16px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <p class="subtitle">Cocher/decocher les sections a inclure. Modifier les champs. Appliquer les suggestions.</p>

        <div class="apply-all-bar">
            <button type="button" class="btn btn-secondary" onclick="applyAllSuggestions()">
                Appliquer toutes les suggestions
            </button>
            <button type="button" class="btn btn-secondary" onclick="toggleAll(true)">
                Tout cocher
            </button>
            <button type="button" class="btn btn-secondary" onclick="toggleAll(false)">
                Tout decocher
            </button>
        </div>

        <form id="prompt-form">
            {sections_html}
        </form>

        <div class="actions">
            <button type="button" class="btn btn-primary" onclick="exportJSON()">
                Exporter JSON
            </button>
            <button type="button" class="btn btn-secondary" onclick="copyJSON()">
                Copier dans le presse-papier
            </button>
            <button type="button" class="btn btn-danger" onclick="resetForm()">
                Reinitialiser
            </button>
        </div>

        <div id="output-area">
            <h3>Specifications JSON</h3>
            <textarea id="output-json" readonly></textarea>
        </div>
    </div>

    <script>
        // Suggestions data
        const suggestions = {{}};
        document.querySelectorAll('.suggestion').forEach(el => {{
            const id = el.id.replace('sug-', '');
            const text = el.querySelector('.suggestion-text').textContent;
            suggestions[id] = text;
        }});

        // Toggle sections
        document.querySelectorAll('.section-toggle').forEach(cb => {{
            cb.addEventListener('change', () => {{
                const section = cb.closest('.section');
                section.classList.toggle('disabled', !cb.checked);
            }});
            // Init
            if (!cb.checked) cb.closest('.section').classList.add('disabled');
        }});

        function applySuggestion(fieldId) {{
            const el = document.getElementById(fieldId);
            if (el && suggestions[fieldId]) {{
                if (el.tagName === 'SELECT') {{
                    const opt = Array.from(el.options).find(o => o.value === suggestions[fieldId]);
                    if (opt) opt.selected = true;
                }} else {{
                    el.value = suggestions[fieldId];
                }}
                el.style.borderColor = '#4aaf4a';
                setTimeout(() => el.style.borderColor = '', 1000);
            }}
        }}

        function applyAllSuggestions() {{
            Object.keys(suggestions).forEach(id => applySuggestion(id));
        }}

        function toggleAll(state) {{
            document.querySelectorAll('.section-toggle').forEach(cb => {{
                cb.checked = state;
                cb.closest('.section').classList.toggle('disabled', !state);
            }});
        }}

        function collectData() {{
            const data = {{ context: "{context_key}", sections: {{}} }};
            document.querySelectorAll('.section').forEach(section => {{
                const id = section.id.replace('section-', '');
                const toggle = section.querySelector('.section-toggle');
                if (!toggle.checked) return;
                const fields = {{}};
                section.querySelectorAll('input, textarea, select').forEach(el => {{
                    if (el.name && !el.name.startsWith('comment-') && el.type !== 'checkbox') {{
                        fields[el.name] = el.value;
                    }}
                }});
                const comment = section.querySelector('.comment-field');
                if (comment && comment.value.trim()) {{
                    fields['_comment'] = comment.value.trim();
                }}
                data.sections[id] = fields;
            }});
            return data;
        }}

        function exportJSON() {{
            const data = collectData();
            const json = JSON.stringify(data, null, 2);
            document.getElementById('output-json').value = json;
            document.getElementById('output-area').style.display = 'block';
            document.getElementById('output-area').scrollIntoView({{ behavior: 'smooth' }});
        }}

        function copyJSON() {{
            const data = collectData();
            const json = JSON.stringify(data, null, 2);
            navigator.clipboard.writeText(json).then(() => {{
                alert('JSON copie dans le presse-papier !');
            }});
        }}

        function resetForm() {{
            if (confirm('Reinitialiser tous les champs ?')) {{
                document.getElementById('prompt-form').reset();
                document.querySelectorAll('.section-toggle').forEach(cb => {{
                    const section = cb.closest('.section');
                    section.classList.toggle('disabled', !cb.checked);
                }});
                document.getElementById('output-area').style.display = 'none';
            }}
        }}
    </script>
</body>
</html>'''

    return html


def main():
    parser = argparse.ArgumentParser(description="Generateur de formulaire HTML pour prompt workshop")
    parser.add_argument("--context", "-c", default="custom",
                        choices=list(CONTEXTS.keys()),
                        help="Contexte du prompt (education-math, software, agent, analysis, creative, custom)")
    parser.add_argument("--output", "-o", required=True,
                        help="Chemin du fichier HTML de sortie")
    parser.add_argument("--open", action="store_true",
                        help="Ouvrir le fichier dans le navigateur apres generation")
    args = parser.parse_args()

    html = generate_html(args.context)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    print(f"Formulaire genere : {output_path}")
    print(f"Contexte : {args.context}")
    print(f"Sections : {len(CONTEXTS[args.context]['sections'])}")

    if args.open:
        import webbrowser
        webbrowser.open(str(output_path.resolve()))


if __name__ == "__main__":
    main()

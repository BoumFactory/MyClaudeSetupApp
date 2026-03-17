#!/usr/bin/env python3
"""
Diagnostic automatique de prompts sur 8 axes de qualité.
Usage:
    python diagnose_prompt.py --file prompt.md
    python diagnose_prompt.py --text "Mon prompt inline..."
"""

import argparse
import re
import sys
import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class AxisScore:
    name: str
    score: int  # 1-5
    max_score: int = 5
    details: str = ""
    recommendations: list = field(default_factory=list)


@dataclass
class DiagnosticReport:
    file_path: Optional[str]
    total_score: int = 0
    max_total: int = 40
    grade: str = ""
    axes: list = field(default_factory=list)
    strengths: list = field(default_factory=list)
    weaknesses: list = field(default_factory=list)
    quick_wins: list = field(default_factory=list)
    token_estimate: int = 0


def count_tokens_approx(text: str) -> int:
    """Estimation grossière : ~4 chars par token."""
    return len(text) // 4


def check_clarity(text: str) -> AxisScore:
    """Axe 1 : Clarté — instructions explicites et non-ambiguës."""
    score = 1
    recs = []
    details_parts = []

    # Forme impérative (verbes d'action en début de phrase)
    imperative_verbs = r'(?:Generer|Creer|Analyser|Lister|Ecrire|Produire|Retourner|Calculer|Identifier|Verifier|Resoudre|Extraire|Transformer|Organiser|Structurer|Generate|Create|Analyze|List|Write|Return|Calculate|Identify|Verify)'
    imperative_count = len(re.findall(imperative_verbs, text, re.IGNORECASE))
    if imperative_count >= 3:
        score += 1
        details_parts.append(f"{imperative_count} verbes d'action détectés")
    else:
        recs.append("Utiliser la forme impérative (Générer, Créer, Analyser...)")

    # Pas de formulations vagues
    vague_patterns = r'\b(quelque chose|un peu|peut-etre|si possible|eventuellement|something|maybe|perhaps|if possible)\b'
    vague_count = len(re.findall(vague_patterns, text, re.IGNORECASE))
    if vague_count == 0:
        score += 1
        details_parts.append("Pas de formulations vagues")
    else:
        recs.append(f"Éliminer {vague_count} formulation(s) vague(s) : {', '.join(re.findall(vague_patterns, text, re.IGNORECASE)[:3])}")

    # Instructions numérotées ou structurées
    numbered = len(re.findall(r'^\s*\d+[\.\)]\s', text, re.MULTILINE))
    bullet = len(re.findall(r'^\s*[-*]\s', text, re.MULTILINE))
    if numbered >= 3 or bullet >= 3:
        score += 1
        details_parts.append(f"{numbered} étapes numérotées, {bullet} bullet points")
    else:
        recs.append("Structurer les instructions avec des étapes numérotées")

    # Longueur suffisante (pas trop court)
    word_count = len(text.split())
    if word_count >= 50:
        score += 1
        details_parts.append(f"{word_count} mots (suffisamment detaille)")
    else:
        recs.append(f"Prompt trop court ({word_count} mots) — developper les instructions")

    return AxisScore("Clarte", min(score, 5), details="; ".join(details_parts), recommendations=recs)


def check_specificity(text: str) -> AxisScore:
    """Axe 2 : Specificite — exemples, format precis."""
    score = 1
    recs = []
    details_parts = []

    # Exemples presents
    example_markers = r'(?:exemple|example|entree|sortie|input|output|e\.g\.|par exemple)'
    example_count = len(re.findall(example_markers, text, re.IGNORECASE))
    if example_count >= 2:
        score += 2
        details_parts.append(f"{example_count} marqueurs d'exemples")
    elif example_count >= 1:
        score += 1
        details_parts.append(f"{example_count} marqueur d'exemple")
        recs.append("Ajouter au moins 1 exemple supplementaire (few-shot)")
    else:
        recs.append("Ajouter des exemples concrets d'entree/sortie (few-shot prompting)")

    # Format de sortie specifie
    format_markers = r'(?:format|json|xml|latex|markdown|csv|tableau|table|schema|structure)'
    if re.search(format_markers, text, re.IGNORECASE):
        score += 1
        details_parts.append("Format de sortie specifie")
    else:
        recs.append("Specifier le format de sortie exact (JSON, LaTeX, Markdown...)")

    # Valeurs concretes (nombres, noms specifiques)
    concrete = len(re.findall(r'\b\d+\b', text))
    if concrete >= 3:
        score += 1
        details_parts.append(f"{concrete} valeurs concretes")
    else:
        recs.append("Ajouter des valeurs concretes (quantites, limites, seuils)")

    return AxisScore("Specificite", min(score, 5), details="; ".join(details_parts), recommendations=recs)


def check_structure(text: str) -> AxisScore:
    """Axe 3 : Structure — sections, XML, headings."""
    score = 1
    recs = []
    details_parts = []

    # Headings markdown
    headings = re.findall(r'^#{1,4}\s', text, re.MULTILINE)
    if len(headings) >= 4:
        score += 2
        details_parts.append(f"{len(headings)} sections Markdown")
    elif len(headings) >= 2:
        score += 1
        details_parts.append(f"{len(headings)} sections Markdown")
        recs.append("Ajouter plus de sections pour mieux organiser")
    else:
        recs.append("Structurer avec des titres Markdown (## Role, ## Instructions, etc.)")

    # XML tags
    xml_tags = re.findall(r'<(\w+)>', text)
    if len(xml_tags) >= 2:
        score += 1
        details_parts.append(f"{len(xml_tags)} balises XML ({', '.join(set(xml_tags[:5]))})")
    else:
        recs.append("Utiliser des balises XML pour separer instructions/donnees (<context>, <instructions>, etc.)")

    # Separation claire des sections (lignes vides, separateurs)
    sections = text.split('\n\n')
    if len(sections) >= 5:
        score += 1
        details_parts.append(f"{len(sections)} blocs separes")
    else:
        recs.append("Mieux separer les sections (double saut de ligne)")

    return AxisScore("Structure", min(score, 5), details="; ".join(details_parts), recommendations=recs)


def check_reasoning(text: str) -> AxisScore:
    """Axe 4 : Raisonnement — CoT, etapes logiques."""
    score = 1
    recs = []
    details_parts = []

    # Chain of thought explicite
    cot_markers = r'(?:etape par etape|step by step|raisonner|thinking|reflexion|reflect|avant de repondre|before answering)'
    if re.search(cot_markers, text, re.IGNORECASE):
        score += 2
        details_parts.append("CoT explicite detecte")
    else:
        recs.append("Ajouter une instruction de raisonnement (\"Raisonner etape par etape avant de repondre\")")

    # Etapes sequentielles
    step_markers = r'(?:etape \d|step \d|phase \d|d\'abord|ensuite|enfin|first|then|finally)'
    step_count = len(re.findall(step_markers, text, re.IGNORECASE))
    if step_count >= 3:
        score += 1
        details_parts.append(f"{step_count} marqueurs de sequence")
    else:
        recs.append("Decomposer en etapes sequentielles (Etape 1, Etape 2...)")

    # Balises thinking/answer
    if re.search(r'<thinking>|<answer>|<reflexion>', text, re.IGNORECASE):
        score += 1
        details_parts.append("Balises thinking/answer presentes")
    else:
        recs.append("Utiliser <thinking> et <answer> pour structurer le raisonnement")

    return AxisScore("Raisonnement", min(score, 5), details="; ".join(details_parts), recommendations=recs)


def check_robustness(text: str) -> AxisScore:
    """Axe 5 : Robustesse — erreurs, fallbacks, cas limites."""
    score = 1
    recs = []
    details_parts = []

    # Gestion d'erreurs
    error_markers = r'(?:erreur|error|echoue|fail|impossible|si.*pas|if.*not|fallback|sinon|otherwise|en cas de)'
    error_count = len(re.findall(error_markers, text, re.IGNORECASE))
    if error_count >= 3:
        score += 2
        details_parts.append(f"{error_count} gestions d'erreur/fallback")
    elif error_count >= 1:
        score += 1
        details_parts.append(f"{error_count} mention(s) d'erreur")
        recs.append("Ajouter plus de cas d'erreur et de fallbacks")
    else:
        recs.append("Ajouter la gestion des cas d'erreur (\"Si X echoue, alors Y\")")

    # Contraintes negatives
    negative_markers = r'(?:ne pas|ne jamais|eviter|interdire|do not|never|avoid|prohibited)'
    neg_count = len(re.findall(negative_markers, text, re.IGNORECASE))
    if neg_count >= 2:
        score += 1
        details_parts.append(f"{neg_count} contraintes negatives")
    else:
        recs.append("Ajouter des contraintes negatives (ce qu'il NE FAUT PAS faire)")

    # Cas limites mentionnes
    edge_markers = r'(?:cas limite|edge case|cas particulier|special case|exception|si vide|if empty|si aucun|if no)'
    if re.search(edge_markers, text, re.IGNORECASE):
        score += 1
        details_parts.append("Cas limites mentionnes")
    else:
        recs.append("Specifier le comportement pour les cas limites (donnees vides, erreurs, etc.)")

    return AxisScore("Robustesse", min(score, 5), details="; ".join(details_parts), recommendations=recs)


def check_reusability(text: str) -> AxisScore:
    """Axe 6 : Reutilisabilite — variables, parametres."""
    score = 1
    recs = []
    details_parts = []

    # Variables {{}}
    variables = re.findall(r'\{\{(\w+)\}\}', text)
    unique_vars = set(variables)
    if len(unique_vars) >= 4:
        score += 2
        details_parts.append(f"{len(unique_vars)} variables uniques ({', '.join(list(unique_vars)[:5])})")
    elif len(unique_vars) >= 2:
        score += 1
        details_parts.append(f"{len(unique_vars)} variables")
        recs.append("Extraire plus de valeurs en variables {{VARIABLE}}")
    else:
        recs.append("Parametriser avec des variables {{NOM_VARIABLE}} pour rendre le prompt reutilisable")

    # Tableau de variables
    if re.search(r'\|\s*Variable\s*\||\|\s*`\{\{', text):
        score += 1
        details_parts.append("Tableau recapitulatif de variables present")
    elif len(unique_vars) >= 2:
        recs.append("Ajouter un tableau recapitulatif des variables avec descriptions et defauts")

    # Valeurs par defaut
    defaults = re.findall(r'(?:defaut|default|par defaut)\s*[:=]\s*', text, re.IGNORECASE)
    if len(defaults) >= 2:
        score += 1
        details_parts.append(f"{len(defaults)} valeurs par defaut")
    else:
        recs.append("Definir des valeurs par defaut pour les variables optionnelles")

    return AxisScore("Reutilisabilite", min(score, 5), details="; ".join(details_parts), recommendations=recs)


def check_verification(text: str) -> AxisScore:
    """Axe 7 : Verification — auto-check, criteres qualite."""
    score = 1
    recs = []
    details_parts = []

    # Checklist
    checklist = re.findall(r'\[[\sx]\]', text, re.IGNORECASE)
    if len(checklist) >= 3:
        score += 2
        details_parts.append(f"{len(checklist)} items de checklist")
    elif len(checklist) >= 1:
        score += 1
        details_parts.append(f"{len(checklist)} item(s) de checklist")
        recs.append("Etoffer la checklist de verification (min 3 criteres)")
    else:
        recs.append("Ajouter une checklist d'auto-verification (pattern Constitutional AI)")

    # Criteres de qualite
    quality_markers = r'(?:qualite|quality|verifier|verify|critere|criteria|valider|validate|confirmer|confirm)'
    q_count = len(re.findall(quality_markers, text, re.IGNORECASE))
    if q_count >= 2:
        score += 1
        details_parts.append(f"{q_count} mentions de verification qualite")
    else:
        recs.append("Ajouter des criteres de qualite explicites a verifier avant finalisation")

    # Pattern revision/auto-critique
    revision_markers = r'(?:relire|reread|reviser|revise|corriger|correct|ameliorer|improve|critique)'
    if re.search(revision_markers, text, re.IGNORECASE):
        score += 1
        details_parts.append("Pattern de revision/auto-critique detecte")
    else:
        recs.append("Ajouter une etape d'auto-critique (Generate → Critique → Revise)")

    return AxisScore("Verification", min(score, 5), details="; ".join(details_parts), recommendations=recs)


def check_conciseness(text: str) -> AxisScore:
    """Axe 8 : Concision — densite, pas de redondance."""
    score = 3  # Par defaut moyen
    recs = []
    details_parts = []

    word_count = len(text.split())
    token_est = count_tokens_approx(text)

    # Ratio contenu/structure
    content_lines = [l for l in text.split('\n') if l.strip() and not l.strip().startswith('#') and not l.strip().startswith('|') and not l.strip().startswith('---')]
    structure_lines = [l for l in text.split('\n') if l.strip().startswith('#') or l.strip().startswith('|') or l.strip().startswith('---')]

    details_parts.append(f"{word_count} mots, ~{token_est} tokens")

    # Trop court (pas assez detaille)
    if word_count < 30:
        score = 2
        recs.append("Prompt trop court — manque de detail")
    # Trop long (probablement redondant)
    elif word_count > 2000:
        score = 2
        recs.append(f"Prompt tres long ({word_count} mots) — chercher les redondances a eliminer")
    elif word_count > 1000:
        score = 3
        recs.append(f"Prompt long ({word_count} mots) — verifier qu'il n'y a pas de redondance")
    else:
        score = 4

    # Repetitions de phrases
    sentences = re.split(r'[.!?\n]', text)
    sentences = [s.strip().lower() for s in sentences if len(s.strip()) > 20]
    seen = set()
    duplicates = 0
    for s in sentences:
        if s in seen:
            duplicates += 1
        seen.add(s)
    if duplicates > 0:
        score = max(score - 1, 1)
        recs.append(f"{duplicates} phrase(s) dupliquee(s) detectee(s)")
    else:
        details_parts.append("Pas de duplication detectee")

    # Bon ratio si structure presente
    if len(structure_lines) > 0 and len(content_lines) / max(len(structure_lines), 1) >= 2:
        score = min(score + 1, 5)
        details_parts.append("Bon ratio contenu/structure")

    return AxisScore("Concision", min(score, 5), details="; ".join(details_parts), recommendations=recs)


def diagnose(text: str, file_path: Optional[str] = None) -> DiagnosticReport:
    """Diagnostic complet d'un prompt sur 8 axes."""
    report = DiagnosticReport(file_path=file_path)

    # Evaluer chaque axe
    axes = [
        check_clarity(text),
        check_specificity(text),
        check_structure(text),
        check_reasoning(text),
        check_robustness(text),
        check_reusability(text),
        check_verification(text),
        check_conciseness(text),
    ]
    report.axes = axes
    report.total_score = sum(a.score for a in axes)
    report.token_estimate = count_tokens_approx(text)

    # Grade
    pct = report.total_score / report.max_total * 100
    if pct >= 90:
        report.grade = "A+ (Excellent)"
    elif pct >= 80:
        report.grade = "A (Tres bon)"
    elif pct >= 70:
        report.grade = "B (Bon)"
    elif pct >= 60:
        report.grade = "C (Correct)"
    elif pct >= 50:
        report.grade = "D (A ameliorer)"
    else:
        report.grade = "F (Insuffisant)"

    # Points forts et faiblesses
    report.strengths = [a.name for a in axes if a.score >= 4]
    report.weaknesses = [a.name for a in axes if a.score <= 2]

    # Quick wins (recommandations des axes les plus faibles)
    weak_axes = sorted(axes, key=lambda a: a.score)
    for a in weak_axes[:3]:
        for rec in a.recommendations[:2]:
            report.quick_wins.append(f"[{a.name}] {rec}")

    return report


def format_report(report: DiagnosticReport) -> str:
    """Formater le rapport en texte lisible."""
    lines = []
    lines.append("=" * 60)
    lines.append("  DIAGNOSTIC DE PROMPT - Meta-Prompt Skill")
    lines.append("=" * 60)

    if report.file_path:
        lines.append(f"\nFichier : {report.file_path}")
    lines.append(f"Tokens estimes : ~{report.token_estimate}")
    lines.append(f"\nScore global : {report.total_score}/{report.max_total} — {report.grade}")
    lines.append("")

    # Barre visuelle par axe
    lines.append("SCORES PAR AXE :")
    lines.append("-" * 40)
    for axis in report.axes:
        bar = "█" * axis.score + "░" * (axis.max_score - axis.score)
        lines.append(f"  {axis.name:<16} [{bar}] {axis.score}/{axis.max_score}")
        if axis.details:
            lines.append(f"                   {axis.details}")
    lines.append("")

    if report.strengths:
        lines.append("POINTS FORTS :")
        for s in report.strengths:
            lines.append(f"  + {s}")
        lines.append("")

    if report.weaknesses:
        lines.append("FAIBLESSES :")
        for w in report.weaknesses:
            lines.append(f"  - {w}")
        lines.append("")

    if report.quick_wins:
        lines.append("QUICK WINS (ameliorations prioritaires) :")
        for i, qw in enumerate(report.quick_wins, 1):
            lines.append(f"  {i}. {qw}")
        lines.append("")

    # Recommandations detaillees
    lines.append("RECOMMANDATIONS DETAILLEES :")
    lines.append("-" * 40)
    for axis in report.axes:
        if axis.recommendations:
            lines.append(f"\n  [{axis.name}] (score: {axis.score}/5)")
            for rec in axis.recommendations:
                lines.append(f"    → {rec}")

    lines.append("\n" + "=" * 60)
    return "\n".join(lines)


def format_json(report: DiagnosticReport) -> str:
    """Formater le rapport en JSON."""
    data = {
        "file": report.file_path,
        "total_score": report.total_score,
        "max_total": report.max_total,
        "percentage": round(report.total_score / report.max_total * 100, 1),
        "grade": report.grade,
        "token_estimate": report.token_estimate,
        "axes": [
            {
                "name": a.name,
                "score": a.score,
                "max": a.max_score,
                "details": a.details,
                "recommendations": a.recommendations,
            }
            for a in report.axes
        ],
        "strengths": report.strengths,
        "weaknesses": report.weaknesses,
        "quick_wins": report.quick_wins,
    }
    return json.dumps(data, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description="Diagnostic automatique de prompts")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", "-f", help="Chemin vers le fichier prompt")
    group.add_argument("--text", "-t", help="Texte du prompt (inline)")
    parser.add_argument("--json", "-j", action="store_true", help="Sortie en JSON")
    args = parser.parse_args()

    # Forcer la sortie UTF-8 sur Windows
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")

    if args.file:
        path = Path(args.file)
        if not path.exists():
            print(f"Erreur: fichier introuvable: {args.file}", file=sys.stderr)
            sys.exit(1)
        text = path.read_text(encoding="utf-8")
        file_path = str(path)
    else:
        text = args.text
        file_path = None

    report = diagnose(text, file_path)

    if args.json:
        print(format_json(report))
    else:
        print(format_report(report))


if __name__ == "__main__":
    main()

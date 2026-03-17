#!/usr/bin/env python3
"""
Correcteur d'accents français pour preplans H5P.

Applique 100+ corrections de regex sur les fichiers JSON pour corriger
les accents français manquants. Valide aussi les endScreens.

Usage:
  python fix_accents.py --input preplan.json
  python fix_accents.py --input preplan.json --output corrected.json
"""
import json
import re
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Tuple


# ============================================================================
# DICTIONNAIRE DE CORRECTIONS
# ============================================================================

CORRECTIONS = [
    # Mots très courants en contexte pédagogique
    (r'\bEtape\b', 'Étape'),
    (r'\betape\b', 'étape'),
    (r'\bReponse\b', 'Réponse'),
    (r'\breponse\b', 'réponse'),
    (r'\bRepondre\b', 'Répondre'),
    (r'\brepondre\b', 'répondre'),
    (r'\bReponds\b', 'Réponds'),
    (r'\breponds\b', 'réponds'),
    (r'\bMethode\b', 'Méthode'),
    (r'\bmethode\b', 'méthode'),
    (r'\bResultat\b', 'Résultat'),
    (r'\bresultat\b', 'résultat'),
    (r'\bResultats\b', 'Résultats'),
    (r'\bresultats\b', 'résultats'),
    (r'\bEleve\b', 'Élève'),
    (r'\beleve\b', 'élève'),
    (r'\bEleves\b', 'Élèves'),
    (r'\beleves\b', 'élèves'),
    (r'\bExercice\b', 'Exercice'),
    (r'\bDeterminer\b', 'Déterminer'),
    (r'\bdeterminer\b', 'déterminer'),
    (r'\bDefis\b', 'Défis'),
    (r'\bdefis\b', 'défis'),
    (r'\bDefi\b', 'Défi'),
    (r'\bdefi\b', 'défi'),
    (r'\bDefinition\b', 'Définition'),
    (r'\bdefinition\b', 'définition'),
    (r'\bPropriete\b', 'Propriété'),
    (r'\bpropriete\b', 'propriété'),
    (r'\bProprietes\b', 'Propriétés'),
    (r'\bproprietes\b', 'propriétés'),
    (r'\bVerification\b', 'Vérification'),
    (r'\bverification\b', 'vérification'),
    (r'\bVerifions\b', 'Vérifions'),
    (r'\bverifions\b', 'vérifions'),
    (r'\bVerifier\b', 'Vérifier'),
    (r'\bverifier\b', 'vérifier'),
    (r'\bVerifie\b', 'Vérifie'),
    (r'\bverifie\b', 'vérifie'),
    (r'\bEquivalent\b', 'Équivalent'),
    (r'\bequivalent\b', 'équivalent'),
    (r'\bEquivalents\b', 'Équivalents'),
    (r'\bequivalents\b', 'équivalents'),
    (r'\bEquation\b', 'Équation'),
    (r'\bequation\b', 'équation'),
    (r'\bEcran\b', 'Écran'),
    (r'\becran\b', 'écran'),
    (r'\bGeneral\b', 'Général'),
    (r'\bgeneral\b', 'général'),
    (r'\bGeometrie\b', 'Géométrie'),
    (r'\bgeometrie\b', 'géométrie'),
    (r'\bGeometriques\b', 'Géométriques'),
    (r'\bgeometriques\b', 'géométriques'),
    (r'\bAlgebre\b', 'Algèbre'),
    (r'\balgebre\b', 'algèbre'),
    (r'\bProbleme\b', 'Problème'),
    (r'\bprobleme\b', 'problème'),
    (r'\bProblemes\b', 'Problèmes'),
    (r'\bproblemes\b', 'problèmes'),
    (r'\bRecapitulatif\b', 'Récapitulatif'),
    (r'\brecapitulatif\b', 'récapitulatif'),
    (r'\bRemediation\b', 'Remédiation'),
    (r'\bremediation\b', 'remédiation'),
    (r'\bReprenons\b', 'Reprenons'),
    (r'\bPresentation\b', 'Présentation'),
    (r'\bpresentation\b', 'présentation'),
    (r'\bDifference\b', 'Différence'),
    (r'\bdifference\b', 'différence'),
    (r'\bDifferent\b', 'Différent'),
    (r'\bdifferent\b', 'différent'),
    (r'\bDifferents\b', 'Différents'),
    (r'\bdifferents\b', 'différents'),
    (r'\bPreference\b', 'Préférence'),
    (r'\bpreference\b', 'préférence'),
    (r'\bGenere\b', 'Généré'),
    (r'\bgenere\b', 'généré'),
    (r'\bResoudre\b', 'Résoudre'),
    (r'\bresoudre\b', 'résoudre'),
    (r'\bResous\b', 'Résous'),
    (r'\bresous\b', 'résous'),
    (r'\bMaitrises\b', 'Maîtrises'),
    (r'\bmaitrises\b', 'maîtrises'),
    (r'\bMaitrise\b', 'Maîtrise'),
    (r'\bmaitrise\b', 'maîtrise'),
    (r'\bMaitriser\b', 'Maîtriser'),
    (r'\bmaitriser\b', 'maîtriser'),
    (r'\bEgal\b', 'Égal'),
    (r'\begal\b', 'égal'),
    (r'\bEgaux\b', 'Égaux'),
    (r'\begaux\b', 'égaux'),
    (r'\bEgalement\b', 'Également'),
    (r'\begalement\b', 'également'),
    (r'\bInteresse\b', 'Intéressé'),
    (r'\binteresse\b', 'intéressé'),
    (r'\bInterdisciplinaire\b', 'Interdisciplinaire'),
    (r'\bbenefices\b', 'bénéfices'),
    (r'\bBenefices\b', 'Bénéfices'),
    (r'\bmelange\b', 'mélange'),
    (r'\bMelange\b', 'Mélange'),
    (r'\bmelanges\b', 'mélanges'),
    (r'\bMelanges\b', 'Mélanges'),
    (r'\bmelanger\b', 'mélanger'),
    (r'\bdenominateur\b', 'dénominateur'),
    (r'\bnumerateur\b', 'numérateur'),
    (r'\belegant\b', 'élégant'),
    (r'\benergie\b', 'énergie'),
    (r'\becole\b', 'école'),
    (r'\belement\b', 'élément'),
    (r'\belements\b', 'éléments'),
    (r'\bevaluation\b', 'évaluation'),
    (r'\bEvaluation\b', 'Évaluation'),
    (r'\bReussi\b', 'Réussi'),
    (r'\breussi\b', 'réussi'),
    (r'\bPreparation\b', 'Préparation'),
    (r'\bpreparation\b', 'préparation'),
    (r'\bPreparer\b', 'Préparer'),
    (r'\bpreparer\b', 'préparer'),
    (r'\bPrepare\b', 'Préparé'),
    (r'\bprepare\b', 'préparé'),
    (r'\bIntermedaire\b', 'Intermédiaire'),
    (r'\bintermediaire\b', 'intermédiaire'),
    (r'\bIntermediaire\b', 'Intermédiaire'),
    (r'\bRecette\b', 'Recette'),
    (r'\brecette\b', 'recette'),
    (r'\bRecettes\b', 'Recettes'),
    (r'\brecettes\b', 'recettes'),
    (r'\bCreer\b', 'Créer'),
    (r'\bcreer\b', 'créer'),
    (r'\bTermine\b', 'Terminé'),
    (r'\btermine\b', 'terminé'),
    (r'\bTermines\b', 'Terminés'),
    (r'\btermines\b', 'terminés'),
    (r'\bExplique\b', 'Explique'),
    (r'\bRepondu\b', 'Répondu'),
    (r'\brepondu\b', 'répondu'),
    (r'\bResume\b', 'Résumé'),
    (r'\bresume\b', 'résumé'),
    (r'\bEnonce\b', 'Énoncé'),
    (r'\benonce\b', 'énoncé'),
    (r'\bEnoncer\b', 'Énoncer'),
    (r'\benoncer\b', 'énoncer'),
    (r'\bCalculee\b', 'Calculée'),
    (r'\bcalculee\b', 'calculée'),
    (r'\bSimplifiee\b', 'Simplifiée'),
    (r'\bsimplifiee\b', 'simplifiée'),
    (r'\bSimplifiees\b', 'Simplifiées'),
    (r'\bsimplifiees\b', 'simplifiées'),
    (r'\bFelicitations\b', 'Félicitations'),
    (r'\bfelicitations\b', 'félicitations'),
    (r'\blegumes\b', 'légumes'),
    (r'\bLegumes\b', 'Légumes'),
    (r'\bbeton\b', 'béton'),
    (r'\bBeton\b', 'Béton'),
    (r'\breponses\b', 'réponses'),
    (r'\bReponses\b', 'Réponses'),
    (r'\bexercices guides\b', 'exercices guidés'),
    (r'\bguide\b(?! )', 'guidé'),
    (r'\bTres bien\b', 'Très bien'),
    (r'\btres bien\b', 'très bien'),
    (r'\btres\b', 'très'),
    (r'\bTres\b', 'Très'),
    (r'\ba la\b', 'à la'),
    (r'\bou\b(?= est\b)', 'où'),
    (r'\bOu\b(?= est\b)', 'Où'),
]


# ============================================================================
# CORRECTION DES ACCENTS
# ============================================================================

def fix_accents_in_string(text: str) -> str:
    """Applique toutes les corrections d'accents sur une chaîne."""
    for pattern, replacement in CORRECTIONS:
        text = re.sub(pattern, replacement, text)
    return text


def fix_accents_in_json(obj) -> any:
    """Parcourt récursivement un objet JSON et corrige les accents."""
    if isinstance(obj, str):
        return fix_accents_in_string(obj)
    elif isinstance(obj, list):
        return [fix_accents_in_json(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: fix_accents_in_json(value) for key, value in obj.items()}
    return obj


# ============================================================================
# VALIDATION DES ENDSCREENS
# ============================================================================

def validate_and_add_endscreens(data: Dict) -> Tuple[int, int]:
    """Valide les endScreens et ajoute les scores manquants.

    Retourne (nombre de corrections, nombre d'endScreens ajoutés).
    """
    corrections = 0
    added_screens = 0

    feedback = data.get('feedback', {})
    scores_in_feedback = feedback.get('score', []) if isinstance(feedback.get('score'), list) else []

    if not isinstance(scores_in_feedback, list):
        scores_in_feedback = [scores_in_feedback] if scores_in_feedback else []

    end_screens = data.get('endScreens', [])
    existing_scores = set(es.get('score', 0) for es in end_screens)

    # Ajouter les endScreens manquants
    for score in scores_in_feedback:
        if score not in existing_scores:
            print(f"  [+] Ajout endScreen pour score {score}")
            data['endScreens'].append({
                'title': f'Score {score}',
                'subtitle': '',
                'score': score
            })
            added_screens += 1
            existing_scores.add(score)

    # Trier par score
    data['endScreens'].sort(key=lambda x: x.get('score', 0))

    return corrections, added_screens


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Corrige les accents français dans un preplan H5P JSON'
    )
    parser.add_argument('--input', '-i', required=True, help='Fichier JSON du preplan')
    parser.add_argument('--output', '-o', help='Fichier de sortie (défaut: remplace input)')

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERREUR: fichier introuvable : {args.input}")
        return 1

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERREUR: JSON invalide ligne {e.lineno}: {e.msg}")
        return 1

    print(f"Correction des accents dans {input_path.name}...")

    # Corriger les accents
    data = fix_accents_in_json(data)
    accent_corrections = sum(
        len(re.findall(pattern, json.dumps(data, ensure_ascii=False)))
        for pattern, _ in CORRECTIONS
    )

    # Valider et ajouter les endScreens
    print("Validation des endScreens...")
    corr_count, added_count = validate_and_add_endscreens(data)

    # Sauvegarder
    output_path = Path(args.output) if args.output else input_path
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print()
    print(f"OK Corrections appliquées : {output_path}")
    print(f"  Corrections d'accents : {len(CORRECTIONS)} patterns")
    print(f"  endScreens ajoutés    : {added_count}")

    return 0


if __name__ == '__main__':
    sys.exit(main())

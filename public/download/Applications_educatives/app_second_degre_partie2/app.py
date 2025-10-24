# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify, request, send_from_directory
from config import Config, BASE_DIR
import json
import os
import sys

# Forcer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Initialiser Flask avec des chemins absolus
app = Flask(__name__,
            static_folder=os.path.join(BASE_DIR, 'static'),
            template_folder=os.path.join(BASE_DIR, 'templates'))
app.config.from_object(Config)

# Chargement du contenu éducatif
def load_content():
    """Charge le contenu éducatif depuis le fichier JSON"""
    content_path = os.path.join(app.config['DATA_FOLDER'], 'content.json')
    with open(content_path, 'r', encoding='utf-8') as f:
        return json.load(f)

CONTENT = load_content()

@app.route('/')
def index():
    """Page principale de l'application"""
    return render_template('index.html',
                         metadata=CONTENT['metadata'],
                         competences=CONTENT['competences'],
                         sections=CONTENT['sections'],
                         config=app.config)

@app.route('/exercices')
def exercices():
    """Page des exercices interactifs"""
    return render_template('exercices.html',
                         metadata=CONTENT['metadata'],
                         exercises=CONTENT['exercises'],
                         config=app.config)

@app.route('/test-js')
def test_js():
    """Page de test JavaScript"""
    return render_template('test_js.html')

@app.route('/api/sections')
def get_sections():
    """API : Récupérer toutes les sections de cours"""
    return jsonify(CONTENT['sections'])

@app.route('/api/sections/<int:section_id>')
def get_section(section_id):
    """API : Récupérer une section spécifique"""
    section = next((s for s in CONTENT['sections'] if s['id'] == section_id), None)
    if not section:
        return jsonify({'error': 'Section not found'}), 404
    return jsonify(section)

@app.route('/api/exercises')
def get_exercises():
    """API : Récupérer tous les exercices"""
    return jsonify(CONTENT['exercises'])

@app.route('/api/exercises/<int:exercise_id>')
def get_exercise(exercise_id):
    """API : Récupérer un exercice spécifique"""
    exercise = next((ex for ex in CONTENT['exercises'] if ex['id'] == exercise_id), None)
    if not exercise:
        return jsonify({'error': 'Exercise not found'}), 404
    return jsonify(exercise)

@app.route('/api/check/<int:exercise_id>', methods=['POST'])
def check_answer(exercise_id):
    """API : Vérifier une réponse d'exercice"""
    data = request.get_json()
    user_answers = data.get('answers', {})

    # Trouver l'exercice
    exercise = next((ex for ex in CONTENT['exercises'] if ex['id'] == exercise_id), None)

    if not exercise:
        return jsonify({'error': 'Exercise not found'}), 404

    # Vérifier chaque champ de réponse
    results = {}
    all_correct = True

    for field in exercise.get('answer_fields', []):
        field_id = field['id']
        user_answer = user_answers.get(field_id, '').strip()

        # Normaliser la réponse utilisateur
        user_answer_normalized = user_answer.lower().replace(' ', '').replace(',', '.')

        # Vérifier selon le type de champ
        if field['type'] == 'number':
            try:
                user_val = float(user_answer_normalized)
                expected_val = float(field['answer'])
                tolerance = field.get('tolerance', 0.01)
                is_correct = abs(user_val - expected_val) <= tolerance
            except (ValueError, TypeError):
                is_correct = False

        elif field['type'] == 'select':
            expected = field['answer'].lower().strip()
            is_correct = user_answer.lower().strip() == expected

        else:  # text
            # Vérifier avec la réponse principale
            expected = str(field['answer']).lower().replace(' ', '').replace(',', '.')
            is_correct = user_answer_normalized == expected

            # Si pas correcte, vérifier avec les alternatives
            if not is_correct and 'alternatives' in field:
                for alt in field['alternatives']:
                    alt_normalized = str(alt).lower().replace(' ', '').replace(',', '.')
                    if user_answer_normalized == alt_normalized:
                        is_correct = True
                        break

        results[field_id] = is_correct
        if not is_correct:
            all_correct = False

    # Retourner le résultat
    return jsonify({
        'correct': all_correct,
        'results': results,
        'hint': exercise.get('hint', ''),
        'solution': exercise.get('solution', '') if not all_correct else None
    })

@app.route('/api/progress', methods=['POST'])
def save_progress():
    """API : Sauvegarder la progression (côté serveur optionnel)"""
    data = request.get_json()
    # Pour l'instant, on retourne juste un statut de succès
    # La sauvegarde réelle se fait côté client avec localStorage
    return jsonify({'status': 'saved', 'message': 'Progression sauvegardée localement'})

@app.errorhandler(404)
def not_found(error):
    """Gestionnaire d'erreur 404"""
    return render_template('error.html', error_code=404, error_message="Page non trouvée"), 404

@app.errorhandler(500)
def internal_error(error):
    """Gestionnaire d'erreur 500"""
    return render_template('error.html', error_code=500, error_message="Erreur interne du serveur"), 500

if __name__ == '__main__':
    print("=" * 80)
    print(f"APPLICATION : {app.config['APP_NAME']}")
    print(f"Niveau : {app.config['APP_LEVEL']}")
    print(f"Thème : {app.config['APP_THEME']}")
    print("=" * 80)
    print(f"Application démarrée sur http://localhost:5000")
    print(f"Cours : http://localhost:5000/")
    print(f"Exercices : http://localhost:5000/exercices")
    print("=" * 80)
    print("Appuyez sur Ctrl+C pour arrêter le serveur")
    print("=" * 80)
    app.run(debug=True, host='127.0.0.1', port=5000)

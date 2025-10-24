import pytest
import json
import sys
import os

# Ajouter le répertoire parent au path pour importer l'application
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app


@pytest.fixture
def client():
    """Fixture pour créer un client de test Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index_page(client):
    """Test de la page d'accueil (cours)"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Second Degr' in response.data
    assert b'Cours' in response.data


def test_exercices_page(client):
    """Test de la page des exercices"""
    response = client.get('/exercices')
    assert response.status_code == 200
    assert b'Exercices' in response.data


def test_api_sections(client):
    """Test de l'API des sections de cours"""
    response = client.get('/api/sections')
    assert response.status_code == 200
    assert response.is_json

    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 3  # 3 sections dans le cours


def test_api_section_detail(client):
    """Test de l'API pour une section spécifique"""
    response = client.get('/api/sections/1')
    assert response.status_code == 200
    assert response.is_json

    data = response.get_json()
    assert data['id'] == 1
    assert 'title' in data
    assert 'content' in data


def test_api_section_not_found(client):
    """Test de l'API avec une section inexistante"""
    response = client.get('/api/sections/9999')
    assert response.status_code == 404


def test_api_exercises(client):
    """Test de l'API des exercices"""
    response = client.get('/api/exercises')
    assert response.status_code == 200
    assert response.is_json

    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 4  # 4 exercices


def test_api_exercise_detail(client):
    """Test de l'API pour un exercice spécifique"""
    response = client.get('/api/exercises/1')
    assert response.status_code == 200
    assert response.is_json

    data = response.get_json()
    assert data['id'] == 1
    assert 'question' in data
    assert 'answer_fields' in data


def test_check_answer_correct(client):
    """Test de vérification - réponse correcte pour l'exercice 1"""
    response = client.post('/api/check/1', json={
        'answers': {
            'delta': '25',
            'x1': '-3/2',
            'x2': '1'
        }
    })

    assert response.status_code == 200
    data = response.get_json()
    assert data['correct'] == True
    assert 'results' in data


def test_check_answer_partial(client):
    """Test de vérification - réponse partiellement correcte"""
    response = client.post('/api/check/1', json={
        'answers': {
            'delta': '25',
            'x1': '-1.5',  # Alternative acceptée
            'x2': '2'  # Incorrect
        }
    })

    assert response.status_code == 200
    data = response.get_json()
    assert data['correct'] == False
    assert data['results']['delta'] == True
    assert data['results']['x1'] == True
    assert data['results']['x2'] == False


def test_check_answer_incorrect(client):
    """Test de vérification - réponse incorrecte"""
    response = client.post('/api/check/1', json={
        'answers': {
            'delta': '20',
            'x1': '0',
            'x2': '0'
        }
    })

    assert response.status_code == 200
    data = response.get_json()
    assert data['correct'] == False
    assert 'solution' in data


def test_check_answer_exercise2(client):
    """Test de vérification pour l'exercice 2"""
    response = client.post('/api/check/2', json={
        'answers': {
            'solution_type': 'Deux solutions distinctes',
            'x1': '1/2',
            'x2': '3'
        }
    })

    assert response.status_code == 200
    data = response.get_json()
    assert data['correct'] == True


def test_check_invalid_exercise(client):
    """Test avec ID d'exercice invalide"""
    response = client.post('/api/check/9999', json={
        'answers': {}
    })

    assert response.status_code == 404


def test_progress_api(client):
    """Test de l'API de sauvegarde de progression"""
    response = client.post('/api/progress', json={
        'completed': [1, 2],
        'score': 80
    })

    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'saved'


def test_404_error(client):
    """Test de la page d'erreur 404"""
    response = client.get('/page-inexistante')
    assert response.status_code == 404


def test_content_json_structure():
    """Test de la structure du fichier content.json"""
    content_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'content.json')

    with open(content_path, 'r', encoding='utf-8') as f:
        content = json.load(f)

    # Vérifier la structure
    assert 'metadata' in content
    assert 'sections' in content
    assert 'exercises' in content
    assert 'competences' in content

    # Vérifier les métadonnées
    assert content['metadata']['version'] == '1.0.0'
    assert content['metadata']['level'] == 'Première Spécialité'

    # Vérifier les sections
    assert len(content['sections']) == 3
    for section in content['sections']:
        assert 'id' in section
        assert 'title' in section
        assert 'content' in section

    # Vérifier les exercices
    assert len(content['exercises']) == 4
    for exercise in content['exercises']:
        assert 'id' in exercise
        assert 'question' in exercise
        assert 'answer_fields' in exercise
        assert 'points' in exercise


def test_all_routes_accessible(client):
    """Test que toutes les routes principales sont accessibles"""
    routes = ['/', '/exercices']

    for route in routes:
        response = client.get(route)
        assert response.status_code == 200, f"Route {route} inaccessible"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

import os
from dotenv import load_dotenv

load_dotenv()

# Chemin de base : répertoire contenant ce fichier config.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-second-degre-2025'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True') == 'True'

    # Métadonnées de l'application
    APP_NAME = 'Second Degré - Partie 2 - Révisions 1ère Spé'
    APP_VERSION = '1.0.0'
    APP_AUTHOR = 'Lycée Camille Claudel'
    APP_LEVEL = 'Première Spécialité'
    APP_THEME = 'Factorisation des trinômes du second degré'

    # Chemins (absolus pour fonctionner depuis n'importe où)
    STATIC_FOLDER = os.path.join(BASE_DIR, 'static')
    TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'templates')
    DATA_FOLDER = os.path.join(BASE_DIR, 'data')

    # Compétences travaillées
    COMPETENCES = [
        "Calculer le discriminant associé à un polynôme de degré 2",
        "Connaître le lien entre discriminant et signe d'un polynôme de degré 2",
        "Dresser le tableau de signes d'une fonction polynôme de degré 2",
        "Résoudre des équations et des inéquations du second degré"
    ]

@echo off
echo ========================================
echo    SETUP SERVEUR ENCODING-FIXER MCP
echo ========================================

cd "%~dp0"

REM Vérification si venv_encoding_fixer existe
if not exist "venv_encoding_fixer" (
    echo 📦 Création de l'environnement virtuel...
    python -m venv venv_encoding_fixer
    if %errorlevel% neq 0 (
        echo ❌ Erreur lors de la création de l'environnement virtuel.
        pause
        exit /b 1
    )
)

REM Activation de l'environnement virtuel
echo 🔄 Activation de l'environnement virtuel...
call venv_encoding_fixer\Scripts\activate.bat

REM Installation/mise à jour des dépendances
echo 📥 Installation des dépendances MCP...
pip install --upgrade pip
pip install "mcp>=1.0.0"

if %errorlevel% neq 0 (
    echo ❌ Erreur lors de l'installation des dépendances.
    pause
    exit /b 1
)

echo ✅ Serveur encoding-fixer MCP configuré avec succès!

REM Créer le répertoire de logs si nécessaire
if not exist "%~dp0logs" (
    mkdir "%~dp0logs"
    echo [OK] Répertoire logs créé
)

REM Test du serveur
echo 🧪 Test du serveur...
python -c "import sys; from pathlib import Path; sys.path.insert(0, str(Path.cwd())); import encoding_fixer_server; print('✅ Import réussi')" 2>nul
if %errorlevel% equ 0 (
    echo ✅ Test du serveur réussi!
) else (
    echo ⚠️  Test du serveur échoué, mais l'installation est OK
)

echo.
echo 🎯 CONFIGURATION CLAUDE CODE:
echo.
echo Ajoutez cette section dans votre settings.json de Claude Code:
echo.
echo   "mcpServers": {
echo     "encoding-fixer-server": {
echo       "command": "python",
echo       "args": [
echo         "%~dp0encoding_fixer_server.py"
echo       ],
echo       "cwd": "%~dp0venv_encoding_fixer\\Scripts",
echo       "env": {}
echo     }
echo   }
echo.
echo 📚 FONCTIONS DISPONIBLES:
echo   - fix_file_encoding(file_path, output_path="", create_backup=True)
echo   - detect_file_encoding(file_path)
echo   - fix_directory_encoding(directory_path, pattern="*.tex", create_backup=True, recursive=False)
echo   - get_encoding_stats()
echo.
echo 💡 USAGE:
echo   Ce serveur corrige automatiquement les problèmes d'encodage UTF-8
echo   dans vos fichiers LaTeX. Particulièrement utile sous Windows!
echo.

pause

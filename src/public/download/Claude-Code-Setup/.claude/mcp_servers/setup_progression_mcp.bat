@echo off
echo ====================================
echo    SETUP SERVEUR PROGRESSION MCP
echo ====================================

cd "%~dp0"

REM Vérification si venv_progression existe
if not exist "venv_progression" (
    echo 📦 Création de l'environnement virtuel...
    python -m venv venv_progression
    if %errorlevel% neq 0 (
        echo ❌ Erreur lors de la création de l'environnement virtuel.
        pause
        exit /b 1
    )
)

REM Activation de l'environnement virtuel
echo 🔄 Activation de l'environnement virtuel...
call venv_progression\Scripts\activate.bat

REM Installation/mise à jour des dépendances
echo 📥 Installation des dépendances MCP...
pip install --upgrade pip
pip install "mcp>=1.0.0"

if %errorlevel% neq 0 (
    echo ❌ Erreur lors de l'installation des dépendances.
    pause
    exit /b 1
)

echo ✅ Serveur progression MCP configuré avec succès!

REM Test du serveur
echo 🧪 Test du serveur...
python -c "from progression-server import mcp; print('✅ Import réussi')" 2>nul
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
echo     "progression-server": {
echo       "command": "python",
echo       "args": [
echo         "%~dp0progression-server.py"
echo       ],
echo       "cwd": "%~dp0",
echo       "env": {}
echo     }
echo   }
echo.
echo 📚 FONCTIONS DISPONIBLES:
echo   - search_progressions(niveau, query)
echo   - filter_by_theme(niveau, theme) 
echo   - filter_by_sequence(niveau, sequence_name)
echo   - get_entry_by_code(niveau, code)
echo   - get_niveaux_available()
echo   - get_themes_available(niveau)
echo   - get_sequences_available(niveau)
echo   - get_progression_stats(niveau)
echo   - advanced_search(niveau, query, theme, sequence)
echo.

pause
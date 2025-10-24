@echo off
echo Configuration du serveur MCP LaTeX Search pour Claude Code
echo.

REM Installer les dépendances (déjà installées normalement)
echo Vérification des dépendances Python...
pip show mcp >nul 2>&1
if %errorlevel% neq 0 (
    echo Installation du package MCP...
    pip install "mcp[cli]"
) else (
    echo Package MCP déjà installé
)

echo.
echo Ajout du serveur MCP LaTeX à Claude Code...

REM Ajouter le serveur MCP avec le chemin complet selon la syntaxe officielle
claude mcp add --scope project latex-search-server -- python "%~dp0latex_search_server.py"

echo.
echo Configuration terminée !
echo.

echo Le serveur MCP 'latex-search-server' est maintenant disponible pour tous vos agents LaTeX.
echo.
echo Outils disponibles :
echo - search_exact_command : Recherche exacte d'une commande LaTeX
echo - search_fuzzy_command : Recherche floue/approximative  
echo - list_available_packages : Liste des packages disponibles
echo - scan_package_commands : Scan complet des commandes d'un package
echo - get_command_definition : Définition complète avec contexte étendu
echo.
echo Les agents peuvent maintenant se documenter automatiquement sur vos packages LaTeX !
echo.
pause
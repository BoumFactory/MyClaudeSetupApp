@echo off
echo Configuration de TOUS les serveurs MCP pour Claude Code
echo.

REM Installer les dépendances
echo Installation des dépendances Python...
pip install "mcp[cli]"

echo.
echo Ajout des serveurs MCP à Claude Code...

REM Supprimer les anciens serveurs s'ils existent
claude mcp remove competences-server 2>nul
claude mcp remove latex-search-server 2>nul

echo.
echo Ajout du serveur Compétences...
claude mcp add --scope project competences-server -- python "%~dp0competences_server_fixed.py"

echo.
echo Ajout du serveur LaTeX Search...
claude mcp add --scope project latex-search-server -- python "%~dp0latex_search_server.py"

echo.
echo Configuration terminée !
echo.

echo ==========================================
echo SERVEURS MCP INSTALLÉS :
echo ==========================================
echo.
echo 1. COMPETENCES-SERVER
echo    - search_competences : Recherche par texte
echo    - filter_by_niveau : Filtre par niveau scolaire
echo    - filter_by_theme : Filtre par thème  
echo    - filter_by_palier : Filtre par palier de difficulté
echo    - get_competence_by_code : Recherche par code exact
echo    - get_niveaux_available : Liste des niveaux
echo    - get_themes_available : Liste des thèmes
echo    - get_paliers_available : Liste des paliers
echo    - get_competences_stats : Statistiques générales
echo    - advanced_search : Recherche multicritères
echo.
echo 2. LATEX-SEARCH-SERVER  
echo    - search_exact_command : Recherche exacte de commandes LaTeX
echo    - search_fuzzy_command : Recherche floue/approximative
echo    - list_available_packages : Liste des packages disponibles
echo    - scan_package_commands : Scan complet des commandes
echo    - get_command_definition : Définition avec contexte étendu
echo.
echo ==========================================
echo Vos agents peuvent maintenant :
echo - Se documenter sur les compétences du programme (286 compétences)
echo - Explorer et analyser vos packages LaTeX automatiquement
echo - Comprendre et adapter le code existant
echo ==========================================
echo.
echo Vérification de l'installation avec : claude mcp list
claude mcp list
echo.
pause
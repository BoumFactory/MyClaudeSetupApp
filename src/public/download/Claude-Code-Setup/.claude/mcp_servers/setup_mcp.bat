@echo off
echo Configuration du serveur MCP Competences pour Claude Code
echo.

REM Installer les dépendances
echo Installation des dépendances Python...
pip install "mcp[cli]"

echo.
echo Ajout du serveur MCP à Claude Code...

REM Ajouter le serveur MCP avec le chemin complet selon la syntaxe officielle
claude mcp add --scope project competences-server -- python "%~dp0competences_server_fixed.py"

echo.
echo Configuration terminée !
echo.
echo Le serveur MCP 'competences-server' est maintenant disponible pour tous vos agents.
echo.
echo Outils disponibles :
echo - search_competences : Recherche par texte
echo - filter_by_niveau : Filtre par niveau scolaire
echo - filter_by_theme : Filtre par thème
echo - filter_by_palier : Filtre par palier de difficulté
echo - get_competence_by_code : Recherche par code exact
echo - get_niveaux_available : Liste des niveaux
echo - get_themes_available : Liste des thèmes
echo - get_paliers_available : Liste des paliers
echo - get_competences_stats : Statistiques générales
echo - advanced_search : Recherche avancée multi-critères
echo.
pause
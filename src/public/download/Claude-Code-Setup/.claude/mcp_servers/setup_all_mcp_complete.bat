@echo off
echo Configuration COMPLETE de TOUS les serveurs MCP pour Claude Code
echo.

REM Installer les dépendances
echo Installation des dépendances Python...
pip install "mcp[cli]"

echo.
echo Suppression des anciens serveurs...

REM Supprimer les anciens serveurs s'ils existent
claude mcp remove competences-server 2>nul
claude mcp remove latex-search-server 2>nul
claude mcp remove document-creator-server 2>nul
claude mcp remove pdf-analyzer-server 2>nul

echo.
echo Ajout de tous les serveurs MCP...

echo.
echo 1. Ajout du serveur Compétences...
claude mcp add --scope project competences-server -- python "%~dp0competences_server_fixed.py"

echo.
echo 2. Ajout du serveur LaTeX Search...
claude mcp add --scope project latex-search-server -- python "%~dp0latex_search_server.py"

echo.
echo 3. Ajout du serveur Document Creator...
claude mcp add --scope project document-creator-server -- python "%~dp0document_creator_server.py"

echo.
echo 4. Ajout du serveur PDF Analyzer...
claude mcp add --scope project pdf-analyzer-server -- "%~dp0venv_pdf_analyzer\Scripts\python.exe" "%~dp0pdf_analyzer_server_lite.py"

echo.
echo Configuration terminée !
echo.

echo ==========================================
echo    SUITE MCP COMPLETE INSTALLÉE !
echo ==========================================
echo.
echo 📊 COMPETENCES-SERVER (286 compétences)
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
echo 🔍 LATEX-SEARCH-SERVER (packages LaTeX)
echo    - search_exact_command : Recherche exacte de commandes
echo    - search_fuzzy_command : Recherche floue/approximative
echo    - list_available_packages : Liste des packages disponibles
echo    - scan_package_commands : Scan complet des commandes
echo    - get_command_definition : Définition avec contexte étendu
echo.
echo 📝 DOCUMENT-CREATOR-SERVER (création guidée)
echo    - start_document_creation : Workflow guidé pas-à-pas
echo    - select_template : Sélection de modèles
echo    - fill_template_fields : Remplissage paramètres
echo    - configure_destination : Configuration finale
echo    - quick_create_document : Mode rapide complet
echo    - list_available_templates : 15 modèles disponibles
echo    - get_template_info : Détails des modèles
echo    - get_workspace_info : Structure workspace
echo.
echo 📄 PDF-ANALYZER-SERVER (analyse complète)
echo    - analyze_pdf : Analyse complète (texte, images, métadonnées)
echo    - extract_pdf_text : Extraction de texte avec mise en page
echo    - extract_pdf_images : Extraction d'images en haute qualité
echo    - extract_pdf_tables : Extraction de tableaux structurés
echo    - get_pdf_metadata : Métadonnées complètes du document
echo    - search_in_pdf : Recherche de texte avec contexte
echo.
echo ==========================================
echo    AGENTS MAINTENANT AUTONOMES !
echo ==========================================
echo.
echo Vos agents peuvent maintenant :
echo ✅ Se documenter sur les 286 compétences du programme
echo ✅ Explorer et analyser vos packages LaTeX automatiquement
echo ✅ Créer des documents structurés via workflow guidé
echo ✅ Analyser des PDF complets (texte, images, tableaux)
echo ✅ Travailler de façon complètement autonome
echo.
echo Vérification de l'installation :
claude mcp list
echo.
echo L'agent latex-bfcours-writer a maintenant TOUS les outils !
pause
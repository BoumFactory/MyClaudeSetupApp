@echo off
echo Configuration du serveur MCP Document Creator pour Claude Code
echo.

REM Vérifier les dépendances
echo Vérification des dépendances Python...
pip show mcp >nul 2>&1
if %errorlevel% neq 0 (
    echo Installation du package MCP...
    pip install "mcp[cli]"
) else (
    echo Package MCP déjà installé
)

echo.
echo Ajout du serveur MCP Document Creator à Claude Code...

REM Ajouter le serveur MCP avec le chemin complet
claude mcp add --scope project document-creator-server -- python "%~dp0document_creator_server.py"

echo.
echo Configuration terminée !
echo.

echo Le serveur MCP 'document-creator-server' est maintenant disponible pour vos agents LaTeX.
echo.
echo Outils disponibles :
echo - start_document_creation : Démarrer le processus guidé
echo - select_template : Sélectionner un modèle  
echo - fill_template_fields : Remplir les champs du modèle
echo - configure_destination : Configurer la destination et options
echo - quick_create_document : Mode rapide avec tous les paramètres
echo - get_template_info : Informations sur un modèle
echo - list_available_templates : Liste tous les modèles
echo - get_workspace_info : Structure du workspace
echo.
echo L'agent latex-bfcours-writer peut maintenant créer des documents automatiquement !
echo.
pause
@echo off
REM Script de configuration du serveur MCP encoding-fixer
echo ======================================================
echo Configuration du serveur MCP encoding-fixer
echo ======================================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou n'est pas dans le PATH
    pause
    exit /b 1
)

echo [OK] Python detecté

REM Installer le package mcp si nécessaire
echo.
echo Installation du package mcp...
pip install mcp >nul 2>&1
if errorlevel 1 (
    echo [WARN] Erreur lors de l'installation de mcp
) else (
    echo [OK] Package mcp installe
)

REM Créer le répertoire de logs si nécessaire
if not exist "%~dp0logs" (
    mkdir "%~dp0logs"
    echo [OK] Repertoire logs cree
)

REM Tester le serveur
echo.
echo Test du serveur encoding-fixer...
python "%~dp0encoding_fixer_server.py" --version >nul 2>&1
if errorlevel 1 (
    echo [WARN] Le serveur n'a pas pu etre testé (normal si pas de flag --version)
) else (
    echo [OK] Serveur operationnel
)

echo.
echo ======================================================
echo Configuration terminée !
echo ======================================================
echo.
echo Le serveur encoding-fixer est pret a etre utilise.
echo.
echo Utilisation dans Claude Code :
echo   - fix_file_encoding(file_path, output_path, create_backup)
echo   - detect_file_encoding(file_path)
echo   - fix_directory_encoding(directory_path, pattern, create_backup, recursive)
echo   - get_encoding_stats()
echo.
pause

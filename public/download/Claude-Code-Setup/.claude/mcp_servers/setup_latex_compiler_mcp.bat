@echo off
echo ============================================
echo Setup du serveur MCP LaTeX Compiler
echo ============================================
echo.

REM Naviguer vers le répertoire des serveurs MCP
cd /d "%~dp0"

echo [1/4] Création de l'environnement virtuel...
if exist venv_latex_compiler (
    echo Environnement virtuel existant détecté, suppression...
    rmdir /s /q venv_latex_compiler
)
python -m venv venv_latex_compiler

echo.
echo [2/4] Activation de l'environnement virtuel...
call venv_latex_compiler\Scripts\activate.bat

echo.
echo [3/4] Installation des dépendances...
pip install --upgrade pip
pip install mcp

echo.
echo [4/4] Test du serveur...
python -c "import mcp.server.fastmcp; print('✓ Package MCP installé correctement')"

if %errorlevel% equ 0 (
    echo.
    echo ============================================
    echo ✅ Installation réussie !
    echo ============================================
    echo.
    echo Le serveur LaTeX Compiler MCP est prêt.
    echo.
    echo Pour tester le serveur :
    echo   python latex_compiler_server.py
    echo.
    echo Méthodes principales disponibles :
    echo   - compile_document(file_path, type, clean)
    echo   - quick_compile(file_path)
    echo   - detect_compilers()
    echo   - test_compilation()
    echo   - add_compilation_profile(name, desc, steps)
    echo.
) else (
    echo.
    echo ============================================
    echo ❌ Erreur lors de l'installation
    echo ============================================
    echo.
    echo Vérifiez que Python est installé et dans le PATH.
    echo.
)

pause
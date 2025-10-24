@echo off
echo ========================================
echo REPARATION DU SERVEUR PDF ANALYZER
echo ========================================
echo.

cd /d "C:\Users\Utilisateur\Documents\Professionnel\1. Reims 2025 - 2026\1. Cours\.claude\mcp_servers"

echo [ETAPE 1] Activation de l'environnement virtuel...
call venv_pdf_analyzer\Scripts\activate.bat

echo.
echo [ETAPE 2] Installation/Mise a jour des dependances...
python -m pip install --upgrade pip
pip install -r requirements_pdf_analyzer.txt

echo.
echo [ETAPE 3] Test du serveur...
python pdf_analyzer_server.py --version 2>nul
if %errorlevel% neq 0 (
    echo ERREUR: Le serveur ne peut pas demarrer
    echo Verification des imports...
    python -c "import PyPDF2, fitz, pdfplumber, PIL, pikepdf, mcp.server; print('Tous les imports OK')"
) else (
    echo Le serveur semble fonctionner correctement
)

echo.
echo ========================================
echo TERMINÉ !
echo ========================================
echo.
echo IMPORTANT: Vous devez redémarrer Claude Desktop pour que les changements prennent effet !
echo.
pause
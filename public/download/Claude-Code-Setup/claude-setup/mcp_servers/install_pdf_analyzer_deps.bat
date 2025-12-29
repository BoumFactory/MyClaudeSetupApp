@echo off
echo ========================================
echo INSTALLATION DES DEPENDANCES PDF ANALYZER (sans pikepdf)
echo ========================================
echo.

cd /d "C:\Users\Utilisateur\Documents\Professionnel\1. Reims 2025 - 2026\1. Cours\.claude\mcp_servers"

echo [ETAPE 1] Activation de l'environnement virtuel...
call venv_pdf_analyzer\Scripts\activate.bat

echo.
echo [ETAPE 2] Installation des dependances sans pikepdf...
python -m pip install --upgrade pip
pip install PyPDF2==3.0.1
pip install PyMuPDF==1.24.0
pip install pdfplumber==0.11.0
pip install Pillow==10.2.0
pip install mcp==1.1.2

echo.
echo [ETAPE 3] Verification des imports...
python -c "import PyPDF2, fitz, pdfplumber, PIL, mcp.server; print('Tous les imports OK !')"

echo.
echo ========================================
echo INSTALLATION TERMINEE !
echo ========================================
echo.
echo IMPORTANT: Redemarrez Claude Desktop maintenant !
echo.
pause
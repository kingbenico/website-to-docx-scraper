@echo off
echo ================================
echo  Site to DOCX - Windows Builder
echo ================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Install Python 3.12 from https://python.org
    pause
    exit /b 1
)

:: Install dependencies including PyInstaller
echo Installing dependencies...
pip install -r requirements.txt
pip install pyinstaller

echo.
echo Building .exe ...
pyinstaller site-to-docx.spec --clean --noconfirm

echo.
if exist "dist\SiteToDocx.exe" (
    echo SUCCESS! Your .exe is at: dist\SiteToDocx.exe
) else (
    echo FAILED. Check the output above for errors.
)
echo.
pause

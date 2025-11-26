@echo off
REM Windows Batch-Script zum Starten der Zuschnittoptimierung
REM Funktioniert mit installiertem Python oder WinPython

echo ========================================
echo Zuschnittoptimierung wird gestartet...
echo ========================================
echo.

REM Prüfe ob Python installiert ist
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Python gefunden!
    echo Starte Streamlit App...
    echo.
    echo Browser oeffnet sich automatisch auf http://localhost:8501
    echo.
    echo Zum Beenden: Strg+C druecken
    echo.
    python -m streamlit run app.py
) else (
    echo FEHLER: Python nicht gefunden!
    echo.
    echo Bitte installieren Sie Python oder verwenden Sie:
    echo 1. Die PyInstaller EXE-Datei
    echo 2. Docker Container
    echo 3. Streamlit Cloud
    echo.
    echo Siehe BUILD_ANLEITUNG.md fuer Details
    pause
)

"""
Build-Script für PyInstaller - Erstellt standalone EXE
Verwendung: python build_exe.py
"""
import PyInstaller.__main__
import sys
from pathlib import Path

print("="*60)
print("  Erstelle Zuschnittoptimierung EXE...")
print("="*60)
print()

# PyInstaller Konfiguration
PyInstaller.__main__.run([
    'app_launcher.py',  # Launcher als Hauptdatei
    '--name=Zuschnittoptimierung',  # Name der EXE
    '--onefile',  # Alles in eine Datei
    '--console',  # Konsolenfenster sichtbar für Fehler und Streamlit
    '--icon=NONE',  # Optional: Pfad zu .ico Datei
    
    # Alle Python-Module einbetten
    '--add-data=app.py;.',
    '--add-data=config.py;.',
    '--add-data=optimizer.py;.',
    '--add-data=excel_handler.py;.',
    '--add-data=pdf_generator.py;.',
    
    # Streamlit und Abhängigkeiten
    '--hidden-import=streamlit',
    '--hidden-import=streamlit.web.cli',
    '--hidden-import=streamlit.runtime.scriptrunner.magic_funcs',
    '--hidden-import=pandas',
    '--hidden-import=openpyxl',
    '--hidden-import=plotly',
    '--hidden-import=plotly.graph_objects',
    '--hidden-import=plotly.express',
    '--hidden-import=altair',
    '--hidden-import=PIL',
    '--hidden-import=PIL.Image',
    '--hidden-import=packaging',
    '--hidden-import=packaging.version',
    '--hidden-import=packaging.specifiers',
    '--hidden-import=packaging.requirements',
    '--hidden-import=pyarrow',
    '--hidden-import=tornado',
    '--hidden-import=tornado.web',
    '--hidden-import=click',
    '--hidden-import=validators',
    '--hidden-import=watchdog',
    '--hidden-import=reportlab',
    '--hidden-import=reportlab.lib',
    '--hidden-import=reportlab.lib.pagesizes',
    '--hidden-import=reportlab.lib.styles',
    '--hidden-import=reportlab.lib.units',
    '--hidden-import=reportlab.platypus',
    '--hidden-import=reportlab.pdfbase',
    '--hidden-import=reportlab.pdfbase.ttfonts',
    
    # Alle Daten sammeln
    '--collect-all=streamlit',
    '--collect-all=plotly',
    '--collect-all=altair',
    
    # Build-Optionen
    '--noconfirm',  # Überschreibe ohne Nachfrage
    '--clean',  # Bereinige vorherige Builds
])

print("\n" + "="*60)
print("  ✅ EXE erfolgreich erstellt!")
print("="*60)
print(f"\n📁 Speicherort:")
print(f"   {Path('dist/Zuschnittoptimierung.exe').absolute()}")
print(f"\n📊 Dateigröße: ~100-150 MB (alle Bibliotheken eingebettet)")
print("\n🚀 So starten Sie die Anwendung:")
print("   1. Doppelklick auf Zuschnittoptimierung.exe")
print("   2. Konsolenfenster öffnet sich (nicht schließen!)")
print("   3. Browser öffnet automatisch nach ~5 Sekunden")
print("   4. Falls nicht: http://localhost:8501 manuell öffnen")
print("\n⏹️  Zum Beenden:")
print("   - Konsolenfenster schließen ODER")
print("   - Strg+C im Konsolenfenster drücken")
print("\n💡 Tipp: EXE kann auf jeden Windows-PC kopiert werden!")
print("="*60)

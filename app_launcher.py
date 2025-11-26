"""
Launcher-Script für Streamlit App - hält Konsole offen und zeigt Fehler
"""
import sys
import os
import subprocess
import webbrowser
import time
from pathlib import Path

def main():
    print("="*60)
    print("  Zuschnittoptimierung - Starte Anwendung...")
    print("="*60)
    print()
    
    # Warte kurz damit Fenster sichtbar ist
    time.sleep(1)
    
    try:
        # Streamlit-Konfiguration sicherstellen
        streamlit_dir = Path.home() / ".streamlit"
        streamlit_dir.mkdir(exist_ok=True)
        
        config_file = streamlit_dir / "config.toml"
        config_content = """[global]
developmentMode = false

[server]
headless = true
port = 8501

[browser]
gatherUsageStats = false
serverAddress = "localhost"
"""
        config_file.write_text(config_content, encoding='utf-8')
        print("✓ Streamlit-Konfiguration erstellt")
        
        # Finde app.py
        if getattr(sys, 'frozen', False):
            # PyInstaller Bundle
            app_dir = Path(sys._MEIPASS)
        else:
            # Normaler Python-Aufruf
            app_dir = Path(__file__).parent
        
        app_file = app_dir / "app.py"
        
        if not app_file.exists():
            raise FileNotFoundError(f"app.py nicht gefunden in: {app_dir}")
        
        print(f"✓ App gefunden: {app_file}")
        print()
        print("Starte Streamlit-Server...")
        print("-" * 60)
        
        # Browser nach kurzer Verzögerung öffnen
        def open_browser():
            time.sleep(3)
            url = "http://localhost:8501"
            print(f"\n✓ Öffne Browser: {url}")
            webbrowser.open(url)
        
        import threading
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
        
        # Streamlit starten (blocking)
        sys.argv = ["streamlit", "run", str(app_file), 
                   "--server.port", "8501",
                   "--server.address", "localhost",
                   "--server.headless", "true",
                   "--browser.gatherUsageStats", "false"]
        
        from streamlit.web import cli as stcli
        sys.exit(stcli.main())
        
    except KeyboardInterrupt:
        print("\n\n✓ Anwendung wurde beendet (Strg+C)")
        print("Fenster schließt in 3 Sekunden...")
        time.sleep(3)
        sys.exit(0)
        
    except Exception as e:
        print("\n" + "="*60)
        print("  FEHLER beim Starten der Anwendung!")
        print("="*60)
        print(f"\nFehlertyp: {type(e).__name__}")
        print(f"Fehlermeldung: {str(e)}")
        print("\nDetails:")
        import traceback
        traceback.print_exc()
        print("\n" + "="*60)
        print("\nDrücken Sie eine beliebige Taste zum Beenden...")
        input()
        sys.exit(1)

if __name__ == "__main__":
    main()

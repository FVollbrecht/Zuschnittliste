# 🚀 Streamlit Cloud Deployment Anleitung

## Voraussetzungen

### 1. Repository auf GitHub
- **WICHTIG:** Repository muss **ÖFFENTLICH** sein für kostenloses Streamlit Cloud
- Alle Dateien müssen gepusht sein
- Repository-URL: https://github.com/FVollbrecht/Zuschnittliste

### 2. Streamlit Cloud Account
- Kostenlos bei https://streamlit.io/cloud
- Mit GitHub-Account anmelden

---

## 📋 Schritt-für-Schritt Deployment

### Schritt 1: Repository vorbereiten

Stelle sicher, dass folgende Dateien vorhanden sind:

```
✅ app.py                    # Hauptdatei
✅ requirements.txt          # Python-Pakete
✅ config.py                 # Konfiguration
✅ optimizer.py              # Optimierungslogik
✅ excel_handler.py          # Excel I/O
✅ pdf_generator.py          # PDF-Export
✅ .streamlit/config.toml    # Streamlit-Konfiguration
✅ packages.txt              # System-Pakete (falls nötig)
```

### Schritt 2: Repository ÖFFENTLICH machen

**Option A: Via GitHub Web-Interface**
1. Gehe zu: https://github.com/FVollbrecht/Zuschnittliste
2. Klicke auf **Settings** (oben rechts)
3. Scrolle ganz nach unten zu **Danger Zone**
4. Klicke auf **Change visibility**
5. Wähle **Make public**
6. Bestätige mit dem Repository-Namen

**Option B: Privat behalten (kostenpflichtig)**
- Streamlit Cloud Pro: $250/Monat
- Oder selbst hosten (siehe unten)

### Schritt 3: Auf Streamlit Cloud deployen

1. **Gehe zu:** https://share.streamlit.io/
2. **Klicke:** "New app" oder "Deploy an app"
3. **Fülle aus:**
   ```
   Repository:    FVollbrecht/Zuschnittliste
   Branch:        main
   Main file:     app.py
   App URL:       zuschnittoptimierung (oder eigener Name)
   ```
4. **Klicke:** "Deploy!"

### Schritt 4: Warten (ca. 3-5 Minuten)

Streamlit Cloud wird:
- Repository klonen
- Dependencies installieren (aus requirements.txt)
- App starten
- URL generieren

### Schritt 5: App ist live! 🎉

Deine App ist erreichbar unter:
```
https://zuschnittoptimierung.streamlit.app
```
(oder dein gewählter Name)

---

## ⚙️ Konfiguration für Deployment

### requirements.txt Prüfen

Aktuelle Pakete:
```txt
pandas>=2.0.0
openpyxl>=3.1.0
streamlit>=1.28.0
plotly>=5.17.0
numpy>=1.24.0
reportlab>=4.0.0
```

**WICHTIG für Streamlit Cloud:**
- Keine Entwicklungs-Pakete (pytest, black, etc.)
- Keine lokalen/relativen Pfade
- Kompatible Versionen

### .streamlit/config.toml

Bereits konfiguriert für Deployment:
```toml
[global]
developmentMode = false

[server]
headless = true
enableCORS = false
maxUploadSize = 50

[browser]
gatherUsageStats = false
```

---

## 🔄 Updates deployen

Nach Code-Änderungen:

1. **Lokal commiten:**
   ```powershell
   git add .
   git commit -m "Update: XYZ Feature"
   ```

2. **Pushen:**
   ```powershell
   git push origin main
   ```

3. **Automatisch deployed!**
   - Streamlit Cloud erkennt Änderungen
   - Automatischer Rebuild
   - App wird aktualisiert (ca. 2-3 Min)

**Manueller Rebuild:**
- In Streamlit Cloud Dashboard: "Reboot" klicken

---

## 🛠️ Troubleshooting

### Problem: "App is not loading"
**Lösung:**
1. Prüfe Logs in Streamlit Cloud Dashboard
2. Teste lokal: `streamlit run app.py`
3. Prüfe requirements.txt auf Fehler

### Problem: "Module not found"
**Lösung:**
1. Prüfe ob alle Pakete in requirements.txt sind
2. Prüfe Schreibweise (Groß-/Kleinschreibung)
3. Teste: `pip install -r requirements.txt`

### Problem: "Out of resources"
**Lösung:**
- Streamlit Cloud Free: 1 GB RAM, 1 CPU
- Optimiere Code für weniger Speicher
- Oder upgrade zu Pro

### Problem: "Upload-Fehler"
**Lösung:**
- maxUploadSize in config.toml erhöhen
- Standard: 50 MB (ausreichend)

---

## 🔒 Alternativen zu öffentlichem Repo

### Option 1: Streamlit Cloud Pro
- **Preis:** $250/Monat
- **Vorteil:** Private Repos, mehr Ressourcen
- **Link:** https://streamlit.io/cloud

### Option 2: Selbst-Hosting (Kostenlos)
```powershell
# Auf eigenem Server/PC:
streamlit run app.py --server.port 8501 --server.address 0.0.0.0

# Mit ngrok für temporären öffentlichen Zugriff:
ngrok http 8501
```

### Option 3: Docker + Cloud-Hosting
```powershell
# Docker-Container bauen
docker build -t zuschnittoptimierung .

# Auf Cloud-Platform deployen:
# - AWS ECS
# - Google Cloud Run
# - Azure Container Apps
# - Heroku
```

### Option 4: Hugging Face Spaces (KOSTENLOS + PRIVAT!)
- **Link:** https://huggingface.co/spaces
- **Vorteil:** Private Apps möglich
- **Anleitung:**
  1. Account erstellen
  2. New Space → Streamlit
  3. Git-Push wie bei GitHub
  4. Private/Public wählbar

---

## 📊 Kosten-Vergleich

| Lösung | Kosten | Privat? | Setup |
|--------|--------|---------|-------|
| Streamlit Cloud Free | 0€ | ❌ Nein | ⭐⭐⭐⭐⭐ Sehr einfach |
| Streamlit Cloud Pro | $250/Mo | ✅ Ja | ⭐⭐⭐⭐⭐ Sehr einfach |
| Hugging Face Spaces | 0€ | ✅ Ja | ⭐⭐⭐⭐ Einfach |
| Selbst-Hosting | 0€ | ✅ Ja | ⭐⭐⭐ Mittel |
| AWS/Azure/GCP | ~$5-50/Mo | ✅ Ja | ⭐⭐ Komplex |

---

## 🎯 Empfehlung für dich

### Für Firmen-/private Nutzung:
→ **Hugging Face Spaces** (kostenlos + privat!)

### Für öffentliche Demo:
→ **Streamlit Cloud Free** (öffentlich erforderlich)

### Für Tablet im Netzwerk:
→ **Selbst-Hosting** auf lokalem PC/Server

---

## ✅ Nächste Schritte

**Wenn du deployen möchtest:**

1. **Entscheide:** Öffentlich oder privat?
2. **Wenn öffentlich:**
   ```powershell
   # Repository pushen
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   
   # Dann auf Streamlit Cloud deployen (siehe oben)
   ```

3. **Wenn privat:**
   - Verwende Hugging Face Spaces, oder
   - Selbst-Hosting lokal

**Soll ich dir bei einem dieser Schritte helfen?**

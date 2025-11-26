# Docker-Image für Zuschnittoptimierung
FROM python:3.11-slim

# Arbeitsverzeichnis
WORKDIR /app

# Systemabhängigkeiten
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Python-Abhängigkeiten kopieren und installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App-Dateien kopieren
COPY app.py .
COPY config.py .
COPY optimizer.py .
COPY excel_handler.py .
COPY README.md .

# Port für Streamlit
EXPOSE 8501

# Streamlit-Konfiguration
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# App starten
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

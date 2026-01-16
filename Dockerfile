FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
COPY app.py .

# --- CHANGEMENT ICI ---
# On dit à Docker de copier DANS un dossier "models/"
# Docker va créer le dossier automatiquement.
COPY models/attack_detector.joblib models/
COPY models/attack_classifier.joblib models/
COPY models/label_encoder_attack.joblib models/
# ----------------------

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
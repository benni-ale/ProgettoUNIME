# Usa un'immagine base di Python
FROM python:3.9

# Imposta la directory di lavoro
WORKDIR /app

# Copia i file di requirements
COPY requirements.txt .

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Copia il resto del codice dell'applicazione
COPY . .

# Esegui lo script per aggiornare la lista dei ticker
RUN python scripts/update_tickers.py

# Esponi la porta su cui l'applicazione gira
EXPOSE 5000

# Comando per eseguire l'applicazione
CMD ["python", "app.py"] 
# Dockerfile
# Använder en liten Python-bild som bas
FROM python:3.9-slim

# Sätt arbetskatalogen inuti containern
WORKDIR /app

# Kopiera Python-filen till containern
COPY app.py .

# Skapa mapp för databasen
RUN mkdir -p /data

# Sätt miljövariabel för databasens sökväg
ENV DB_PATH=/data/test_users.db

# Kör app.py när containern startar
CMD ["python", "app.py"]
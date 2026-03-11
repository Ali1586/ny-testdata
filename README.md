# GDPR Testdata System

Ett enkelt system som hanterar testdata enligt GDPR.  
Kursprojekt: *Testdata, testmiljöer och dataskyddsförordningen (GDPR)*

---

## 📁 Projektstruktur

```
projekt/
├── app.py                          # Huvudapplikation med GDPR-funktioner
├── Dockerfile                      # Container-definition
├── docker-compose.yml              # Startar appen med persistent databas
├── .gitignore                      # Filer som ignoreras av Git
├── README.md                       # Den här filen
└── .github/
    └── workflows/
        └── build-test.yml          # CI/CD Pipeline (GitHub Actions)
```

---

## 🚀 Kom igång

### Krav
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installerat

### Starta applikationen

```bash
# Bygg och starta containern
docker-compose up --build
```

Applikationen:
1. Skapar databasen automatiskt
2. Lägger till två testanvändare
3. Kör anonymisering och radering som demonstration

---

## 🔧 Testa GDPR-funktioner manuellt

Öppna ett **nytt terminalfönster** medan containern körs:

```bash
# Visa alla användare
docker exec gdpr-user-registry python -c "import app; app.display_users()"

# Anonymisera alla användare (GDPR Art. 4(5))
docker exec gdpr-user-registry python -c "import app; app.anonymize_data(); app.display_users()"

# Radera ALL data (GDPR Art. 17 – Right to be Forgotten)
docker exec gdpr-user-registry python -c "import app; app.clear_test_data(); app.display_users()"

# Radera en specifik användare (t.ex. ID 1)
docker exec gdpr-user-registry python -c "import app; app.delete_user(1); app.display_users()"
```

---

## ⚖️ GDPR-implementationer

| Funktion           | GDPR-artikel | Beskrivning                                      |
|--------------------|-------------|--------------------------------------------------|
| `anonymize_data()` | Art. 4(5)   | Ersätter namn och e-post med anonym information  |
| `clear_test_data()`| Art. 17     | Raderar all data ur databasen                    |
| `delete_user(id)`  | Art. 17     | Raderar en specifik användare på begäran         |

---

## 🔄 CI/CD Pipeline

GitHub Actions kör automatiskt vid varje `push` till `main`:
1. Installerar Python och kör `app.py`
2. Bygger Docker-imagen
3. Startar containern och verifierar att allt fungerar

---

## 🛑 Viktigt – GDPR-regler följs

- ✅ Endast **testdata** används (anna@test.se, bo@test.se)
- ✅ Ingen riktig personinformation sparas
- ✅ All data körs i en **isolerad Docker-container**
- ✅ Databasen versionshanteras **inte** (se .gitignore)
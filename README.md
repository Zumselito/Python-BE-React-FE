# NutriTrack — Zutaten-Datenbank

Eine vollständige Fullstack-Anwendung zur Verwaltung und Visualisierung von Lebensmittel-Nährwertdaten.  
Entwickelt als Portfolio-Projekt mit dem Stack der EWE AG Stellenausschreibung WD-5519.

## Tech Stack

| Schicht | Technologie |
|---|---|
| Frontend | React 19, TypeScript, Material UI, Recharts |
| Backend | Python 3.12, FastAPI, pandas |
| Datenbank | AWS DynamoDB (NoSQL) / DynamoDB Local |
| Cloud | AWS Lambda, API Gateway, S3, CloudFront (CDK) |
| CI/CD | GitHub Actions, Docker, GHCR |
| Dev | Devcontainer (VS Code), Docker Compose |

## Schnellstart (Devcontainer)

```bash
# 1. Repository klonen
git clone https://github.com/<dein-username>/nutritrack.git
cd nutritrack

# 2. In VS Code öffnen → "Reopen in Container"
# → Docker Compose startet automatisch:
#   - DynamoDB Local   → http://localhost:8001
#   - FastAPI Backend  → http://localhost:8000
#   - React Frontend   → http://localhost:5173
```

### Ohne Devcontainer (Docker Compose direkt)

```bash
docker compose up --build

# Datenbank mit Beispieldaten befüllen:
docker compose exec backend python -m app.db.seed --force-recreate
```

## API-Dokumentation

Nach dem Start erreichbar unter:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints

```
GET    /api/v1/ingredients/          Liste aller Zutaten (Filter, Suche, Pagination)
POST   /api/v1/ingredients/          Neue Zutat anlegen
GET    /api/v1/ingredients/{id}      Einzelne Zutat
PATCH  /api/v1/ingredients/{id}      Zutat aktualisieren
DELETE /api/v1/ingredients/{id}      Zutat löschen
```

## Tests

```bash
# Im Container:
pytest --cov=app --cov-report=term-missing

# Lokal (mit venv):
cd backend && pip install -e ".[dev]" && pytest
```

## Datenmodell

Jede Zutat (`/100g Rohgewicht`) enthält:

- **Makros**: Kalorien, Protein, Kohlenhydrate, Zucker, Fett, Ballaststoffe, Wasser
- **Vitamine**: A, B1–B12, C, D, E, K (vollständig)
- **Mineralien**: Ca, Fe, Mg, P, K, Na, Zn, Cu, Mn, Se, I, F
- **Kochverhalten**: Vitaminerhalt-Faktoren pro Garmethode (Kochen, Dämpfen, ...)

## Projektstruktur

```
nutritrack/
├── .devcontainer/          # VS Code Devcontainer-Konfiguration
├── .github/workflows/      # GitHub Actions CI/CD
├── backend/
│   ├── app/
│   │   ├── api/v1/         # FastAPI Router
│   │   ├── core/           # Config (pydantic-settings)
│   │   ├── db/             # DynamoDB Client + Seed
│   │   ├── models/         # Pydantic-Modelle
│   │   └── services/       # Business-Logik
│   ├── tests/
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend/               # React + TypeScript (folgt)
├── infrastructure/         # AWS CDK (folgt)
└── docker-compose.yml
```

## CI/CD Pipeline

```
git push → Test (pytest + moto) → Lint (ruff + black + mypy)
         → Build Docker Image → Push GHCR → Deploy AWS CDK
```

## Erweiterungsplanung

- [ ] Rezepte-Modul (nutzt diese API als eigenständigen Service)
- [ ] Nährwert-Bedarfsberechnung (Tagesreferenzwerte)
- [ ] Import via CSV/XLSX (pandas)
- [ ] Authentifizierung (AWS Cognito)

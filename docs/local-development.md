# Ghid local de dezvoltare

## 1. Scop

Acest document descrie pornirea locala a scheletului MVP si comenzile de baza pentru dezvoltare.

Aplicatia ramane read-only fata de WMS si WME. Nu exista integrare live si nu exista scriere in sistemele sursa.

## 2. Cerinte locale

- Docker
- Docker Compose
- Python 3.11, pentru rulare backend fara Docker
- Node.js 20, pentru rulare frontend fara Docker

## 3. Pornire cu Docker Compose

Din radacina repository-ului:

```bash
docker compose up --build
```

Servicii:

- backend: http://localhost:8000
- backend health: http://localhost:8000/health
- frontend: http://localhost:5173
- PostgreSQL: localhost:5432

## 4. Backend local fara Docker

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Testare backend:

```bash
cd backend
pytest
ruff check .
```

## 5. Migrare baza de date

Cu PostgreSQL pornit prin Docker Compose:

```bash
cd backend
alembic upgrade head
```

Generare migrare noua, dupa modificari de model:

```bash
cd backend
alembic revision --autogenerate -m "describe change"
```

Rollback ultima migrare:

```bash
cd backend
alembic downgrade -1
```

## 6. Frontend local fara Docker

```bash
cd frontend
npm install
npm run dev
```

Verificare frontend:

```bash
cd frontend
npm run lint
npm run build
```

## 7. Status MVP-00

MVP-00 livreaza scheletul tehnic:

- backend FastAPI;
- endpoint /health;
- test backend minim;
- frontend React/Vite placeholder;
- Dockerfile backend;
- Dockerfile frontend;
- Docker Compose;
- CI GitHub Actions.

## 8. Status MVP-01

MVP-01 livreaza schema initiala de baza de date:

- configurare DATABASE_URL;
- SQLAlchemy Base;
- sesiune database;
- modele ORM;
- Alembic config;
- migrare initiala;
- test metadata pentru tabelele MVP-01.

Tabele incluse:

- products;
- lots;
- import_batches;
- wms_events;
- wme_events;
- reconciliation_runs;
- reconciliation_matches;
- audit_logs.

## 9. Limite curente

Nu include inca:

- import WMS;
- import WME;
- matching;
- UI operational complet;
- autentificare;
- integrare live ERP/WMS/WME.

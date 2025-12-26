# Backend FleetCommand (FastAPI)

Ce dossier contient le backend FastAPI et la couche de persistance SQLAlchemy. L'objectif est de fournir une base structurée pour développer les modules métier FleetCore/FleetCrew.

## Structure détaillée

```
apps/
├── app/
│   ├── core/           # configuration, logging, sécurité (squelettes)
│   ├── db/             # base SQLAlchemy + modèles
│   ├── integrations/   # intégrations externes (ex: ai_gateway)
│   ├── modules/        # domaines métiers (auth, véhicules, work orders...)
│   ├── utils/          # helpers (uuid, pagination, dates)
│   └── main.py         # point d’entrée FastAPI
├── alembic/            # scripts de migration
├── alembic.ini         # configuration Alembic
├── requirements.txt    # dépendances Python
└── tests/              # tests (squelettes)
```

## Point d'entrée API

Le serveur FastAPI est défini dans `app/main.py` et inclut les routers suivants :

- `app.modules.auth.router`
- `app.modules.users.router`
- `app.modules.vehicles.router`
- `app.modules.repair_requests.router`
- `app.modules.work_orders.router`

Chaque module est prêt à être complété par des schémas Pydantic, des services et des routes CRUD.

## Configuration

La configuration est centralisée dans `app/core/config.py` via `pydantic-settings`.

Variables attendues dans `apps/.env` :

```
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/fleetcommand
JWT_SECRET=change_me
```

## Procédure de démarrage rapide

### 1) Installer les dépendances

```bash
cd apps
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Lancer les migrations

```bash
cd apps
alembic revision --autogenerate -m "init"
alembic upgrade head
```

### 3) Démarrer l'API

```bash
cd apps
uvicorn app.main:app --reload
```

L'API expose par défaut :

- Swagger UI : `http://127.0.0.1:8000/docs`
- OpenAPI JSON : `http://127.0.0.1:8000/openapi.json`

## Modèles de données

Les modèles SQLAlchemy se trouvent dans `app/db/models/` et couvrent :

- véhicules et statut de maintenance,
- utilisateurs et rôles,
- demandes de réparation,
- ordres de travail et historique de statuts.

## Tests

Les fichiers de tests sont présents dans `apps/tests/` mais doivent être complétés. Une suite minimale attendue :

- tests unitaires par module (`auth`, `vehicles`, `work_orders`, etc.),
- tests d'intégration (workflow complet : création véhicule → demande → ordre de travail).

## Bonnes pratiques recommandées

- Créer des schémas Pydantic pour toutes les entrées/sorties d'API.
- Isoler la logique métier dans `services.py` par module.
- Centraliser la gestion des erreurs HTTP dans un module commun.
- Documenter chaque endpoint avec des exemples de payloads.

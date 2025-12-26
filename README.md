# FleetCommand

FleetCommand est un **squelette d'application de gestion de flotte** (SaaS) organisé autour d'un backend FastAPI/SQLAlchemy. Le dépôt pose les bases de deux volets annoncés : **FleetCore** (back-office) et **FleetCrew** (terrain). À ce stade, le backend est prêt à être complété avec des cas d'usage et des vues métier.

## Contenu du dépôt

```
.
├── README.md
└── apps/
    ├── app/               # code FastAPI (routers + logique métier)
    ├── alembic/           # migrations SQLAlchemy
    ├── alembic.ini        # configuration Alembic
    ├── requirements.txt   # dépendances Python
    └── tests/             # tests (squelettes)
```

## Composants principaux

- **API FastAPI** : point d'entrée `apps/app/main.py` avec routers pour l'auth, les utilisateurs, les véhicules, les ordres de travail et les demandes de réparation.
- **SQLAlchemy** : modèles dans `apps/app/db/models/`.
- **Migrations Alembic** : configuration prête dans `apps/alembic/`.
- **Configuration** : via `pydantic-settings` et fichier `.env`.

## Pré-requis

- Python 3.11+
- Une base PostgreSQL (locale ou via Docker)

## Procédure d'installation locale (pas-à-pas)

### 1) Préparer l'environnement Python

```bash
cd apps
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Configurer les variables d'environnement

Créer un fichier `apps/.env` :

```
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/fleetcommand
JWT_SECRET=change_me
```

> `apps/app/core/config.py` charge automatiquement ce fichier.

### 3) Initialiser la base de données

Assurez-vous que la base PostgreSQL est accessible avec l'URL ci-dessus, puis :

```bash
cd apps
alembic revision --autogenerate -m "init"
alembic upgrade head
```

### 4) Lancer l'API

```bash
cd apps
uvicorn app.main:app --reload
```

- API : `http://127.0.0.1:8000`
- Swagger UI : `http://127.0.0.1:8000/docs`

## Modèles disponibles (SQLAlchemy)

Les entités principales déjà présentes :

- **Vehicle** : véhicule, VIN, kilométrage, dates d'entrée en service.
- **User** : utilisateur (driver, mechanic, manager).
- **RepairRequest** : demande de réparation liée à un véhicule et un conducteur.
- **WorkOrder** : ordre de travail, statut, origine, liens vers véhicule et technicien.
- **WorkOrderStatusHistory** : historique des changements de statut.

## Prochaines étapes suggérées

- Ajouter des endpoints CRUD complets pour chaque module.
- Définir les permissions par rôle et la gestion des tokens JWT.
- Écrire des tests unitaires et d'intégration dans `apps/tests/`.
- Documenter l'API métier (exemples de payloads et erreurs).

---

Pour plus de détails sur l'API et la configuration backend, consultez `apps/README.md`.

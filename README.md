# FleetCommand

FleetCommand est un **squelette d'application de gestion de flotte** (SaaS) avec deux volets annoncés : **FleetCore** (back‑office) et **FleetCrew** (terrain). Le dépôt contient principalement un backend FastAPI/SQLAlchemy prêt à être complété.

## État actuel du dépôt

Le projet est encore en phase de mise en place. On y trouve surtout :

- une base **backend FastAPI** (structure de modules + configuration),
- des **modèles SQLAlchemy** pour la gestion de la flotte,
- une configuration **Alembic** pour les migrations,
- des fichiers de tests vides (à compléter).

## Structure principale

```
.
├── README.md
└── apps/
    ├── app/
    │   ├── core/           # configuration, logging, sécurité (squelettes)
    │   ├── db/             # base SQLAlchemy + modèles
    │   ├── integrations/   # intégrations externes (ex: ai_gateway)
    │   ├── modules/        # domaines métiers (auth, véhicules, work orders...)
    │   ├── utils/          # helpers (uuid, pagination, dates)
    │   └── main.py         # point d’entrée (actuellement vide)
    ├── alembic/            # scripts de migration
    ├── alembic.ini         # configuration Alembic
    ├── requirements.txt    # dépendances Python
    └── tests/              # tests (actuellement vides)
```

## Modèles de données disponibles

Les modèles SQLAlchemy existants décrivent les entités principales :

- **Vehicle** : véhicule, VIN, kilométrage, dates d’entrée en service.
- **User** : utilisateur (driver, mechanic, manager).
- **RepairRequest** : demande de réparation liée à un véhicule et un conducteur.
- **WorkOrder** : ordre de travail, statut, origine, liens vers véhicule et technicien.
- **WorkOrderStatusHistory** : historique des changements de statut.

Ces modèles se trouvent dans `apps/app/db/models/`.

## Configuration

Le projet utilise `pydantic-settings` pour charger la configuration depuis un fichier `.env` :

```
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/fleetcommand
JWT_SECRET=change_me
```

> Le fichier `apps/app/core/config.py` lit automatiquement ce `.env`.

## Démarrage (prévu)

Le point d’entrée `apps/app/main.py` est vide pour l’instant. Une fois complété, l’application pourra être lancée avec :

```
uvicorn app.main:app --reload
```

## Migrations (Alembic)

Pour lancer des migrations, une fois le backend opérationnel :

```
alembic revision --autogenerate -m "init"
alembic upgrade head
```

La configuration Alembic se base sur `DATABASE_URL` et est définie dans `apps/alembic/env.py`.

## Tests

Le dossier `apps/tests/` contient des fichiers de tests vides. Ils sont prêts à être remplis pour valider les modules métiers (auth, work orders, repair requests, etc.).

## Prochaines étapes suggérées

- Implémenter le **point d’entrée FastAPI** dans `apps/app/main.py`.
- Compléter les **routers/services** dans `apps/app/modules/`.
- Ajouter des tests unitaires et d’intégration.
- Documenter les endpoints API avec OpenAPI/Swagger.

---

Si vous souhaitez que je complète le backend ou ajoute les endpoints de base, indiquez vos priorités (auth, gestion des véhicules, etc.).

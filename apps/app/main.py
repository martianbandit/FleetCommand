from fastapi import FastAPI

from app.modules.auth.router import router as auth_router
from app.modules.files.router import router as files_router
from app.modules.notifications.router import router as notifications_router
from app.modules.planning.router import router as planning_router
from app.modules.repair_requests.router import router as repair_requests_router
from app.modules.users.router import router as users_router
from app.modules.vehicles.router import router as vehicles_router
from app.modules.work_orders.router import router as work_orders_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="FleetCommand API",
        description=(
            "API pour la gestion de flotte FleetCommand. "
            "Authentification, véhicules, demandes de réparation, ordres de travail et notifications."
        ),
        version="0.1.0",
        openapi_tags=[
            {"name": "auth", "description": "Inscription et authentification."},
            {"name": "users", "description": "Profil utilisateur et identité."},
            {"name": "vehicles", "description": "Catalogue des véhicules."},
            {"name": "repair_requests", "description": "Demandes de réparation."},
            {"name": "work_orders", "description": "Ordres de travail et suivi."},
            {"name": "planning", "description": "Planning des interventions."},
            {"name": "files", "description": "Gestion des fichiers partagés."},
            {"name": "notifications", "description": "Notifications temps réel."},
        ],
    )

    app.include_router(auth_router)
    app.include_router(users_router)
    app.include_router(vehicles_router)
    app.include_router(repair_requests_router)
    app.include_router(work_orders_router)
    app.include_router(planning_router)
    app.include_router(files_router)
    app.include_router(notifications_router)
    return app


app = create_app()

from __future__ import annotations

from dataclasses import dataclass, field

from fastapi import FastAPI

from app.core.config import settings
from app.core.constants import APP_NAME
from app.core.logging import configure_logging
from app.modules.auth.router import router as auth_router
from app.modules.repair_requests.router import router as repair_requests_router
from app.modules.users.router import router as users_router
from app.modules.vehicles.router import router as vehicles_router
from app.modules.work_orders.router import router as work_orders_router


@dataclass
class AppCore:
    app: FastAPI = field(init=False)
    logger: object = field(init=False)

    def __post_init__(self) -> None:
        self.logger = configure_logging(APP_NAME, settings.LOG_LEVEL)
        self.app = FastAPI(title=settings.APP_NAME)
        self._register_routers()
        self._register_events()

    def _register_routers(self) -> None:
        self.app.include_router(auth_router)
        self.app.include_router(users_router)
        self.app.include_router(vehicles_router)
        self.app.include_router(repair_requests_router)
        self.app.include_router(work_orders_router)

    def _register_events(self) -> None:
        @self.app.on_event("startup")
        async def _startup() -> None:
            self.logger.info("FleetCommand core started")

        @self.app.on_event("shutdown")
        async def _shutdown() -> None:
            self.logger.info("FleetCommand core shutdown")

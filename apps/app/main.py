from fastapi import FastAPI

from app.core.constants import APP_NAME
from app.core.logging import configure_logging
from app.modules.auth.router import router as auth_router
from app.modules.repair_requests.router import router as repair_requests_router
from app.modules.users.router import router as users_router
from app.modules.vehicles.router import router as vehicles_router
from app.modules.work_orders.router import router as work_orders_router

configure_logging()

app = FastAPI(title=APP_NAME)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(vehicles_router)
app.include_router(repair_requests_router)
app.include_router(work_orders_router)

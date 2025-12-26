from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.modules.auth.router import router as auth_router
from app.modules.repair_requests.router import router as repair_requests_router
from app.modules.users.router import router as users_router
from app.modules.vehicles.router import router as vehicles_router
from app.modules.work_orders.router import router as work_orders_router

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="FleetCommand API")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def read_dashboard() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(vehicles_router)
app.include_router(repair_requests_router)
app.include_router(work_orders_router)

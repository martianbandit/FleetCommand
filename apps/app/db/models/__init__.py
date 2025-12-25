# Importer TOUS les modèles ici pour que:
# 1) SQLAlchemy connaisse toutes les tables
# 2) Alembic puisse auto-générer les migrations

from app.db.models.user import User, UserRole
from app.db.models.vehicle import Vehicle
from app.db.models.repair_request import RepairRequest, RepairRequestStatus
from app.db.models.work_order import WorkOrder, WorkOrderStatus, WorkOrderOrigin
from app.db.models.work_order_status_history import WorkOrderStatusHistory

__all__ = [
    "User",
    "UserRole",
    "Vehicle",
    "RepairRequest",
    "RepairRequestStatus",
    "WorkOrder",
    "WorkOrderStatus",
    "WorkOrderOrigin",
    "WorkOrderStatusHistory",
]

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.db.models.user import User
from app.modules.work_orders.schemas import WorkOrderResponse
from app.modules.work_orders.service import list_work_orders

router = APIRouter(prefix="/work-orders", tags=["work_orders"])


@router.get("", response_model=list[WorkOrderResponse])
def get_work_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[WorkOrderResponse]:
    """Lister les ordres de travail visibles pour l'utilisateur."""
    work_orders = list_work_orders(db, current_user)
    return [WorkOrderResponse.model_validate(item) for item in work_orders]

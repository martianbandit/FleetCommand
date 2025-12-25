from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.db.models.user import User
from app.modules.repair_requests.schemas import RepairRequestResponse
from app.modules.repair_requests.service import list_repair_requests

router = APIRouter(prefix="/repair-requests", tags=["repair_requests"])


@router.get("", response_model=list[RepairRequestResponse])
def get_repair_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[RepairRequestResponse]:
    requests = list_repair_requests(db, current_user)
    return [RepairRequestResponse.model_validate(item) for item in requests]

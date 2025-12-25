from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.db.models.user import User
from app.modules.planning.schemas import PlanningItem
from app.modules.planning.service import list_planning

router = APIRouter(prefix="/planning", tags=["planning"])


@router.get("", response_model=list[PlanningItem])
def get_planning(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[PlanningItem]:
    return list_planning(db, current_user)

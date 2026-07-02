from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.oauth2 import receptionist_required

from app.schemas.visit import (
    VisitCreate,
    VisitUpdate,
    VisitResponse
)

from app.services.visit_service import (
    create_visit,
    get_visits,
    get_visit,
    update_visit,
    filter_visits
)

router = APIRouter(
    prefix="/visits",
    tags=["Visits"]
)


@router.post(
    "",
    response_model=VisitResponse
)
def create(
    visit: VisitCreate,
    db: Session = Depends(get_db),
    current_user=Depends(receptionist_required)
):
    return create_visit(visit, db)


@router.get(
    "",
    response_model=list[VisitResponse]
)
def get_all(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(receptionist_required)
):
    return get_visits(db, page, limit)


@router.get(
    "/{visit_id}",
    response_model=VisitResponse
)
def get_one(
    visit_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(receptionist_required)
):
    return get_visit(visit_id, db)


@router.put(
    "/{visit_id}",
    response_model=VisitResponse
)
def update(
    visit_id: int,
    visit: VisitUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(receptionist_required)
):
    return update_visit(visit_id, visit, db)


@router.get(
    "/filter"
)
def filter_visit(
    visit_date: date | None = None,
    status: str | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(receptionist_required)
):
    return filter_visits(
        db,
        visit_date,
        status
    )


@router.get(
    "/today",
    response_model=list[VisitResponse]
)
def today_visitors(
    db: Session = Depends(get_db),
    current_user=Depends(receptionist_required)
):
    return filter_visits(
        db,
        visit_date=date.today()
    )
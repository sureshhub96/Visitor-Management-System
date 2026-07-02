from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.visit import Visit
from app.models.visitor import Visitor
from app.schemas.visit import VisitCreate, VisitUpdate


ACTIVE_STATUS = [
    "Scheduled",
    "Checked In"
]


def create_visit(
    visit: VisitCreate,
    db: Session
):

    visitor = (
        db.query(Visitor)
        .filter(
            Visitor.id == visit.visitor_id,
            Visitor.is_deleted == False
        )
        .first()
    )

    if not visitor:
        raise HTTPException(
            status_code=404,
            detail="Visitor not found"
        )

    active_visit = (
        db.query(Visit)
        .filter(
            Visit.visitor_id == visit.visitor_id,
            Visit.status.in_(ACTIVE_STATUS),
            Visit.is_deleted == False
        )
        .first()
    )

    if active_visit:
        raise HTTPException(
            status_code=400,
            detail="Visitor already has an active visit"
        )

    if (
        visit.check_in
        and visit.check_out
        and visit.check_out <= visit.check_in
    ):
        raise HTTPException(
            status_code=400,
            detail="Check-out must be after check-in"
        )

    new_visit = Visit(**visit.model_dump())

    db.add(new_visit)
    db.commit()
    db.refresh(new_visit)

    return new_visit


def get_visits(
    db: Session,
    page: int = 1,
    limit: int = 10
):

    offset = (page - 1) * limit

    return (
        db.query(Visit)
        .filter(Visit.is_deleted == False)
        .offset(offset)
        .limit(limit)
        .all()
    )


def get_visit(
    visit_id: int,
    db: Session
):

    visit = (
        db.query(Visit)
        .filter(
            Visit.id == visit_id,
            Visit.is_deleted == False
        )
        .first()
    )

    if not visit:
        raise HTTPException(
            status_code=404,
            detail="Visit not found"
        )

    return visit


def update_visit(
    visit_id: int,
    visit: VisitUpdate,
    db: Session
):

    db_visit = get_visit(visit_id, db)

    update_data = visit.model_dump(exclude_unset=True)

    check_in = update_data.get(
        "check_in",
        db_visit.check_in
    )

    check_out = update_data.get(
        "check_out",
        db_visit.check_out
    )

    if (
        check_in
        and check_out
        and check_out <= check_in
    ):
        raise HTTPException(
            status_code=400,
            detail="Check-out must be greater than check-in"
        )

    if (
        update_data.get("status") == "Checked Out"
        and not check_in
    ):
        raise HTTPException(
            status_code=400,
            detail="Cannot check out before check in"
        )

    for key, value in update_data.items():
        setattr(db_visit, key, value)

    db.commit()
    db.refresh(db_visit)

    return db_visit


def filter_visits(
    db: Session,
    visit_date=None,
    status=None
):

    query = (
        db.query(Visit)
        .filter(
            Visit.is_deleted == False
        )
    )

    if visit_date:
        query = query.filter(
            Visit.visit_date == visit_date
        )

    if status:
        query = query.filter(
            Visit.status == status
        )

    return query.all()
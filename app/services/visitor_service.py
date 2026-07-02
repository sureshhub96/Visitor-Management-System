from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.visitor import Visitor
from app.schemas.visitor import VisitorCreate, VisitorUpdate


def create_visitor(visitor: VisitorCreate, db: Session):
    """
    Create Visitor
    """

    existing = (
        db.query(Visitor)
        .filter(
            Visitor.email == visitor.email,
            Visitor.is_deleted == False
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    new_visitor = Visitor(**visitor.model_dump())

    db.add(new_visitor)
    db.commit()
    db.refresh(new_visitor)

    return new_visitor


def get_visitors(
    db: Session,
    page: int = 1,
    limit: int = 10
):
    offset = (page - 1) * limit

    return (
        db.query(Visitor)
        .filter(Visitor.is_deleted == False)
        .offset(offset)
        .limit(limit)
        .all()
    )


def get_visitor(visitor_id: int, db: Session):

    visitor = (
        db.query(Visitor)
        .filter(
            Visitor.id == visitor_id,
            Visitor.is_deleted == False
        )
        .first()
    )

    if not visitor:
        raise HTTPException(
            status_code=404,
            detail="Visitor not found"
        )

    return visitor


def update_visitor(
    visitor_id: int,
    visitor: VisitorUpdate,
    db: Session
):

    db_visitor = get_visitor(visitor_id, db)

    update_data = visitor.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_visitor, key, value)

    db.commit()
    db.refresh(db_visitor)

    return db_visitor


def delete_visitor(visitor_id: int, db: Session):

    visitor = get_visitor(visitor_id, db)

    visitor.is_deleted = True

    db.commit()

    return {
        "message": "Visitor deleted successfully"
    }


def search_visitors(
    keyword: str,
    db: Session
):

    return (
        db.query(Visitor)
        .filter(
            Visitor.is_deleted == False,
            (
                Visitor.name.ilike(f"%{keyword}%")
            )
            |
            (
                Visitor.phone.ilike(f"%{keyword}%")
            )
        )
        .all()
    )
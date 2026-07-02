from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.oauth2 import receptionist_required

from app.schemas.visitor import (
    VisitorCreate,
    VisitorUpdate,
    VisitorResponse
)

from app.services.visitor_service import (
    create_visitor,
    get_visitors,
    get_visitor,
    update_visitor,
    delete_visitor,
    search_visitors
)

router = APIRouter(
    prefix="/visitors",
    tags=["Visitors"]
)


@router.post(
    "",
    response_model=VisitorResponse
)
def create(
    visitor: VisitorCreate,
    db: Session = Depends(get_db),
    current_user=Depends(receptionist_required)
):
    return create_visitor(visitor, db)


@router.get(
    "",
    response_model=list[VisitorResponse]
)
def get_all(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(receptionist_required)
):
    return get_visitors(db, page, limit)


@router.get(
    "/search",
    response_model=list[VisitorResponse]
)
def search(
    keyword: str,
    db: Session = Depends(get_db),
    current_user=Depends(receptionist_required)
):
    return search_visitors(keyword, db)


@router.get(
    "/{visitor_id}",
    response_model=VisitorResponse
)
def get_one(
    visitor_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(receptionist_required)
):
    return get_visitor(visitor_id, db)


@router.put(
    "/{visitor_id}",
    response_model=VisitorResponse
)
def update(
    visitor_id: int,
    visitor: VisitorUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(receptionist_required)
):
    return update_visitor(visitor_id, visitor, db)


@router.delete(
    "/{visitor_id}"
)
def delete(
    visitor_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(receptionist_required)
):
    return delete_visitor(visitor_id, db)
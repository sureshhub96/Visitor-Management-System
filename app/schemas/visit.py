from datetime import date, time
from pydantic import BaseModel


class VisitBase(BaseModel):
    visitor_id: int
    host_name: str
    department: str
    visit_date: date
    check_in: time | None = None
    check_out: time | None = None
    status: str = "Scheduled"


class VisitCreate(VisitBase):
    pass


class VisitUpdate(BaseModel):
    host_name: str | None = None
    department: str | None = None
    visit_date: date | None = None
    check_in: time | None = None
    check_out: time | None = None
    status: str | None = None


class VisitResponse(VisitBase):
    id: int

    class Config:
        from_attributes = True
from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Time,
    Boolean,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Visit(Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True, index=True)

    visitor_id = Column(
        Integer,
        ForeignKey("visitors.id"),
        nullable=False
    )

    host_name = Column(String(100), nullable=False)

    department = Column(String(100), nullable=False)

    visit_date = Column(Date, nullable=False)

    check_in = Column(Time, nullable=True)

    check_out = Column(Time, nullable=True)

    status = Column(
        String(30),
        default="Scheduled"
    )

    is_deleted = Column(Boolean, default=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Many Visits -> One Visitor
    visitor = relationship(
        "Visitor",
        back_populates="visits"
    )
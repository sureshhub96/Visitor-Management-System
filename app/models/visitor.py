from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Visitor(Base):
    __tablename__ = "visitors"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    phone = Column(String(15), nullable=False)

    email = Column(String(150), unique=True, nullable=False)

    company = Column(String(150), nullable=False)

    purpose_of_visit = Column(String(255), nullable=False)

    is_deleted = Column(Boolean, default=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # One Visitor -> Many Visits
    visits = relationship(
        "Visit",
        back_populates="visitor",
        cascade="all, delete-orphan"
    )
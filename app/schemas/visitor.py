from pydantic import BaseModel, EmailStr, Field


class VisitorBase(BaseModel):
    name: str
    phone: str = Field(
        ...,
        min_length=10,
        max_length=10
    )
    email: EmailStr
    company: str
    purpose_of_visit: str


class VisitorCreate(VisitorBase):
    pass


class VisitorUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    company: str | None = None
    purpose_of_visit: str | None = None


class VisitorResponse(VisitorBase):
    id: int

    class Config:
        from_attributes = True
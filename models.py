from pydantic import BaseModel, Field


class Address(BaseModel):
    country: str = Field(...)
    city: str = Field(...)
    street: str = Field(...)
    house_number: str = Field(...)

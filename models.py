from bson import ObjectId
from pydantic import BaseModel, Field
from pydantic.class_validators import Optional


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class SensorDataModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    temperature: Optional[int]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Sensor",
                "temperature": 300
            }
        }


class SensorUpdateModel(BaseModel):
    name: Optional[str]
    temperature: Optional[int]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "New Sensor Name",
                "temperature": 320
            }
        }


class Address:
    country: str
    city: str
    street: str
    house_number: str

    def __init__(self, country, city, street, house_number):
        self.country = country
        self.city = city
        self.street = street
        self.house_number = house_number

from pydantic import BaseModel, field_validator

class Student(BaseModel):
    name : str
    age :int
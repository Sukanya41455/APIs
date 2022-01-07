from pydantic import BaseModel, Field, validator
from pydantic import BaseSettings
from typing import Optional, List
from pydantic.class_validators import Validator
from pydantic.error_wrappers import ValidationError
import re

# .env file with
"""
LOGIN=Sukanya
API_KEY=SeCR€t!
SEED=42"""
class Settings(BaseSettings): # parsing environment values (python-dotenv)
    api_key: str
    login: str
    seed: int
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

class Address(BaseModel):
    street: str
    number: int
    zipcode: str

class Person(BaseModel):
    first_name: str
    last_name: str
    interest: Optional[List[str]]

# with constraints
class Student(BaseModel):
    first_name : str = Field(min_length=2, max_length=20)
    last_name : str
    age: int = Field(le=100) # less than or equal to 100
    phone_number: str
    address: Optional[Address]

    @validator("phone_number")
    def phone_number_validation(cls, v):
        match = re.match(r"0\d{9}", v)
        if (match is None) or (len(v) != 10):
            raise ValueError("Phone number must have 10 digits")
        return v

address_data = {"street":"main street", "number":1234567890, "zipcode":0000}
address = Address(**address_data)
print(address)

person_data = {"first_name":"Sukanya","last_name":"Sahoo"}
try:
    person = Person(**person_data)
    print(person)
except ValidationError as e:
    print(e.json())


print(person.first_name)

student_data = {"first_name":"Sukanya","last_name":"Sahoo","age":20,"phone_number": "0234567890"}
student = Student(**student_data)
print(student)
print(student.dict())
print(student.json())
print(student.schema())

settings = Settings()
print(settings)
# https://towardsdatascience.com/8-reasons-to-start-using-pydantic-to-improve-data-parsing-and-validation-4f437eae7678

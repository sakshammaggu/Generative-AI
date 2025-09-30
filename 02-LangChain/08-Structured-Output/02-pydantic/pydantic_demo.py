"""
make a dictionary - enter student name and store it and data type is of string not anything else
"""

from pydantic import BaseModel, EmailStr
from typing import Optional

class Student(BaseModel):
    name: str
    age: Optional[int] = None
    email: EmailStr

new_student_dict = {
    "name": "abc",
    "age": 22,
    "email": "abc@gmail.com"
}
student = Student(**new_student_dict)
print(student)
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class Student(BaseModel):
    name: str
    age: Optional[int] = None
    email: EmailStr
    cgpa: float = Field(..., gt=0.0, lt=10.0, description="CGPA must be between 0.0 and 10.0")

new_student_dict = {
    "name": "abc",
    "age": 22,
    "email": "abc@gmail.com",
    "cgpa": 8.4
}

student = Student(**new_student_dict)
print(student)

# pydantic object to dictionary
student_dict = dict(student)
print(student_dict)
print(type(student_dict))

# pydantic object to dictionary
student_new_dict = student.model_dump()
print(student_new_dict)
print(type(student_new_dict))

# pydantic object to JSON
student_json = student.model_dump_json()
print(student_json)
print(type(student_json))
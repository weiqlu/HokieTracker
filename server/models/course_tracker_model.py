from pydantic import BaseModel 

class Section(BaseModel): 
    email: str
    subject_code: str
    course_number: str
    crn: str
    year: int
    semester: str

class User(BaseModel): 
    email: str 
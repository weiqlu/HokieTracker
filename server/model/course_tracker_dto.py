from pydantic import BaseModel 
from datetime import datetime
from typing import Optional 

class SignUpRequest(BaseModel): 
    email: str
    password: str

class LoginRequest(BaseModel): 
    email: str
    password: str

class AddSectionRequest(BaseModel):
    user_id: int
    subject_code: str
    course_number: str
    crn: str
    year: int
    semester: str

######################################################
# Response DTO 
######################################################

class ErrorResponse(BaseModel): 
    error: str

class SuccessResponse(BaseModel): 
    message: str

class UserResponse(BaseModel): 
    id: int 
    email: str
    created_at: datetime
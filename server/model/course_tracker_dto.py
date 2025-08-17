from pydantic import BaseModel 
from datetime import datetime
from typing import Optional 

class SignUpRequest(BaseModel): 
    email: str
    password: str

class LoginRequest(BaseModel): 
    email: str
    password: str

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
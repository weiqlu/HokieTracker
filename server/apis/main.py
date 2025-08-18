from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from repo.course_tracker_repo import CourseTrackerRepo
from service.course_tracker_svc import CourseTrackerSvc
from model.course_tracker_dto import SignUpRequest, LoginRequest, AddSectionRequest, ErrorResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

repo = CourseTrackerRepo()
svc = CourseTrackerSvc(repo=repo)

#####################################################################
# Routes 
#####################################################################

@app.post("/signup")
async def create_user(signup_request: SignUpRequest):
    user = svc.signup_user(email=signup_request.email, password=signup_request.password)

    # existing user (email already exists)
    if isinstance(user, ErrorResponse):
        raise HTTPException(status_code=400, detail=user.error)
    return user

@app.post("/login")
async def login_user(login_request: LoginRequest):
    user = svc.login_user(email=login_request.email, password=login_request.password)
    
    # incorrect password
    if isinstance(user, ErrorResponse):
        raise HTTPException(status_code=401, detail=user.error)
    return user

@app.post("/add_section")
async def add_section(section_request: AddSectionRequest):
    result = svc.add_section(
        user_id=section_request.user_id,
        subject_code=section_request.subject_code,
        course_number=section_request.course_number,
        crn=section_request.crn,
        year=section_request.year,
        semester=section_request.semester
    )

    if isinstance(result, ErrorResponse):
        raise HTTPException(status_code=400, detail=result.error)
    return result

@app.get("/sections/{user_id}")
async def get_sections(user_id: int):
    sections = svc.get_section(user_id=user_id)
    return sections 

@app.delete("/sections/{section_id}")
async def delete_section(section_id: int):
    result = svc.delete_section(section_id=section_id)
    if isinstance(result, ErrorResponse):
        raise HTTPException(status_code=404, detail=result.error)
    return result
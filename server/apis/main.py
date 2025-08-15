from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from repo.course_tracker_repo import CourseTrackerRepo
from service.course_tracker_svc import CourseTrackerSvc
from model.course_tracker_dto import SignUpRequest

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
    return user

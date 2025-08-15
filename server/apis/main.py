from fastapi import FastAPI
import os
import sys

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from repo.course_tracker_repo import CourseTrackerRepo
from service.course_tracker_svc import CourseTrackerSvc

app = FastAPI()

repo = CourseTrackerRepo()
svc = CourseTrackerSvc(repo=repo)

#####################################################################
# Routes 
#####################################################################

@app.post("/signup")
async def create_user(email: str, password: str):
    user = svc.signup_user(email=email, password=password)
    return user

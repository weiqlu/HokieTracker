import os
import sys

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from repo.course_tracker_repo import CourseTrackerRepo

class CourseTrackerSvc: 
    def __init__(self, repo: CourseTrackerRepo):
        self.repo = repo

    # create a new user
    def signup_user(self, email: str, password: str): 
        user = self.repo.create_user(email=email, password=password)
        return user
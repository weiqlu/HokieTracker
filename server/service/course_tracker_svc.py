import os
import sys
import bcrypt

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from repo.course_tracker_repo import CourseTrackerRepo

class CourseTrackerSvc: 
    def __init__(self, repo: CourseTrackerRepo):
        self.repo = repo

    # create a new user
    def signup_user(self, email: str, password: str): 
        # check if email already exists
        if self.repo.get_user_by_email(email=email):
            return {"error": "Email already exists. Please use a different email or try logging in."}

        # password hashing
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        user = self.repo.create_user(email=email, password=hashed_password.decode('utf-8'))
        return user

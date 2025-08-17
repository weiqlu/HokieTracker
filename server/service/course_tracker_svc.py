import os
import sys
import bcrypt

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from repo.course_tracker_repo import CourseTrackerRepo
from model.course_tracker_dto import UserResponse, ErrorResponse, SuccessResponse

class CourseTrackerSvc: 
    def __init__(self, repo: CourseTrackerRepo):
        self.repo = repo

    # create a new user
    def signup_user(self, email: str, password: str): 
        # check if email already exists
        if self.repo.get_user_by_email(email=email):
            return ErrorResponse(error="Email already exists. Please use a different email or try logging in.")

        # password hashing
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        user = self.repo.create_user(email=email, password=hashed_password.decode('utf-8'))
        return SuccessResponse(message="Account created successfully.")

    def login_user(self, email: str, password: str): 
        user = self.repo.get_user_by_email(email=email)

        # verify user exists
        if not user:
            return ErrorResponse(error="Invalid email or password. Please try again.")

        # verify password 
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return UserResponse(
                id=user.id,
                email=user.email,
                created_at=user.created_at
            )
        else: 
            return ErrorResponse(error="Invalid password. Please try again.")

        
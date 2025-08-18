from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Optional, List
import os
import sys
import dotenv

# load environment variables
dotenv.load_dotenv()

# get the path to the parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from model.course_tracker_model import Users, TrackedSections

DATABASE_URL = os.getenv("DATABASE_URL")

try:     
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    connection = engine.connect()
    print("Database connected")
    connection.close()
except Exception as e: 
    print(f"Connection failed: {e}")
    sys.exit(1)


class CourseTrackerRepo(): 
    def __init__(self): 
        self.db = SessionLocal()

    def close(self):
        self.db.close()

    ############################################################
    # USERS 
    ############################################################

    def create_user(self, email: str, password: str) -> Users:
        user = Users(email=email, password=password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_user_by_email(self, email: str) -> Optional[Users]:
        return self.db.query(Users).filter(Users.email == email).first()
    
    ############################################################
    # TRACKED_SECTIONS
    ############################################################

    def create_tracked_section(self, user_id: int, subject_code: str, course_number: str, 
                             crn: str, year: int, semester: str) -> TrackedSections:
        section = TrackedSections(
            user_id=user_id,
            subject_code=subject_code,
            course_number=course_number,
            crn=crn,
            year=year,
            semester=semester,
            # campus defaults to 0 (blacksburg)
            # is_available defaults to false
            # notifications_enabled defaults to true
        )
        self.db.add(section)
        self.db.commit()
        self.db.refresh(section)
        return section
    
    def get_user_tracked_sections(self, user_id: int) -> List[TrackedSections]:
        return self.db.query(TrackedSections).filter(TrackedSections.user_id == user_id).all()
    
    def delete_tracked_section(self, section_id: int) -> bool:
        section = self.db.query(TrackedSections).filter(TrackedSections.id == section_id).first()
        if section:
            self.db.delete(section)
            self.db.commit()
            return True
        return False
    
    def toggle_notifications(self, section_id: int) -> Optional[TrackedSections]:
        section = self.db.query(TrackedSections).filter(TrackedSections.id == section_id).first()
        if section:
            section.notifications_enabled = not section.notifications_enabled
            self.db.commit()
            self.db.refresh(section)
            return section
        return None

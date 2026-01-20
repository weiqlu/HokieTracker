from sqlalchemy import Column, Integer, String, Text, DateTime, func, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base() 

class TrackedSections(Base): 
    __tablename__ = "tracked_sections"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    subject_code = Column(String(10), nullable=False)
    course_number = Column(String(10), nullable=False)
    crn = Column(String(10), nullable=False)
    year = Column(Integer, nullable=False)
    semester = Column(String(10), nullable=False)
    campus = Column(String(10), default="0")
    is_available = Column(Boolean, default=False)
    notifications_enabled = Column(Boolean, default=True)
    

class Users(Base): 
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    phone_number = Column(String(20), nullable=True)
    password = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

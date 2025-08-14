from fastapi import FastAPI
from models.course_tracker_model import Section, User

app = FastAPI()


#####################################################################
# Routes 
#####################################################################

@app.post("/user")
async def create_user(user: User): 
    return 

@app.post("/section")
async def track_section(section: Section): 
    return 

@app.get("/user/{email}/courses")
async def get_user_sections(email: str):
    return 

@app.delete("/section/{section_id}")
async def delete_section(section_id: int):
    return 
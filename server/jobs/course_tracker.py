import requests
from sqlalchemy.orm import Session
from repo.course_tracker_repo import SessionLocal
from model.course_tracker_model import TrackedSections

BASE = "https://selfservice.banner.vt.edu/ssb/HZSKVTSC.P_ProcRequest"
NO_SECTIONS = "NO SECTIONS FOUND FOR THIS INQUIRY."
SEM_CODES = {"SPRING": "01", "SUMMER": "06", "FALL": "09", "WINTER": "12"}

def term_code(year: int, semester: str) -> str:
    sem = semester.upper()
    y = year - 1 if sem == "WINTER" else year
    return f"{y}{SEM_CODES.get(sem, '09')}"

def check_and_update_section(db: Session, section: TrackedSections) -> bool:
    """
    checks a single section against vt. 
    updates the db state immediately if changed.
    returns true if open, false if closed.
    """
    tc = term_code(section.year, section.semester)
    
    payload = {
        "CAMPUS": str(section.campus) if section.campus else "0",
        "TERMYEAR": tc,
        "CORE_CODE": "AR%",
        "subj_code": section.subject_code,
        "SCHDTYPE": "%",
        "CRSE_NUMBER": section.course_number,
        "crn": "", 
        "open_only": "on", 
        "disp_comments_in": "Y",
        "sess_code": "%",
        "BTN_PRESSED": "FIND+class+sections",
        "inst_name": ""
    }

    try:
        r = requests.post(BASE, data=payload, timeout=5)
        txt = r.text
        
        is_open = False
        if NO_SECTIONS not in txt:
            if section.crn in txt:
                is_open = True
        
        # check for state change
        if is_open != section.is_available:
            section.is_available = is_open
            
            if is_open:
                print(f"UPDATE: {section.crn} is now open!")
                # todo: trigger notification here
            
            db.commit() 
            db.refresh(section)
            
        return is_open

    except Exception as e:
        print(f"Error checking {section.crn}: {e}")
        return section.is_available 



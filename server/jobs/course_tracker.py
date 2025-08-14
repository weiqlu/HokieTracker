import sys
import time
import requests

BASE = "https://selfservice.banner.vt.edu/ssb/HZSKVTSC.P_ProcRequest"
NO_SECTIONS = "NO SECTIONS FOUND FOR THIS INQUIRY."

SEM_CODES = {"SPRING": "01", "SUMMER": "06", "FALL": "09", "WINTER": "12"}

def term_code(year: int, semester: str) -> str:
    sem = semester.upper()
    y = year - 1 if sem == "WINTER" else year
    print(f"{y}{SEM_CODES[sem]}")
    return f"{y}{SEM_CODES[sem]}"

queries = []

def add_class(major: str, course_number: str, crns, year: int, semester: str,
              campus: str = "0", core_code: str = "AR%"):
    tc = term_code(year, semester)
    query = {
        "request": {
            "CAMPUS": campus,
            "TERMYEAR": tc,
            "CORE_CODE": core_code,
            "subj_code": major,
            "SCHDTYPE": "%",
            "CRSE_NUMBER": course_number,
            "crn": "",
            "open_only": "on",
            "disp_comments_in": "Y",
            "sess_code": "%",
            "BTN_PRESSED": "FIND+class+sections",
            "inst_name": ""
        },
        "crnFilter": list(crns),
    }
    queries.append(query)


# add_class("MATH", "1026", ["91234"], year=2025, semester="FALL")
add_class("CS", "3724", ["83561"], year=2025, semester="FALL")

while True:
    for query in queries:
        try:
            r = requests.post(BASE, data=query["request"])
            txt = r.text
        except:
            print("Connection error occurred, continuing.")
            continue

        # check if sections found
        if NO_SECTIONS not in txt:
            cut_off = txt.find("<b class=blue_msg>(Optional)</b>")
            sliced = txt[cut_off:] if cut_off != -1 else txt

            found_any = False
            for crn in query["crnFilter"]:
                if crn in sliced:
                    print(f"{query['request']['subj_code']} {query['request']['CRSE_NUMBER']}, CRN: {crn} - True")
                    found_any = True
            
            if not found_any:
                for crn in query["crnFilter"]:
                    print(f"{query['request']['subj_code']} {query['request']['CRSE_NUMBER']}, CRN: {crn} - False")
        else:
            # no sections found at all
            for crn in query["crnFilter"]:
                print(f"{query['request']['subj_code']} {query['request']['CRSE_NUMBER']}, CRN: {crn} - False (No sections found)")

    time.sleep(1)
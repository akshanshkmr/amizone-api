from fastapi import FastAPI, Header, Form
from starlette.responses import RedirectResponse
from typing import Optional
from models import *
from utils import AMIZONE

app = FastAPI(
    title='Amizone API',
    description="REST API for Amity\'s student portal: [Amizone](https://amizone.net/) </br> Made with love by: [Akshansh Kumar](https://github.com/akshanshkmr)💟",
    version='2.0')

@app.get("/", tags=["Metadata"])
async def root():
    return RedirectResponse(url='/docs')

@app.post("/login", tags=["Post"], response_model=LoginResponse)
async def login(username: str = Form(...), password: str = Form(...)):
    client = AMIZONE()
    cookie = client.login(username, password)
    return {'session_cookie':cookie}

@app.get("/profile", tags=["Get"], response_model=ProfileResponse)
async def user_profile(session_cookie: Optional[str] = Header(...)):
    client = AMIZONE(session_cookie)
    profile = client.my_profile()
    return profile

@app.get("/courses", tags=["Get"], response_model=CourseResponse)
async def courses(session_cookie: Optional[str] = Header(...), sem: Optional[str] = None):
    client = AMIZONE(session_cookie)
    courses = client.my_courses(sem)
    return courses

@app.get("/result", tags=["Get"], response_model=ResultResponse)
async def result(session_cookie: Optional[str] = Header(...), sem: Optional[str] = None):
    client = AMIZONE(session_cookie)
    result = client.results(sem)
    return result

@app.get("/faculty", tags=["Get"], response_model=FacultyResponse)
async def faculty(session_cookie: Optional[str] = Header(...)):
    client = AMIZONE(session_cookie)
    faculty = client.my_faculty()
    return faculty

@app.get("/exam_schedule", tags=["Get"], response_model=ExamScheduleResponse)
async def exam_schedule(session_cookie: Optional[str] = Header(...)):
    client = AMIZONE(session_cookie)
    exam_schedule = client.exam_schedule()
    return exam_schedule

@app.get("/timetable", tags=["Get"], response_model=TimeTableResponse)
async def timetable(session_cookie: Optional[str] = Header(...)):
    client = AMIZONE(session_cookie)
    timetable = client.timetable()
    return timetable

@app.get("/sem_count", tags=["Metadata"], response_model=SemCountResponse)
async def sem_count(session_cookie: Optional[str] = Header(...)):
    client = AMIZONE(session_cookie)
    sem_count = client.sem_count()
    return sem_count
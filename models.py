from pydantic import BaseModel

class LoginResponse(BaseModel):
    session_cookie : dict

class ProfileResponse(BaseModel):
    name: str
    enrollment: str
    programme: str
    sem: str
    passyear: str

class CourseResponse(BaseModel):
    course_code: list[str]
    course_name: list[str]
    attendance: list[str]
    syllabus: list[str]

class ResultResponse(BaseModel):
    sem_result: dict
    combined: dict

class FacultyResponse(BaseModel):
    faculties: list[str]
    subjects: list[str]
    images: list[str]

class ExamScheduleResponse(BaseModel):
    course_code: list[str]
    course_title: list[str]
    exam_date: list[str]
    exam_time: list[str]

class TimeTableResponse(BaseModel):
    course_code: list[str]
    course_teacher: list[str]
    class_location: list[str]
    class_time: list[str]

class SemCountResponse(BaseModel):
    sem_count: int
import requests
import bs4
import json

class AMIZONE:
    def __init__(self, session_cookie=None):
        self.URL_BASE    = "https://s.amizone.net"
        self.URL_LOGIN   = "https://student.amizone.net/Login/Login"
        self.URL_HOME    = "https://s.amizone.net/Home"
        self.session     = requests.Session()
        self.session.headers.update({"Referer": self.URL_BASE})
        if session_cookie:
            self.session.cookies.update(json.loads(session_cookie))

    def saveCookie(self):
        with open('cookie.json', 'w') as f:
            json.dump(requests.utils.dict_from_cookiejar(self.session.cookie), f)
    
    def loadCookie(self):
        with open('cookie.json', 'r') as f:
            cookiejar = requests.utils.cookiejar_from_dict(json.load(f))
            self.session.cookies.update(cookiejar)

    def login(self,user,pwd):
        defaultPage=self.session.get(self.URL_BASE)
        htmlObject = bs4.BeautifulSoup(defaultPage.content,'html.parser')
        rvt = htmlObject.find(id="loginform").input['value']
        data = {
            "_UserName": user,
            "_Password": pwd,
            "__RequestVerificationToken": rvt
        }
        self.session.post(self.URL_BASE,data=data)
        return self.session.cookies
    
    def my_profile(self):
        a = self.session.get("https://student.amizone.net/Electives/NewCourseCoding")
        b = bs4.BeautifulSoup(a.content, 'html.parser')
        row1=[x.text for x in b.find_all("div",attrs={"class":"col-md-3"})]
        row2 = [x.text for x in b.find_all("div", attrs={"class": "col-md-2"})]
        name=row1[0].split(': ')[1].strip()
        Enrollment=row1[1].split(': ')[1].strip()
        programme=row2[0].split(': ')[1].strip()
        sem=row2[1].split(': ')[1].strip()
        passyear=row2[2].split(': ')[1].strip()
        return {
            'name':name,
            'enrollment':Enrollment,
            'programme':programme,
            'sem':sem,
            'passyear':passyear
        }
    
    def my_courses(self, sem=None):
        if sem:
            a = self.session.post("https://s.amizone.net/Academics/MyCourses/CourseListSemWise", data= {'sem':sem})
        else:
            a = self.session.get("https://student.amizone.net/Academics/MyCourses")
        b = bs4.BeautifulSoup(a.content, 'html.parser')
        courseCode = [c.text.strip() for c in b.find_all(attrs={'data-title': "Course Code"})]
        courseName = [c.text.strip() for c in b.find_all(attrs={'data-title': "Course Name"})]
        attendance = [c.text.strip() for c in b.find_all(attrs={'data-title': "Attendance"})]
        syllabus   = [c.decode_contents() for c in b.find_all(attrs={'data-title': "Course Syllabus"})]
        # this returned a list(string) of anchor tags so the below code is to extract href from it
        syllabus   = [i[i.find('"')+1:i.find('"',i.find('"')+1)] for i in syllabus]
        return {
            'course_code':courseCode,
            'course_name':courseName,
            'attendance':attendance,
            'syllabus':syllabus,
        }
    
    def results(self, sem=None):
        if sem:
            a = self.session.post("https://s.amizone.net/Examination/Examination/ExaminationListSemWise", data= {'sem':sem})
        else:
            a = self.session.get("https://student.amizone.net/Examination/Examination")
        b = bs4.BeautifulSoup(a.content, 'html.parser')
        courseCode = [c.text.strip() for c in b.find_all(attrs={'data-title': "Course Code"})]
        courseTitle = [c.text.strip() for c in b.find_all(attrs={'data-title': "Course Title"})]
        GradeObtained = [c.text.strip() for c in b.find_all(attrs={'data-title': "Go"})]
        GradePoint=[c.text.strip() for c in b.find_all(attrs={'data-title': "GP"})]

        sgpa=[x.text.strip() for x in b.find_all(attrs={'data-title': "SGPA"})]
        cgpa=[x.text.strip() for x in b.find_all(attrs={'data-title': "CGPA"})]

        return {
            "sem_result":{
                "course_code":courseCode,
                "course_title":courseTitle,
                "grade_obtained":GradeObtained,
                "grade_point":GradePoint,
            },
            "combined":{
                "sgpa":sgpa,
                "cgpa":cgpa
            }
        }
    
    def my_faculty(self):
        a=self.session.get("https://student.amizone.net/FacultyFeeback/FacultyFeedback")
        b = bs4.BeautifulSoup(a.content, 'html.parser')
        faculties=[x.text.strip() for x in b.find_all(attrs={"class":"faculty-name"})]
        subjects=[x.text.strip() for x in b.find_all(attrs={"class":"subject"})]
        images=[x["src"] for x in b.find_all(attrs={"class":"img-responsive"})]
        return {
            'faculties':faculties,
            'subjects':subjects,
            'images':images
        }
    
    def exam_schedule(self):
        a=self.session.get('https://student.amizone.net/Examination/ExamSchedule')
        b = bs4.BeautifulSoup(a.content, 'html.parser')
        courseCode = [c.text.strip() for c in b.find_all(attrs={'data-title': "Course Code"})]
        courseTitle = [c.text.strip() for c in b.find_all(attrs={'data-title': "Course Title"})]
        ExamDate = [c.text.strip() for c in b.find_all(attrs={'data-title': "Exam Date"})]
        Time = [c.text.strip() for c in b.find_all(attrs={'data-title': "Time"})]
        return {
            'course_code':courseCode,
            'course_title':courseTitle,
            'exam_date':ExamDate,
            'exam_time':Time
        }
    
    def timetable(self):
        a=self.session.get("https://student.amizone.net/TimeTable/Home")
        b = bs4.BeautifulSoup(a.content, 'html.parser')
        courseCode = [x.text.strip() for x in b.find_all(attrs={"class":"course-code"})]
        courseTeacher = [c.text.strip() for c in b.find_all(attrs={'class': "course-teacher"})]
        classLocation = [x.text.strip() for x in b.find_all(attrs={"class":"class-loc"})]
        Time = [x.text.strip() for x in b.find_all(attrs={"class": "class-time"})]
        return {
            'course_code':courseCode,
            'course_teacher':courseTeacher,
            'class_location':classLocation,
            'class_time':Time
        }

    def sem_count(self):
        a = self.session.get("https://student.amizone.net/Examination/Examination")
        b = bs4.BeautifulSoup(a.content, 'html.parser')
        sgpa=[x.text.strip() for x in b.find_all(attrs={'data-title': "SGPA"})]
        return {
            "sem_count":len(sgpa)
        }
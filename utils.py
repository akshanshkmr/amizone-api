import requests
import bs4
import json
from fastapi                import HTTPException
from datetime               import datetime
from dateutil.relativedelta import *

class AMIZONE:
    def __init__(self, session_cookie=None):
        self.URL_BASE    = "https://s.amizone.net"
        self.URL_LOGIN   = "https://student.amizone.net/Login/Login"
        self.URL_HOME    = "https://s.amizone.net/Home"
        self.session     = requests.Session()
        self.session.headers.update({"Referer": self.URL_BASE})
        if session_cookie:
            try:
                self.session.cookies.update(json.loads(session_cookie))
            except:
                raise HTTPException(status_code=401, detail="Invalid or Expired cookie")

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
        try:
            a = self.session.get("https://student.amizone.net/Electives/NewCourseCoding")
            b = bs4.BeautifulSoup(a.content, 'html.parser')
            row1=[x.text for x in b.find_all("div",attrs={"class":"col-md-3"})]
            row2 = [x.text for x in b.find_all("div", attrs={"class": "col-md-2"})]
            name=row1[0].split(': ')[1].strip()
            Enrollment=row1[1].split(': ')[1].strip()
            programme=row2[0].split(': ')[1].strip()
            sem=row2[1].split(': ')[1].strip()
            passyear=row2[2].split(': ')[1].strip()
        except:
            raise HTTPException(status_code=401, detail="Invalid or Expired cookie")
        else:
            return {
                'name':name,
                'enrollment':Enrollment,
                'programme':programme,
                'sem':sem,
                'passyear':passyear
            }
    
    def my_courses(self, sem=None):
        try:
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
            percentage=[]
            for i in attendance:
                try:
                    x=float(i[i.find("(")+1:i.find(")")])
                    percentage.append(x)
                except:
                    percentage.append(100.0)
        except:
            raise HTTPException(status_code=401, detail="Invalid or Expired cookie")
        else:
            return {
                'course_code':courseCode,
                'course_name':courseName,
                'attendance':attendance,
                'attendance_pct':percentage,
                'syllabus':syllabus,
            }
    
    def results(self, sem=None):
        try:
            if sem:
                a = self.session.post("https://s.amizone.net/Examination/Examination/ExaminationListSemWise", data= {'sem':sem})
            else:
                a = self.session.get("https://student.amizone.net/Examination/Examination")
            b = bs4.BeautifulSoup(a.content, 'html.parser')
            courseCode = [c.text.strip() for c in b.find_all(attrs={'data-title': "Course Code"})]
            courseTitle = [c.text.strip() for c in b.find_all(attrs={'data-title': "Course Title"})]
            GradeObtained = [c.text.strip() for c in b.find_all(attrs={'data-title': "Go"})]
            GradePoint=[c.text.strip() for c in b.find_all(attrs={'data-title': "GP"})]
            sgpa=[float(x.text.strip()) for x in b.find_all(attrs={'data-title': "SGPA"})]
            cgpa=[x.text.strip() for x in b.find_all(attrs={'data-title': "CGPA"})]
            if len(sgpa):
                cgpa[0] = sgpa[0]
                cgpa=[float(x) for x in cgpa]
        except:
            raise HTTPException(status_code=401, detail="Invalid or Expired cookie")
        else:
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
        try:
            a = self.session.get("https://student.amizone.net/FacultyFeeback/FacultyFeedback")
            b = bs4.BeautifulSoup(a.content, 'html.parser')
            faculties=[x.text.strip() for x in b.find_all(attrs={"class":"faculty-name"})]
            subjects=[x.text.strip() for x in b.find_all(attrs={"class":"subject"})]
            images=[x["src"] for x in b.find_all(attrs={"class":"img-responsive"})]
        except:
            raise HTTPException(status_code=401, detail="Invalid or Expired cookie")
        else:
            return {
                'faculties':faculties,
                'subjects':subjects,
                'images':images
            }
    
    def exam_schedule(self):
        try:
            a = self.session.get('https://student.amizone.net/Examination/ExamSchedule')
            b = bs4.BeautifulSoup(a.content, 'html.parser')
            courseCode = [c.text.strip() for c in b.find_all(attrs={'data-title': "Course Code"})]
            courseTitle = [c.text.strip() for c in b.find_all(attrs={'data-title': "Course Title"})]
            ExamDate = [c.text.strip() for c in b.find_all(attrs={'data-title': "Exam Date"})]
            Time = [c.text.strip() for c in b.find_all(attrs={'data-title': "Time"})]
        except:
            raise HTTPException(status_code=401, detail="Invalid or Expired cookie")
        else:
            return {
                'course_code':courseCode,
                'course_title':courseTitle,
                'exam_date':ExamDate,
                'exam_time':Time
            }
    
    def timetable(self, date=datetime.now().strftime("%Y-%m-%d")):
        import re
        timestamp = round(datetime.now().timestamp()*1000)
        start = datetime.strptime(date, "%Y-%m-%d")
        end = start
        try:
            res = self.session.get("https://s.amizone.net/Calendar/home/GetDiaryEvents?start={0}&end={1}&_={2}".format(date, end, timestamp))
            res_json = json.loads(res.content)
            courseCode = [i['CourseCode'] for i in res_json]
            courseTitle = [i['title'] for i in res_json]
            courseTeacher = [re.sub('&lt;/?[a-z]+&gt;', '', i['FacultyName'].split('[')[0]) for i in res_json]
            classLocation = [i['RoomNo'] for i in res_json]
            Time = [i['start'].split(' ')[1].replace(':00','') + ' - ' + i['end'].split(' ')[1].replace(':00','') for i in res_json]
            Attendance = []
            for i in res_json:
                if i['AttndColor'] == '#4FCC4F':
                    Attendance.append(1)
                elif i['AttndColor'] == '#f00':
                    Attendance.append(-1)
                elif i['AttndColor'] == '#3a87ad':
                    Attendance.append(0)
        except:
            raise HTTPException(status_code=401, detail="Invalid or Expired cookie")
        else:
            return {
                'course_code':courseCode,
                'course_title':courseTitle,
                'course_teacher':courseTeacher,
                'class_location':classLocation,
                'class_time':Time,
                'attendance':Attendance
            }

    def sem_count(self):
        try:
            a = self.session.get("https://student.amizone.net/Academics/MyCourses")
            b = bs4.BeautifulSoup(a.content, 'html.parser')
            sem = b.find('option', selected=True).text.strip()
        except:
            raise HTTPException(status_code=401, detail="Invalid or Expired cookie")
        else:
            return {
                'sem_count':sem
            }
    
    def cookie_status(self):
        try:
            a = self.session.get("https://student.amizone.net/Academics/MyCourses")
            b = bs4.BeautifulSoup(a.content, 'html.parser')
            b.find('option', selected=True).text.strip()
        except:
            raise HTTPException(status_code=401, detail="Invalid or Expired cookie")
        else:
            return {
                'cookie_status':'valid',
            }

import pickle
import requests
import bs4

URL_HOME = "https://student.amizone.net/Home"
URL = "https://student.amizone.net/"
URL_LOGIN = "https://student.amizone.net/Login/Login"

#Enter your credentials here
username=""
password=""

class Cookies:
    def __init__(self):
        self.filename = "cookies"
        self.cookies = None

    def saveCookie(self,requestsCookieJar):
        with open("./"+self.filename,'wb') as f:
            pickle.dump(requestsCookieJar,f)
        self.cookies=requestsCookieJar

    def loadCookie(self):
        with open("./"+self.filename,'rb') as f:
            self.cookies = pickle.load(f)

    def login(self,user,pwd):
        s= requests.Session()
        s.headers.update({"Referer":URL})
        defaultPage=s.get(URL)
        htmlObject = bs4.BeautifulSoup(defaultPage.content,'html.parser')
        rvt = htmlObject.find(id="loginform").input['value']
        data = {
            "_UserName": user,
            "_Password": pwd,
            "__RequestVerificationToken": rvt
        }
        logged = s.post(URL_LOGIN,data=data)
        self.saveCookie(s.cookies)

r = requests.Session()
r.headers.update({"Referer": URL})
c = Cookies()

def login():
    try:
        c.loadCookie()
    except:
        if (r.get(URL_HOME).url == URL):
            c.login(username,password)
    finally:
        r.cookies = c.cookies

def my_profile():
    a = r.get("https://student.amizone.net/Electives/NewCourseCoding?X-Requested-With=XMLHttpRequest")
    b = bs4.BeautifulSoup(a.content, 'html.parser')
    row1=[x.text for x in b.find_all("div",attrs={"class":"col-md-3"})]
    row2 = [x.text for x in b.find_all("div", attrs={"class": "col-md-2"})]
    name=row1[0]
    Enrollment=row1[1]
    programme=row2[0]
    sem=row2[1]
    passyear=row2[2]
    img="https://amizone.net/amizone/Images/Signatures/"+username+"_P.png"
    print(name)
    print(Enrollment)
    print(programme)
    print(sem)
    print(passyear)

def my_courses():
    a = r.get("https://student.amizone.net/Academics/MyCourses?X-Requested-With=XMLHttpRequest")
    b = bs4.BeautifulSoup(a.content, 'html.parser')
    courseId = [c.button.get('onclick').split("'")[1].strip() for c in b.find_all(attrs={"data-title": "Attendance"})]
    courseCode = [c.text.strip() for c in b.find_all(attrs={'data-title': "Course Code"})]
    courseName = [c.text.strip() for c in b.find_all(attrs={'data-title': "Course Name"})]
    attendance = [c.text.strip() for c in b.find_all(attrs={'data-title': "Attendance"})]

    print("Course code     Course name                                                  Attendance")
    for i in range(len(courseCode)):
        print("{:15s} {:60s} {:10s}".format(courseCode[i], courseName[i], attendance[i]))
    return (courseId)


def results():
    a=r.get("https://student.amizone.net/Examination/Examination?X-Requested-With=XMLHttpRequest")
    b = bs4.BeautifulSoup(a.content, 'html.parser')
    sgpa=[x.text.strip() for x in b.find_all(attrs={'data-title': "SGPA"})]
    cgpa=[x.text.strip() for x in b.find_all(attrs={'data-title': "CGPA"})]
    print("Semester SGPA CGPA")
    for i in range(len(sgpa)):
        print("{}        {:4} {:4}".format(i+1,sgpa[i],cgpa[i]))

def my_faculty():
    a=r.get("https://student.amizone.net/FacultyFeeback/FacultyFeedback?X-Requested-With=XMLHttpRequest")
    b = bs4.BeautifulSoup(a.content, 'html.parser')
    faculties=[x.text.strip() for x in b.find_all(attrs={"class":"faculty-name"})]
    subjects=[x.text.strip() for x in b.find_all(attrs={"class":"subject"})]
    images=[x["src"] for x in b.find_all(attrs={"class":"img-responsive"})]
    print("Subjects                                                          Faculties            Image Url")
    for i in range(len(subjects)):
         print("{:65s} {:20s} {}".format(subjects[i],faculties[i],images[i]))


if __name__ == "__main__":
    login()
    results()

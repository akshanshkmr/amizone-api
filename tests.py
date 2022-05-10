from fastapi.testclient import TestClient
from main import *
import pytest

client = TestClient(app)

class Test_Amizone():

    def test_client(self):
        response = client.get("/")
        assert response.status_code == 200

    @pytest.mark.xfail(reason="Expected failure due to incorrect credentials")
    def test_login(self):
        username = 'incorrect_username'
        password = 'incorrect_password'
        response = client.post('/login', data={'username': username, 'password': password})
        assert response.status_code == 200

    def test_profile(self):
        response = client.get('/profile', headers={'session-cookie': 'incorrect_cookie'})
        assert response.status_code == 401
    
    def test_courses(self):
        response = client.get('/courses', headers={'session-cookie': 'incorrect_cookie'})
        assert response.status_code == 401

    def test_result(self):
        response = client.get('/result', headers={'session-cookie': 'incorrect_cookie'})
        assert response.status_code == 401

    def test_faculty(self):
        response = client.get('/faculty', headers={'session-cookie': 'incorrect_cookie'})
        assert response.status_code == 401
    
    def test_exam_schedule(self):
        response = client.get('/exam_schedule', headers={'session-cookie': 'incorrect_cookie'})
        assert response.status_code == 401
    
    def test_timetable(self):
        response = client.get('/timetable', headers={'session-cookie': 'incorrect_cookie'})
        assert response.status_code == 401

    def test_sem_count(self):
        response = client.get('/sem_count', headers={'session-cookie': 'incorrect_cookie'})
        assert response.status_code == 401

    def test_cookie_status(self):
        response = client.get('/cookie_status', headers={'session-cookie': 'incorrect_cookie'})
        assert response.status_code == 401

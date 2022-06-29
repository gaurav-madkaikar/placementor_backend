from app.routes import logout
import datetime
import json
import unittest
import logging
import jwt

from app import db
from app.models import Student, Recruiter, InstiAdmin
from app.test.base import BaseTestCase

def add_student(self, name, email, password):
    return self.client.post(
        '/register',
        data=json.dumps({
            'email':email,
            'username':name,
            'password':password,
            'usertype':'student'
        }),
        content_type='application/json'
    )

def add_recruiter(self, name, email, password, gen_id):
    return self.client.post(
        '/register',
        data=json.dumps({
            'email':email,
            'username':name,
            'password':password,
            'usertype':'recruiter',
            'gen_id': gen_id
        }),
        content_type='application/json'
    )

def add_alumni(self, name, email, password):
    return self.client.post(
        '/register',
        data=json.dumps({
            'email':email,
            'username':name,
            'password':password,
            'usertype':'alumni'
        }),
        content_type='application/json'
    )


def login_user(self, name, password):
    return self.client.post(
        '/login',
        data=json.dumps({
            'username': name,
            "password": password
        }),
        content_type='application/json'
    )

def logout_user(self, login_response):
    return self.client.post(
        '/logout',
        data=json.dumps({}),
        content_type='application/json',
        headers = dict(Authorization='Bearer' + ' ' + json.loads(login_response.data.decode())['auth_token'])
    )


# Tests for authentication
class TestAuth(BaseTestCase):

    def test_user_authentication(self):
        """ Test for registration, login and logout for an User"""

        with self.client:
            # ----- Register -----
            # Valid details
            # Student
            stud = add_student(self, name="Gaurav", email="gm@123", password="testpass")
            response_data = json.loads(stud.data.decode())
            self.assertTrue(response_data['status'] == 'success')
            self.assertEqual(stud.status_code, 200)

            # Alumni
            alum = add_alumni(self, name="Mahesh", email="mm@123", password="testpass")
            response_data = json.loads(alum.data.decode())
            self.assertTrue(response_data['status'] == 'success')
            self.assertEqual(stud.status_code, 200)

            # Recruiter
            rec = add_recruiter(self, name="Citi", email="citi@company", password="testpass", gen_id="#CIT@2002")
            response_data = json.loads(rec.data.decode())
            self.assertTrue(response_data['status'] == 'success')
            self.assertEqual(stud.status_code, 200)

            # COMMENT
            # Duplicate Id's
            # same name
            stud = add_student(self, name="Gaurav", email="hm@123", password="testpass")
            response_data = json.loads(stud.data.decode())
            self.assertTrue(response_data['status'] == 'invalid')
            self.assertEqual(stud.status_code, 401)

            # same email
            alum = add_alumni(self, name="Vineet", email="mm@123", password="testpass")
            response_data = json.loads(alum.data.decode())
            self.assertTrue(response_data['status'] == 'invalid')
            self.assertEqual(stud.status_code, 401)

            #  Invalid Id (only for recruiter)
            rec = add_recruiter(self, name="ABS", email="abs@company", password="testpass", gen_id="#ab@111")
            response_data = json.loads(rec.data.decode())
            self.assertTrue(response_data['status'] == 'invalid')
            self.assertEqual(stud.status_code, 401)

            # ----- Login -----
            # ----- Login for the student: Gaurav (existing) -----
            login_response = login_user(self, name="Gaurav", password="testpass")
            data = json.loads(login_response.data.decode())
            self.assertTrue(data['username'] == "Gaurav")
            self.assertEqual(login_response.status_code, 200)

            # # ----- Logout -----
            result = logout_user(self, login_response)
            res = json.loads(result.data.decode())
            self.assertTrue(res['status'] == 'success')
            self.assertTrue(result.status_code == 200)

            # ----- Login for a non-existing student:  -----
            login_response = login_user(self, "Ramu", "testpass")
            data = json.loads(login_response.data.decode())
            self.assertTrue(data['status'] == "invalid")
            self.assertEqual(login_response.status_code, 404)

            # ----- Login for the alumnus: Mahesh -----
            login_response = login_user(self, "Mahesh", "testpass")
            data = json.loads(login_response.data.decode())
            self.assertTrue(data['username'] == "Mahesh")
            self.assertEqual(login_response.status_code, 200)

            # ----- Logout -----
            result = logout_user(self, login_response)
            res = json.loads(result.data.decode())
            self.assertTrue(res['status'] == 'success')
            self.assertTrue(result.status_code == 200)

            # ----- Login for a non-existing alumnus:  -----
            login_response = login_user(self, "Shyam", "testpass")
            data = json.loads(login_response.data.decode())
            self.assertTrue(data['status'] == "invalid")
            self.assertEqual(login_response.status_code, 404)

            # ----- Login for the recruiter: Citi -----
            login_response = login_user(self, "Mahesh", "testpass")
            data = json.loads(login_response.data.decode())
            self.assertTrue(data['username'] == "Mahesh")
            self.assertEqual(login_response.status_code, 200)

            # ----- Logout -----
            result = logout_user(self, login_response)
            res = json.loads(result.data.decode())
            self.assertTrue(res['status'] == 'success')
            self.assertTrue(result.status_code == 200)

            # ----- Login for a non-existing recruiter:  -----
            login_response = login_user(self, "Deutsche", "testpass")
            data = json.loads(login_response.data.decode())
            self.assertTrue(data['status'] == "invalid")
            self.assertEqual(login_response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
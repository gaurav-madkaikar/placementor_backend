from datetime import datetime
import json
import unittest

from app import db
from app.models import Student, Recruiter, InstiAdmin, Alumni, Message, Profile, Feedback, Notice, Application, ToBeRead
from app.test.base import BaseTestCase
import time


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
            "password": password,
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

## UseCases

class TestUseCases(BaseTestCase):
        # Search users by a search string
        def test_user_search_byname(self):
            with self.client:
                # register an user
                user_response = add_recruiter(self, "Doodle", "hello@123", "testpass", "#DOO@2020")
                response_data = json.loads(user_response.data.decode())
                self.assertTrue(response_data['status'] == 'success')
                self.assertEqual(user_response.status_code, 200)

                # login the user
                login_response = login_user(self, "Doodle", "testpass")
                data = json.loads(login_response.data.decode())
                self.assertTrue(data['username'] == "Doodle")
                self.assertEqual(login_response.status_code, 200)

                
                # Load dummy users
                user1 = add_student(self, "Gaurav", "gm@mail", "testpass")
                user2 = add_student(self, "Pooran", "np@mail", "testpass")

                response1 = self.client.post(
                    '/fetchusernames',
                    data=json.dumps({'string': 'oo'}),
                    content_type='application/json',
                    headers = dict(Authorization='Bearer' + ' ' + json.loads(login_response.data.decode())['auth_token'])
                    )
                   

                response2 = self.client.post(
                    '/fetchusernames',
                    data=json.dumps({'string': 'az'}),
                    content_type='application/json',
                    headers = dict(Authorization='Bearer' + ' ' + json.loads(login_response.data.decode())['auth_token'])
                    )

                data1 = json.loads(response1.data.decode())
                data2 = json.loads(response2.data.decode())

                self.assertTrue(data1['status'] == 'success')
                self.assertEqual(data1['names'][0], "Doodle")
                self.assertEqual(data1['names'][1], "Pooran")
                self.assertEqual(len(data1['names']), 2)
                self.assertTrue(response1.status_code == 200)

                self.assertEqual(data2['status'], 'success')
                self.assertEqual(len(data2['names']), 0)
                self.assertTrue(response2.status_code == 200)

                result = logout_user(self, login_response)
                res = json.loads(result.data.decode())
                self.assertTrue(res['status'] == 'success')
                self.assertTrue(result.status_code == 200)
                
        # Get data for a logged-in user
        def test_get_data(self):
            with self.client:
                # register an user
                user_response = add_alumni(self, "Ramesh", "ram@123", "testpass")
                response_data = json.loads(user_response.data.decode())
                self.assertTrue(response_data['status'] == 'success')
                self.assertEqual(user_response.status_code, 200)

                # login the user
                login_response = login_user(self, "Ramesh", "testpass")
                datax = json.loads(login_response.data.decode())
                self.assertTrue(datax['username'] == "Ramesh")
                self.assertEqual(login_response.status_code, 200)

                # Load dummy users
                user1 = add_student(self, "Varun", "vs@mail", "testpass")
                data1 = json.loads(user1.data.decode())
                self.assertEqual(data1['status'], 'success')
                self.assertEqual(user_response.status_code, 200)

                user2 = add_recruiter(self, name="Microsoft", email="ms@mail", password="testpass", gen_id="#MST@1997")
                data2 = json.loads(user2.data.decode())
                self.assertEqual(data2['status'], 'success')
                self.assertEqual(user_response.status_code, 200)

                auth = Recruiter.query.filter_by(username="Microsoft").first()
                id1 = Alumni.query.filter_by(username="Ramesh").first().id
                id2 = Student.query.filter_by(username="Varun").first().id

                # Create dummy data for test 
                m = Message(content="Hello !!", date_time=time.time(), author_id=id1, recipient_id=id2)
                db.session.add(m)

                p = Profile(profileName="SDE", company=auth, ctc=2500000, releaseDate=time.time(), description="WFH", degree="Btech, Dual, Msc", dept="CS, EE, ECE")
                db.session.add(p)
                db.session.commit()

                n = Notice(date_time=time.time(), subject="New job position update", content="Microsoft India open a new position for the role of SDE", author_id=1)
                db.session.add(n)

                # Get the response
                response = self.client.post(
                    '/getdata',
                    data=json.dumps({'timestamp': 0}),
                    content_type='application/json',
                    headers = dict(Authorization='Bearer' + ' ' + json.loads(login_response.data.decode())['auth_token'])
                    )

                data_rec = json.loads(response.data.decode())
                self.assertTrue(data_rec['status'] == 'success')
                self.assertTrue(response.status_code == 200)
                self.assertFalse(len(data_rec['notices']) == 0)
                self.assertFalse(len(data_rec['messages']) == 0)
                self.assertFalse(len(data_rec['positions']) == 0)

                result = logout_user(self, login_response)
                res = json.loads(result.data.decode())
                self.assertTrue(res['status'] == 'success')
                self.assertTrue(result.status_code == 200)

         # Create messages
        def test_create_messages(self):
            with self.client:
                user1 = add_student(self, "MrA", "a@123", "testpass")
                r1 = json.loads(user1.data.decode())
                user2 = add_student(self, "MrB", "b@123", "testpass")
                r2 = json.loads(user2.data.decode())
                user3 = add_alumni(self, "MrC", "c@123", "testpass")
                r3 = json.loads(user3.data.decode())
                user4 = add_recruiter(self, "Tata", "tata@123", "testpass", "#TAT@2000")
                r3 = json.loads(user4.data.decode())

                # login the user
                login_response = login_user(self, "MrA", "testpass")
                datax = json.loads(login_response.data.decode())
                self.assertTrue(datax['username'] == "MrA")
                self.assertEqual(login_response.status_code, 200)

                # /createmessage : Student - Same Student
                response_ = self.client.post('/createmessage', 
                    data=json.dumps({
                        "recipient_username": "MrA",
                        "msg_content": "Hello!"
                },
                ),
                content_type = 'application/json',
                headers = dict(Authorization='Bearer' + ' ' + json.loads(login_response.data.decode())['auth_token'])
                )
                rec_data = json.loads(response_.data.decode())
                self.assertTrue(rec_data['status'] == "invalid")
                self.assertEqual(response_.status_code, 400)

                # /createmessage : Student - Different Student
                response_ = self.client.post('/createmessage', 
                    data=json.dumps({
                        "recipient_username": "MrB",
                        "msg_content": "Hello!"
                }),
                content_type = 'application/json',
                headers = dict(Authorization='Bearer' + ' ' + json.loads(login_response.data.decode())['auth_token'])
                )
                rec_data = json.loads(response_.data.decode())
                self.assertTrue(rec_data['status'] == "invalid")
                self.assertEqual(response_.status_code, 403)

                # /createmessage : Student - Alumni
                response_ = self.client.post('/createmessage', 
                    data=json.dumps({
                        "recipient_username": "MrC",
                        "msg_content": "Hello Sir!"
                }),
                content_type = 'application/json',
                headers = dict(Authorization='Bearer' + ' ' + json.loads(login_response.data.decode())['auth_token'])
                )

                rec_data = json.loads(response_.data.decode())
                self.assertTrue(rec_data['status'] == "success")
                self.assertEqual(response_.status_code, 200)

                # /createmessage : Student - InstiAdmin
                response_ = self.client.post('/createmessage', 
                    data=json.dumps({
                        "recipient_username": "admin",
                        "msg_content": "Hello Sir!"
                }),
                content_type = 'application/json',
                headers = dict(Authorization='Bearer' + ' ' + json.loads(login_response.data.decode())['auth_token'])
                )

                rec_data = json.loads(response_.data.decode())
                self.assertTrue(rec_data['status'] == "invalid")
                self.assertEqual(response_.status_code, 403)

                # Logout user: MrA
                result = logout_user(self, login_response)
                res = json.loads(result.data.decode())
                self.assertTrue(res['status'] == 'success')
                self.assertTrue(result.status_code == 200)

                # Login user: Alumni
                login_response = login_user(self, "MrC", "testpass")
                datax = json.loads(login_response.data.decode())
                self.assertTrue(datax['username'] == "MrC")
                self.assertEqual(login_response.status_code, 200)

                # /createmessage : Alumni - Student
                response_ = self.client.post('/createmessage', 
                    data=json.dumps({
                        "recipient_username": "MrB",
                        "msg_content": "Hello student!"
                }),
                content_type = 'application/json',
                headers = dict(Authorization='Bearer' + ' ' + json.loads(login_response.data.decode())['auth_token'])
                )

                rec_data = json.loads(response_.data.decode())
                self.assertTrue(rec_data['status'] == "success")
                self.assertEqual(response_.status_code, 200)

                 # /createmessage : Alumni - InstiAdmin
                response_ = self.client.post('/createmessage', 
                    data=json.dumps({
                        "recipient_username": "admin",
                        "msg_content": "Hello Sir!"
                }),
                content_type = 'application/json',
                headers = dict(Authorization='Bearer' + ' ' + json.loads(login_response.data.decode())['auth_token'])
                )
                rec_data = json.loads(response_.data.decode())
                self.assertEqual(rec_data['status'], "invalid")
                self.assertEqual(response_.status_code, 403)

                # Logout user: MrC
                result = logout_user(self, login_response)
                res = json.loads(result.data.decode())
                self.assertTrue(res['status'] == 'success')
                self.assertTrue(result.status_code == 200)

                # Login user: Recruiter
                login_response = login_user(self, "Tata", "testpass")
                datax = json.loads(login_response.data.decode())
                self.assertTrue(datax['username'] == "Tata")
                self.assertEqual(login_response.status_code, 200)

                # /createmessage : Recruiter - InstiAdmin
                response_ = self.client.post('/createmessage', 
                    data=json.dumps({
                        "recipient_username": "admin",
                        "msg_content": "Hello Sir!"
                }),
                content_type = 'application/json',
                headers = dict(Authorization='Bearer' + ' ' + json.loads(login_response.data.decode())['auth_token'])
                )

                rec_data = json.loads(response_.data.decode())
                self.assertTrue(rec_data['status'] == "success")
                self.assertEqual(response_.status_code, 200)

                # /createmessage : Recruiter - Student
                response_ = self.client.post('/createmessage', 
                    data=json.dumps({
                        "recipient_username": "MrB",
                        "msg_content": "Hello student!"
                }),
                content_type = 'application/json',
                headers = dict(Authorization='Bearer' + ' ' + json.loads(login_response.data.decode())['auth_token'])
                )

                rec_data = json.loads(response_.data.decode())
                self.assertTrue(rec_data['status'] == "invalid")
                self.assertEqual(response_.status_code, 403)

                # /createmessage : Recruiter - Alumni
                response_ = self.client.post('/createmessage', 
                    data=json.dumps({
                        "recipient_username": "MrC",
                        "msg_content": "Hello student!"
                }),
                content_type = 'application/json',
                headers = dict(Authorization='Bearer' + ' ' + json.loads(login_response.data.decode())['auth_token'])
                )

                rec_data = json.loads(response_.data.decode())
                self.assertTrue(rec_data['status'] == "invalid")
                self.assertEqual(response_.status_code, 403)

                # Logout user: Tata
                result = logout_user(self, login_response)
                res = json.loads(result.data.decode())
                self.assertTrue(res['status'] == 'success')
                self.assertTrue(result.status_code == 200)

                # Non-existing user
                user5 = add_alumni(self, "MrX", "c@123", "testpass")
                r5 = json.loads(user5.data.decode())

                response_ = self.client.post('/createmessage', 
                    data=json.dumps({
                        "recipient_username": "MrD",
                        "msg_content": "Hello student!"
                }),
                content_type = 'application/json',
                headers = dict(Authorization='Bearer' + ' ' + json.loads(login_response.data.decode())['auth_token'])
                )
                rec_data = json.loads(response_.data.decode())
                self.assertTrue(rec_data['status'] == "fail")
                self.assertEqual(response_.status_code, 500)

                # Logout user: MrX
                result = logout_user(self, login_response)
                res = json.loads(result.data.decode())
                self.assertTrue(res['status'] == 'success')
                self.assertTrue(result.status_code == 200)

        # Create feedbacks
        def test_give_feedback(self):
            with self.client:
                #register a recruiter
                user_response = add_recruiter(self, "Doodle", "doo@abc", "testpass", "#DOO@2020")
                response_data = json.loads(user_response.data.decode())
                self.assertTrue(response_data['status'] == 'success')
                self.assertEqual(user_response.status_code, 200)

                #register an alumni
                user_response2 = add_alumni(self, "aditya", "adi@123", "testpass")
                response_data = json.loads(user_response2.data.decode())
                self.assertTrue(response_data['status'] == 'success')
                self.assertEqual(user_response2.status_code, 200)

                #login the alumni
                login_response = login_user(self, "aditya", "testpass")
                data = json.loads(login_response.data.decode())
                self.assertTrue(data['username'] == "aditya")
                self.assertEqual(login_response.status_code, 200)

                #create a job profile
                profile = Profile(profileName = 'profile4',companyName = 'Doodle',ctc = 1000000,createDate = time.time(),deadline = datetime(2021,4,10).timestamp(),description = 'description',degree = 'B.Tech, M.Tech',dept = 'CS, EC')
                db.session.add(profile)
                db.session.commit()

                response = self.client.post('/writefeedback',data = json.dumps({'feedback_content' : 'feedback','subject' : 'nice company','profile_id' : profile.id}),content_type = 'application/json',headers = dict(Authorization='Bearer' + ' ' + json.loads(login_response.data.decode())['auth_token']))
                response1 = self.client.post('/writefeedback',data = json.dumps({'feedback_content' : 'feedback','subject' : 'nice company','profile_id' : -1}),content_type = 'application/json',headers = dict(Authorization='Bearer' + ' ' + json.loads(login_response.data.decode())['auth_token']))

                data = json.loads(response.data.decode())
                data1 = json.loads(response1.data.decode())

                self.assertTrue(data['status'] == 'success')
                self.assertEqual(response.status_code,200)
                self.assertTrue(isinstance(Feedback.query.filter_by(profile_id = profile.id,author_id = Alumni.query.filter_by(username = 'aditya').first().id).first(),Feedback))

                self.assertTrue(data1['status'] == 'fail')
                self.assertEqual(response1.status_code,404)

                #logout the user
                result = logout_user(self, login_response)
                res = json.loads(result.data.decode())
                self.assertTrue(res['status'] == 'success')
                self.assertTrue(result.status_code == 200)

        # Create applications
        def test_create_applications(self):
            with self.client:
                #register a recruiter
                user_response = add_recruiter(self, "Doodle", "doo@abc", "testpass", "#DOO@2020")
                response_data = json.loads(user_response.data.decode())
                self.assertTrue(response_data['status'] == 'success')
                self.assertEqual(user_response.status_code, 200)

                #register a student
                user_response2 = add_student(self, "bharath", "hello@abc", "testpass")
                response_data = json.loads(user_response2.data.decode())
                self.assertTrue(response_data['status'] == 'success')
                self.assertEqual(user_response2.status_code, 200)

                #login the student
                login_response = login_user(self, "bharath", "testpass")
                data = json.loads(login_response.data.decode())
                self.assertTrue(data['username'] == "bharath")
                self.assertEqual(login_response.status_code, 200)

                #create a job profile
                profile = Profile(profileName = 'profile2',companyName = 'Doodle',ctc = 1200000,createDate = time.time(),deadline = datetime(2022,4,10).timestamp(), description = 'description',degree = 'B.Tech,M.Tech',dept = 'CS,EC',recruiter_id = Recruiter.query.filter_by(username = "Doodle").first().id)
                profile1 = Profile(profileName = 'profile3',companyName = 'Doodle',ctc = 1300000,createDate = time.time(),deadline = datetime(2021,3,27).timestamp(), description = 'description',degree = 'B.Tech,M.Tech',dept = 'CS,EC',recruiter_id = Recruiter.query.filter_by(username = "Doodle").first().id)
                db.session.add(profile)
                db.session.add(profile1)
                db.session.commit()

                response = self.client.post('/application',data = json.dumps({'profile_id' : profile.id,'resume_link': 'https://novoresume.com/editor/new-resume'}),content_type = 'application/json',headers = dict(Authorization='Bearer' + ' ' + json.loads(login_response.data.decode())['auth_token']))
                response1 = self.client.post('/application',data = json.dumps({'profile_id' : profile1.id,'resume_link' : 'https://novoresume.com/editor/new-resume'}),content_type = 'application/json',headers = dict(Authorization='Bearer' + ' ' + json.loads(login_response.data.decode())['auth_token']))
                response2 = self.client.post('/application',data = json.dumps({'profile_id' : -1,'resume_link' : 'https://novoresume.com/editor/new-resume'}),content_type = 'application/json',headers = dict(Authorization='Bearer' + ' ' + json.loads(login_response.data.decode())['auth_token']))

                data = json.loads(response.data.decode())
                data1 = json.loads(response1.data.decode())
                data2 = json.loads(response2.data.decode())

                self.assertEqual(data['status'],'success')
                self.assertEqual(response.status_code, 200)
                self.assertTrue(isinstance(Application.query.filter_by(profile_id = profile.id,student_id = Student.query.filter_by(username = 'bharath').first().id).first(),Application))

                self.assertTrue(data1['status'] == 'invalid')
                self.assertEqual(response1.status_code,404)

                self.assertTrue(data2['status'] == 'fail')
                self.assertEqual(response2.status_code,404)

                #logout the user
                result = logout_user(self, login_response)
                res = json.loads(result.data.decode())
                self.assertTrue(res['status'] == 'success')
                self.assertTrue(result.status_code == 200)


        def test_accept_applications(self):
            with self.client:
                #register a student
                user_response = add_student(self, "bharath", "bha@abc", "testpass")
                response_data = json.loads(user_response.data.decode())
                self.assertTrue(response_data['status'] == 'success')
                self.assertEqual(user_response.status_code, 200)

                #register a recruiter
                user_response2 = add_recruiter(self, "Doodle", "doo@abc", "testpass", "#DOO@2020")
                response_data = json.loads(user_response2.data.decode())
                self.assertTrue(response_data['status'] == 'success')
                self.assertEqual(user_response2.status_code, 200)

                # login the recruiter
                login_response = login_user(self, "Doodle", "testpass")
                data = json.loads(login_response.data.decode())
                self.assertTrue(data['username'] == "Doodle")
                self.assertEqual(login_response.status_code, 200)

                #create a job profile
                profile = Profile(profileName = 'profile1',companyName = 'Doodle',ctc = '1200000',createDate = time.time(),deadline = datetime(2021,4,10).timestamp(),description = 'description',degree = 'B.Tech,M.Tech',dept = 'CS,EC',recruiter_id = Recruiter.query.filter_by(username = "Doodle").first().id)
                db.session.add(profile)

                #application for the job
                app = Application(date_time = time.time(),status = 0,content = 'resume link',profile_id = profile.id,student_id = Student.query.filter_by(username = 'bharath').first().id)
                db.session.add(app)
                db.session.commit()

                response = self.client.post('/selectapplication',data = json.dumps({'application_id' : app.id,'new_status' : 1}),content_type = 'application/json',headers = dict(Authorization='Bearer' + ' ' + json.loads(login_response.data.decode())['auth_token']))

                data = json.loads(response.data.decode())

                self.assertTrue(data['status'] == 'success')
                self.assertEqual(response.status_code,200)
                self.assertTrue(Application.query.filter_by(id = app.id).first().status == 1)

                #logout the user
                result = logout_user(self, login_response)
                res = json.loads(result.data.decode())
                self.assertTrue(res['status'] == 'success')
                self.assertTrue(result.status_code == 200)

        def test_create_profile(self):
            with self.client:
                #register the recruiter
                user_response2 = add_recruiter(self, "Doodle", "doo@abc", "testpass","#DOO@2020")
                response_data = json.loads(user_response2.data.decode())
                self.assertTrue(response_data['status'] == 'success')
                self.assertEqual(user_response2.status_code, 200)

                # login the recruiter
                login_response = login_user(self, "Doodle", "testpass")
                data = json.loads(login_response.data.decode())
                self.assertTrue(data['username'] == "Doodle")
                self.assertEqual(login_response.status_code, 200)

                response = self.client.post('/createposition',data = json.dumps({'profileName' : 'SE_Lead','companyName' : 'Doodle','CTC' : 1200000,'createDate' : time.time(),'deadline' : datetime(2021,4,10).timestamp(), 'description' : 'description','degrees': 'B.Tech, M.Tech','depts' : 'CS, EC'}), content_type = 'application/json',headers = dict(Authorization='Bearer' + ' ' + json.loads(login_response.data.decode())['auth_token']))

                data = json.loads(response.data.decode())

                self.assertEqual(data['status'], 'success')
                self.assertEqual(response.status_code,200)
                self.assertTrue(isinstance(Profile.query.filter_by(profileName = 'SE_Lead',companyName = 'Doodle',deadline = datetime(2021,4,10).timestamp()).first(),Profile))
                
                #logout the user
                result = logout_user(self, login_response)
                res = json.loads(result.data.decode())
                self.assertTrue(res['status'] == 'success')
                self.assertTrue(result.status_code == 200)

        def test_release_profile(self):
            with self.client:
                #register a student
                user_response2 = add_student(self, "bharath", "hello@abc", "testpass")
                response_data = json.loads(user_response2.data.decode())
                self.assertTrue(response_data['status'] == 'success')
                self.assertEqual(user_response2.status_code, 200)

                # register a recruiter
                user_response = add_recruiter(self, "Doodle", "hello@123", "testpass", "#DOO@2020")
                response_data = json.loads(user_response.data.decode())
                self.assertTrue(response_data['status'] == 'success')
                self.assertEqual(user_response.status_code, 200)

                # login the insti admin
                login_response = login_user(self, "admin", "adminpassword")
                data = json.loads(login_response.data.decode())
                self.assertTrue(data['username'] == "admin")
                self.assertEqual(login_response.status_code, 200)

                #create a profile
                profile = Profile(profileName = 'profile5',companyName = 'Doodle',ctc = '1500000',createDate = time.time(),deadline = datetime(2021,4,13).timestamp(),description = 'description',degree = 'B.Tech,M.Tech',dept = 'CS,EC',recruiter_id = Recruiter.query.filter_by(username = "Doodle").first().id)
                db.session.add(profile)
                db.session.commit()

                response = self.client.post('/releaseposition',data = json.dumps({'position_id': profile.id}),content_type = 'application/json',headers = dict(Authorization='Bearer' + ' ' +json.loads(login_response.data.decode())['auth_token']))

                data = json.loads(response.data.decode())

                self.assertEqual(data['status'], 'success')
                self.assertEqual(response.status_code,200)
                self.assertTrue(isinstance(ToBeRead.query.filter_by(user_id = Student.query.filter_by(username = 'bharath').first().id,entity_id = profile.id).first(),ToBeRead))

                #logout the user
                result = logout_user(self, login_response)
                res = json.loads(result.data.decode())
                self.assertTrue(res['status'] == 'success')
                self.assertTrue(result.status_code == 200)
        
        #get applications for a given position
        def test_get_applications(self):
            with self.client:
                user_response = add_recruiter(self, "Doodle", "hello@123", "testpass", "#DOO@2020")
                user_response2 = add_student(self, "bharath", "hello@abc", "testpass")
                login_response = login_user(self, "bharath", "testpass")

                #create a profile
                prof = Profile(profileName = 'profile6',companyName = 'Doodle',ctc = '1400000',createDate = time.time(),deadline = datetime(2021,4,16).timestamp(),description = 'description',degree = 'B.Tech,M.Tech',dept = 'CS,EC',recruiter_id = Recruiter.query.filter_by(username = 'Doodle').first().id)
                db.session.add(prof)

                db.session.commit()

                response = self.client.post('/positiondetails',data = json.dumps({'positionId': prof.id}),content_type = 'application/json',headers = dict(Authorization='Bearer' + ' ' +json.loads(login_response.data.decode())['auth_token']))
                response1 = self.client.post('/positiondetails',data = json.dumps({'positionId': -1}),content_type = 'application/json',headers = dict(Authorization='Bearer' + ' ' +json.loads(login_response.data.decode())['auth_token']))

                data = json.loads(response.data.decode())
                data1 = json.loads(response1.data.decode())

                self.assertTrue(data['status'] == 'success')
                self.assertEqual(response.status_code,200)

                self.assertTrue(data1['status'] == 'Fail')
                self.assertEqual(response1.status_code,404)

                # logout the user
                result = logout_user(self, login_response)
                res = json.loads(result.data.decode())
                self.assertTrue(res['status'] == 'success')
                self.assertTrue(result.status_code == 200)
                

# Main function
if __name__ == '__main__':
    unittest.main()
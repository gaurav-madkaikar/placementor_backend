
import unittest

from app import db
from app.models import InstiAdmin, Recruiter, Student, Alumni
from app.test.base import BaseTestCase


class TestUserModel(BaseTestCase):
    def test_user_models(self):
        # Check if the objects created are pushed appropriately into the database

        # Correct Credentials
        # ---- Student ----
        stud = Student(
            username='stud123',
            email='stud@mail.com',
        )
        stud.set_password('stud_abc')
        db.session.add(stud)
        db.session.commit()

        studRes = Student.query.filter_by(username="stud123").first()
        self.assertTrue(isinstance(studRes, Student))

        db.session.delete(stud)
        db.session.commit()

        # ---- InstiAdmin ----
        # Only one Institute Admin will exist
        adminRes = InstiAdmin.query.filter_by(username="admin").all()
        self.assertTrue(adminRes is not None)
        self.assertTrue(len(adminRes) == 1)

        # ---- Recruiter ----
        rec = Recruiter(
            username='rec123',
            email='rec@mail.com',
            gen_id='#ABC@2020'
        )
        rec.set_password('#ABC@2020')
        db.session.add(rec)
        db.session.commit()

        recRes = Recruiter.query.filter_by(username="rec123").first()
        self.assertTrue(recRes.type == 'recruiter')

        db.session.delete(rec)
        db.session.commit()

        # ---- Alumni ----
        alum = Alumni(
            username='alum123',
            email='alum@mail.com',
        )
        alum.set_password("alum_abc")
        db.session.add(alum)
        db.session.commit()

        alumRes = Alumni.query.filter_by(username="alum123").first()
        self.assertTrue(isinstance(alumRes, Alumni))

        db.session.delete(alum)
        db.session.commit()


if __name__ == '__main__':
    unittest.main()
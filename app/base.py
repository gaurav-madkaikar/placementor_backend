from app.models import InstiAdmin
from flask_testing import TestCase

from app import db
from manage import app


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app.config.from_object('app.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        u = InstiAdmin(username="admin", email="admi@admin.com")
        u.set_password("adminpassword")
        db.session.add(u)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

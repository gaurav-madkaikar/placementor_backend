from flask_testing import TestCase

from app.models import InstiAdmin
from app import db
from manage import app


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app.config.from_object('app.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        admin = InstiAdmin(username="admin", email="admin@admin.com")
        admin.set_password("adminpassword")
        db.session.add(admin)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()



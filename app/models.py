from werkzeug.security import check_password_hash, generate_password_hash
from app import db, login, app
from flask_login import UserMixin
import jwt
import datetime


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(128), unique=True)
    hash_password = db.Column(db.String(128))
    description = db.Column(db.Text)

    type = db.Column(db.String(64))

    __mapper_args__ = {'polymorphic_identity': 'users', 'polymorphic_on': type}

    sent_msgs = db.relationship('Message',
                                backref='author',
                                foreign_keys='Message.author_id',
                                lazy='dynamic')
    recieve_msgs = db.relationship('Message',
                                   backref='recipient',
                                   foreign_keys='Message.recipient_id',
                                   lazy='dynamic')

    toberead = db.relationship('ToBeRead',
                               backref='user',
                               foreign_keys='ToBeRead.user_id',
                               lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.hash_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hash_password, password)

    # """
    # Generates the Auth Token
    # :return: string
    # """
    def encode_auth_token(self, user_id):
        try:
            payload = {
                'exp':
                datetime.datetime.utcnow() +
                datetime.timedelta(hours=2, seconds=0),
                'iat':
                datetime.datetime.utcnow(),
                'sub':
                user_id
            }
            return jwt.encode(payload,
                              app.config.get('SECRET_KEY'),
                              algorithm='HS256')
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class Student(User):
    __tablename__ = "student"
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    roll_num = db.Column(db.String(64), unique=True)
    cgpa = db.Column(db.Float)
    degree = db.Column(db.String(64))
    dept = db.Column(db.String(64))
    resume_link = db.Column(db.String(256))

    applications = db.relationship('Application',
                                   backref='student',
                                   foreign_keys='Application.student_id',
                                   lazy='dynamic')

    __mapper_args__ = {'polymorphic_identity': 'student'}

    def __repr__(self):
        return f'<Student {self.username}>'


class Recruiter(User):
    __tablename__ = "recruiter"
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    gen_id = db.Column(db.String(64), unique=True)

    profiles = db.relationship('Profile',
                               backref='company',
                               foreign_keys='Profile.recruiter_id',
                               lazy='dynamic')
    __mapper_args__ = {'polymorphic_identity': 'recruiter'}

    def __repr__(self):
        return f'<Recruiter {self.username}>'


class Alumni(User):
    __tablename__ = "alumni"
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    degree = db.Column(db.String(64))
    dept = db.Column(db.String(64))
    year = db.Column(db.Integer)

    feedback = db.relationship('Feedback',
                               backref='author',
                               foreign_keys='Feedback.author_id',
                               lazy='dynamic')

    __mapper_args__ = {'polymorphic_identity': 'alumni'}

    def __repr__(self):
        return f'<Alumni {self.username}>'


class InstiAdmin(User):
    __tablename__ = "instiadmin"
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    notices = db.relationship('Notice',
                              backref='author',
                              foreign_keys='Notice.author_id',
                              lazy='dynamic')

    __mapper_args__ = {'polymorphic_identity': 'instiadmin'}

    def __repr__(self):
        return f'<InstiAdmin {self.username}>'


class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    date_time = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<Message {self.content} from {self.author_id} to {self.recipient_id}>'


class Notice(db.Model):
    __tablename__ = 'notice'
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.Integer)
    subject = db.Column(db.String(64))
    content = db.Column(db.Text)

    author_id = db.Column(db.Integer, db.ForeignKey('instiadmin.id'))


class ToBeRead(db.Model):
    __tablename__ = 'toberead'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    type = db.Column(db.String(64))
    entity_id = db.Column(db.Integer)
    timestamp = db.Column(db.Integer)


class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    profileName = db.Column(db.String(64))
    companyName = db.Column(db.String(64))
    ctc = db.Column(db.Float)
    createDate = db.Column(db.Integer)
    releaseDate = db.Column(db.Integer)
    deadline = db.Column(db.Integer)
    description = db.Column(db.String(128))
    degree = db.Column(db.String(128))
    dept = db.Column(db.String(128))

    recruiter_id = db.Column(db.Integer, db.ForeignKey('recruiter.id'))
    feedback = db.relationship('Feedback',
                               backref='profile',
                               foreign_keys='Feedback.profile_id',
                               lazy='dynamic')
    applications = db.relationship('Application',
                                   backref='profile',
                                   foreign_keys='Application.profile_id',
                                   lazy='dynamic')


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.Integer)
    subject = db.Column(db.String(64))
    content = db.Column(db.String(128))

    author_id = db.Column(db.Integer, db.ForeignKey('alumni.id'))
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))


class Application(db.Model):
    __tablename__ = 'application'
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.Integer)
    status = db.Column(db.Integer)
    content = db.Column(db.String(128))

    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))


@login.user_loader
def load_user(id):
    try:
        return User.query.get(int(id))
    except:
        return None

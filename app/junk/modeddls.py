from werkzeug.security import check_password_hash, generate_password_hash
from app import db, login
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    written_posts = db.relationship('Post', backref='author', lazy='dynamic')
    recieved_posts = db.relationship('Post', backref='reicipient', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(64))
    content = db.Column(db.String(128))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id')) # author
    to_id = db.Column(db.Integer, db.ForeignKey('users.id')) #to

    author_user = User/object

    post =Post()
    post.author = author_user
    post.recipient = 

    def __repr__(self):
        return f'<Post {self.subject} : {self.content} written by {self.user_id}>'


class Account(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    hash_password = db.Column(db.String(128))
    type = db.Column(db.String(64))

    messages = db.relationship('Message', backref='author', lazy='dynamic')

    __mapper_args__ = {
        'polymorphic_identity': 'account',
        'polymorphic_on': type
    }


class Student(Account):
    __tablename__ = "student"
    id = db.Column(db.Integer, db.ForeignKey('account.id'), primary_key=True)
    roll_num = db.Column(db.String(64), index=True, unique=True)
    __mapper_args__ = {'polymorphic_identity': 'student'}


class Recruiter(Account):
    __tablename__ = "recruiter"
    id = db.Column(db.Integer, db.ForeignKey('account.id'), primary_key=True)
    gen_id = db.Column(db.String(64), index=True, unique=True)
    __mapper_args__ = {'polymorphic_identity': 'recruiter'}


class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(64))
    content = db.Column(db.String(128))

    author_id = db.Column(db.Integer, db.ForeignKey('account.id'))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    # id is passed as a string


# User
class tableA(db.Model):
    __tablename__ = 'table_a'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    hash_password = db.Column(db.String(128))

    posts = db.relationship('tableB', backref='author', lazy='dynamic')


# Post
class tableB(db.Model):
    __tablename__ = "table_b"
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(64))
    content = db.Column(db.String(128))

    author_id = db.Column(db.Integer, db.ForeignKey('table_a.id'))


# Inheritance of tables in databases


class BaseClass(db.Model):
    __tablename__ = 'base_classes'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    hash_password = db.Column(db.String(128))

    __mapper_args__ = {'polymorphic_identity': 'base_classes'}


class DerivedClass(BaseClass):
    __tablename__ = "derived_classes"
    id = db.Column(db.Integer,
                   db.ForeignKey('base_classes.id'),
                   primary_key=True)
    email = db.Column(db.String(128), index=True, unique=True)

    __mapper_args__ = {'polymorphic_identity': 'derived_classes'}

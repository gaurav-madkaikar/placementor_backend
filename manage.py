from app import app, db
from app.models import Student, InstiAdmin, Recruiter, Alumni
import unittest
from flask_script import Manager

manager = Manager(app) 

@app.shell_context_processor
def make_shell_context():
    return {'db' : db, 'stud' : Student, 'admin': InstiAdmin, 'rec': Recruiter, 'alum': Alumni}

@manager.command
def test():
    """Run the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        # Return error code
        return 0
    return 1

@manager.command
def run():
    app.run(debug=True)

if __name__ == "__main__":
    manager.run()
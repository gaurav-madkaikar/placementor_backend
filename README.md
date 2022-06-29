
## Flask Unit Testing

This folder contains unit tests for the backend of Placementor: a software application for managing online placements, written using python unittest and Flask-Testing

### Folder Structure:
<pre>
.
├── app
│   └── test
│       ├── __init__.py
│       ├── base.py
│       ├── test_auth.py
│       ├── test_config.py
│       ├── test_model.py
│       └── test_usecases.py
</pre>

**test_config:** Tests for the configurations required in different environments- 'Production', 'Development' and 'Testing'
**test_auth:** Tests for user authentication
**test_model:** Tests for pushing and retrieving user data from the database
**test_usecases:** Tests for Usecases and routes as specified in **routes.py**

### To run the tests, run the following command on your system terminal:
```
$ python manage.py test
```

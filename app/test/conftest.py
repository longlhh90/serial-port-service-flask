import pytest
from app.main import create_app, db
from app.main.model.user import User
import json


@pytest.fixture(scope='module')
def new_user():
    user = User('lukas@123.com', 'thisispassword')
    return user


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('test')

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!


@pytest.fixture(scope='module')
def init_database(test_client):
    # Create the database and the database table
    db.create_all()

    # Insert user data
    user1 = User(email='lukas@123.com', password='PaSsW0rD')
    user1.save_to_db()

    yield

    db.drop_all()


@pytest.fixture(scope='function')
def login_default_user(test_client):
    payload = json.dumps({
        'email': 'lukas@123.com',
        'password': 'PaSsW0rD'
    })
    response = test_client.post(
        '/auth',
        data=payload,
        content_type='application/json',
    )
    return response.json['access_token']

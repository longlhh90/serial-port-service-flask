def test_new_user(new_user):
    assert new_user.email == 'lukas@123.com'
    assert new_user.hashed_password != 'thisispassword'


def test_check_password(new_user):
    assert new_user.email == 'lukas@123.com'
    assert new_user.check_password('thisispassword')


def test_get_password__fail(new_user):
    assert new_user.email == 'lukas@123.com'
    try:
        new_user.password
    except AttributeError as e:
        assert e.args[0] == "password: write-only field"

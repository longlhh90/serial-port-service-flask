from werkzeug.datastructures import Headers
from unittest import mock
import json
from app.serialcore import _serial


class MockPort:
    def __init__(self, device, name, description, hwid=None, vid=None, pid=None, serial_number=None, location=None, manufacturer=None, product=None, interface=None):
        self.device = device
        self.name = name
        self.description = description
        self.hwid = hwid
        self.vid = vid
        self.pid = pid
        self.serial_number = serial_number
        self.location = location
        self.manufacturer = manufacturer
        self.product = product
        self.interface = interface


mock_ports = [
    MockPort('device fake1', 'fake1', 'this is fake 1'),
    MockPort('device fake2', 'fake2', 'this is fake 2')
]


class MockSerial:
    def __init__(self, port, is_open):
        self.is_open = is_open
        self.port = port

    def write(self, mes):
        pass


def test_list_ports__without_login__fail(test_client):
    response = test_client.get('/ports/')
    assert response.status_code == 401
    assert response.json == {
        'description': 'Request does not contain an access token',
        'error': 'Authorization Required',
        'status_code': 401
    }


@mock.patch("serial.tools.list_ports.comports", return_value=mock_ports)
def test_list_ports__with_login__success(mocked_port, test_client, init_database, login_default_user):
    # REMOVE: Only when need to keep default headers
    # test_client.environ_base['HTTP_AUTHORIZATION'] = 'JWT {0}'.format(
    #     login_default_user)

    headers = [('Authorization', 'JWT {0}'.format(login_default_user))]
    response = test_client.get('/ports/', headers=headers)
    assert response.status_code == 200
    assert response.json["ports"] == [
        {
            'device': 'device fake1',
            'name': 'fake1',
            'description': 'this is fake 1',
            'hwid': None,
            'vid': None,
            'pid': None,
            'serial_number': None,
            'location': None,
            'manufacturer': None,
            'product': None,
            'interface': None
        },
        {
            'device': 'device fake2',
            'name': 'fake2',
            'description': 'this is fake 2',
            'hwid': None,
            'vid': None,
            'pid': None,
            'serial_number': None,
            'location': None,
            'manufacturer': None,
            'product': None,
            'interface': None
        }
    ]


def test_init_serial_port__without_login__fail(test_client):
    response = test_client.post('/init-port/')
    assert response.status_code == 401
    assert response.json == {
        'description': 'Request does not contain an access token',
        'error': 'Authorization Required',
        'status_code': 401
    }


@mock.patch("serial.Serial.open", return_value=True)
@mock.patch("serial.Serial.close", return_value=True)
def test_init_serial_port__with_login__success(mocked_serial_open, mocked_serial_close, test_client, init_database, login_default_user):
    headers = [('Authorization', 'JWT {0}'.format(login_default_user))]
    payload = json.dumps({
        'port': 'COM8'
    })
    response = test_client.post(
        '/init-port/',
        data=payload,
        headers=headers,
        content_type='application/json',)

    assert response.status_code == 200
    assert response.json["message"] == "Port COM8 has opened!"


def test_write_to_serial_port__without_login__fail(test_client):
    response = test_client.post('/send-msg/')
    assert response.status_code == 401
    assert response.json == {
        'description': 'Request does not contain an access token',
        'error': 'Authorization Required',
        'status_code': 401
    }


@mock.patch("serial.Serial.write", return_value=0)
def test_write_to_serial_port__with_login__success(mocked_serial, test_client, init_database, login_default_user):
    _serial.is_open = True
    headers = [('Authorization', 'JWT {0}'.format(login_default_user))]
    payload = json.dumps({
        'message': 'Hello World!'
    })
    response = test_client.post(
        '/send-msg/',
        data=payload,
        headers=headers,
        content_type='application/json')

    assert response.status_code == 200
    assert response.json["message"] == "Write to COM8 successfully"


def test_write_to_serial_port__with_login_and_port_not_open__fail(test_client, init_database, login_default_user):
    _serial.is_open = False
    headers = [('Authorization', 'JWT {0}'.format(login_default_user))]
    payload = json.dumps({
        'message': 'Hello World!'
    })
    response = test_client.post(
        '/send-msg/',
        data=payload,
        headers=headers,
        content_type='application/json',)

    # assert response.status_code == 400
    assert response.json["message"] == "Port COM8 is not open. Please open the port first"

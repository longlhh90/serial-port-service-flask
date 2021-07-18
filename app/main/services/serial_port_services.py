from app.serialcore import get_list_ports, init_serial_port, write_to_serial_port
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from app.init.api import api
from app.utils import Collections
import serial


# HELPERS
def positive_integer(value):
    if value <= 0:
        raise ValueError("Value is not positive")

    return value


def message_validator(value):
    if not isinstance(value, str):
        raise ValueError("Message should be string")
    if len(value) > 500:
        raise ValueError("Maximum length of message is 500")

    return value


@api.resource('/ports/')
class PortListInfo(Resource):

    @jwt_required()
    def get(self):
        data = get_list_ports()
        return data, 200


@api.resource('/send-msg/')
class SerialPortMessage(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'message',
        type=message_validator,
        required=True,
        help="{error_msg}"
    )

    @jwt_required()
    def post(self):
        args = SerialPortMessage.parser.parse_args()
        message = bytes(args["message"], 'ascii')
        response_msg, status_code = write_to_serial_port(message)

        return {"message": response_msg}, status_code


@api.resource('/init-port/')
class InitSerialPort(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument(
        'port',
        type=str,
        location='json',
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument(
        'baudrate',
        choices=serial.Serial.BAUDRATES,
        type=int,
        required=False,
        help="Bad choice: {error_msg}." +
        "The choices are: {}".format(serial.Serial.BAUDRATES)
    )
    parser.add_argument(
        'bytesize',
        choices=serial.Serial.BYTESIZES,
        type=int,
        required=False,
        help="Bad choice: {error_msg}." +
        "The choices are: {}".format(serial.Serial.BYTESIZES)
    )
    parser.add_argument(
        'stopbits',
        choices=serial.Serial.STOPBITS,
        type=int,
        required=False,
        help="Bad choice: {error_msg}." +
        "The choices are: {}".format(serial.Serial.STOPBITS)
    )
    parser.add_argument(
        'parity',
        choices=serial.Serial.PARITIES,
        type=int,
        required=False,
        help="Bad choice: {error_msg}." +
        "The choices are: {}".format(serial.Serial.PARITIES)
    )
    parser.add_argument(
        'flow_control',
        choices=('xonxoff', 'rtscts', 'dsrdtr'),
        type=str,
        required=False,
        help="Bad choice: {error_msg}. The choices are: ('xonxoff', 'rtscts', 'dsrdtr')"
    )
    parser.add_argument(
        'write_timeout',
        type=positive_integer,
        required=False,
        help="Error: {error_msg}"
    )
    parser.add_argument(
        'timeout',
        type=positive_integer,
        required=False,
        help="Error: {error_msg}"
    )

    @jwt_required()
    def post(self):
        args = Collections.drop_none(InitSerialPort.parser.parse_args())
        response_msg, status_code = init_serial_port(**args)
        return {"message": response_msg}, status_code

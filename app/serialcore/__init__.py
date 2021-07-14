import serial
from serial.serialutil import PARITY_NONE
import serial.tools.list_ports as port_list

_serial = serial.Serial()


def get_list_ports():
    ports = list(port_list.comports())
    return {
        "ports": [
            {
                "device": i.device,
                "name": i.name,
                "description": i.description,
                "hwid": i.hwid,
                "vid": i.vid,
                "pid": i.pid,
                "serial_number": i.serial_number,
                "location": i.location,
                "manufacturer": i.manufacturer,
                "product": i.product,
                "interface": i.interface,
            } for i in ports
        ]
    }


def init_serial_port(port, baudrate=9600, bytesize=8, stopbits=1, parity=PARITY_NONE, flow_control=None, write_timeout=None, timeout=None):
    global _serial
    if _serial.is_open:
        _serial.close()
    _serial.port = port
    _serial.baudrate = baudrate
    _serial.bytesize = bytesize
    _serial.stopbits = stopbits
    _serial.parity = parity
    _serial.write_timeout = write_timeout
    _serial.timeout = timeout

    if flow_control == "xonxoff":
        _serial.xonxoff = True
        _serial.rtscts = False
        _serial.dsrdtr = False
    elif flow_control == "rtscts":
        _serial.xonxoff = False
        _serial.rtscts = True
        _serial.dsrdtr = False
    elif flow_control == "dsrdtr":
        _serial.xonxoff = False
        _serial.rtscts = False
        _serial.dsrdtr = True
    else:
        _serial.xonxoff = False
        _serial.rtscts = False
        _serial.dsrdtr = False

    _serial.open()

    return "Port {0} has opened!".format(_serial.port)


def write_to_serial_port(message):
    global _serial
    if _serial.is_open:
        _serial.write(message)
        return "Write to {} successfully".format(_serial.port)

    return "Port {0} is not open. Please open the port first".format(_serial.port)

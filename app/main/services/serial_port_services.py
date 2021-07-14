import serial
import serial.tools.list_ports as port_list


def get_list_ports():
    ports = list(port_list.comports())
    for p in ports:
        print(p)
    return ports


def woww():
    ser = serial.Serial('/pyprj/abc/COM8', write_timeout=10)
    ser.write(b"hello")
    msg = ser.read(5)
    print(ser.name, ser.port, ser.baudrate, ser.bytesize, ser.is_open, msg)
    ser.close()

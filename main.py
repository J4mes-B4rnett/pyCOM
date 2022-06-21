from asyncio.windows_events import NULL
import configparser
from inspect import formatargvalues
import serial, argparse, sys, atexit, time, os
from serial.tools import list_ports

sys.tracebacklimit = 0

def listPorts(config):
    ports = serial.tools.list_ports.comports()
    print("\nPorts in use:")
    for port, desc, hwid in sorted(ports):
        print("   {0}: {1}".format(port, desc))

def openPort(config):
    port = config.__dict__['COM Port']
    baud = config.__dict__['Baud Rate']

    print("Set Port: COM{0}".format(port))
    print("Set Baud Rate: {0}".format(baud))

    time.sleep(1)

    try:
        console = serial.Serial()
        console.port = "COM{0}".format(port)
        console.baudrate = int(baud)
        console.timeout = 0
        console.parity = serial.PARITY_EVEN

        console.open()
    except:
        raise Exception("Failed to open serial terminal. \nThis can be due to: \n  -Incorrect port \n  -Port already open in another program")

    while True:
        recieved_val = console.readline().decode('utf-8').rstrip('\r\n')
        if len(recieved_val) > 0:
            print("{0}".format(recieved_val))

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
subparsers = parser.add_subparsers(title="actions")

parser_list = subparsers.add_parser('list')
parser_list.set_defaults(func=listPorts)

parser_open = subparsers.add_parser('open')
parser_open.add_argument("COM Port", help="port to open serial terminal")
parser_open.add_argument("Baud Rate", help="frequency of serial communication")
parser_open.set_defaults(func=openPort)

config=parser.parse_args()
config.func(config)

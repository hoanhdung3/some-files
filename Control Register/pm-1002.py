#! /usr/bin/python3
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
import time
import argparse
import sys
import paho.mqtt.client as paho
import json
from paho import mqtt

regs = {
   3926 : {'name' : 'V1', 'state' : False, 'reg' : 3926},
   3912 : {'name' : 'A', 'state' : False, 'reg' : 3912},
   3906 : {'name' : 'PF', 'state' : False, 'reg' : 3906},
   3940 : {'name' : 'V2', 'state' : False, 'reg' : 3940},
   3954 : {'name' : 'V3', 'state' : False, 'reg' : 3954},
   3902 : {'name' : 'W', 'state' : False, 'reg' : 3902},
   3918 : {'name' : 'W1', 'state' : False, 'reg' : 3918},
   3932 : {'name' : 'W2', 'state' : False, 'reg' : 3932},
   3946 : {'name' : 'W3', 'state' : False, 'reg' : 3946},
   3928 : {'name' : 'A1', 'state' : False, 'reg' : 3928},
   3942 : {'name' : 'A2', 'state' : False, 'reg' : 3942},
   3956 : {'name' : 'A3', 'state' : False, 'reg' : 3956},
   3914 : {'name' : 'F', 'state' : False, 'reg' : 3914}
   }


def validator(instance):
        if not instance.isError():
                decoder = BinaryPayloadDecoder.fromRegisters(
                        instance.registers,
                        byteorder = Endian.Big, wordorder = Endian.Little
                )
                return float(decoder.decode_32bit_float())
        else:
                print("There aren't the register. Try again")
                return None

def set_reg_status(reg,state):
   regs[reg]['state'] = state

def on_message(client,userdata, msg):
   data = json.loads(msg.payload)
   set_reg_status(data['reg'], data['state'])

client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set('hoanhdung3','Hoanhdung3')
client.connect("b976624c2da24f02b01e2c920ee699bc.s2.eu.hivemq.cloud", 8883)
client.subscribe('test/dung')
# client.on_message = on_message
client.loop_start()

try:
        while True:
                try:
                        client.on_message = on_message
                        for i in regs:
                                if regs[i]['state'] == True:
                                        modbus = ModbusClient(method = 'rtu', port = '/dev/ttyUSB0', baudrate = 9600, timeout = 1, parity = 'E', bytesize = 8)
                                        modbus.connect()
                                        reg_value = validator(modbus.read_holding_registers(i, 2, unit=1))
                                        print(regs[i]['name'] + ": {}".format(reg_value)+"\n")
                                        modbus.close()
                        # voltage_data['voltage'] = voltage_value
                        # client.publish('v1/devices/me/telemetry',json.dumps(voltage_data))
                        print("\n")
                        time.sleep(5)
                except AttributeError as e:
                        print(e)
except KeyboardInterrupt:
    pass
client.loop_stop()
client.disconnect()

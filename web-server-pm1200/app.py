from flask import Flask, render_template, request
import paho.mqtt.client as paho
from paho import mqtt
import json

client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set('hoanhdung3','Hoanhdung3')
client.connect("b976624c2da24f02b01e2c920ee699bc.s2.eu.hivemq.cloud", 8883)
client.loop_start()
app = Flask(__name__)


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

@app.route("/")
def main():
   templateData = {
      'regs' : regs
      }
   return render_template('main.html', **templateData)

@app.route("/", methods=["POST"])
def query():
	delay = request.form.get('delay')
	client.publish('test/delay',delay)
	templateData = {
      		'regs' : regs
      	}
	return render_template('main.html', delay=delay, **templateData)

@app.route("/<changePin>/<action>")
def action(changePin, action):
   changePin = int(changePin)
   deviceName = regs[changePin]['name']
   if action == "on":
      regs[changePin]['state'] = True
      data = {'reg' : regs[changePin]['reg'], 'state' : regs[changePin]['state']}
      client.publish('test/dung',json.dumps(data))
      message = "Reading " + deviceName
   if action == "off":
      regs[changePin]['state'] = False
      data = {'reg' : regs[changePin]['reg'], 'state' : regs[changePin]['state']}
      client.publish('test/dung',json.dumps(data))
      message = "Unread " + deviceName

   templateData = {
      'regs' : regs
   }

   return render_template('main.html', **templateData)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)


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


regs = {}

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

@app.route("/create/", methods=["POST"])
def create():
   abb = request.form['abb']
   regis = int(request.form['regis'])
   stt = request.form['stt']

   if stt == '1':
      stt = True
   else:
      stt = False

   regs[regis] = {'name' : abb, 'state': bool(stt), 'reg' : regis }

   templateData = {
      		'regs' : regs
      	}
   return render_template('main.html', **templateData, abb=abb, regis=regis, stt=stt)

@app.route("/<changePin>/<action>")
def action(changePin, action):
   changePin = int(changePin)
   if action == "on":
      regs[changePin]['state'] = True
      data = {'reg' : regs[changePin]['reg'], 'state' : regs[changePin]['state']}
      client.publish('test/dung',json.dumps(data))

   if action == "off":
      regs[changePin]['state'] = False
      data = {'reg' : regs[changePin]['reg'], 'state' : regs[changePin]['state']}
      client.publish('test/dung',json.dumps(data))

   templateData = {
      'regs' : regs
   }

   return render_template('main.html', **templateData)

if __name__ == "__main__":
   #app.run(host='0.0.0.0', port=80, debug=True)
   app.run(debug=True)


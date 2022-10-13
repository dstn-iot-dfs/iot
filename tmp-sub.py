import paho.mqtt.subscribe as subscribe
import json 

while 1:
	msg = subscribe.simple("img", hostname="localhost")
	obj = json.loads(msg.payload)
	print(msg.payload[:100])
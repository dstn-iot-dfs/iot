import paho.mqtt.subscribe as subscribe

while 1:
	msg = subscribe.simple("img", hostname="localhost")
	print(msg.payload, type(msg.payload))
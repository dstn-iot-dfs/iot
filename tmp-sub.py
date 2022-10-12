import paho.mqtt.subscribe as subscribe

msg = subscribe.simple("img", hostname="localhost")
print(msg.payload, type(msg.payload))
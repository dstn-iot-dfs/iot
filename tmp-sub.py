import paho.mqtt.subscribe as subscribe
import json 
from config import config
while 1:
	msg = subscribe.simple("img", hostname=config.mqtt_borker_ip)
	obj = json.loads(msg.payload)
	print(msg.payload[:100], len(msg.payload))
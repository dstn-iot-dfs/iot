from config import config
import paho.mqtt.client	#import client library
import time, os
from img_proc import img_pre_proc

connected = False

def on_connect(client, userdata, flags, rc):
	if rc == 0:
		connected = True
		print("connected ok")
	else:
		print("connnection failed with code: ", rc)

def on_publish(client, userdata, result):
	# print(result)
	print("published")

def on_disconnect(client, userdata, rc):
	connected = False
	print("disconn")

img_proc = img_pre_proc(encoding='b64', compression='')
# setup
client = paho.mqtt.client.Client("cam1")			 #create new instance 
client.on_connect = on_connect  #bind call back function
client.on_publish = on_publish
client.on_disconnect = on_disconnect


client.connect(config.mqtt_borker_ip, port=1883)			   #connect to broker
# while not connected:
time.sleep(1)
print('attempting to connect')

base_path = './sample-data/raw/'
for img in os.listdir(base_path):
	payload = img_proc.json_for_img(base_path+img)
	client.publish(topic="img",payload=payload,qos=0)
	time.sleep(config.img_xmit_time )
	print('waiting for next img')

ret_val = client.publish(topic="img",payload=payload,qos=2)

client.disconnect()
# import paho.mqtt.subscribe as subscribe

# msg = subscribe.simple("debug", hostname="tanmay-g3")
# print("%s %s" % (msg.topic, msg.payload))

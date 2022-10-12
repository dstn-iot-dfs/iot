import paho.mqtt.client	#import client library
import time
from img_proc import get_json_for_img

connected = False

def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print("connected ok")
	else:
		print("connnection failed with code: ", rc)

def on_publish(client, userdata, result):
	print(result)
	print("published")

def on_disconnect(client, userdata, rc):
   print("client disconnected ok")

# setup
client = paho.mqtt.client.Client("python1")			 #create new instance 
client.on_connect=on_connect  #bind call back function
client.on_publish = on_publish
client.on_disconnect = on_disconnect


client.connect("localhost", port=1883)			   #connect to broker
time.sleep(3)

payload = get_json_for_img('./test-img.raw')
ret_val = client.publish(topic="img",payload=payload,qos=2)

client.disconnect()
# import paho.mqtt.subscribe as subscribe

# msg = subscribe.simple("debug", hostname="tanmay-g3")
# print("%s %s" % (msg.topic, msg.payload))
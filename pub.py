import threading
from config import config
import paho.mqtt.client	#import client library
import time
from helper import *
from queue import Queue

# Global vars
q = Queue(maxsize=config.queue_size_limit)
img_proc = img_pre_proc(encoding='b64', compression='',device_id=config.mqtt_client_name)

# MQTT setup
client = paho.mqtt.client.Client(config.mqtt_client_name)
client.on_connect = on_connect
client.on_publish = on_publish
client.on_disconnect = on_disconnect
print('attempting to connect with id: ', config.mqtt_client_name)
client.connect(config.mqtt_borker_ip, port=1883)
time.sleep(0.5)
client.loop_start()

lock = threading.Lock()

# Start data loading
load_data_thr = threading.Thread(target=load_data, args=(lock,q,img_proc))
load_data_thr.start()

while True:
	# check network and broker connection
	weak, quality = is_network_weak()
	timeout_cnt = 0
	while (weak):
		time.sleep(1)
		timeout_cnt += 1
		print("wating for better signal, current strength = ",quality,"%")
		if timeout_cnt == config.max_timeouts: 
			break
		weak, quality = is_network_weak()
	
	if timeout_cnt == config.max_timeouts:
		break

	lock.acquire()
	if not q.empty():
		payload = q.get()
	else: # nothing to publish
		lock.release()
		continue
	lock.release()

	print("attempting publish")
	client.publish(topic="img",payload=payload,qos=0)
	time.sleep(config.img_xmit_time )

load_data_thr.join()
client.loop_stop()
import paho.mqtt.client	#import client library
import time,os
from config import config
from img_proc import img_pre_proc


class mqtt_publisher():
	mqtt_port = config.mqtt_port
	#fns for client
	def on_connect(client, userdata, flags, rc):
		if rc == 0:
			# publisher.connected = True
			print("connected ok")
		else:
			# publisher.connected = False
			print("connnection failed with code: ", rc)
	def on_publish(client, userdata, result):
		print(result)
		print("published")
	def on_disconnect(client, userdata, rc):
		# publisher.connected = False
		print("client disconnected")
	
	def __init__(self, broker_ip, topic, client_name, delay):
		self.broker_ip = broker_ip
		self.topic = topic
		self.client_name = client_name
		self.delay = delay
		self.connected = False
		self.img_processor = img_pre_proc('b64','')
		#client setup
		self.setup()

	def setup(self):
		self.client = paho.mqtt.client.Client(self.client_name)
		self.client.on_connect = mqtt_publisher.on_connect  #bind call back function
		self.client.on_publish = mqtt_publisher.on_publish
		self.client.on_disconnect = mqtt_publisher.on_disconnect
		self.client.connect(self.broker_ip, port=mqtt_publisher.mqtt_port)

	def conn_active(self):
		# todo
		return True

	def publish_img(self,path):
		payload = self.img_processor.preproc_and_get_json(path=path)
		
		while(not self.conn_active()):
			time.sleep(2)
		
		self.client.publish(topic=self.topic,payload=payload,qos=2)

	def disconnect(self):
		self.client.disconnect()


# import paho.mqtt.subscribe as subscribe
if __name__ == '__main__':
	publisher = mqtt_publisher(config.mqtt_borker_ip,config.mqtt_topic,
							config.mqtt_client_name, config.img_xmit_time)
	
	while( not publisher.conn_active()):
		time.sleep(2)
	base_path = './sample-data/raw/'
	for img in os.listdir(base_path):
		publisher.publish_img(base_path + img)
		time.sleep(config.img_xmit_time )


# msg = subscribe.simple("debug", hostname="tanmay-g3")
# print("%s %s" % (msg.topic, msg.payload))
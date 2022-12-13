# a file with all required config params.

class config():
	
	mqtt_borker_ip = "localhost"
	mqtt_topic = "img"
	mqtt_port = 1883
	mqtt_client_name = "camera_device0"
	queue_size_limit = 5
	cutoff_strength = 60
	max_timeouts = 100
	img_xmit_time = 1 #time after which xmit in s
	img_gen_time = 5


import subprocess, time
import re, os, threading
from config import config
from img_proc import img_pre_proc
from queue import Queue

# Signal check ##############################

def read_data_from_cmd(): # inspired from https://github.com/s7jones/Wifi-Signal-Plotter
	p = subprocess.Popen("iwconfig", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out = p.stdout.read().decode()
	m = re.findall('Signal level=(-[0-9]+) dBm', out, re.DOTALL)
	p.communicate()
	if len(m)==0 :
		return -100
	else:
		return int(m[0])

def dbm_to_quality():
	dBm = read_data_from_cmd()
	if(dBm <= -100):
		quality = 0
	elif(dBm >= -50):
		quality = 100
	else:
		quality = 2 * (dBm + 100)

	return quality

def is_network_weak():
	quality = dbm_to_quality()
	if(quality <= config.cutoff_strength):
		return True, quality
	return False, quality

def debug():
	interfaceDict = dict()
	quality = dbm_to_quality()
	print("Wifi strength: ",quality,"%")
	return

# Callbacks ##############################

def on_connect(client, userdata, flags, rc):
	# global connected
	if rc == 0:
		# connected = True
		print("connected ok")
	else:
		print("connnection failed with code: ", rc)

def on_publish(client, userdata, result):
	# print(result)
	print("published")

def on_disconnect(client, userdata, rc):
	# global connected
	# connected = False
	print("disconn")

# Data Loader ##############################

def load_data(lock, queue:Queue, img_proc:img_pre_proc):
	base_path = './sample-data/raw/'
	imgs = os.listdir(base_path)
	num_imgs = len(imgs)
	count = 0
	while True:
		time.sleep(config.img_gen_time )
		lock.acquire()
		print("generating an image")
		if(queue.full()):
			print("q full, dequeuing one element")
			queue.get()
		payload = img_proc.preproc_and_get_json(base_path+imgs[(count+1)%num_imgs])
		queue.put(payload)
		lock.release()
		count += 1 
		print("waiting for next img, queue size: ", queue.qsize())

if __name__ == '__main__':
	debug()
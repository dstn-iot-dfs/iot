import subprocess
import re
from config import config

def read_data_from_cmd():
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

if __name__ == '__main__':
	debug()
import json
import time, base64


class img_pre_proc():
	def __init__(self, encoding, compression, device_id):
		self.encoding = encoding
		self.compression = compression
		self.device_id = device_id

	def read_raw_img (self,path):
		in_fh = open(path, "rb") #get raw byte data
		raw_bytes = in_fh.read()
		in_fh.close()
		return raw_bytes

	def encode_b64(self, raw_bytes):
		return str( base64.b64encode(raw_bytes) )

	def json_for_img(self, encoded_str):
		data = {}
		data['id'] = self.device_id
		data['ts'] = time.time_ns()
		data['compr'] = self.compression
		data['enc'] = self.encoding
		data['data'] = encoded_str
		return json.dumps(data)
		
	def preproc_and_get_json(self,path):
		raw_bytes = self.read_raw_img(path)
		encoded_str = self.encode_b64(raw_bytes)
		# with open('b64.txt','w') as fh:
		# 	fh.write(encoded_str)
		json_object = self.json_for_img(encoded_str)
		return json_object

# for debug purposes only
def main(): 
	# path = input("Enter absolute file path to read ")
	path = "./sample-data/test-img.raw"
	img_processor =  img_pre_proc(encoding='b64',compression='')
	json_obj = img_processor.preproc_and_get_json(path= path)
	print(json_obj)
	# with open("./ignore/tmp.bin","wb") as out_file:
	# 	out_file.write(raw_bytes)
	# with open("./ignore/b64.txt","w") as out_file:
	# 	out_file.write(encoded_str)

if __name__ == "__main__":
	main()
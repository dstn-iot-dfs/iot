import json
import os, base64

def read_raw_img (path):
	in_fh = open(path, "rb") #get raw byte data
	raw_bytes = in_fh.read()
	in_fh.close()
	return raw_bytes

def encode_b64(raw_bytes):
	encoded_bytes = base64.b64encode(raw_bytes)
	return str(encoded_bytes)

def get_json_for_img(path):
	raw_bytes = read_raw_img(path)
	b64_str = encode_b64(raw_bytes)
	data = {}
	data['data'] = b64_str
	data['compression'] = ''
	data['encoding'] = 'b64'
	json_object = json.dumps(data)
	return json_object

# for debug purposes only
def main(): 
	# path = input("Enter absolute file path to read ")
	path = "./test-img.raw"
	
	raw_bytes = read_raw_img(path)
	encoded_str = encode_b64(raw_bytes)
	print(type(encoded_str))
	
	with open("tmp.bin","wb") as out_file:
		out_file.write(raw_bytes)
	with open("b64.txt","w") as out_file:
		out_file.write(encoded_str)

if __name__ == "__main__":
	main()
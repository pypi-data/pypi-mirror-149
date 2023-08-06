import os, json

def dprint(message, debug, end="\n"):
	if debug:
		print(message)

def get_config_dict():
	file_name = 'config.json'
	if not os.path.exists(file_name):
		#create the file
		config_object = {
			'engine_path': '../../engines/stockfish_20090216_x64_avx2.exe'
		}
		with open(file_name, 'w') as f:
			json.dump(config_object, f, indent="")
		print("Created config file.")

	with open(file_name, 'r') as f:
		return json.load(f)


#Do not use these generically, they are flipped
def index_to_chess_square(index):
	rank = 8 - (index // 8)
	file = chr(7 - (index % 8) + 97)

	return "%s%s" % (file, rank)

def chess_square_to_index(square):
	col = 7- (ord(square[0]) - 97)
	row = 8- (int(square[1]))

	return row*8 + col
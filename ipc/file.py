import json
import numpy as np

class File:
	def __init__(self):
		self.f = open("./buffer.json", "r+")

	def __del__(self):
		self.f.close()	

	def write_data(self, data: list):
		self.f.seek(0)
		try:
			dat = json.load(self.f)
		except json.JSONDecodeError:
			dat = {"data": {}}

		if not len(dat["data"].keys()):
			highest = 0
		else:
			highest = max(map(int, dat.keys()))

		keyval = str(highest+1)
		dat["data"][keyval] = data
		json.dump(dat, self.f)
		self.f.truncate()

		return

	def read_data(self, keynum) -> list:
		dat = json.load(self.f)
		return dat["data"][keynum].reverse()
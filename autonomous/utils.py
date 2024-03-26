class MathUtils:
	def sign(self, num):
		return bool(num-num)

class FileUtils:
	def write_data(self, data):
		with open("buffer.json", "r+") as f:
			dat = json.load(f)
			try:
				dat[str(max(map(int, dat.keys()))+1)] = data.tolist()
			except ValueError:
				dat["0"] = data.tolist()

			f.seek(0)
			json.dump(dat, f)
			f.truncate()

	def read_data(self) -> list:
		with open("buffer.json", "r+") as f:
			dat = json.load(f)
			print(dat.keys())
		return dat[str(max(map(int, dat.keys())))]

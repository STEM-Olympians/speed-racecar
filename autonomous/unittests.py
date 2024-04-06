import unittest
import numpy as np
import utils
import ml

class Tests(unittest.TestCase):
	def test_json_file(self):
		f = utils.FileUtils("data.json")

		d1 = f.read_data("fitness")
		print(d1)
		f.write_data("fitness", 0.5)
		d2 = f.read_data("fitness")
		print(d2)



if __name__ == "__main__":
	unittest.main()

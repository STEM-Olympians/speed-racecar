import unittest
import random
import numpy as np
import utils
import ml

class Tests(unittest.TestCase):
	"""
	def test_json_file(self):
		f = utils.FileUtils("data.json")

		d1 = f.read_data("fitness")
		print(d1)
		f.write_data("fitness", 0.5)
		d2 = f.read_data("fitness")
		print(d2)
	"""

	"""
	def test_gui_utils(self):
		gutils = utils.GUIUtils("RacecarSim")
		while True:
			gutils.start()
			gutils.enter()
			gutils.end()
	"""

	def test_file(self):
		f = utils.FileUtils("test.json")
		while True:
			f.write_data("instruction_set", [random.uniform(-1, 1) for _ in range(random.randint(5, 10))])



if __name__ == "__main__":
	unittest.main()

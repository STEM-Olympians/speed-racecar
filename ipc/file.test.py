import unittest
import file
import random

class FILE_TEST(unittest.TestCase):
	def test_ipc(self):
		for i in range(1_000):
			data = [[0 for _ in range(720)] for _ in range(3)]
			f = file.File()
			f.write_data(data)
			f.read_data()


if __name__ == "__main__":
	unittest.main()

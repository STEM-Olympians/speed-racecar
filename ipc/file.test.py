import unittest
import file
import random

class FILE_TEST(unittest.TestCase):
	def test_ipc(self):
		data = [1, 2, 3, 4, 5]
		f = file.File()
		f.write_data(data)
		print(f.read_data(1))


if __name__ == "__main__":
	unittest.main()

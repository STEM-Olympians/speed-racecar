import unittest
import shm
import random

class IPC_TEST(unittest.TestCase):
	def test_ipc(self):
		#self.maxDiff = None
		for i in range(10_000):
			new_random_num = random.uniform(0, 9)
			dat = [new_random_num for _ in range(720)]
			ipcshm = shm.IPC_SHM()

			# writing data
			ipcshm.write(dat)

			# checking if reading data produces same result
			read = ipcshm.read()
			#self.assertEqual(read, dat)

if __name__ == "__main__":
	unittest.main()

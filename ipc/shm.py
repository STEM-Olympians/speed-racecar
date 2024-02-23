from multiprocessing import shared_memory
import struct

class IPC_SHM:
	def __init__(self):
		self.shm_a = shared_memory.SharedMemory(create=True, size=720*4)

	def __del__(self):
		self.shm_a.close()
		self.shm_a.unlink()

	def write(self, data: list):
		if len(data) != 720:
			raise ValueError("length of data must be 720")
			return

		barr = struct.pack("f"*720, *data)
		print("LENGTH - ", len(barr))

		#self.shm_a = self.shm_a.buf[:len(barr)]
		self.shm_a.buf[:720*4] = barr
		return

	def read(self) -> list:
		result_data = list(struct.unpack("f"*720, self.shm_a.buf[:720*4]))
		return result_data

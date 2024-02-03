import torch
import numpy as np
import sys
sys.path.insert(0, "../library")
from racecar_core import create_racecar
import racecar_utils

class Depth:
	def __init__(self):
		self.car = create_racecar()
		self.speed = 0
		self.angle = 0

	def start(self):
		self.car.drive.set_max_speed(0.3)
		self.car.drive.stop()

	def update(self):
		pass

	def update_slow(self):
		pool = torch.nn.AvgPool1d(kernel_size=4, stride=4)
		img = pool(torch.tensor(np.array(self.car.camera.get_depth_image())).long()).unsqueeze(0)

		far = 0
		for i in range(len(img[0])//2):
			for j in range(len(img[0][i])):
				_in = -i
				if far < img[0][i][j] < img[0][_in][j]:
					far = max([img[0][i][j], img[0][_in][j]])
		print(far)

if __name__ == "__main__":
	obj = Depth()
	obj.car.set_start_update(obj.start, obj.update, update_slow=obj.update_slow)
	obj.car.go()

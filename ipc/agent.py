import numpy as np
import nptyping
import sys
import os
import file
sys.path.insert(0, "/Users/mitya/desktop/speed/speed-racecar/library")
import racecar_core
import racecar_utils

class Agent:
	def __init__(self):
		self.car = racecar_core.create_racecar()
		self.write_status = True

	def start(self):
		self.car.drive.set_max_speed(0.5)
		self.car.drive.stop() # start at a standstill
	def update(self):
		lidarsamples = np.expand_dims(self.car.lidar.get_samples(), axis=3)

		file_obj = file.File()

		file_obj.write_data(lidarsamples)

def get() -> list:
	a = Agent()
	a.car.set_start_update(a.start, a.update)
	a.car.go()

print(get())

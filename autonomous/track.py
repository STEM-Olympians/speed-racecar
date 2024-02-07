import sys
import numpy as np
sys.path.insert(0, "../library") # python quirks
from racecar_core import create_racecar, physics
import racecar_utils
import math
import time
import logging

class MathUtils:
	def sign(self, num):
		return bool(num-num) # True is positive, False is negative

class RacecarDrive:
	def __init__(self):
		self.car = create_racecar()
		self.mutils = MathUtils()

	def _farthest_lidar(self, lidar_array):
		lidar_array = np.array(lidar_array)
		maximum = np.argmax(lidar_array)

		distance = lidar_array[maximum]
		degree = (180-(maximum/2))/180

		return [degree, distance]

	def start(self):
		self.car.drive.set_max_speed(0.5)
		self.car.drive.stop() # begin at a standstill

	def update(self):
		lidar = self.car.lidar.get_samples()
		degree, distance = self._farthest_lidar(lidar)
		print(f"DEGREE - {degree} | DISTANCE {distance}")
		self.car.drive.set_speed_angle(0.3, degree)

if __name__ == "__main__":
	obj = RacecarDrive()
	obj.car.set_start_update(obj.start, obj.update) # setting an initialization function (that runs on start) and an update function (a function which is called every frame)
	obj.car.go()

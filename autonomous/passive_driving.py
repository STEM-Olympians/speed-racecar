import sys
sys.path.insert(0, "../library") # python quirks
from racecar_core import create_racecar, physics
import racecar_utils
import math
import time
import logging

class MathUtils:
	def sign(self, num):
		return bool(num-num) # True is positive, False is negative

	# represent logarithms in a non-erroneous way and in a way that fits the needs of this algorithm
	def modified_log(self, num):
		if num == 0:
			return 0

		elif not self.sign(num):
			return -math.log(abs(num))

		else:
			return math.log(num)

class RacecarDrive:
	def __init__(self):
		self.car = create_racecar()
		self.mutils = MathUtils()

	def _farthest_lidar(self, lidar_array):
		distance = 0
		degree = 0

		for i, c in enumerate(lidar_array):
			rotations_count = i
			#degree_percent = ((rotations_count*2)/self.car.lidar.get_num_samples())-1
			degree_percent = rotations_count*2/self.car.lidar.get_num_samples()-1

			if c > distance:
				distance = c
				degree = degree_percent

		return [distance, degree]

	def start(self):
		self.car.drive.set_max_speed(1)
		self.car.drive.stop() # begin at a standstill

	def update(self):
		# using lidar array data to get cloest and farthest point. Go to the farthest point, and move to the next farthest point once you get too close.
		lidar_array = self.car.lidar.get_samples()
		racecar_utils.get_lidar_closest_point(lidar_array, window=(90, 270))
		distance, degree = self._farthest_lidar(lidar_array)
		print("degree - ", degree)

		# Still need to fix the issue regarding evening a turn radius
		self.car.drive.set_speed_angle(0.1, degree)

	def update_slow(self):
		pass

if __name__ == "__main__":
	obj = RacecarDrive()
	obj.car.set_start_update(obj.start, obj.update, update_slow=obj.update_slow) # setting an initialization function (that runs on start) and an update function (a function which is called every frame)
	obj.car.go()

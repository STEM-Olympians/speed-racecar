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

		logging.basicConfig(filename="logs/drive_track.log", encoding="utf-8", level=logging.DEBUG, filemode="w")

	def _farthest_lidar(self, lidar_array):
		distance = 0
		degree = 0

		for i, c in enumerate(lidar_array):
			rotations_count = i
			#degree_percent = ((rotations_count*2)/self.car.lidar.get_num_samples())-1
			degree_percent = rotations_count*2/self.car.lidar.get_num_samples()-1

			if c > distance and degree_percent > -0.5 and degree_percent < 0.5:
				distance = c
				degree = degree_percent

		return [distance, degree]

	def rad_log_growth(self, bounds_min, bounds_max):
		arr = [bounds_min]
		i = 0
		while self.mutils.modified_log(arr[-1]) < bounds_max:
			arr.append(self.mutils.modified_log(arr[-1]))
		return arr

	def rad_log_decay(self, bounds_min, bounds_max):
		arr = [bounds_max]
		while self.mutils.modified_log(arr[-1]) > bounds_min:
			arr.append(self.mutils.modified_log(arr[-1]))

	def start(self):
		self.car.drive.set_max_speed(1)
		self.car.drive.stop() # begin at a standstill

	def update_slow(self):
		lidar_array = self.car.lidar.get_samples()
		distance, degree = self._farthest_lidar(lidar_array)
		print("degree - ", degree)
		logging.info(f"DISTANCE - {distance} , DEGREE - {degree}")

		rad_follow = []
		if self.mutils.sign(degree):
			rad_follow = self.rad_log_decay(degree, 0)
		else:
			rad_follow = self.rad_log_growth(0, degree)

		for i, c in enumerate(rad_follow):
			self.car.set_speed_angle(0.1, c)

	def update(self):
		pass

if __name__ == "__main__":
	obj = RacecarDrive()
	obj.car.set_start_update(obj.start, obj.update, update_slow=obj.update_slow) # setting an initialization function (that runs on start) and an update function (a function which is called every frame)
	obj.car.go()

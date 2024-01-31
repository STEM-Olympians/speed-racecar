import sys
sys.path.insert(0, "../library") # python quirks
import racecar_core
import racecar_utils
import math
#import time

class RacecarDrive:
	def __init__(self):
		self.car = racecar_core.create_racecar()
		#self.speed = 0
		#self.angle = 0

	def start(self):
		self.car.drive.set_max_speed(1)
		self.car.drive.stop() # begin at a standstill

	def get_lidar_data(self):
		scan = self.car.lidar.get_samples()
		return scan

	# is currently driving
	#def drive(self, speed: float, angle: float):
	#	self.car.drive.set_speed_angle(speed, angle)
	# self.car.drive.stop()

	def update_slow(self):
		self.get_lidar_data()
		if self.car.controller.was_pressed(self.car.controller.Button.A):
			print("meow kitten")
			self.drive()

	def update(self):
		lidar_array = self.get_lidar_data()
		#print(lidar_array)

		highest_distance = 0
		highest_distance_degree_percentage = 0
		for i, c in enumerate(lidar_array):
			rotations_count = i+1
			#degree_percent = (rotations_count-math.floor(rotations_count))
			degree_percent = ((rotations_count*2)/720)-1# -(360/720)
			print(degree_percent)

			if c > highest_distance:
				highest_distance = c
				highest_distance_degree_percentage = degree_percent

		#print(highest_distance_degree_percentage)
		print(highest_distance)
		print(highest_distance_degree_percentage)
		while racecar_utils.ARMaker.get_orientation() < highest_distance_degree_percentage:
			self.car.drive.set_speed_angle(0.3, highest_distance_degree_percentage)
		self.car.drive.set_speed_angle(0.3, highest_distance_degree_percentage)

if __name__ == "__main__":
	obj = RacecarDrive()
	obj.car.set_start_update(obj.start, obj.update, update_slow=obj.update_slow) # setting an initialization function (that runs on start) and an update function (a function which is called every frame)
	obj.car.go()


import sys
import numpy as np
import utils
import random
from threading import Thread, Lock
sys.path.insert(0, "../library") # python quirks
from racecar_core import create_racecar, physics
import racecar_utils
import math
import time
import logging


"""

10 instances of the game will run at the same time.

After all of them terminate, the fittest node will be determined, and its genome will be passed down in mutated form to the next generation.

The fitness function will be largely based on parameters like time to survive, and productivity encouragement, like preventing the car from just going in circles.

"""

	# you can just mutate everything in the start function
	# you can append everythign to the file after the car crashes without actually stopping the car process, but you can do that in the parent process if you'd like.
	# the rule for playing the instructions is that it plays a new instruction every 0.5 seconds. So it will play a new instruction for every iteration of the slow update, and the slow update time will be set to 0.5 in the start function.
	# crash will be checked when deciding whether to stop the simulation or not, and time-to-crash and angular velocity will be used in order to determine fitness function, and the fitness function of the instruction set in the json file, and the one that was just played will be conditioned, whichever one is better will be set as the json file instruction set that will be referenced in later playthroughs or training iterations.

# racecar run is going to take the instruction set in the json file and is going to play it
class RacecarRun:
	def __init__(self):
		self.car = create_racecar()
		u = utils.FileUtils("data.json")
		self.dat_arr = u.read_data("instruction_set")
		self.i = -1
		self.speed = 0.3

	def start(self):
		self.car.drive.set_max_speed(self.speed)
		self.car.drive.stop()
		self.car.set_update_slow_time(1.5)

	def update(self):
		pass

	def update_slow(self):
		self.i += 1
		if self.i < len(self.dat_arr)-1:
			self.car.drive.set_speed_angle(self.speed, self.dat_arr[self.i])
		else:
			self.car.drive.stop()

"""
run code:
	rc = RacecarRun()
	rc.set_start_update(rc.start, None, rc.update_slow)
	rc.go()
"""


# racecar train is going to train the racecar evolutionary algortihm
class RacecarTrain:
	def __init__(self):
		self.current_agent=np.array([])
		self.car = create_racecar()

# template datastructure for what is to be put into the fitness function
# tuple: 0=angle 1=distance
		fitness_datastructure = {
			"turned_too_far":False,
			"time_to_crash":0,
		}

	def mutate(self, agent):
		possible_mutations = ["insert", "remove", "alter"]
		mutation = random.choice(possible_mutations)

		# insert
		if mutation == possible_mutations[0]:
			replacement_value = random.uniform(-1, +1)

			child = np.append(child, replacement_value)

		# remove
		elif mutation == possible_mutations[1]:
			deletion_index = random.uniform(0, len(child)-1)

			child = np.delete(chid, deletion_index, None)

		# alter
		elif mutation == possible_mutations[2]:
			alter_index = random.ranint(len(child)-1)
			alter_value = random.randint(-1, +1)

			child = np.put(child, alter_index, alter_value)

		return child

	def fitness(self, turn_too_far, time_to_crash_seconds):
		return (int(turn_too_far)*10)+time_to_crash_seconds

# A class for collecting data about the environment and the car.

	car       = create_racecar()
	mutils    = utils.MathUtils()

	def farthest_lidar(self, lidar_array):
		lidar_array = np.array(lidar_array)
		maximum = np.argmax(lidar_array)

		distance = lidar_array[maximum]
		angle = (180-(maximum/2))/180 # maps 720 length array to -1 to +1 where over 180 degrees increases from -1 to 0.

		return (angle, distance)

	def nearest_lidar(self, lidar_array):
		lidar_array = np.array(lidar_array)
		window      = (0, 360)
		angle, distance    = racecar_utils.get_lidar_closest_point(lidar_array, window)
		return (distance, angle)

	def front_lidar(self, lidar_array):
		lidar_array = np.array(lidar_array)

		distance = lidar_array[0]
		angle    = (180-(0/2))/180

		return (distance, angle)

	def angular_velocity_turn_too_far(self):
		turn = self.car.physics.get_angular_velocity()[1]
		if turn > 0.6 or turn < -0.6: # I basically made up the 0.6 figure.
			return True
		return False

	def is_crashed(self):
		start = time.time()
		print("TIME - ", round(time.time()-start))
		while time.time()-start >= 2:
			print("asdlfjasldkfjaslkdfjsalk")
			print("STOPPED? IDK - ", self.car.physics.get_angular_velocity()[2])
			if self.car.physics.get_angular_velocity()[2] <= 0.1:
				return False
			return True

	def start(self):
		self.car.drive.set_max_speed(1)
		self.car.drive.stop() # begin at a standstill
		self.car.set_update_slow_time(0.5)

	# upate function is going to mainly be checking for the crash
	def update(self):
		"""
		print("CRASH STATUS ", self.is_crashed())
		print("FAR TURN STATUS ", self.angular_velocity_turn_too_far())
		"""
		if self.is_crashed():
			print("crash detected.")

		if self.angular_velocity_turn_too_far():
			print("sharp turn detected.")

		#self.car.drive.set_speed_angle(0.3, -0.6)
		self.car.drive.set_speed_angle(0.3, 0.6)

	def update_slow(self):
			pass


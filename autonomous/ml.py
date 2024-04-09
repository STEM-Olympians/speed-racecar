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
		self.speed = 0.5

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
        self.mutils = utils.MathUtils()
        self.current_agent=np.array([])
        self.car = create_racecar()
        self.speed = 0.5

        #self.start_time = 0 # simply defining the variable for the start time, time of simulation starting will be assigned to it when self.start() is called.
        #self.start_time_game_time_to_crash = 0

        self.time_to_crash = 0
        self.times_turned_too_far = 0

        self.u = utils.FileUtils("data.json")
        print(self.u.read_data("instruction_set"))
        self.mutated_driving_instruction_set = self.mutate(np.array(self.u.read_data("instruction_set")))
        print("MUTATED INSTRUCTION SET - ", self.mutated_driving_instruction_set)

        self.previous_fitness = self.u.read_data("fitness")
        self.i = -1

		#self.start = time.time() # start time to check time to crash

		#self.time_to_crash = 0 # this value will be decided when you actually crash, and the difference of the start time and ththe time of the crash is calculated.

		# there must be one crash signal in order to determine to reset
		# it must turn too far once in order to determine to reset
		#self.death_factor_tally_overturn = 0

    # template datastructure for what is to be put into the fitness function
    # tuple: 0=angle 1=distance
    def mutate(self, child):
        possible_mutations = ["insert", "remove", "alter"]
        mutation = random.choice(possible_mutations)

		# insert
        if mutation == possible_mutations[0]:
            print("insert")
            replacement_value = random.uniform(-0.5, 0.5)
            child = np.append(child, replacement_value)

        # remove
        elif mutation == possible_mutations[1]:
            print("remove")
            deletion_index = random.randint(0, len(child)-1)
            child = np.delete(child, deletion_index, None)

		# alter
        elif mutation == possible_mutations[2]:
            print("alter")
            alter_index = random.randint(0, len(child)-1)
            print("alter index - ", alter_index)
            alter_value = random.uniform(-0.5, 0.5)
            print("alter_value - ", alter_value)

            #child = np.put(child, alter_index, alter_value)
            np.put(child, alter_index, alter_value)
            print("child - ", child)

        return child

    def fitness(self, times_turned_too_far, time_to_crash_seconds):
        return time_to_crash_seconds-times_turned_too_far

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
        turn = self.car.physics.get_angular_velocity()[2]
        #print("TURN ", turn)
        if turn > 0.5 or turn < -0.5: # I basically made up the 0.6 figure.
            return True
        return False

    # this funuction won't work if it's called in self.update() because self.update() runs every frame, which will violate the 2 second while loop used to determine crash. Instead, call in update_slow()
    def is_crashed(self):
        if time.time()-self.start_time >= 2:
            if self.car.physics.get_linear_acceleration()[2] <= 0.05:
                return True

    def start(self):
        self.car.drive.set_max_speed(1)
        self.car.drive.stop() # begin at a standstill
        self.car.set_update_slow_time(1)
        self.start_time = time.time()
        self.start_time_game_time_to_crash = time.time()

    def update(self):
        if self.angular_velocity_turn_too_far():
            self.times_turned_too_far += 1
            print("turn too far")

        #self.car.drive.set_speed_angle(1, -0.6)
        self.car.drive.set_speed_angle(self.speed, 0.1)

    def update_slow(self):
        if self.is_crashed():
            self.time_to_crash = time.time()-self.start_time_game_time_to_crash
            print(self.time_to_crash)
            fitness = self.fitness(self.times_turned_too_far, self.time_to_crash)
            print("CURRENT FITNESS ", fitness)
            print("PREV FITNESS", self.previous_fitness)

            if fitness > self.previous_fitness:
                self.u.write_data("instruction_set", self.mutated_driving_instruction_set.tolist())
                self.u.write_data("fitness", fitness)

            print("crashed, time - ", self.time_to_crash)

            sys.exit(0)

        self.i += 1
        print(self.mutated_driving_instruction_set)
        if self.i < len(self.mutated_driving_instruction_set)-1:
            self.car.drive.set_speed_angle(self.speed, self.mutated_driving_instruction_set[self.i])
        else:
            self.car.drive.stop()


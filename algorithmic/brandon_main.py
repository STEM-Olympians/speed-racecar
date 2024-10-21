import sys
import numpy as np
from datetime import datetime
import time
import math
import matplotlib.pyplot as plt

sys.path.insert(0, "/Users/admin/Documents/Repos/speed/library")

from racecar_core import create_racecar
import racecar_utils

from motor_controller.controller import Controller
from motor_controller.lidar_sensor import Lidar_Sensor

class Algorithmic:
    def __init__(self):
        #self.car = create_racecar()
        self.controller = Controller()
        self.controller.stop()
        self.lidar_sensor = Lidar_Sensor()
        self.speed = 0.5

        self.turn_history = [0] # determine next turn based on similarity to previous turns to prevent issues with committing to turns.


        # defined in start() to remain unchanged by update() resets.
        # Brandon here - not really sure what the above comment meant... since we do change start time
        self.start_time = time.time()

        #self.lidar = self.car.lidar.get_samples()
        self.lidar = self.lidar_sensor.get_samples()


        self.angleToTurn = self.getHighestLidar(self.lidar) # defined in start() to be changed when turn finishes and not when update() resets.

        self.turn_history.append(self.angleToTurn)

        # You guys never told me u needed a gyro T-T
        self.angvel = 0

        self.travel_time = 0

    # Deadbanding fr fr
    def highlight(self, distance):
        if distance > self.avg+(0.7*self.dev):
            print("DISTANCE ", distance)
            return distance
        return 0

    def getHighestSummedWindowIndex(self, lidar):
        self.avg = np.average(lidar)
        self.dev = np.std(lidar)

        print("STANDARD DEVIATION ", self.dev)
        print("AVERAGE ", self.avg)

        lidar = list(map(self.highlight, lidar))
        #print(lidar)

        highest = 0
        highestIndex = 0

        current = 0
        #currentIndex = 0

        for i in range(1, len(lidar)):
            if lidar[i] != 0 and lidar[i-1] == 0:
                current = 1

            if lidar[i-1] != 0 and lidar[i] != 0:
                current += 1
                if current > highest:
                    print("Highest valued index: ", highestIndex)
                    highest = current
                    highestIndex = i-highest

        window =  lidar[highest:highest+highestIndex]
        #print(window)
        return (highestIndex, highest+highestIndex)


    def getHighestLidar(self, lidar_array):
        lidar_array = np.array(lidar_array)

        first = lidar_array[0:180]
        second = lidar_array[540:-1]
        lidar = np.append(second, first)


        #print("SIZE FIRST ", len(first))
        #print(first)
        #print("SIZE SECOND ", len(second))
        first, second = self.getHighestSummedWindowIndex(lidar)
        """
        if not sliced:
            idx = lidar
            print("LIDAR  ", lidar)
        """
        #print("SLICED ", sliced)

        #idx = np.argmax(sliced)
        idx = np.argmax(lidar[first:second])

        angle = idx+first
        print("IDX ", idx)
        print("FIRST ", first)
        print("SECOND ", second)

        distance = lidar[angle]
        angle = angle/180
        angle -= 1

        A_constant = math.pi

        #print("LENGTH: ", len(sliced))
        #angle /= len(lidar)/2 # 0 to 2
        #angle -= 1 # shift the non-linear angle to be from -1 to +1
        angle_nl = angle**2# Non-linear angle: from 0 to 1, but more angles accumulate in the lower half from 0 to 0.5
        #angle_nl = A_constant* angle_nl if angle_nl * A_constant < 1 else 1
        angle_nl = A_constant*angle_nl if A_constant*angle_nl < 1 else 1
        print("NL ANGLE ", angle_nl)

        turn_angle = -angle_nl if angle < 0 else angle_nl
        print("TURN ANGLE ", turn_angle)

        return turn_angle


    def getSimilarAngle(self, angles):
        #reference = sum(self.turn_history)/len(self.turn_history) # so my brain doesn't get lost again
        reference = self.turn_history[-1]

        ref = np.array([])
        for i in range(len(angles)):
            ref = np.append(ref, abs(angles[i]-reference))

        return angles[np.argmin(ref)] # will return angle with minimum distance to the relative angle

    def update(self):
        if time.time()-self.start_time >= self.travel_time:
            #self.lidar = self.car.lidar.get_samples()
            self.lidar = self.lidar_sensor.get_samples()

            self.angleToTurn = self.getHighestLidar(self.lidar) # defined in start() to be changed when turn finishes and not when update() resets.z
            print(self.angleToTurn)
            self.turn_history.append(self.angleToTurn)

            self.angvel = self.car.physics.get_angular_velocity()[0]

            try:
                self.travel_time = (self.angvel/self.angleToTurn)
            except RuntimeWarning as e:
                self.travel_time = 0


            self.start_time = time.time() # defined in start() to remain unchanged by update() resets.
            
            
            #self.car.drive.set_speed_angle(self.speed, self.angleToTurn)
            self.controller.drive(self.speed, self.angleToTurn)

        else:
            #self.car.drive.set_speed_angle(self.speed, 0)
            self.controller.drive(self.speed, 0)


if __name__ == "__main__":
    a = Algorithmic()

    # Introduce rate limiting? lol
    while True:
        a.update()

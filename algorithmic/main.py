import sys
import numpy as np
from datetime import datetime
import time
import math
import matplotlib.pyplot as plt

sys.path.insert(0, "../library")
from racecar_core import create_racecar
import racecar_utils

class Algorithmic:
    def __init__(self):
        self.car = create_racecar()
        self.speed = 0.5

        self.turn_history = [0] # determine next turn based on similarity to previous turns to prevent issues with committing to turns.

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

    def start(self):
        self.car.drive.set_max_speed(self.speed)
        self.car.drive.stop()
        self.car.set_update_slow_time(1)

        self.start = time.time() # defined in start() to remain unchanged by update() resets.

        self.lidar = self.car.lidar.get_samples()


        self.angleToTurn = self.getHighestLidar(self.lidar) # defined in start() to be changed when turn finishes and not when update() resets.

        self.turn_history.append(self.angleToTurn)

        self.car.drive.set_speed_angle(self.speed, self.angleToTurn)
        self.angvel = self.car.physics.get_angular_velocity()[0]

        self.travel_time = (self.angvel/self.angleToTurn)

    def update(self):
        if time.time()-self.start >= self.travel_time:
            self.lidar = self.car.lidar.get_samples()

            self.angleToTurn = self.getHighestLidar(self.lidar) # defined in start() to be changed when turn finishes and not when update() resets.z
            print(self.angleToTurn)
            self.turn_history.append(self.angleToTurn)

            self.angvel = self.car.physics.get_angular_velocity()[0]

            try:
                self.travel_time = (self.angvel/self.angleToTurn)
            except RuntimeWarning as e:
                self.travel_time = 0

            #print(summed_buffer_array.shape)
            #print(summed_buffer_array)

            """
            # This is just some plotting code to test my procedurally generated lidar data.
            plt.rcParams["figure.figsize"] = [720, 1000]
            plt.rcParams["figure.autolayout"] = True
            y = self.lidar
            x = range(len(y))
            plt.plot(x, y, color="red")
            plt.show()
            """

            self.start = time.time() # defined in start() to remain unchanged by update() resets.
            self.car.drive.set_speed_angle(self.speed, self.angleToTurn)
        else:
            self.car.drive.set_speed_angle(self.speed, 0)

    def update_slow(self):
        pass


if __name__ == "__main__":
    a = Algorithmic()
    a.car.set_start_update(a.start, a.update, update_slow=a.update_slow)
    a.car.go()

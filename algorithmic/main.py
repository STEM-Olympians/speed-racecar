import sys
import numpy as np
from datetime import datetime
import time

sys.path.insert(0, "../library")
from racecar_core import create_racecar
import racecar_utils


class Algorithmic:
    def __init__(self):
        self.car = create_racecar()
        self.speed = 0.5

    def getHighestLidar(self, lidar_array):
        lidar_array = np.array(lidar_array)
        first = lidar_array[0:180]
        second = lidar_array[540:-1]

        print("SIZE FIRST ", len(first))
        print(first)
        print("SIZE SECOND ", len(second))

        maximum = np.argmax(np.append(second, first))

        distance = lidar_array[maximum]
        # angle = (180-(maximum/2))/180
        angle = maximum #**2
        angle -= 180
        angle /= 180
        print("maximum ", maximum)
        print("angle ", angle)

        """
        # add some arbitrary padding to account for the width of the car
        if angle < 0:
            angle += 0.001

        elif angle >= 0:
            angle += 0.001

        if angle > 1.0:
            angle = 1.0
        if angle < -1.0:
            angle = -1.0
        """

        print("")
        print(str(time.time()), " ANGLE - ",    angle)
        print(str(time.time()), " DISTANCE - ", distance)
        print("")

        return (angle, distance)


    def start(self):
        self.car.drive.set_max_speed(self.speed)
        self.car.drive.stop()
        self.car.set_update_slow_time(1)

        self.start = time.time() # defined in start() to remain unchanged by update() resets.

        self.lidar = self.car.lidar.get_samples()
        self.angleToTurn = self.getHighestLidar(self.lidar)[0] # defined in start() to be changed when turn finishes and not when update() resets.

        self.car.drive.set_speed_angle(self.speed, self.angleToTurn)
        self.angvel = self.car.physics.get_angular_velocity()[0]
        self.travel_time = self.angvel/self.angleToTurn


        print("Travel Time ", self.travel_time)
        print("Angle to Turn ", self.angleToTurn)

    def update(self):
        if time.time()-self.start >= self.travel_time:
            self.lidar = self.car.lidar.get_samples()

            self.angleToTurn = self.getHighestLidar(self.lidar)[0] # defined in start() to be changed when turn finishes and not when update() resets.z

            self.angvel = self.car.physics.get_angular_velocity()[0]
            self.travel_time = self.angvel/self.angleToTurn

            self.start = time.time() # defined in start() to remain unchanged by update() resets.
            self.car.drive.set_speed_angle(self.speed, self.angleToTurn)

        else:
            self.car.drive.set_speed_angle(self.speed, 0)
            print("TIME DELTA ", time.time()-self.start)

    def update_slow(self):
        pass


if __name__ == "__main__":
    a = Algorithmic()
    a.car.set_start_update(a.start, a.update, update_slow=a.update_slow)
    a.car.go()

import sys
import numpy as np
from datetime import datetime
import time
import math
import matplotlib.pyplot as plt

sys.path.insert(0, "/Users/admin/Documents/Repos/speed/library")

# from racecar_core import create_racecar
# import racecar_utils

from controller import Controller
from lidar_sensor import Lidar_Sensor

class Algorithmic:
    def __init__(self):
        #self.car = create_racecar()
        # self.controller = Controller()
        # self.controller.stop()
        # self.lidar_sensor = Lidar_Sensor()
        # self.speed = 0.5

        self.turn_history = [0] # determine next turn based on similarity to previous turns to prevent issues with committing to turns.


        # defined in start() to remain unchanged by update() resets.
        # Brandon here - not really sure what the above comment meant... since we do change start time
        self.start_time = time.time()

        # #self.lidar = self.car.lidar.get_samples()
        # self.lidar = self.lidar_sensor.get_samples()


        # self.angleToTurn = self.getHighestLidar(self.lidar) # defined in start() to be changed when turn finishes and not when update() resets.
        self.angleToTurn = 0

        self.turn_history.append(self.angleToTurn)

        # self.highlight_vectorized = np.vectorize(self.highlight)

        # You guys never told me u needed a gyro T-T
        # self.angvel = 0

        # self.travel_time = 0

    # # Deadbanding fr fr
    # def highlight(self, distance):
    #     if distance > self.avg+(0.7*self.dev):
    #         print("DISTANCE ", distance)
    #         return distance
    #     return 0

    def getHighestSummedWindow(self, lidar):
        avg = np.average(lidar[:, 1])
        dev = np.std(lidar[:, 1])

        print("STANDARD DEVIATION ", dev)
        print("AVERAGE ", avg)

        # mask = lidar[:, 1] > self.avg+(0.7*self.dev)
        # lidar = self.highlight_vectorized(lidar)
        
        # Only grabbing second column (range)
        range = lidar[:,1]

        print(range)
        highlighted_range = np.where(range > avg + (0.7*dev), range, 0)
        highlighted_range = np.concatenate([[0.0], highlighted_range, [0.0]])
        # highlighted_range = np.where(range[1:-1] > avg + (0.7*dev), range[1:-1], 0)

        print("highlight")
        print(highlighted_range)
        # checking for whether neighbors are zero
        zero_neighbor = (highlighted_range[:-2] is not 0) & (highlighted_range[2:] is not 0)

        # Find where both neighbors are 0, and the current is non-zero
        left_neighbors_are_zero = (highlighted_range[1:-1] != 0) & (highlighted_range[:-2] == 0)
        right_neighbors_are_zero = (highlighted_range[1:-1] != 0) & (highlighted_range[2:] == 0)
        neighbors_are_zero = (highlighted_range[:-2] == 0) | (highlighted_range[2:] == 0)

        zero_left_neighbor_indices = np.where(left_neighbors_are_zero)[0]
        zero_right_neighbor_indices = np.where(right_neighbors_are_zero)[0]

        print("left zero", zero_left_neighbor_indices)
        print("right zero", zero_right_neighbor_indices)
        zipped = np.c_[zero_left_neighbor_indices, zero_right_neighbor_indices]
        


        # print("zero neighbor")
        # print(zero_neighbor)
        # # Indices of elements with zero as a neighbor (ignoring first and last element for comparison)
        # zero_indices = np.where(zero_neighbor)[0] + 1  # Shift by 1 to account for array slicing

        # print("indices")
        # print(zero_indices)
        diff = np.diff(zipped)
        print(np.diff(zipped))

        highest_diff_index = np.argmax(diff)

        print("high diff, no cap")
        print(highest_diff_index)

        # print(left_neighbors_are_zero)

        # Zero left neighbor
        print("Zero left neighbor", zero_left_neighbor_indices)
        # Zero right neighbor
        print("Zero right neighbor", zero_right_neighbor_indices)


        # Subtract 1 bc we shifted one index to the right earlier when we added a zero at the front lol
        start_index = zero_left_neighbor_indices[highest_diff_index]
        end_index = zero_right_neighbor_indices[highest_diff_index]
        print("start", start_index )
        print("end", end_index )
        print("result", lidar[start_index: end_index])
        print("theoretically better end :(", end_index + 1)
        print("Result...better?", lidar[start_index: end_index + 1])
        return lidar[start_index: end_index + 1]
    
        # print("how long is this range?")
        # print(len(printed_range))
        return start_index, end_index

        lidar[lower_zero_index: higher_zero_index]

        # list_zero_indices = zero_indices.tolist()
        
        # lower = list_zero_indices[0]
        # higher = list_zero_indices[1]

        # highestDifference = higher - lower

        # for i in list_zero_indices[1:]:
        #     currentDifference = i - 



        # #print

        # highest = 0
        # highestIndex = 0

        # current = 0
        # #currentIndex = 0

        # for i in range(1, len(lidar)):
        #     if lidar[i] != 0 and lidar[i-1] == 0:
        #         current = 1

        #     if lidar[i-1] != 0 and lidar[i] != 0:
        #         current += 1
        #         if current > highest:
        #             print("Highest valued index: ", highestIndex)
        #             highest = current
        #             highestIndex = i-highest

        # window =  lidar[highest:highest+highestIndex]
        # #print(window)
        # return (highestIndex, highest+highestIndex)


    def transformRawLidarArray(self, lidar_array):


        angle = np.array(angle)
        angle = ((np.pi / 2) - np.radians(5) + angle)
        angle = angle.tolist()


        lidar_array = np.array(lidar_array)

        # getting first 90 degrees
        first = lidar_array[0:180]
        # and last 90
        second = lidar_array[540:-1]

        # Flipping the array? ohh, left then right...?
        lidar = np.append(second, first)

        return lidar


    def getHighestLidar(self, lidar_array):
        # lidar_array = np.array(lidar_array)

        # # getting first 90 degrees
        # first = lidar_array[0:180]
        # # and last 90
        # second = lidar_array[540:-1]

        # # Flipping the array? ohh, left then right...?
        # lidar = np.append(second, first)


        #print("SIZE FIRST ", len(first))
        #print(first)
        #print("SIZE SECOND ", len(second))
        print("lidar arr")
        print(lidar_array)
        highlighted_section = self.getHighestSummedWindow(lidar_array)
        """
        if not sliced:
            idx = lidar
            print("LIDAR  ", lidar)
        """
        #print("SLICED ", sliced)

        #idx = np.argmax(sliced)
        # print("funny")
        # print("first", first)
        # print("second", second)
        
        range_arr = highlighted_section[:, 1]
        angle_arr = highlighted_section[:, 0]


        

        max_range_index = np.argmax(range_arr)

        angle = angle_arr[max_range_index]
        print("angle arr")
        print(angle_arr)

        print("range arr")
        print(range_arr)

        print("angle")
        print(angle)
        print("index of max range ", max_range_index)
       

        # distance = lidar_array[max_range_index][1]

        angle = angle/90
        # angle -= 1

        A_constant = math.pi

        #print("LENGTH: ", len(sliced))
        #angle /= len(lidar)/2 # 0 to 2
        #angle -= 1 # shift the non-linear angle to be from -1 to +1
        angle_nl = angle**2# Non-linear angle: from 0 to 1, but more angles accumulate in the lower half from 0 to 0.5
        #angle_nl = A_constant* angle_nl if angle_nl * A_constant < 1 else 1
        angle_nl = A_constant*angle_nl if A_constant*angle_nl < 1 else 1
        print("NL ANGLE ", angle_nl)

        # Copy sign iirc
        turn_angle = -angle_nl if angle < 0 else angle_nl
        print("TURN ANGLE ", turn_angle)

        # turn_angle, is like nl angle? from -1 to 1??
        # Shifting back to -90 space
        turn_angle *= 90

        return turn_angle


    def getSimilarAngle(self, angles):
        #reference = sum(self.turn_history)/len(self.turn_history) # so my brain doesn't get lost again
        reference = self.turn_history[-1]

        ref = np.array([])
        for i in range(len(angles)):
            ref = np.append(ref, abs(angles[i]-reference))

        return angles[np.argmin(ref)] # will return angle with minimum distance to the relative angle

    def update(self):
        # if time.time()-self.start_time >= self.travel_time:
            #self.lidar = self.car.lidar.get_samples()
            # self.lidar = self.lidar_sensor.get_samples()

            results = self.lidar_sensor.update()

            self.angleToTurn = self.getHighestLidar(results) # defined in start() to be changed when turn finishes and not when update() resets.z
            print(self.angleToTurn)
            self.turn_history.append(self.angleToTurn)

            # self.angvel = self.car.physics.get_angular_velocity()[0]

            # try:
            #     self.travel_time = (self.angvel/self.angleToTurn)
            # except RuntimeWarning as e:
            #     self.travel_time = 0


            # self.start_time = time.time() # defined in start() to remain unchanged by update() resets.
            
            
            #self.car.drive.set_speed_angle(self.speed, self.angleToTurn)

            left, right = self.controller.calculateArcadeSpeeds(1, self.angleToTurn)
            self.controller.drive(self.speed, self.angleToTurn)

        # else:
        #     #self.car.drive.set_speed_angle(self.speed, 0)
        #     self.controller.drive(self.speed, 0)


if __name__ == "__main__":
    a = Algorithmic()

    # Introduce rate limiting? lol
    while True:
        a.update()

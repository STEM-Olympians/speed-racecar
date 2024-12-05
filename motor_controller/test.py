# from lidar_sensor import Lidar_Sensor

# lidar = Lidar_Sensor()

import numpy as np
np.set_printoptions(suppress=True)

# for i in range (0, 100):
#     lidar.update()

# from controller import Controller
# from lidar_sensor import Lidar_Sensor

# controller = Controller()
# laser = Lidar_Sensor()

# left, right = controller.calculateArcadeSpeeds(1, 90)

# print("Left:", left)
# print("right:", right)

# arr = np.array([[2, 7], [3, 0.3],[1, 6]])

# sorted_arr = arr[arr[:, 0].argsort()]

# print(sorted_arr)

# array = np.array([
#     [10, 20],
#     [30, 40],
#     [50, 60],
#     [70, 80],
#     [100, 110],
#     [200, 210],
#     [275, 2],
#     [300, 310],
#     [350, 69]
# ])

# # array = np.radians(array - 85)
# # print(array[:, 0])
# # print(array[:, 1])
# # print(laser.normalize(array[:, 0], array[:, 1]))

# zipped = np.c_[array[:, 0], array[:, 1]]
# zipped = zipped[zipped[:, 0].argsort()]
# # zipped = np.argsort(zipped, axis=0)
# print("zipped")
# print(zipped)
# print("\n\n")

# # Condition: angle < 90 or angle > 270
# mask = (zipped[:, 0] < 90) | (zipped[:, 0] > 270)

# # Apply mask to filter rows
# filtered_array = zipped[mask]

# print(filtered_array)
 

# # Split the filtered array into two parts

# # the right side - those from 0-90 degrees
# right_side = filtered_array[filtered_array[:, 0] < 90]
# print("right")
# print(right_side)
# print("\n\n")
# # The left side - those from 270-360 degrees 
# left_side = filtered_array[filtered_array[:, 0] > 270]
# # Shifting to make sure the range from -90-0 degrees (cause 0 is north)
# left_side = np.stack((left_side[:, 0] - 360, left_side[:, 1]), axis=1) 



# # Concatenate them back together in the correct order
# final_array = np.vstack((left_side, right_side))

# print( final_array)

arr = np.array([1, 0, 2, 5, 6, 2, 1, 1, 0, 2, 0, 6, 0, 0, 0, 3, 0, 8])

# Adding zeros so we can detect an "edge"
# detects neighbors, but in the beginning there may be no neighbors
# we should assume they're the beginning of a trend tho

arr = np.concatenate([[0], arr, [0]])
print(arr)

# Find where both neighbors are 0, and the current is non-zero
left_neighbors_are_zero = (arr[1:-1] != 0) & (arr[:-2] == 0)
right_neighbors_are_zero = (arr[1:-1] != 0) & (arr[2:] == 0)
neighbors_are_zero = (arr[:-2] == 0) | (arr[2:] == 0)

zero_left_neighbor_indices = np.where(left_neighbors_are_zero)[0]
zero_right_neighbor_indices = np.where(right_neighbors_are_zero)[0]

zipped = np.c_[zero_left_neighbor_indices, zero_right_neighbor_indices]
print(np.diff(zipped))
print(np.argmax(np.diff(zipped)))

# Indices where both neighbors are 0 (ignoring first and last element for comparison)
zero_neighbor_indices = np.where(neighbors_are_zero)[0]  # Shift by 1 to account for array slicing

print("Indices where neighbors are 0:", zero_neighbor_indices)
print("Indices where left neighbors are 0:", zero_left_neighbor_indices)
print("Indices where right neighbors are 0:", zero_right_neighbor_indices)

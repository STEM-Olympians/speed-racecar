# DO NOT TOUCH ANY OF THIS
#%%
import numpy as np

import matplotlib.pyplot as plt

from brandon_main import Algorithmic
from lidar_sensor import Lidar_Sensor


np.random.seed(1144)

# Jank af
angle_counter = -np.pi / 2 

randomized = np.random.rand(90)
far = np.array([1] * 45)
super_far = np.array([2] * 45)

angle = np.arange(-90, 90)

new = np.c_[angle, np.concatenate([super_far, randomized, far, ])]
print(new)

left_wall = []
for i in range(63):
  h = 1 / np.cos(np.radians(i))
  left_wall.append([angle_counter, h])
  angle_counter += np.radians(1)

left_wall = np.array(left_wall)


right_wall = []
for i in range(45, 0, -1):
    h = 1 / np.cos(np.radians(i))
    right_wall.append([angle_counter, h])
    angle_counter += np.radians(1)
right_wall = np.array(right_wall)

far_wall_left = []

for i in range(27, 0, -1):
    h = 2 / np.cos(np.radians(i))
    far_wall_left.append([angle_counter, h])
    angle_counter += np.radians(1)
far_wall_left = np.array(far_wall_left)

far_wall_right = []

for i in range(45):
    h = 2 / np.cos(np.radians(i))
    far_wall_right.append([angle_counter, h])
    angle_counter += np.radians(1)
far_wall_right = np.array(far_wall_right)




walls = np.concatenate([far_wall_right, right_wall, left_wall, far_wall_left,])

# walls = np.c_[np.linspace(np.pi * 2), walls]

a = Algorithmic()
lidar = Lidar_Sensor()

cleaned = lidar.normalize(walls[:, 0], walls[:, 1])
#print(a.getHighestLidar(cleaned))

calculated_angle = a.getHighestLidar(new)
RMAX = 32.0

lidar_polar = plt.subplot(polar=True)

lidar_polar.set_rmax(RMAX)
lidar_polar.grid(True)
lidar_polar.set_theta_offset(np.pi / 2)  # start month labels north
lidar_polar.set_theta_direction(-1)  # set month labels in clockwise order

#print(cleaned)
# lidar_polar.scatter(np.radians(cleaned[:, 0]), cleaned[:, 1], c=[1] * len(cleaned), cmap='hsv', alpha=0.95)
#lidar_polar.scatter(np.radians(walls[:, 0]), walls[:, 1], c=[1] * len(cleaned), cmap='hsv', alpha=0.95)

print(new)

lidar_polar.scatter(np.radians(new[:, 0]), new[:, 1], c=[1] * len(new), cmap='hsv', alpha=0.95)


lidar_polar.scatter(np.radians([calculated_angle]), [0.5], color="blue", cmap='hsv', alpha=0.95)

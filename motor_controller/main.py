import os
import time

from matplotlib.patches import Arc
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from lidar_sensor import Lidar_Sensor

import sys
sys.path.append("/home/pi/YDLidar-SDK/build/python")
import ydlidar

RMAX = 32.0


fig = plt.figure()
#fig.canvas.set_window_title('YDLidar LIDAR Monitor')
plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True
lidar_polar = plt.subplot(1, 1, 1, projection='polar')
lidar_polar.set_theta_direction(-1)
lidar_polar.set_theta_offset(np.pi / 2.0)
#lidar_polar = plt.subplot(polar=True)

lidar_polar.autoscale_view(True,True,True)
lidar_polar.set_rmax(RMAX)
lidar_polar.grid(True)

# ports = ydlidar.lidarPortList()
# port = "/dev/ydlidar"
# for key, value in ports.items():
#     port = value
    
# laser = ydlidar.CYdLidar()
# laser.setlidaropt(ydlidar.LidarPropSerialPort, port)
# laser.setlidaropt(ydlidar.LidarPropSerialBaudrate, 230400)
# laser.setlidaropt(ydlidar.LidarPropLidarType, ydlidar.TYPE_TOF)
# laser.setlidaropt(ydlidar.LidarPropDeviceType, ydlidar.YDLIDAR_TYPE_SERIAL)
# laser.setlidaropt(ydlidar.LidarPropScanFrequency, 10.0)
# laser.setlidaropt(ydlidar.LidarPropSampleRate, 8)
# laser.setlidaropt(ydlidar.LidarPropSingleChannel, False)
# laser.setlidaropt(ydlidar.LidarPropMaxAngle, 180.0)
# laser.setlidaropt(ydlidar.LidarPropMinAngle, -180.0)
# laser.setlidaropt(ydlidar.LidarPropMaxRange, 32.0)
# laser.setlidaropt(ydlidar.LidarPropMinRange, 0.01)

laser = Lidar_Sensor()

# scan = ydlidar.LaserScan()


def animate(num):
    
   
    results = laser.update()
       
                
    print(results)

    angle = results[:, 0]
    range = results[:, 1]


    lidar_polar.clear()
    lidar_polar.scatter(angle, range, cmap='hsv', alpha=0.95)
    lidar_polar.set_theta_direction(-1)
    lidar_polar.set_theta_offset(np.pi / 2.0)


ani = animation.FuncAnimation(fig, animate, interval=50)
plt.show()


# ret = laser.initialize()
# if ret:
#     ret = laser.turnOn()
#     if ret:
#         ani = animation.FuncAnimation(fig, animate, interval=50)
#         plt.show()

laser.turnOff()
laser.disconnecting()
plt.close()

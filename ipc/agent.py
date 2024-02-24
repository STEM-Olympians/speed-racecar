import numpy as np
import sys
sys.path.insert("../library")
import racecar_core
import racecar_utils

class Agent:
    def __init__(self):
        self.car == racecar_core.create_car()
        self.write_status = True

    def start(self):
        self.car.drive.set_max_speed(0.5)
        self.car.drive.stop() # start at a standstill

    def update(self):
        self.car.camera.lidar_samples

def get() -> list:
    a = Agent()
    a.set_start_update(a.start, a.update)
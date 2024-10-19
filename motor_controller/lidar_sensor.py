import RPi.GPIO as GPIO
import numpy as np
from nptyping import NDArray

class Lidar_Sensor:
   
    def __init__(self):      
        self.samples = np.empty(0)


    def get_samples(self) -> NDArray[720, np.float32]:
        return self.samples
    
    def update():
        print("idk")
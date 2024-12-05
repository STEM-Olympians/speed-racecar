
import numpy as np
np.set_printoptions(suppress=True)
import sys
# sys.path.append("/home/pi/YDLidar-SDK/build/python")
# import ydlidar



class Lidar_Sensor:
   
    def __init__(self):      
        RMAX = 32.0

        # 90 because belle set it approximately 90 degrees, but it overshot a bit, so reduced by 5
        self.offset_degrees = 90 - 5 


        # ports = ydlidar.lidarPortList()
        # port = "/dev/ydlidar"
        # for key, value in ports.items():
        #     port = value
            
        # self.laser = ydlidar.CYdLidar()
        # self.laser.setlidaropt(ydlidar.LidarPropSerialPort, port)
        # self.laser.setlidaropt(ydlidar.LidarPropSerialBaudrate, 230400)
        # self.laser.setlidaropt(ydlidar.LidarPropLidarType, ydlidar.TYPE_TOF)
        # self.laser.setlidaropt(ydlidar.LidarPropDeviceType, ydlidar.YDLIDAR_TYPE_SERIAL)
        # self.laser.setlidaropt(ydlidar.LidarPropScanFrequency, 10.0)
        # self.laser.setlidaropt(ydlidar.LidarPropSampleRate, 8)
        # self.laser.setlidaropt(ydlidar.LidarPropSingleChannel, False)
        # self.laser.setlidaropt(ydlidar.LidarPropMaxAngle, 180.0)
        # self.laser.setlidaropt(ydlidar.LidarPropMinAngle, -180.0)
        # self.laser.setlidaropt(ydlidar.LidarPropMaxRange, 32.0)
        # self.laser.setlidaropt(ydlidar.LidarPropMinRange, 0.01)

        # self.scan = ydlidar.LaserScan()

        self.results = np.array([])

        self.vectorized_offset = np.vectorize(self.offset)


    def scan(self):
        r = self.laser.doProcessSimple(self.scan)
        if r:
            angle = []
            range = []
            # intensity = []
            for point in self.scan.points:
                angle.append(point.angle)
                range.append(point.range)
                # intensity.append(point.intensity)
                
            angle = np.array(angle)
            range = np.array(range)
        
        return angle, range
    
    

    def offset(self, angle_radian):
            angle_degrees = np.degrees(angle_radian)

            # Shifting to offset the lidar's heading
            angle_degrees = self.offset_degrees + angle_degrees

            # Truncating to 3 decimal places
            angle_degrees = np.trunc( angle_degrees * 1000) / 1000
            
            # Ensuring there are no negative angles (makes it easier to decipher later)
            return angle_degrees if angle_degrees > 0 else angle_degrees + 360 

    
    def normalize(self, angle_arr, range_arr):
        angle_arr = self.vectorized_offset(angle_arr)

        zipped = np.c_[angle_arr, range_arr]
        zipped = zipped[zipped[:, 0].argsort()]

        # Filtering on whether angle < 90 or angle > 270
        mask = (zipped[:, 0] < 90) | (zipped[:, 0] > 270)

        # Apply mask to filter rows
        filtered_array = zipped[mask]
 

        # Split the filtered array into two parts

        # The left side - those from 270-360 degrees 
        left_side = filtered_array[filtered_array[:, 0] > 270]
        # Shifting to make sure the range from -90-0 degrees (cause 0 is north)
        left_side = np.stack((left_side[:, 0] - 360, left_side[:, 1]), axis=1) 

        # the right side - those from 0-90 degrees
        right_side = filtered_array[filtered_array[:, 0] < 90]


        # Concatenate them back together in the correct order
        final_array = np.vstack((left_side, right_side))

        return final_array
    

    def update(self):
        raw_angle, raw_range = self.scan()
        self.results = self.normalize(raw_angle, raw_range)
        return self.results


    def close(self) :
        self.laser.turnOff()
        self.laser.disconnecting()
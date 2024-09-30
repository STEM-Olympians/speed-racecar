import RPi.GPIO as GPIO

class Motor:
   
    def __init__(self, in1_pin, in2_pin, enable_pin, reversed = False):

         # These control direction of motor spin
        self.in1_pin = in1_pin
        self.in2_pin = in2_pin

        # Will send desired pwm signal to motor driver
        self.enable_pin = enable_pin

        self.reversed = reversed
        
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.in1_pin,GPIO.OUT)
        GPIO.setup(self.in2_pin,GPIO.OUT)
        GPIO.setup(self.enable_pin,GPIO.OUT)

        self.power_pwm = GPIO.PWM(self.enable_pin, 100)
        self.power_pwm.start(0)


    '''
        Power from [-1, 1]
        Will round power to 2 decimal places
    '''
    def drive(self, power):

        # Round power to 2 decimal places
        power = round(power, 2)
        
        # Handles direction
        # Spins one way based on power and reversed        
        if(power < 0 and (not self.reversed)) or (power > 0 and (self.reversed)):
            GPIO.output(self.in1_pin,GPIO.HIGH)
            GPIO.output(self.in2_pin,GPIO.LOW)
        elif (power > 0 and (not self.reversed)) or (power < 0 and (self.reversed)):
            GPIO.output(self.in1_pin,GPIO.LOW)
            GPIO.output(self.in2_pin,GPIO.HIGH)
        else:
            print("Edge case in drive?")
            self.stop()

        # We only want magnitude of power
        power_abs = abs(power)

        # Clamped to a max of one
        power_clamped = self.clamp(power_abs, 1)

        # Scaling clamped power to the frequency of the pwm
        power_duty_cycle = power_clamped * 100

        # Driving pwm with new power
        self.power_pwm.ChangeDutyCycle(power_duty_cycle) 


    # Stops the motors
    def stop(self):
        self.power_pwm.stop()


    # Makes sure we don't exceed max magnitude
    def clamp(self, num, max):
        if num > max: 
            return max
        else: 
            return num
import math

from motor import Motor





class Controller :
   
   
   def __init__(self):
      # We need to actually fill these values for real
      print("controller starting")
      self.front_left = Motor(0, 0, 0)
      self.front_right = Motor(0, 0, 0)
      self.back_left = Motor(0, 0, 0)
      self.back_right = Motor(0, 0, 0)


   '''
      Power: [-1, 1] - sets speed of motors 
      Angle: [-90, 90] degrees 
         0 degrees is forward, 
         -90 degrees is left, 
         90 degrees is right
   '''
   def drive(self, power, angle):

      angle = -angle
      
      # First index is left speed, Second index is right speed
      speeds = self.calculateArcadeSpeeds(power, angle)
      
      # The left and right motors will have the same speeds
      self.front_left.drive(speeds[0])
      self.back_left.drive(speeds[0])

      self.front_right.drive(speeds[1])
      self.back_right.drive(speeds[1])


   
   def calculateArcadeSpeeds(self, power, angle):

      #angle -= 90

      # Converting from polar coordinates to cartesian
      xSpeed = power * math.cos(math.radians(angle))
      zRotation = power * math.sin(math.radians(angle))

      # Clamping speeds...we might need deadbanding to go to zero
      xSpeed = self.clamp(xSpeed, -1.0, 1.0)
      zRotation = self.clamp(zRotation, -1.0, 1.0)


      # Representing both speed and direction in a single value
      leftSpeed = xSpeed - zRotation
      rightSpeed = xSpeed + zRotation

     
      greaterInput = max(abs(xSpeed), abs(zRotation))
      lesserInput = min(abs(xSpeed), abs(zRotation))

      # We might need to deadband...
      # This says if either one is zero, then we just don't move
      if (greaterInput == 0.0):
         return [0, 0]
      
      # ...Taking the...average? honestly not sure what this does
      saturatedInput = (greaterInput + lesserInput) / greaterInput
      
      
      leftSpeed /= saturatedInput
      rightSpeed /= saturatedInput

      return [leftSpeed, rightSpeed]
   

   # Makes sure we don't exceed max magnitude
   def clamp(self, num, min, max):
      if num < min:
         return min
      elif num > max: 
         return max
      else: 
         return num
      
   def deadband(self, num, min, max):
      # If in deadband, just go to zero
      # Allows the robot to actually stop
      if num > min and num < max:
         return 0
      
      return num

   




# GPIO.setwarnings(False)

# # Right Motor
# in1 = 17
# in2 = 27
# en_a = 4
# # Left Motor
# in3 = 5
# in4 = 6
# en_b = 13


# GPIO.setmode(GPIO.BCM)
# GPIO.setup(in1,GPIO.OUT)
# GPIO.setup(in2,GPIO.OUT)
# GPIO.setup(en_a,GPIO.OUT)

# GPIO.setup(in3,GPIO.OUT)
# GPIO.setup(in4,GPIO.OUT)
# GPIO.setup(en_b,GPIO.OUT)

# q=GPIO.PWM(en_a,100)
# p=GPIO.PWM(en_b,100)
# p.start(75)
# q.start(75)

# GPIO.output(in1,GPIO.LOW)
# GPIO.output(in2,GPIO.LOW)
# GPIO.output(in4,GPIO.LOW)
# GPIO.output(in3,GPIO.LOW)

# # Wrap main content in a try block so we can  catch the user pressing CTRL-C and run the
# # GPIO cleanup function. This will also prevent the user seeing lots of unnecessary error messages.
# try:
# # Create Infinite loop to read user input
#    while(True):
#       # Get user Input
#       user_input = input()

#       # To see users input
#       # print(user_input)

#       if user_input == 'w':
#          GPIO.output(in1,GPIO.HIGH)
#          GPIO.output(in2,GPIO.LOW)

#          GPIO.output(in4,GPIO.HIGH)
#          GPIO.output(in3,GPIO.LOW)

#          print("Forward")

#       elif user_input == 's':
#          GPIO.output(in1,GPIO.LOW)
#          GPIO.output(in2,GPIO.HIGH)

#          GPIO.output(in4,GPIO.LOW)
#          GPIO.output(in3,GPIO.HIGH)
#          print('Back')

#       elif user_input == 'd':
#          GPIO.output(in1,GPIO.LOW)
#          GPIO.output(in2,GPIO.HIGH)

#          GPIO.output(in4,GPIO.LOW)
#          GPIO.output(in3,GPIO.LOW)
#          print('Right')

#       elif user_input == 'a':
#          GPIO.output(in1,GPIO.HIGH)
#          GPIO.output(in2,GPIO.LOW)

#          GPIO.output(in4,GPIO.LOW)
#          GPIO.output(in3,GPIO.LOW)
#          print('Left')

#       # Press 'c' to exit the script
#       elif user_input == 'c':
#          GPIO.output(in1,GPIO.LOW)
#          GPIO.output(in2,GPIO.LOW)

#          GPIO.output(in4,GPIO.LOW)
#          GPIO.output(in3,GPIO.LOW)
#          print('Stop')

# # If user press CTRL-C
# except KeyboardInterrupt:
#   # Reset GPIO settings
#   GPIO.cleanup()
#   print("GPIO Clean up")


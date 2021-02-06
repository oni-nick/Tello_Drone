from djitellopy import tello
from time import sleep

drone = tello.Tello()
drone.connect()
print(drone.get_battery())
print('this is battery')



#
# drone.takeoff()
# drone.send_rc_control(0, 50, 0, 0)
# sleep(2)
# drone.send_rc_control(0, -50, 0, 0)
# sleep(2)
# # This is python built in function
# # drone.send_rc_control(30, 0, 0, 100)
# # sleep(2)
# drone.send_rc_control(0, 0, 0, 0)
# drone.land()
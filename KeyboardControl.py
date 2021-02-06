import KeyPressModule as kp
from djitellopy import tello
from time import sleep

kp.init()
drone = tello.Tello()
drone.connect()
print(drone.get_battery())


def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50

    if kp.get_key('LEFT'):      # if-elif-elif-elif-elif-elif-elif-elif-elif 에서 수정 1/28/2021 pm 3:24
        lr = -speed
    elif kp.get_key('RIGHT'):
        lr = +speed
    if kp.get_key('UP'):
        fb = +speed
    elif kp.get_key('DOWN'):
        fb = -speed
    if kp.get_key('w'):
        ud = +speed
    elif kp.get_key('s'):
        ud = -speed
    if kp.get_key('a'):
        yv = +speed
    elif kp.get_key('d'):
        yv = -speed
    if kp.get_key('q'):
        drone.land()
    if kp.get_key('e'):
        drone.takeoff()
    return [lr, fb, ud, yv]


while True:
    vals = getKeyboardInput()
    drone.send_rc_control(vals[0], vals[1], vals[2], vals[3])

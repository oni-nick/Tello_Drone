# Just gathering two code : ImageCapture.py + KeyboardControl.py
import KeyPressModule as kp
from djitellopy import tello
import cv2
import time
global img

kp.init()
drone = tello.Tello()
drone.connect()
print(drone.get_battery())

drone.streamon()

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
        time.sleep(3)
    if kp.get_key('e'):
        drone.takeoff()
    if kp.get_key('z'):
        cv2.imwrite(f'Resources/Images/{time.time()}.jpg', img)
        time.sleep(0.5)   # If there is no sleep function, z 한번 누르더라도 사진 20장 넘게 캡쳐됨
    return [lr, fb, ud, yv]


while True:
    vals = getKeyboardInput()
    drone.send_rc_control(vals[0], vals[1], vals[2], vals[3])

    img = drone.get_frame_read().frame
    img = cv2.resize(img, (640, 480))
    cv2.imshow("Image from Drone", img)
    cv2.waitKey(1)

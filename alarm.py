#Import pc uses and interactions 
import threading
import winsound

import cv2
import imutils

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

#camera frame setting
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

_, start_frame = cap.read()

start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)

start_frame = cv2.GaussianBlur(start_frame, (21,21), 0)

alarm = False
alarm_mode = False
alarm_counter = 0

# When the function is activated, it can toggle some action, in this case when there is some moviment on the 'alarm_counter', it toggles the sound system
def beep_alarm():
    global alarm
    for _ in range(5):
        if not alarm_mode:
            break
        print('Alarm')
        winsound.Beep(250, 1000)
    alarm = False

while True:
    _, frame = cap.read()
    frame = imutils.resize(frame, width=500)

    if alarm_mode:
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (5,5), 0)

        dif = cv2.absdiff(frame_bw, start_frame)
        threshhold = cv2.threshold(dif, 25, 255,cv2.THRESH_BINARY)[1]
        start_frame = frame_bw

        if threshhold.sum() > 400:
            alarm_counter += 1
        else:
            if alarm_counter > 0:
                alarm_counter -= 1
        cv2.imshow("CAM", threshhold)
    else:
        cv2.imshow("CAM", frame)

    if alarm_counter > 20:
        if not alarm: 
            alarm = True
            threading.Thread(target=beep_alarm).start()

    key_to_press = cv2.waitKey(30)
    if key_to_press == ord("c"):
        alarm_mode = not alarm_mode
        alarm_counter = 0
    if key_to_press == ord("q"):
        alarm_mode = False
        break

cap.release()
cv2.destroyAllWindows()


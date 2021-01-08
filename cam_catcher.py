import sys
import os
import time
import signal
import numpy as np
import cv2 as cv
import function_module as c_module


def stop_recording(sigum, stack):
    '''Signal handler for SIGALARM.'''
    global is_recording
    global output
    is_recording = False
    output.release()


def stop_program(sigum, stack):
    '''Signal handler for SIGINT.'''
    global is_running
    print('\nStopping the program')
    is_running = False


OUTPUT_DIRECTORY = 'recordings'
MOTION_THRESHOLD = 4500
frame_count = 0
is_running = True
is_recording = False

capture = cv.VideoCapture(0)
capture.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

fourcc = cv.VideoWriter_fourcc(*'DIVX')
output = None

fgbg = cv.createBackgroundSubtractorMOG2(300, 400, True)

c_module.generate_folder(OUTPUT_DIRECTORY)
os.chdir(OUTPUT_DIRECTORY)

signal.signal(signal.SIGINT, stop_program)
signal.signal(signal.SIGALRM, stop_recording)

if not capture.isOpened():
    print('Cannot open the camera')
    sys.exit(1)

time.sleep(6)

print('Starting to watch, press "Ctrl + C" at any time to exit the program')

while is_running:
    ret, frame = capture.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    frame_count += 1
    fgmask = fgbg.apply(frame)
    non_zero_frames = np.count_nonzero(fgmask)

    #If something is moving
    if (not is_recording
        and frame_count > 1
        and non_zero_frames > MOTION_THRESHOLD):
        output = cv.VideoWriter(
            c_module.return_recording_name(), fourcc,
            10.0, (1280, 720))
        is_recording = True
        signal.alarm(6)
        print('Something captured at: '
            + time.strftime("%H:%M:%S", time.strptime(time.ctime()))
            + '.')
        
    elif is_recording:
        output.write(frame)

    if cv.waitKey(1) == ord('q'):
        break

capture.release()
output.release()
cv.destroyAllWindows()

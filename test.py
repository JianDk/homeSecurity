from utils import Stream, motionDetection
import json
from threading import Thread
from time import sleep

#cam parameters
with open('cred.txt','r') as file:
    cred = json.load(file)
    
cam1StreamSub = Stream(camName = 'frontCam1',
                       rtsp = cred['frontCam1']['rtsp_sub'],
                       rtspSource = 'sub',
                       sec_betweenFrame = 0.5)

cam2StreamSub = Stream(camName = 'frontCam2',
                       rtsp = cred['frontCam2']['rtsp_sub'],
                       rtspSource = 'sub',
                       sec_betweenFrame = 0.5) #0.5 sec between frame sampling

detectMotion = motionDetection()


cam1StreamThread = Thread(target = cam1StreamSub.stream)
cam2StreamThread = Thread(target = cam2StreamSub.stream)

motionDetectionThread = Thread(target = detectMotion.continousMotionDetect, args = (80000,))
cam1StreamThread.start()
cam2StreamThread.start()
sleep(10)
motionDetectionThread.start()

sleep(60)
cam1StreamSub.closeStream()
cam2StreamSub.closeStream()
detectMotion.continousMotionDetectSwitch = False
print('complete')

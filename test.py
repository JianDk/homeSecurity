from utils import Stream, motionDetection
import json
from threading import Thread
from time import sleep

#cam parameters
with open('cred.txt','r') as file:
    cred = json.load(file)
    
cam1StreamSub = Stream('frontCam1',
                       cred['frontCam1']['rtsp_sub'],
                       'sub')

detectMotion = motionDetection()


t1 = Thread(target = cam1StreamSub.stream)
t1.start()

sleep(60)
cam1StreamSub.closeStream()
print('complete')

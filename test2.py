from utils import motionDetection
import os
import glob

#Get into the each sub directory and check for motion detection
detectMotion = motionDetection()
status, img1Path, img2Path = detectMotion.getLatestFrames(detectMotion.subStreamDirPaths[0])
print(status)

    
    
    
    
    

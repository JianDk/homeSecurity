import cv2
import datetime
from pathlib import Path
import os
import glob
import time

class Stream:
    def __init__(self, camName, rtsp, rtspSource):
        self.camName = camName
        self.rtsp = rtsp
        self.timeFormat = '%d-%m-%Y %H_%M_%S_%f'
        self.rtspSource = rtspSource
        
        #create output folder if it does not already exist
        self.imgFolder = Path(f'databin/{self.camName}/{rtspSource}/')
        self.imgFolder.mkdir(parents = True, exist_ok = True)
    
    def stream(self):
        self.cap = cv2.VideoCapture(self.rtsp)
        print('stream capture object created')
        self.streamOn = True
        while self.streamOn:
            ret, frame = self.cap.read()
            if ret is False:
                continue
            else:
                #get file name with time stamp
                imgPath = str(self.getFileName())
                cv2.imwrite(imgPath, frame)
    
    def closeStream(self):
        self.streamOn = False
        time.sleep(2)
        self.cap.release()
        print('released capture')
        
    def getFileName(self):
        '''
            Contruct the image file name with time stamp and output as string
        '''
        timeNow = datetime.datetime.now().strftime(self.timeFormat) + '.jpg'
        fileName = self.imgFolder / timeNow
        return fileName

class motionDetection:
    '''
        Goes into the data bin and look up for all the sub folders inside.
        It then get the current time and find the latest two pictures and subtract them from each other.
        If the threshold is above the preset limit an alarm will be raised. 
    '''
    def __init__(self):
        '''
            get all directory paths to sub stream
        '''
        self.subStreamDirPaths = list()
        for dirPath in os.walk('databin'):
            if 'sub' in dirPath[0]:
                self.subStreamDirPaths.append(dirPath[0])
        
        self.continousMotionDetectSwitch = False
    
    def _listTimeSortedFiles(self, dirPath):
        '''
            Given a root dir get a list of strings containing full paths to images
            sorted in modification time
        '''
        list_of_files = glob.glob(dirPath + '/*jpg')
        self.list_of_files = sorted(list_of_files,
                                    key = os.path.getmtime,
                                    reverse = True)
        
    def getLatestFrames(self, dirPath):
        '''
            Given dirPath the method returns two frames. The first being the latest recorded frame
            used for motion detection and the second being the reference frame for motion detection.
            It returns the paths to these two frames
        '''
        self._listTimeSortedFiles(dirPath)
        #If directory is empty
        if not self.list_of_files:
            status = False
            img1Path = False
            img2Path = False
            return status, img1Path, img2Path
        
        img1Path = self.list_of_files[0] #The test frame
        if len(self.list_of_files) >= 5:
            img2Path = self.list_of_files[5]
        elif len(self.list_of_files) <= 2:
            img2Path = self.list_of_files[2]
        else: #There is only one test image in the folder
            status = False
            img1Path = False
            img2Path = False
            return status, img1Path, img2Path
        
        status = True
        return status, img1Path, img2Path

    def motionDetectSingleCam(self, img1Path, img2Path, threshold):
        '''
            Given the path to root stream folder containing the images
            detect movement of the latest image pairs
        '''
        #import images
        img1 = cv2.imread(img1Path)
        img2 = cv2.imread(img2Path)
        #gray scale
        img1gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        img2gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        #Gaussian filter to remove high frequency variation in image
        img1gray = cv2.GaussianBlur(img1gray, (11, 11),0)
        img2gray = cv2.GaussianBlur(img2gray, (11, 11),0)
        #Substract images from each other
        imgdiff = cv2.absdiff(img1gray, img2gray)
        diff_value = cv2.sumElems(imgdiff)
        if diff_value[0] <= threshold:
            return False
        else:
            return True
    
    def continousMotionDetect(self, threshold):
        self.continousMotionDetectSwitch = True
        while self.continousMotionDetectSwitch:
            pass
        
        
        
        
    

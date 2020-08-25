import cv2
import datetime
from pathlib import Path
import os
import glob
import time
import queue

class Stream:
    def __init__(self, camName, rtsp, rtspSource, sec_betweenFrame):
        self.camName = camName
        self.rtsp = rtsp
        self.timeFormat = '%d-%m-%Y %H_%M_%S_%f'
        self.rtspSource = rtspSource
        self.sec_betweenFrame = sec_betweenFrame
        self.queue = queue.Queue()
        
        #create output folder if it does not already exist
        self.imgFolder = Path(f'databin/{self.camName}/{rtspSource}/')
        self.imgFolder.mkdir(parents = True, exist_ok = True)
    
    def stream(self):
        self.cap = cv2.VideoCapture(self.rtsp)
        print(f'stream capture object created for {self.camName}')
        self.streamOn = True
        while self.streamOn:
            try:
                ret, frame = self.cap.read()
            except:
                continue
            
            if ret is False:
                continue
            else:
                #get file name with time stamp
                imgPath = str(self.getFileName())
                #Put it in the queue. In this way the stream will not be interupted
                imgFrame = dict()
                imgFrame['imgPath'] = imgPath
                imgFrame['frame'] = frame
                self.queue.put(imgFrame)
    
    def readStream(self):
        #Get current time
        now = datetime.datetime.now()
        nextFrameTime = now + datetime.timedelta(seconds = self.sec_betweenFrame)
            
        while True:
            
            if self.queue.empty() != True:
                imgFrame = self.queue.get()
                #check if this frame is above the limit
                frameTime = datetime.datetime.strptime(imgFrame['imgPath'][0:-4].split('/')[-1],
                                                       self.timeFormat)
                if frameTime >= nextFrameTime:
                    cv2.imwrite(imgFrame['imgPath'], imgFrame['frame'])
                    #Get current time
                    now = datetime.datetime.now()
                    nextFrameTime = now + datetime.timedelta(seconds = self.sec_betweenFrame)
    
    
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
        if len(self.list_of_files) <= 2:
            img2Path = self.list_of_files[1]
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
        img1gray = cv2.GaussianBlur(img1gray, (31, 31),0)
        img2gray = cv2.GaussianBlur(img2gray, (31, 31),0)
        #Substract images from each other
        imgdiff = cv2.absdiff(img1gray, img2gray)
        diff_value = cv2.sumElems(imgdiff)
        print('diff value ', str(diff_value[0]), img1Path)
        if diff_value[0] <= threshold:
            return False, diff_value[0]
        else:
            return True, diff_value[0]
    
    def continousMotionDetect(self, threshold):
        self.continousMotionDetectSwitch = True
        while self.continousMotionDetectSwitch:
            for subPaths in self.subStreamDirPaths:
                #Get the latest frame from each camera、s sub stream dir
                status, img1, img2 = self.getLatestFrames(subPaths)
                if status is False:
                    continue
            
                #check for motion
                motionStatus, diffValue = self.motionDetectSingleCam(img1, img2, threshold)
                if motionStatus:
                    print('motion detected')

class garbageCollect(motionDetection):
    def __init__(self, daysOld):
        #In this way we get the paths to the camera streams
        super().__init__()
        self.timeFormat = '%d-%m-%Y %H_%M_%S_%f'
        self.removeGarbage(daysOld)
    
    def removeGarbage(self, daysOld):
        daysOld = datetime.datetime.now() - datetime.timedelta(days = daysOld)
        for path in self.subStreamDirPaths:
            #get all file names in directory
            self._listTimeSortedFiles(path)
            for relativeFilePath in self.list_of_files:
                dateTimeObj = self.getDateTimeFromFilePath(relativeFilePath)
                if dateTimeObj < daysOld:
                    os.remove(relativeFilePath)
    
    def getDateTimeFromFilePath(self, relativeFilePath):
        '''
            Given an absolute or relative file path, this method turns
            the date time in file name into a datetime object
        '''
        fileName = os.path.basename(relativeFilePath)
        #Remove the .jpg from filename
        fileName = fileName.replace('.jpg','')
        #Convert to datetime string into datetime object
        dateTimeObj = datetime.datetime.strptime(fileName, self.timeFormat)
        
        return dateTimeObj       
    
        
        
        
        
    

#import os
import cv2
from threading import Thread
from base_camera import BaseCamera
import time
import os

class Video_Thread:

    def __init__(self,file_path):
        self.filename = os.path.basename(file_path)
        self.video = cv2.VideoCapture(self.filename)
        self.VIDEO_FPS = self.video.get(cv2.CAP_PROP_FPS)
        self.frame_interval=(10**9)/self.VIDEO_FPS
        self.video_frame=None 
        self._thread= Thread(name='video_thread',target=self.__play_video)
        self._thread.start()
             
    def __play_video(self):
        time_line = 0
        t0=time.time_ns()
        
        while(self.video.isOpened()):
            
            if((time.time_ns()-t0)<time_line):
                continue

            ret, frame = self.video.read()
            time_line+=self.frame_interval
            
            if ret == False:
                break
            
            self.video_frame=frame

        self.video.release()

class Camera(BaseCamera):
    
    Video=Video_Thread('PCC.mp4')

    @staticmethod
    def frames():
        while True:
            # read current frame
            if Camera.Video.video_frame is None:
                print('continue')
                continue
            img = Camera.Video.video_frame

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()

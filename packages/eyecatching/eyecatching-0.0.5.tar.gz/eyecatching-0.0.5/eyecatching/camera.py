# -*- coding: utf-8 -*-
# Author: Jimei Shen
import cv2
import datetime
import pandas as pd
from eyecatching.eyeDetect import *
from eyecatching.settings import *
import pickle

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def get_frame(self):

        run_time = 180+initTime
        start_time = datetime.datetime.now()
        res = pd.DataFrame(columns=['time', 'x', 'y'])

        if self.video.isOpened():  # try to get the first frame
            (readSuccessful, frame) = self.video.read()
        else:
            raise (Exception("failed to open camera."))
            readSuccessful = False

        while datetime.datetime.now()<= start_time+datetime.timedelta(seconds=run_time) and readSuccessful:
            pupilOffsetXYList = getOffset(frame, allowDebugDisplay=True)
            cv2.waitKey(10)
            print(datetime.datetime.now(), pupilOffsetXYList)
            if pupilOffsetXYList != None:
                res = res.append(pd.DataFrame(
                    {'time': [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")], 'x': [pupilOffsetXYList[0]],
                     'y': [pupilOffsetXYList[1]]})).reset_index(drop=True)

            (readSuccessful, frame) = self.video.read()

        with open('pupilOffsetXYList.pkl', 'wb') as f:
            pickle.dump(res, f)
            f.close()

        ret, jpeg = cv2.imencode('.jpg', frame)

        return jpeg.tobytes()
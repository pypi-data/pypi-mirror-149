# -*- coding: utf-8 -*-
# Author: Jimei Shen
import numpy as np
import cv2

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp', 'jpeg'])


verbose=True
showMainImg=True
BLOWUP_FACTOR = 1 # Resizes image before doing the algorithm. Changing to 2 makes things really slow. So nevermind on this.
RELEVANT_DIST_FOR_CORNER_GRADIENTS = 8*BLOWUP_FACTOR
dilationWidth = 1+2*BLOWUP_FACTOR #must be an odd number
dilationHeight = 1+2*BLOWUP_FACTOR #must be an odd number
dilationKernel = np.ones((dilationHeight,dilationWidth),'uint8')
writeEyeDebugImages = False #enable to export image files showing pupil center probability
eyeCounter = 0
lastCornerProb = np.ones([1,1])


# init the filters we'll use below
haarFaceCascade = cv2.CascadeClassifier("./eyecatching/haarcascades/haarcascade_frontalface_alt.xml")
haarEyeCascade = cv2.CascadeClassifier("./eyecatching/haarcascades/haarcascade_eye.xml")
OffsetRunningAvg = None
PupilSpacingRunningAvg = None

# global stuff for Adam's virtual ref point
#initialize the SURF descriptor
hessianThreshold = 500
nOctaves = 4
nOctaveLayers = 2
extended = True
upright = True
detector = cv2.xfeatures2d.SURF_create(hessianThreshold, nOctaves, nOctaveLayers, extended, upright)
#figure out a way to nearest neighbor map to index
virtualpoint = None
warm=0

useSURFReference = True
RANSAC_MIN_INLIERS = 7

WINDOW_NAME = "EyeTracking"
initTime = 10
plotNumber = 9
# pointPerPlot = 5
plotNColumn = 3

mode = 'test' #deploy
import os
from typing import Dict

import numpy as np
import cv2

from utilities.filehandler.handle_path import get_absolute_path

dirname = os.path.dirname(__file__)
CONFIDENCE_MINIMUM = 0.7

OPENCV_PROTOTXT = get_absolute_path("video_emotion/facial_recognition/deploy"
                                    + ".prototxt.txt")

OPENCV_MODEl = get_absolute_path("video_emotion/facial_recognition/res10_300x"
                                 + "300_ssd_iter_140000_fp16.caffemodel")
# Load model from disk
NET = cv2.dnn.readNetFromCaffe(OPENCV_PROTOTXT, OPENCV_MODEl)

# Various numeral constants
IMAGE_RESIZE = 300
SIZE_CONSTANT = 1.0
RED = 104.0
GREEN = 177.0
BLUE = 123.0


def analyze_video(video_path : str, time_range:int =None) -> Dict:
    """Analyses video finding faces, given videopath and a timerange

    Parameters
    ----------
    video_path : str
        the path of the video
    time_range : int, optional
        the time range in the video you want analyzed
        Given none the entire video will be analyzed

    Returns
    -------
    Dict
        A dictionary of the facetuples found from the frames
    """

    if time_range is not None:
        fro, to = time_range
    cap = cv2.VideoCapture(video_path)
    dict_of_faces = {}
    while cap.isOpened():
        # Get frame from video
        ret, frame = cap.read()

        # Check if we received a frame
        if ret is False:
            break

        # Ignore frames that are not within the given time_range
        if time_range is not None:
            timestamp = cap.get(cv2.CAP_PROP_POS_MSEC)
            if timestamp < fro:
                continue
            elif timestamp > to:
                break

        # Get faces from frame
        faces = analyze_frame(frame)

        # Add found frames to our dictionary
        if len(faces) > 0:
            dict_of_faces[str(int(cap.get(cv2.CAP_PROP_POS_MSEC)))] = faces #save current time rounded
    # Release resources used to open video
    cap.release()

    return dict_of_faces


def analyze_frame(frame) -> [[int, int]]:
    """Analyses a single frame, finding faces returning as a coordinate

    Parameters
    ----------
    frame
        the frame of the video taken from cap.read()

    Returns
    -------
    [[int, int]]
        A list of facetuples that describe the placement of a face in the frame
    """
    
    # Get width and height of frame
    (h, w) = frame.shape[:2]

    # Resize frame and load it as blob
    blob = cv2.dnn.blobFromImage(cv2.resize(frame,
                                            (IMAGE_RESIZE, IMAGE_RESIZE)),
                                            SIZE_CONSTANT,
                                            (IMAGE_RESIZE, IMAGE_RESIZE),
                                            (RED, GREEN, BLUE))

    # Detect faces in the frame and loop over the detections
    NET.setInput(blob)
    detections = NET.forward()

    faces_tuple = []
    for i in range(0, detections.shape[2]):
        # extract the confidence of this specific detection
        confidence = detections[0, 0, i, 2]

        # Ignore detections with confidences lower
        # than the set minimum confidence
        if confidence < CONFIDENCE_MINIMUM:
            continue

        # Get the bounding bounding_box of the detection
        bounding_box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = bounding_box.astype("int")

        # Filter out detections that are outside the image boundary
        # (Not sure why the NN does this)
        if startX >= w or startY >= h or endX <= 0 or endY <= 0:
            continue

        # Fix partly out of bounds detections
        if endX > w:
            endX = w
        if endY > h:
            endY = h
        if startX < 0:
            startX = 0
        if startY < 0:
            startY = 0

        # Remove detections that have an x to y ratio and
        # therefore likely, do not contain a face
        xy_ratio = 1 / (endX - startX) * (endY - startY)
        if xy_ratio < 0.5 or xy_ratio > 2:
            continue

        # Cut face out of frame and add it to our array of faces
        face = frame[int(startY):int(endY), int(startX):int(endX)]
        faces_tuple.append(face)
    return faces_tuple

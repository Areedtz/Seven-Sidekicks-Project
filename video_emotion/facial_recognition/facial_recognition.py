import numpy as np
import cv2
import os





def analyze_video(video_path, time_range=None):
    if time_range is not None:
        fro, to = time_range
    cap = cv2.VideoCapture(video_path)
    dict_of_faces = {}
    i = 1
    while(cap.isOpened()):
        # Get frame from video
        ret, frame = cap.read()

        # Ignore frames that are not within the given time_range
        if time_range is not None:
            timestamp = cap.get(cv2.CAP_PROP_POS_MSEC)
            if timestamp < fro:
                continue
            elif timestamp > to:
                break

        # Check if we received a frame
        if ret is False:
            break

        # Get faces from frame
        faces = analyze_frame(frame)

        # Add found frames to our dictionary
        if len(faces) > 0:
            dict_of_faces[str(i)] = faces
        i += 1
    # Release resources used to open video
    cap.release()

    return dict_of_faces


def analyze_frame(frame):
    dirname = os.path.dirname(__file__)
    opencv_prototxt = os.path.join(
        dirname, "deploy.prototxt.txt")
    opencv_model = os.path.join(
        dirname, "res10_300x300_ssd_iter_140000_fp16.caffemodel")
    CONFIDENCE_MINIMUM = 0.7
    # Load model from disk
    net = cv2.dnn.readNetFromCaffe(opencv_prototxt, opencv_model)

    # Get width and height of frame
    (h, w) = frame.shape[:2]

    # Resize frame and load it as blob
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

    # Detect faces in the frame and
    net.setInput(blob)
    detections = net.forward()

    faces_tuple = []
    # loop over the detections
    for i in range(0, detections.shape[2]):
        # extract the confidence of this specific detection
        confidence = detections[0, 0, i, 2]

        # Ignore detections with confidences lower
        # than the set minimum confidence
        if confidence < CONFIDENCE_MINIMUM:
            continue

        # Get the bounding box of the detection
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")

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

        # Remove detections that have a x to y ratio and
        # therefore likely, do not contain a face
        xy_ratio = 1 / (endX - startX) * (endY - startY)
        if xy_ratio < 0.5 or xy_ratio > 2:
            continue

        # Cut face out of frame and add it to our array of faces
        face = frame[int(startY):int(endY), int(startX):int(endX)]
        faces_tuple.append(face)
    return faces_tuple

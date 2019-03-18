from video_emotion.emotionTagger.face_emotion_extraction import classify_face
from video_emotion.emotionTagger.face_emotion_extraction import get_labels
from video_emotion.emotionTagger.face_emotion_extraction import preprocess_input
import numpy as np
import cv2
import os

def test_angry_face():
    dirname = os.path.abspath(os.path.dirname(__file__))
    filename = os.path.join(
        dirname,
        "test_face_emotion_extraction_data/angry1.png")
    im = cv2.imread(filename)
    faceData = classify_face(im)
    assert len(faceData) == 7
    assert faceData[0] > 0.5

def test_happy_1():
    dirname = os.path.abspath(os.path.dirname(__file__))
    filename = os.path.join(
        dirname,
        "test_face_emotion_extraction_data/happy1.png")
    im = cv2.imread(filename)
    faceData = classify_face(im)
    assert len(faceData) == 7
    assert faceData[3] > 0.5

def test_happy_2():
    dirname = os.path.abspath(os.path.dirname(__file__))
    filename = os.path.join(
        dirname,
        "test_face_emotion_extraction_data/happy2.png")
    im = cv2.imread(filename)
    faceData = classify_face(im)
    assert len(faceData) == 7
    assert faceData[3] > 0.5

def test_happy_3():
    dirname = os.path.abspath(os.path.dirname(__file__))
    filename = os.path.join(
        dirname,
        "test_face_emotion_extraction_data/happy3.png")
    im = cv2.imread(filename)
    faceData = classify_face(im)
    assert len(faceData) == 7
    assert faceData[3] > 0.3
    
def test_neutral_1():
    dirname = os.path.abspath(os.path.dirname(__file__))
    filename = os.path.join(
        dirname,
        "test_face_emotion_extraction_data/neutral1.png")
    im = cv2.imread(filename)
    faceData = classify_face(im)
    assert len(faceData) == 7
    assert faceData[6] > 0.5

def test_get_labels_valid_input():
    dataset_expected = {0:'angry', 1:'disgust', 2:'fear',
                        3:'happy', 4:'sad', 5:'surprise',
                        6:'neutral'}

    result = get_labels('fer2013')

    assert dataset_expected == result

def test_preprocess_input():
    expected = 0.9607843137254901

    tf = np.float32(250) # testing float
    result = preprocess_input(tf, True)

    assert (expected == result)


    
    
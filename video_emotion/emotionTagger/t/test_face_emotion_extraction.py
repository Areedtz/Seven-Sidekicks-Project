from video_emotion.emotionTagger.face_emotion_extraction import classify_face
import cv2
import os
def testAngryFace():
    dirname = os.path.abspath(os.path.dirname(__file__))
    filename = os.path.join(
        dirname,
        "test_face_emotion_extraction_data\\angry1.png")
    im = cv2.imread(filename)
    faceData = classify_face(im)
    assert len(faceData) == 7
    assert faceData[0] > 0.5
def testHappy1():
    dirname = os.path.abspath(os.path.dirname(__file__))
    filename = os.path.join(
        dirname,
        "test_face_emotion_extraction_data\\happy1.png")
    im = cv2.imread(filename)
    faceData = classify_face(im)
    assert len(faceData) == 7
    assert faceData[3] > 0.5
def testHappy2():
    dirname = os.path.abspath(os.path.dirname(__file__))
    filename = os.path.join(
        dirname,
        "test_face_emotion_extraction_data\\happy2.png")
    im = cv2.imread(filename)
    faceData = classify_face(im)
    assert len(faceData) == 7
    assert faceData[3] > 0.5
def testHappy3():
    dirname = os.path.abspath(os.path.dirname(__file__))
    filename = os.path.join(
        dirname,
        "test_face_emotion_extraction_data\\happy3.png")
    im = cv2.imread(filename)
    faceData = classify_face(im)
    assert len(faceData) == 7
    assert faceData[3] > 0.3
def testNeutral1():
    dirname = os.path.abspath(os.path.dirname(__file__))
    filename = os.path.join(
        dirname,
        "test_face_emotion_extraction_data\\neutral1.png")
    im = cv2.imread(filename)
    faceData = classify_face(im)
    assert len(faceData) == 7
    assert faceData[6] > 0.5
    
    
import os

import cv2
import numpy
from keras.models import load_model
import glob


def get_labels():
    return {0: 'angry', 1: 'disgust', 2: 'fear',
            3: 'happy', 4: 'sad', 5: 'surprise',
            6: 'neutral'}


def preprocess_input(x):
    x = x.astype('float32')
    return ((x / 255.0) - 0.5) * 2.0


def classify_faces(faces):
    # parameters for loading data and images
    dirname = os.path.abspath(os.path.dirname(__file__))
    emotion_model_path = os.path.join(
        dirname,
        "models/emotion_model.hdf5")

    # loading models
    emotion_classifier = load_model(emotion_model_path)

    # getting input model shapes for inference
    emotion_target_size = emotion_classifier.input_shape[1:3]
    processed_faces = []
    for face in faces:
        face_grey = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        face_resized = cv2.resize(face_grey, (emotion_target_size))
        face_processed = preprocess_input(face_resized)
        face_expanded_more = numpy.expand_dims(face_processed, -1)
        processed_faces.append(face_expanded_more)

    emotion_prediction = emotion_classifier.predict(numpy.asarray(processed_faces))

    return emotion_prediction
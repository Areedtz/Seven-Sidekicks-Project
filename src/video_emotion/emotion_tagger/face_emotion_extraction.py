from typing import Dict

import cv2
import numpy
from keras.models import load_model
from keras import backend as K

from utilities.filehandler.handle_path import get_absolute_path


def get_labels() -> Dict[int, str]:
    """Get the labels for each argument in the emotion array

    Returns
    -------
    Dict[int, str]
        Returns the labels for each emotion as a dictionary
    """

    return {0: 'angry', 1: 'disgust', 2: 'fear',
            3: 'happy', 4: 'sad', 5: 'surprise',
            6: 'neutral'}


def preprocess_input(x: float) -> float:
    """Prepossesses input

    Parameters
    ----------
    x:float
        The float to be processed, by flooring it to between 0-255


    Returns
    -------
    float
        Returns the input, but preprocessed
    """

    x = x.astype('float32')
    return ((x / 255.0) - 0.5) * 2.0


def classify_faces(faces) -> [[float]]:
    """Classifies the given faces

    Parameters
    ----------
    faces
        The faces to be processed

    Returns
    -------
    array
        Returns a 2d array containing the face emotion data, for each face
        is an array index with a subarray containing the emotions
        indexed like in getlabels
    """

    # parameters for loading data and images
    emotion_model_path = get_absolute_path("video_emotion/" +
                                           "emotion_tagger/" +
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

    emotion_prediction = emotion_classifier.predict(numpy.
                                                    asarray(processed_faces))
    K.clear_session()

    return emotion_prediction

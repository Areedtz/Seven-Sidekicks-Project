import cv2
import os
import numpy as np
from keras.models import load_model
import glob

def get_labels(dataset_name):
    if dataset_name == 'fer2013':
        return {0:'angry', 1:'disgust', 2:'fear',
                3:'happy', 4:'sad', 5:'surprise',
                6:'neutral'}
    else:
        raise Exception('Invalid dataset name')

def preprocess_input(x, v2=True):
    x = x.astype('float32')
    x = x / 255.0
    if v2:
        x = x - 0.5
        x = x * 2.0
    return x
    
def classify_face(face):
    # parameters for loading data and images
    dirname = os.path.abspath(os.path.dirname(__file__))
    emotion_model_path = os.path.join(
        dirname,
        "models/emotion_model.hdf5")
    emotion_labels = get_labels('fer2013')

    # loading models
    emotion_classifier = load_model(emotion_model_path)

    # getting input model shapes for inference
    emotion_target_size = emotion_classifier.input_shape[1:3]

    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    face = cv2.resize(face, (emotion_target_size))
    face = preprocess_input(face, True)
    face = np.expand_dims(face, 0)
    face = np.expand_dims(face, -1)
    
    emotion_prediction = emotion_classifier.predict(face) 
    emotion_probability = np.max(emotion_prediction)
    emotion_label_arg = np.argmax(emotion_prediction)
    emotion_text = emotion_labels[emotion_label_arg]
    
    #print("Mood: [" + str(emotion_labels[0]) + "]     Percentage: [" + str(emotion_prediction[0][0]) + "]")
    #print("Mood: [" + str(emotion_labels[1]) + "]   Percentage: [" + str(emotion_prediction[0][1]) + "]")
    #print("Mood: [" + str(emotion_labels[2]) + "]      Percentage: [" + str(emotion_prediction[0][2]) + "]")
    #print("Mood: [" + str(emotion_labels[3]) + "]     Percentage: [" + str(emotion_prediction[0][3]) + "]")
    #print("Mood: [" + str(emotion_labels[4]) + "]       Percentage: [" + str(emotion_prediction[0][4]) + "]")
    #print("Mood: [" + str(emotion_labels[5]) + "]  Percentage: [" + str(emotion_prediction[0][5]) + "]")
    #print("Mood: [" + str(emotion_labels[6]) + "]   Percentage: [" + str(emotion_prediction[0][6]) + "]")
    return emotion_prediction[0]
    
if __name__ == "__main__":	
    for filename in glob.glob('./faces/*.png'): #assuming gif
        im = cv2.imread(filename)
        classify_face(im)
        print(filename)

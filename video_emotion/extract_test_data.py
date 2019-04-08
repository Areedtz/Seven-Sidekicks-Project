import sys
import os
from os import listdir
from os.path import isfile, join

sys.path.insert(0, os.path.abspath("../"))

import cv2
import numpy as np

from video_emotion.extract_classifier import classify_video
from video_emotion.facial_recognition.facial_recognition import analyze_video
from video_emotion.emotionTagger.face_emotion_extraction import classify_faces

def generate_log_data(interval, emotion_set):
    output_log_data = ""
    output_log_data += "From,To,emotion_angry,emotion_disgust,emotion_fear," \
                        + "emotion_happy,emotion_sad," \
                          "emotion_surprise,emotion_neutral\n"
    for x in range(0, len(emotion_set)):
        output_log_data += str(x * interval) +\
                           "," +\
                           str((x + 1) * interval) +\
                           "," + str(emotion_set[x]["angry"]) +\
                           "," + str(emotion_set[x]["disgust"]) +\
                           "," + str(emotion_set[x]["fear"]) +\
                           "," + str(emotion_set[x]["happy"]) +\
                           "," + str(emotion_set[x]["sad"]) +\
                           "," + str(emotion_set[x]["surprise"]) +\
                           "," + str(emotion_set[x]["neutral"]) +\
                           "\n"


    return output_log_data


def find_emotions_cutoffs(emotions):

    emotions2 = {
        "angry": emotions[0],
        "disgust": emotions[1],
        "fear": emotions[2],
        "happy": emotions[3],
        "sad": emotions[4],
        "surprise": emotions[5],
        "neutral": emotions[6]
    }
    string = ""
    for key,value in emotions2.items():
        if value > 0.3:
            string = string + key + "_" + str(value.round(decimals=2)) + "_"
    return string


def generate_log_data_images_cutoff(video_path, name,folder):
    faces = analyze_video(video_path)
    realFaces = []
    facesDict2 = {}
    i = 0
    for key, value in faces.items():
        for face in value:
            realFaces.append(face)
            facesDict2[str(i)] = key
            i = i + 1
    emotions_data = classify_faces(realFaces)

    for x in range(0, len(faces)):
        cutOff_emotions = find_emotions_cutoffs(emotions_data[x])
        if cutOff_emotions != "":
            cv2.imwrite(folder + name + "_" + facesDict2[str(x)] + "_" + cutOff_emotions + ".jpg", realFaces[x])


if __name__ == "__main__":
    folder = sys.argv[1]
    onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]
    for file in onlyfiles:
        name = file.split('_', 1)[0]
        folder2 = folder + name  + "/"
        if os.path.isdir(folder2) == False:
            os.mkdir(folder2)
        else:
            folder2 = folder + name + "_2" + "/"
            os.mkdir(folder2)
        generate_log_data_images_cutoff(folder + file, name, folder2)

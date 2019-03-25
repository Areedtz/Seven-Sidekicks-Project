import sys


from video_emotion.facial_recognition.facial_recognition import analyze_video
from video_emotion.emotionTagger.face_emotion_extraction import classify_face, classify_faces


def classify_video(video_path, time_range=None):
    faces = analyze_video(video_path, time_range)
    angry_sum = disgust_sum = fear_sum = happy_sum = sad_sum = surprise_sum = neutral_sum = 0.0
    number_of_faces = 0
    realFaces = []
    for key, value in faces.items():
        for face in value:
            realFaces.append(face)
    faces = classify_faces(realFaces)

    for emotions in faces:
        angry_sum += emotions[0]
        disgust_sum += emotions[1]
        fear_sum += emotions[2]
        happy_sum += emotions[3]
        sad_sum += emotions[4]
        surprise_sum += emotions[5]
        neutral_sum += emotions[6]
        number_of_faces = number_of_faces + 1
    return {
        "angry": angry_sum / number_of_faces,
        "disgust": disgust_sum / number_of_faces,
        "fear": fear_sum / number_of_faces,
        "happy": happy_sum / number_of_faces,
        "sad": sad_sum / number_of_faces,
        "surprise": surprise_sum / number_of_faces,
        "neutral": neutral_sum / number_of_faces
    }


if __name__ == "__main__":
    data = classify_video(sys.argv[0], (0, 30000))
    print(str(data))

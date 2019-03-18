from facial_recognition.facial_recognition import analyze_video
from emotionTagger.face_emotion_extraction import classify_face

def classify_video(video_path,time_range=None):
    faces = analyze_video(video_path,time_range)
    angry_sum = disgust_sum = fear_sum = happy_sum = sad_sum = surprise_sum = neutral_sum = 0.0
    for key,value in faces.items():
        for face in value:
            emotions = classify_face(face)
            angry_sum += emotions[0]
            disgust_sum += emotions[1]
            fear_sum += emotions[2]
            happy_sum += emotions[3]
            sad_sum += emotions[4]
            surprise_sum += emotions[5]
            neutral_sum += emotions[6]
    numberOfFaces = len(faces)
    return {
        "angry":angry_sum/numberOfFaces,
        "disgust":disgust_sum/numberOfFaces,
        "fear":fear_sum/numberOfFaces,
        "happy":happy_sum/numberOfFaces,
        "sad":sad_sum/numberOfFaces,
        "surprise":surprise_sum/numberOfFaces,
        "neutral":neutral_sum/numberOfFaces
    }

if __name__ == "__main__":
    data = classify_video('./Fun_at_a_Fair.mp4')
    print(data)
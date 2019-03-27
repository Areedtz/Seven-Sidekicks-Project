import sys

from video_emotion.extract_classifier import classify_video


def generate_log_data(interval, emotion_set):
    output_log_data = ""
    output_log_data += "From,To,emotion_disgust,emotion_fear," \
                        + "emotion_happy,emotion_sad," \
                          "emotion_surprise,emotion_neutral\n"
    for x in range(0, len(emotion_set)):
        output_log_data += str(x * interval) +\
                           "," +\
                           str((x + 1) * interval) +\
                           "," + str(emotion_set[x-1]["angry"]) +\
                           "," + str(emotion_set[x-1]["disgust"]) +\
                           "," + str(emotion_set[x-1]["fear"]) +\
                           "," + str(emotion_set[x-1]["happy"]) +\
                           "," + str(emotion_set[x-1]["sad"]) +\
                           "," + str(emotion_set[x-1]["surprise"]) +\
                           "," + str(emotion_set[x-1]["neutral"]) +\
                           "\n"
    return output_log_data


if __name__ == "__main__":
    filename = sys.argv[1]
    data = []
    for x in range(0, 30000, 5000):
        data.append(classify_video(filename, (x, x+5000)))

    formatted_data = generate_log_data(5000, data)

    f = open(filename.replace(".mp4", ".csv"), "+w")
    f.write(formatted_data)
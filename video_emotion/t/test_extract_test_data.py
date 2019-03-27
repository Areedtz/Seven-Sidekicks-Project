from video_emotion.extract_test_data import generate_log_data


def test_generate_log_data_formats_as_expected():
    data = generate_log_data(500, [{"happy": 10, "angry": 10, "fear": 10,
                                    "disgust": 5, "sad": 5, "surprise": 5,
                                    "neutral": 5}])
    assert data == ("From,To,emotion_disgust,"
                    + "emotion_fear,emotion_happy,emotion_sad,"
                    + "emotion_surprise,emotion_neutral\n"
                    + "0,500,10,5,10,10,5,5,5\n")

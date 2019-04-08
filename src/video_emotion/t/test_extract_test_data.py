from video_emotion.extract_test_data import generate_log_data

def test_generate_log_data_formats_as_expected():
    data = generate_log_data(500, [{"happy": 10, "angry": 10, "fear": 10}])
    assert data == "From,To,Emotions\n0,500,{\'happy\': 10, \'angry\': 10, "\
                   + "\'fear\': 10}\n"

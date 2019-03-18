import os
import cv2

from video_emotion.extract_classifier import classify_video

def test_of_emotion_range_in_given_video_snippet():
    dirname = os.path.dirname(__file__)
    test_filename = os.path.join(
        dirname, "test_video_emotion/Fun_at_a_Fair.mp4")

    output_dict = classify_video(test_filename, (3000, 4000))
    
    assert len(output_dict) != 0

    assert output_dict['angry'] < 0.009
    assert output_dict['disgust'] < 0.001
    assert output_dict['fear'] < 0.029
    assert output_dict['happy'] > 0.7
    assert output_dict['sad'] < 0.045
    assert output_dict['suprise'] < 0.015
    assert output_dict['neutral'] > 0.15
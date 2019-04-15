import json

from video_emotion.extract_classifier import classify_video


def process_data_and_extract_emotions(video_id, video_path, time_range, output_file_path):
    data = classify_video(video_path, (time_range['From'], time_range['To']))

    with open(output_file_path + '/' + video_id + '.json', 'w') as outfile:
        json.dump(data, outfile)

    return False

import os

from classification.extractor.low_level_data_extractor import make_low_level_data_file
from utilities.filehandler.handle_path import get_absolute_path

def test_song_data_extraction():
    filename = get_absolute_path("classification/extractor/t/test_extractor/"
                                 + "8376-1-1 Demolition_Man_"
                                   "proud_music_preview.wav")

    dirname = os.path.abspath(os.path.dirname(__file__))
    output_filename = os.path.join(dirname, "8376-1-1_output.json")

    make_low_level_data_file(filename, output_filename)

    assert os.path.isfile(output_filename)
    assert os.stat(output_filename) != 0

    os.remove(output_filename)

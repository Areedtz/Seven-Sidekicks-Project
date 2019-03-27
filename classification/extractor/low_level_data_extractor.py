import sys
import subprocess

from utilities.filehandler.handle_path import get_absolute_path

def make_low_level_data_file(filename, output_file_path):
    extractor_path = get_absolute_path("utilities/ressources/extractors/streaming_extractor_music")

    command = '{} {} {}'.format(extractor_path, filename, output_file_path)

    subprocess.run(command, shell=True)


if __name__ == "__main__":
    filename, output_filename = sys.argv[1], sys.argv[2]

    make_low_level_data_file(filename, output_filename)

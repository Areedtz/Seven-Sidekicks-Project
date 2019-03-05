import os
import sys
import subprocess


def make_high_level_data_file(filename, output_file_path):
    dirname = os.path.abspath(os.path.dirname(__file__))
    extractor_path = os.path.join(
        dirname,
        './extractors/streaming_extractor_music')

    command = '{} {} {}'.format(extractor_path, filename, output_file_path)

    subprocess.run(command, shell=True)


if __name__ == "__main__":
    filename, output_filename = sys.argv[1], sys.argv[2]

    make_high_level_data_file(filename, output_filename)

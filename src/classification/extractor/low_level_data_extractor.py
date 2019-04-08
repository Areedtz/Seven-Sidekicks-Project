import sys
import subprocess
import os

sys.path.insert(0, os.path.abspath("../"))
import utilities.filehandler.handle_path as path_handler 

def make_low_level_data_file(filename, output_file_path):
    extractor_path = path_handler.get_absolute_path("utilities/ressources"
                                       + "/extractors/"
                                       + "streaming_extractor_music")

    command = '{} {} {}'.format(extractor_path, filename, output_file_path)

    subprocess.run(command, shell=True)

    print("I am inside the extractor")


if __name__ == "__main__":
    filename, output_filename = sys.argv[1], sys.argv[2]

    make_low_level_data_file(filename, output_filename)

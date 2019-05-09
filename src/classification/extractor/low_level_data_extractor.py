#!/usr/local/bin/python3.6
import sys
import subprocess
import os

import utilities.filehandler.handle_path as path_handler


def make_low_level_data_file(filename: str, output_file_path: str):
    """Extracts the lowlevel datafile from a given song file 
    and outputs in the given outputfile

    Parameters
    ----------
    filename
        single song file path
    output_file_path
        output path of the lowlevel datafile
    """
    
    extractor_path = path_handler.get_absolute_path("utilities/ressources"
                                                    + "/extractors/"
                                                    + "streaming_extractor_music")

    command = '{} {} {}'.format(extractor_path, filename, output_file_path)

    subprocess.run(command, shell=True)
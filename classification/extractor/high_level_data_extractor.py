import os
import sys

def get_high_level_data(filename, output_file_path):
    dataFileName = output_file_path
    
    dirname = os.path.dirname(__file__)
    extractor_path = os.path.join(
                                dirname, 
                                './extractors/streaming_extractor_music')
    command = '{} {} {}'.format(extractor_path, filename, dataFileName)
    
    os.system(command)

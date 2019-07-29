import subprocess

from utilities.filehandler.handle_path import get_absolute_path


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

    # Escape characters that the command line can't handle normally
    fixed_filename = filename.replace(" ", r"\ ") \
                             .replace("(", r"\(") \
                             .replace(")", r"\)") \
                             .replace("&", r"\&") \
                             .replace("'", r"\'")

    extractor_path = get_absolute_path("utilities/ressources" +
                                       "/extractors/" +
                                       "streaming_extractor_music")

    command = '{} {} {}'.format(
        extractor_path, fixed_filename, output_file_path)

    subprocess.run(command, shell=True)

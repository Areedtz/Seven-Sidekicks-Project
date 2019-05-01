import os

import yaml


def load_config():
    configpath = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "..", "config.yml"))
    with open(configpath, "r") as file:
        cfg = yaml.load(file, Loader=yaml.FullLoader)

    return cfg

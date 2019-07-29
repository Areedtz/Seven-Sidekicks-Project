from typing import Dict, Any
import os

import yaml


def load_config() -> Dict[str, Any]:
    """Loads the project's config file and returns it as an dictionary

    Returns
    -------
    dict
        A dictionary with the configs from the config file
    """

    configpath = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "..", "config.yml"))

    with open(configpath, "r") as file:
        cfg = yaml.load(file, Loader=yaml.FullLoader)

    return cfg

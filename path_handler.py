"""Module for handling paths."""

import os
import yaml


def get_input_dir(source_file: str = "settings.yml") -> str:
    """Returns the input directory from the source file."""

    if not os.path.exists(source_file):
        raise FileNotFoundError("Source file not found.")

    with open(source_file, "r", encoding="utf-8") as stream:
        data = yaml.safe_load(stream)

    return os.path.join(data["FabSim3"]["location"], data["FabSim3"]["input_path"])

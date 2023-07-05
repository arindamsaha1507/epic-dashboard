"""Module for parsing data for the application."""

import os
import pandas as pd


def get_location_from_filename(filename: str) -> str:
    """Returns the location from the filename."""

    if not os.path.isfile(filename):
        raise ValueError("Filename must be a file.")

    if not filename.endswith(".csv"):
        raise ValueError("Filename must be a CSV file.")

    if not filename.split(".")[0].endswith("_buildings"):
        raise ValueError("Filename must end with '_buildings'.")

    raw = filename.split(".")[0][:-10]

    return raw.replace("_", " ").title()


def get_location_from_directory(directory: str) -> str:
    """Returns the location from the directory."""

    # if not os.path.isdir(directory):
    #     raise ValueError("{} must be a directory.".format(directory))

    return directory.replace("_", " ").title()


def get_location(source: str) -> str:
    """Returns the location from the filename or directory."""

    if "." in source:
        return get_location_from_filename(source)

    return get_location_from_directory(source)


def get_location_list(data_dir: str) -> list[str]:
    """Returns a list of locations."""

    contents = os.listdir(data_dir)

    locations = list(map(get_location, contents))
    locations.sort()
    locations.insert(0, "None")

    return locations


def location_to_filename(location: str) -> str:
    """Returns the filename for the location."""

    return location.lower().replace(" ", "_") + "_buildings.csv"


def location_to_directory(location: str) -> str:
    """Returns the directory for the location."""

    return location.lower().replace(" ", "_")


def get_data(location: str, data_dir: str) -> pd.DataFrame:
    """Returns the data for the location."""

    filename = location_to_filename(location)
    directoryname = location_to_directory(location)
    filepath = os.path.join(data_dir, f"{directoryname}/covid_data", filename)

    data = pd.read_csv(filepath)
    data.columns = ["Type", "Longitude", "Latitude", "Area"]
    data["Type"] = data["Type"].apply(lambda x: x.title())
    data = data.sort_values("Type")

    return data


def summarize_data(data: pd.DataFrame) -> pd.DataFrame:
    """Returns a summary of the data."""

    summary = data.groupby("Type").agg({"Area": ["sum", "count"]})

    summary = pd.DataFrame(summary.reset_index())
    summary = summary[summary["Type"] != "House"]
    summary = pd.DataFrame(summary.reset_index(drop=True))
    summary.columns = ["Type", "Area", "Count"]
    summary["Mean Area"] = summary["Area"] / summary["Count"]

    return summary


if __name__ == "__main__":
    fabsim_dir = "/home/arindam/FabSim3/plugins/FabCovid19/config_files/"
    print(get_location_list(fabsim_dir))

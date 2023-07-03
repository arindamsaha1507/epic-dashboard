"""Module for parsing data for the application."""

import os
import pandas as pd


def get_location_from_filename(filename: str) -> str:
    """Returns the location from the filename."""

    if not filename.endswith(".csv"):
        raise ValueError("Filename must be a CSV file.")

    if not filename.split(".")[0].endswith("_buildings"):
        raise ValueError("Filename must end with '_buildings'.")

    raw = filename.split(".")[0][:-10]

    return raw.replace("_", " ").title()


def get_location_list(data_dir: str) -> list[str]:
    """Returns a list of locations."""

    files = os.listdir(data_dir)

    locations = list(map(get_location_from_filename, files))
    locations.sort()
    locations.insert(0, "None")

    return locations


def location_to_filename(location: str) -> str:
    """Returns the filename for the location."""

    return location.lower().replace(" ", "_") + "_buildings.csv"


def get_data(location: str, data_dir: str) -> pd.DataFrame:
    """Returns the data for the location."""

    filename = location_to_filename(location)
    filepath = os.path.join(data_dir, filename)

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

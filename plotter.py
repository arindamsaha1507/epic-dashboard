"""All plotting functions for the project."""

from functools import partial

import plotly.express as px
import plotly.graph_objects as go

from pandas import DataFrame


COLORS = [
    "#1f77b4",  # muted blue
    "#ff7f0e",  # safety orange
    "#2ca02c",  # cooked asparagus green
    "#d62728",  # brick red
    "#9467bd",  # muted purple
    "#8c564b",  # chestnut brown
    "#e377c2",  # raspberry yogurt pink
    "#7f7f7f",  # middle gray
    "#bcbd22",  # curry yellow-green
    "#17becf",  # blue-teal
]


def create_color_map(data: DataFrame, column: str) -> dict[str, str]:
    """Creates a color map for the data."""

    if column not in data.columns:
        raise ValueError(f"Column '{column}' not in data.")

    values = data[column].unique().tolist()

    if column == "Type" and "House" not in values:
        values.append("House")

    values.sort()
    colors = COLORS[: len(values)]

    return dict(zip(values, colors))


def create_summary_plots(summary: DataFrame, size: int = 500) -> dict[str, go.Figure]:
    """Creates summary plots for the data."""

    columns = summary.columns
    if "Type" not in columns:
        raise ValueError("Summary must have a 'Type' column.")
    columns = columns.drop("Type")

    cdm = create_color_map(summary, "Type")

    charter = partial(
        px.pie,
        data_frame=summary,
        names="Type",
        width=size,
        height=size,
        color="Type",
        color_discrete_map=cdm,
    )
    figs = list(map(lambda x: charter(values=x), columns))

    for fig in figs:
        fig.update_layout(showlegend=False)
        fig.update_layout(autosize=True)
        fig.update_traces(textinfo="label", textposition="inside")

    figs = dict(zip(columns, figs))

    return figs


def create_map(data: DataFrame) -> go.Figure:
    """Creates a map for the data."""

    essential = ["Type", "Longitude", "Latitude"]

    if not all(x in data.columns for x in essential):
        raise ValueError(f"Data must have columns {essential}.")

    cdm = create_color_map(data, "Type")

    fig = px.scatter_mapbox(
        data,
        lat="Latitude",
        lon="Longitude",
        color="Type",
        zoom=10,
        color_discrete_map=cdm,
    )
    fig.update_layout(mapbox_style="open-street-map")

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig

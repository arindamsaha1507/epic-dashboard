"""All plotting functions for the project."""

import plotly.express as px
import plotly.graph_objects as go
from pandas import DataFrame


def create_summary_plots(summary: DataFrame, size: int = 500) -> dict[str, go.Figure]:
    """Creates summary plots for the data."""

    columns = summary.columns
    if "Type" not in columns:
        raise ValueError("Summary must have a 'Type' column.")
    columns = columns.drop("Type")

    figs = list(
        map(
            lambda x: px.pie(summary, values=x, names="Type", width=size, height=size),
            columns,
        )
    )

    for fig in figs:
        fig.update_layout(showlegend=False)
        fig.update_layout(autosize=True)
        fig.update_traces(textinfo="label", textposition="inside")

    figs = dict(zip(columns, figs))

    return figs

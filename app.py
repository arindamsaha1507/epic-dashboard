"""Creates a map application using Streamlit."""

# pylint: disable=import-error

import streamlit as st
import pandas as pd
import plotly.express as px


import data_parser as dp


def main() -> None:
    """The main function of the app."""

    st.title("Map Application")

    st.markdown(
        """
        This application is a demo of how to create an interactive map using
        Streamlit. The map is created using Plotly Express.
        """
    )

    st.sidebar.title("Region Selection")
    st.sidebar.markdown(
        """
        The maps are created using data from OpenStreetMaps.
        """
    )

    data_dir = "data/"

    locations = dp.get_location_list(data_dir)

    location = st.sidebar.selectbox("Select a location", locations)

    if location and location != "None":
        data = dp.get_data(location, data_dir)

        summary = dp.summarize_data(data)

        st.dataframe(summary, use_container_width=True)

        fig = px.pie(summary, values="Area", names="Type")
        st.plotly_chart(fig)

        fig = px.pie(summary, values="Mean Area", names="Type")
        st.plotly_chart(fig)

        fig = px.scatter_mapbox(
            data, lat="Latitude", lon="Longitude", color="Type", zoom=10
        )
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        st.plotly_chart(fig)


if __name__ == "__main__":
    main()

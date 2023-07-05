"""Creates a map application using Streamlit."""


import streamlit as st

import data_parser as dp
import plotter as pl


def main() -> None:
    """The main function of the app."""

    st.set_page_config(layout="wide")

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

        figures = pl.create_summary_plots(summary)
        titles = list(figures.keys())
        plots = list(figures.values())

        with st.container():
            st.markdown("---")
            st.markdown("## Summary Plots")
            st.markdown("---")
            columns = st.columns(len(figures))
            for index, column in enumerate(columns):
                with column:
                    st.markdown(f"## {titles[index]}")
                    st.plotly_chart(plots[index])

        with st.container():
            st.markdown("---")
            st.markdown("## Map")
            st.markdown("---")

            fig = pl.create_map(data)
            st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()

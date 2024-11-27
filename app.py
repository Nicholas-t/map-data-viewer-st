import streamlit as st
import pandas as pd
import pydeck


HS_PORTAL_ID = st.secrets["HS_PORTAL_ID"]
# Title of the app
st.set_page_config(page_title="Map viewer", layout="wide")
# Upload CSV file
uploaded_file = st.file_uploader("Upload a CSV file with lat and long columns", type=["csv"])

if uploaded_file is not None:
    # Read the CSV file
    data = pd.read_csv(uploaded_file)

    # Check if the necessary columns exist
    if 'latitude' in data.columns and 'longitude' in data.columns:
        # Initialize the viewport state
        map_container, company_data_container = st.columns(2)
        with map_container:
            point_layer = pydeck.Layer(
                "ScatterplotLayer",
                data=data,
                id="data",
                get_position=["longitude", "latitude"],
                get_color="[255, 75, 75]",
                pickable=True,
                auto_highlight=True,
                get_radius=250
            )
            view_state = pydeck.ViewState(
                latitude=data["latitude"].mean(), longitude=data["longitude"].mean(), controller=True, zoom=10, pitch=0
            )

            chart = pydeck.Deck(
                point_layer,
                initial_view_state=view_state,
                tooltip={"html": "{Company name}<br> {Street Address}, {City}<br>(Click to view)"},
            )
            event = st.pydeck_chart(chart, on_select="rerun", selection_mode="multi-object")
        with company_data_container:
            if "data" in event.selection["objects"]:
                st.markdown("## {} company data".format(event.selection["objects"]["data"][0]["Company name"]))
                for key, label in event.selection["objects"]["data"][0].items():
                    st.markdown(f"{key} : {label}")
                st.link_button("Open in HS", f"https://app.hubspot.com/contacts/{HS_PORTAL_ID}/record/0-2/{event.selection['objects']['data'][0]['Record ID']}")
    else:
        st.error("The uploaded file must contain 'latitude' and 'longitude' columns.")
else:
    st.info("Upload a CSV file to get started.")

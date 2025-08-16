import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.title("Item Data")

# Connect to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Dropdown for worksheet
choice = st.selectbox(
    "Select one:",
    ["Please select one", "Air filter", "Blower motor", "Condensor coil", "Compressor","Evaporator coil","Expension valve","Filter dryer receiver","radiator motor"]
)

if choice == "Please select one":
    st.markdown("Please select the item to see the data...")
else:
    # Read data from sheet
    existing_data = conn.read(worksheet=choice)
    existing_data = existing_data.dropna(how="all").reset_index(drop=True)

    # Editable table with ability to add/delete rows
    edited_data = st.data_editor(
        existing_data,
        hide_index=True,
        num_rows="dynamic"  # allows adding/removing rows
    )

    # Save changes back to sheet
    if st.button("Save Changes"):
        # Drop fully empty rows (if user leaves them blank)
        cleaned_data = edited_data.dropna(how="all").reset_index(drop=True)

        # Update entire worksheet with the cleaned data
        conn.update(data=cleaned_data, worksheet=choice)
        st.success("Sheet updated successfully!")

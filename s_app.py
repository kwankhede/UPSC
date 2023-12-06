import streamlit as st
import plotly.express as px
import pandas as pd

# Load data
excel_file_path = "upsc_2022.xlsx"
upsc_2022_df = pd.DataFrame()

sheets_dict = pd.read_excel(excel_file_path, sheet_name=None)

for sheet_name, sheet_df in sheets_dict.items():
    sheet_df = sheet_df[
        ["Roll_No", "Name", "Comm", "PwBD", "W_total", "PT_Marks", "F_Total", "Rank"]
    ]
    upsc_2022_df = pd.concat([upsc_2022_df, sheet_df], ignore_index=True)

upsc_2022_df["Comm"] = upsc_2022_df["Comm"].fillna("Open")
upsc_2022_df["PwBD"] = upsc_2022_df["PwBD"].fillna("No")

# Streamlit app
st.title(" UPSC : Interview vs Written Marks by Categories")

# Dropdown for filtering by 'Comm'
selected_comm = st.multiselect(
    "Select Comm Category", upsc_2022_df["Comm"].unique(), upsc_2022_df["Comm"].unique()
)

# Slider for filtering by 'W_total'
w_total_range = st.slider(
    "Select range for written marks",
    upsc_2022_df["W_total"].min(),
    upsc_2022_df["W_total"].max(),
    (upsc_2022_df["W_total"].min(), upsc_2022_df["W_total"].max()),
    step=25,
)

# Range slider for number of rows to display
rows_range = st.slider(
    "Select range for UPSC All India Ranks to display",
    1,
    upsc_2022_df.shape[0],
    (1, upsc_2022_df.shape[0]),
    step=25,
)

# Filter the DataFrame based on user input
filtered_df = upsc_2022_df[
    (upsc_2022_df["Comm"].isin(selected_comm))
    & (upsc_2022_df["W_total"] >= w_total_range[0])
    & (upsc_2022_df["W_total"] <= w_total_range[1])
    & (upsc_2022_df.index >= rows_range[0] - 1)  # Adjust the start index
    & (upsc_2022_df.index < rows_range[1])
]

# Scatter plot
scatter_fig = px.scatter(
    filtered_df,
    x="W_total",  # Corrected column name
    y="PT_Marks",  # Corrected column name
    color="Comm",
    title="Interview vs Written Marks in UPSC by Categories",
)

# Display the scatter plot
st.plotly_chart(scatter_fig)

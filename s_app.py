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

# Use light24 colors for each 'Comm' category
comm_colors = px.colors.qualitative.Pastel1[:5]

# Streamlit app
st.title("UPSC Result 2022 : Data Analysis ")
st.header("Interview vs Written Marks by Categories")

# Default values for range and all data
default_comm = upsc_2022_df["Comm"].unique()
default_w_total_range = (upsc_2022_df["W_total"].min(), upsc_2022_df["W_total"].max())
default_rows_range = (1, upsc_2022_df.shape[0])

# Dropdown for filtering by 'Comm'
selected_comm = st.multiselect(
    "Select Comm Category", upsc_2022_df["Comm"].unique(), default_comm
)

# Slider for filtering by 'W_total'
w_total_range = st.slider(
    "Select range for written marks",
    upsc_2022_df["W_total"].min(),
    upsc_2022_df["W_total"].max(),
    default_w_total_range,
    step=25,
)

# Range slider for number of rows to display
rows_range = st.slider(
    "Select range for UPSC All India Ranks to display",
    1,
    upsc_2022_df.shape[0],
    default_rows_range,
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

# Scatter plot with custom color mapping
scatter_fig = px.scatter(
    filtered_df,
    x="W_total",
    y="PT_Marks",
    color="Comm",
    color_discrete_map=dict(zip(selected_comm, comm_colors)),
    title="Interview vs Written Marks in UPSC by Categories",
)

# Add x and y axis labels
scatter_fig.update_layout(xaxis_title="Written Marks", yaxis_title="Interview Marks")

# Pie chart
comm_counts = filtered_df["Comm"].value_counts()
pie_fig = px.pie(
    comm_counts,
    names=comm_counts.index,
    values=comm_counts.values,
    hole=0.3,
    color=comm_counts.index,
    color_discrete_map=dict(zip(comm_counts.index, comm_colors)),
)
pie_fig.update_traces(
    hoverinfo="label+percent", textinfo="percent+label", textfont_size=15
)

# Box plot
box_fig = px.box(
    filtered_df,
    x="PT_Marks",
    y="Comm",
    color="Comm",
    labels={"PT_Marks": "Interview Marks", "Comm": "Categories"},
    category_orders={"Comm": selected_comm},
    color_discrete_map=dict(zip(selected_comm, comm_colors)),
)
# Add vertical line for full data median
full_data_median = upsc_2022_df["PT_Marks"].median()
box_fig.update_layout(
    shapes=[
        {
            "type": "line",
            "x0": full_data_median,
            "x1": full_data_median,
            "y0": -0.5,
            "y1": len(selected_comm) - 0.5,
            "xref": "x",
            "yref": "y",
            "line": dict(color="red", width=2),
        },
    ],
    annotations=[
        dict(
            x=1.15,
            y=0.5,
            xref="paper",
            yref="paper",
            showarrow=False,
            align="left",
            font=dict(size=12),
        )
    ],
)

# Display the charts
st.plotly_chart(scatter_fig)
st.header("Distribution of Categories")
st.plotly_chart(pie_fig)
st.header("Distribution of Categories Wise Interview Marks")
st.plotly_chart(box_fig)

# Add another blank row with an empty string
st.markdown("")
st.markdown("")
st.markdown("")
st.markdown("")
st.markdown("")

# Add a link to the data source
st.markdown("[Data Source: UPSC CSM 2022 Marks Recorded Candidates](https://upsc.gov.in/sites/default/files/CSM_2022_MksRcdCandts_Eng_24052023.pdf)")



 

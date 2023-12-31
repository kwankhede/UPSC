import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff
import numpy as np
import pandas as pd
import plotly.graph_objects as go

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

# Fixed colors for each 'Comm' category
comm_colors = {
    "OBC": "rgb(251,180,174)",  # Pastel1[0]
    "SC": "rgb(179,205, 227)",  # Pastel1[1]
    "EWS": "rgb(204,235, 197)",  # Pastel1[2]
    "ST": "rgb(222, 203, 228)",  # Pastel1[3]
    "Open": "rgb(254, 217, 166)",  # Pastel1[4]
}

# Streamlit app
st.title("UPSC Result 2022: Data Analysis ")
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

# Range slider for the number of rows to display
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

# Scatter plot with fixed color mapping
scatter_fig = px.scatter(
    filtered_df,
    x="W_total",
    y="PT_Marks",
    color="Comm",
    color_discrete_map=comm_colors,
    title="Interview vs Written Marks in UPSC by Categories",
)

# Add x and y-axis labels
scatter_fig.update_layout(xaxis_title="Written Marks", yaxis_title="Interview Marks")

# Pie chart
comm_counts = filtered_df["Comm"].value_counts()
pie_fig = px.pie(
    comm_counts,
    names=comm_counts.index,
    values=comm_counts.values,
    hole=0.3,
    color=comm_counts.index,
    color_discrete_map=comm_colors,
    title="Interview vs Written Marks in UPSC by Categories",
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
    color_discrete_map=comm_colors,
    title="Distribution of Categories Wise Interview Marks",
)
# Add a vertical line for the full data median
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

# Box plot for 'W_total'
box_fig_w_total = px.box(
    filtered_df,
    x="W_total",
    y="Comm",
    color="Comm",
    labels={"W_total": "Written Marks", "Comm": "Categories"},
    category_orders={"Comm": selected_comm},
    color_discrete_map=comm_colors,
    title="Distribution of Categories Wise Written Marks",
)
# Add a vertical line for the full data median
full_data_median_w_total = upsc_2022_df["W_total"].median()
box_fig_w_total.update_layout(
    shapes=[
        {
            "type": "line",
            "x0": full_data_median_w_total,
            "x1": full_data_median_w_total,
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
st.plotly_chart(pie_fig)
st.plotly_chart(box_fig)
st.plotly_chart(box_fig_w_total)

# Add histograms and rug plots for 'PT_Marks' and 'W_total'
fig_pt_marks = go.Figure()

for comm, color in comm_colors.items():
    hist_data_comm = filtered_df[filtered_df["Comm"] == comm]["PT_Marks"]
    fig_pt_marks.add_trace(
        go.Histogram(
            x=hist_data_comm,
            histnorm="probability",
            name=comm,
            marker_color=color,
            opacity=0.7,
        )
    )

fig_pt_marks.update_layout(
    barmode="overlay",
    title_text="Distribution of Interview Marks",
    xaxis_title="Interview Marks",
    yaxis_title="Probability",
)

st.plotly_chart(fig_pt_marks)

fig_w_total = go.Figure()

for comm, color in comm_colors.items():
    hist_data_comm = filtered_df[filtered_df["Comm"] == comm]["W_total"]
    fig_w_total.add_trace(
        go.Histogram(
            x=hist_data_comm,
            histnorm="probability",
            name=comm,
            marker_color=color,
            opacity=0.7,
        )
    )

fig_w_total.update_layout(
    barmode="overlay",
    title_text="Distribution of Written Marks",
    xaxis_title="Written Marks",
    yaxis_title="Probability",
)

st.plotly_chart(fig_w_total)

# Add another blank row with an empty string
st.markdown("")
st.markdown("")
st.markdown("")
st.markdown("")
st.markdown("")

# Add a link to the data source
st.markdown(
    "[Data Source: UPSC CSM 2022 Marks Recorded Candidates](https://upsc.gov.in/sites/default/files/CSM_2022_MksRcdCandts_Eng_24052023.pdf)"
)

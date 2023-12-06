import dash
from dash import dcc, html
from dash.dependencies import Input, Output
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

# Create Dash app
app = dash.Dash(__name__)

# Define layout of the app
app.layout = html.Div(
    [
        html.H1("Interview vs Written by Categories"),
        html.Label("Dropdown for filtering by 'Comm' - Select categories"),
        # Dropdown for filtering by 'Comm'
        dcc.Dropdown(
            id="comm-dropdown",
            options=[
                {"label": comm, "value": comm} for comm in upsc_2022_df["Comm"].unique()
            ],
            multi=True,
            value=upsc_2022_df["Comm"].unique(),
            style={"width": "50%"},
            placeholder="Select Comm Category",
        ),
        html.Label(" Written marks"),
        # Slider for filtering by 'W_total'
        dcc.RangeSlider(
            id="w-total-slider",
            min=upsc_2022_df["W_total"].min(),
            max=upsc_2022_df["W_total"].max(),
            step=50,  # Increase the step to 25
            marks={
                i: str(i)
                for i in range(
                    upsc_2022_df["W_total"].min(), upsc_2022_df["W_total"].max() + 1, 50
                )
            },
            value=[upsc_2022_df["W_total"].min(), upsc_2022_df["W_total"].max()],
        ),
        html.Label("UPSC Rank from 1 to 926 "),
        # Slider for number of rows to display
        dcc.Slider(
            id="rows-slider",
            min=1,
            max=upsc_2022_df.shape[0],
            step=50,
            marks={i: str(i) for i in range(1, upsc_2022_df.shape[0] + 1, 50)},
            value=100,
        ),
        dcc.Graph(id="scatter-plot"),
    ]
)


# Callback to update the scatter plot based on the selected number of rows, filtered 'Comm', and 'W_total' range
@app.callback(
    Output("scatter-plot", "figure"),
    [
        Input("rows-slider", "value"),
        Input("comm-dropdown", "value"),
        Input("w-total-slider", "value"),
    ],
)
def update_scatter_plot(selected_rows, selected_comm, selected_w_total_range):
    filtered_df = upsc_2022_df[
        (upsc_2022_df["Comm"].isin(selected_comm))
        & (upsc_2022_df["W_total"] >= selected_w_total_range[0])
        & (upsc_2022_df["W_total"] <= selected_w_total_range[1])
    ].iloc[:selected_rows]

    scatter_fig = px.scatter(
        filtered_df,
        x="W_total",
        y="PT_Marks",
        color="Comm",
        title="Interview vs Written by Categories",
    )

    return scatter_fig


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)

import dash                     # pip install dash
from dash.dependencies import Input, Output, State
from dash import dcc
from dash import html
import plotly.express as px     # pip install plotly==5.2.2

import pandas as pd             # pip install pandas

df = pd.read_csv("sales.csv")
df["Time"] = pd.to_datetime(df["Time"])
df["Time"] = df["Time"].dt.hour
print(df.head())


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1("Analytics for Arada sales  (Dash Plotly)", style={"textAlign": "center"}),
    html.Hr(),
    html.P("Choose item of interest:"),
    html.Div(html.Div([
        dcc.Dropdown(id='Item name', clearable=False,
                     value="Item",
                     options=[{'label': x, 'value': x} for x in
                              df["Item name"].unique()]),
    ],className="two columns"),className="row"),

    html.Div(id="output-div", children=[]),
])


@app.callback(Output(component_id="output-div", component_property="children"),
              Input(component_id="Item name", component_property="value"),)
def make_graphs(Item_chosen):
    # HISTOGRAM
    df_hist = df[df["Item name"] == Item_chosen]
    fig_hist = px.histogram(df_hist, x="Item quantity")
    fig_hist.update_xaxes(categoryorder="total descending")

    # STRIP CHART
    fig_strip = px.strip(df_hist, x="Territory", y="Item quantity")

    # SUNBURST
    df_sburst = df.dropna(subset=['Territory'])
    df_sburst = df_sburst[df_sburst["Item name"].isin(["Apple", "PG", "Lime"])]
    fig_sunburst = px.sunburst(df_sburst, path=["Item quantity", "Area"], color="Time")

    # Empirical Cumulative Distribution
    df_ecdf = df[df["Item name"].isin(["Apple", "PG", "Lime"])]
    fig_ecdf = px.ecdf(df_ecdf, x="Date", color="Time")

    # LINE CHART
    df_line = df.sort_values(by=["Time"], ascending=True)
    df_line = df_line.groupby(
        ["Territory", "Item name"]).size().reset_index(name="count")
    fig_line = px.line(df_line, x="Item name", y="count",
                       color="Item name", markers=True)

    return [
        html.Div([
            html.Div([dcc.Graph(figure=fig_hist)], className="six columns"),
            html.Div([dcc.Graph(figure=fig_strip)], className="six columns"),
        ], className="row"),
        html.H2("All Items", style={"textAlign": "center"}),
        html.Hr(),
        html.Div([
            html.Div([dcc.Graph(figure=fig_sunburst)], className="six columns"),
            html.Div([dcc.Graph(figure=fig_ecdf)], className="six columns"),
        ], className="row"),
        html.Div([
            html.Div([dcc.Graph(figure=fig_line)], className="twelve columns"),
        ], className="row"),
    ]


if __name__ == '__main__':
    app.run_server(debug=True)

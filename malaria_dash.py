import pandas as pd
from dash import dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

df = pd.read_csv('./1_data/incedenceOfMalaria.csv')
df.rename(columns={'Location':'Country','Period':'Year','First Tooltip':'Incidence per 1000 population'},
         index={'Sudan (until 2011)':'Sudan'}, inplace=True)

df.sort_values(['Country', 'Year'],
              ascending = [True, True], inplace = True)

animations = {
    'Choropleth': px.choropleth(
        df, locations="Country", locationmode="country names", animation_frame="Year", 
        color="Incidence per 1000 population", hover_name="Country", color_continuous_scale="Reds",
        height=600),
    'line': px.line(
        df, x='Year', y='Incidence per 1000 population',color='Country',
        animation_frame="Year"
    )
}

app = dash.Dash(__name__)


app.layout = html.Div([
    html.P("Select an animation:"),
    dcc.RadioItems(
        id='selection',
        options=[{'label': x, 'value': x} for x in animations],
        value='Choropleth'
    ),
    dcc.Graph(id="graph"),
])


@app.callback(
    Output("graph", "figure"), 
    [Input("selection", "value")])
def display_animated_graph(s):
    return animations[s]


if __name__ == "__main__":
    app.run_server(debug=True)
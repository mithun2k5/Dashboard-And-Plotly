import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

df = pd.read_csv("/Users/mitalukd/Desktop/Performance/Sample1.csv")

app = dash.Dash()
# https://dash.plot.ly/dash-core-components/dropdown
# We need to construct a dictionary of dropdown values for the years
image_options = []
for image in df['Image_Name'].unique():
    image_options.append({'label':str(image),'value':image})

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Dropdown(id='image-picker',options=image_options,value="Mitun")
])

@app.callback(Output('graph-with-slider', 'figure'),
              [Input('image-picker', 'value')])
def update_figure(selected_image):
    df1 = df[df["Image_Name"] == selected_image]
    df2 = df1[["Features","Device1 Mbps","Device2 Mbps","Device3 Mbps","Device4 Mbps"]]
    df2.set_index("Features",inplace=True)
    traces = []

    traces.append(go.Scatter(
        x = df2.index,
        y = df2[col],
        mode = 'markers+lines',
        opacity=0.75,
        name = col
        ) for col in df2.columns
        )

    return {
        'data': traces,
        'layout': go.Layout(
            title="Performance Report",
                xaxis=dict(title = 'Features'),
                yaxis=dict(title = 'Throughput in Mbps'),
                hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server(port=8300,host="0.0.0.0")

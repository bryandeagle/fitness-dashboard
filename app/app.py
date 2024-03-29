import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px
from health import Health
import plotly.io as pio
import pandas as pd
import json
import dash
import os


PERIOD = '6m'  # 1d, 7d, 30d, 1w, 1m, 3m, 6m, 1y, or max
RESOURCES = ['body/bmi',
             'body/fat',
             'body/weight',
             'activities/tracker/calories',
             'activities/tracker/distance']


# Default plot template
template = dict(
    layout=go.Layout(
        dict(
            height=400,
            margin=dict(l=20, r=20, b=20, t=40),
            dragmode=False,
            hovermode='closest',
            bargap=0.25,
            plot_bgcolor='#F9F9F9',
            paper_bgcolor='#F9F9F9',
            title=dict(
                x=0.5,
                xanchor='center',
                yanchor='top'
            ),
            xaxis=dict(
                zeroline=False,
                automargin=True,
                showgrid=False,
                showline=True,
                linewidth=1,
                linecolor='black',
                dtick='D1',
                tickformat='%m/%d'
            ),
            yaxis=dict(
                zeroline=False,
                showline=False,
                automargin=True,
                gridcolor='#e9e9e9'
            )
        )
    )
)


def layout():
    """ Layout of the Dashboard """
    global health

    df = pd.DataFrame(health.get_data(RESOURCES[0], PERIOD))
    for resource in RESOURCES[1:]:
        metric = pd.DataFrame(health.get_data(resource, PERIOD))
        df = df.merge(metric, on='Date')
    df['Delta'] = df['Weight'].diff(1)

    return html.Div([
        dbc.Container([
            dbc.Row(
                dbc.Col(
                    html.Div(
                        html.H4(
                            '2021 Fitness Dashboard'
                        ),
                        className='card p-3'
                    ),
                    width=12
                ),
                className='mb-2'
            ),
            dbc.Row([
                dbc.Col(
                    html.Div(
                        dcc.Graph(
                            id='body-weight',
                            figure=px.line(df.tail(30),
                                           x='Date',
                                           y='Weight',
                                           title='Body Weight (Lbs)',
                                           line_shape='spline')
                        ),
                        className='card p-2'
                    ),
                    className='mb-2',
                    width=12
                )],
                className='gx-2'
            ),
            dbc.Row([
                dbc.Col(
                    html.Div(
                        dcc.Graph(
                            id='weight-delta',
                            figure=px.bar(df.tail(30),
                                          x='Date',
                                          y='Delta',
                                          title='Daily Weight Loss/Gain (Lbs)')
                        ),
                        className='card p-2'
                    ),
                    className='mb-2',
                    width=12
                )
                ],
                className='gx-2'
            )]
        )]
    )


# Default template from utils/template.py
pio.templates['dashboard'] = template
pio.templates.default = 'dashboard'

# Load config file an initialize Health API
env_var = os.getenv('FITNESS_CONFIG')
if env_var:
    config_path = env_var
else:
    config_path = os.path.dirname(os.path.abspath(__file__))

with open('config.json', 'rt') as f:
    health = Health(**json.load(f))

# Use Bootstrap 5 and initiatlize app
bootstrap = 'https://stackpath.bootstrapcdn.com/bootstrap/5.0.0-alpha2/css/bootstrap.min.css'
open_sans = 'https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400&display=swap'
app = dash.Dash(__name__, external_stylesheets=[bootstrap, open_sans])
app.layout = layout


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=False)

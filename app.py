import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import pandas as pd
import dash

import datetime
import numpy as np

bootstrap = 'https://stackpath.bootstrapcdn.com/bootstrap/5.0.0-alpha2/css/bootstrap.min.css'

app = dash.Dash(__name__, external_stylesheets=[bootstrap])


def get_data():
    df = pd.DataFrame({
        'Weight': [180,
                   177,
                   179,
                   176,
                   178,
                   175,
                   174,
                   -172],
        'Date': ['11/23/2020',
                 '11/24/2020',
                 '11/25/2020',
                 '11/26/2020',
                 '11/27/2020',
                 '11/28/2020',
                 '11/29/2020',
                 '11/30/2020'],
    })
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    return df


# Default template for graphs
pio.templates['dashboard'] = dict(
    layout=go.Layout(
        dict(
            height=250,
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
pio.templates.default = 'dashboard'


def weight(data):
    return px.line(data,
                   x='Date',
                   y='Weight',
                   title='Weight Over Time',
                   line_shape='spline')


def delta(data):
    return px.bar(data,
                  x='Date',
                  y='Weight',
                  title='Daily Weight Loss/Gain')


def table(data):
    df_table = data[['Date', 'Weight']].head(4)
    return dbc.Table.from_dataframe(df_table,  # pylint: disable=no-member
                                    striped=False,
                                    bordered=True,
                                    hover=True)


def calendar():
    year = datetime.datetime.now().year

    d1 = datetime.date(year, 1, 1)
    d2 = datetime.date(year, 5, 30)
    delta = d2 - d1

    dates_in_year = [d1 + datetime.timedelta(i) for i in range(delta.days+1)]
    weekdays_in_year = [i.weekday() for i in dates_in_year]
    weeknumber_of_dates = [int(i.strftime('%V')) for i in dates_in_year]
    z = np.random.uniform(low=0.0, high=1.0, size=(len(dates_in_year,)))
    text = [str(i) for i in dates_in_year]

    data = [
        go.Heatmap(
            y=weekdays_in_year,
            x=weeknumber_of_dates,
            z=z,
            text=text,
            hoverinfo='text',
            xgap=4,
            ygap=4,
            colorscale='Viridis'
        )
    ]
    layout = go.Layout(
        title='Exercise Calendar',
        yaxis=dict(
            showgrid=False,
            tickmode='array',
            ticktext=['Sun', 'Sat', 'Fri', 'Thu', 'Wed', 'Tue', 'Mon'],
            tickvals=[0, 1, 2, 3, 4, 5, 6],
        ),
        xaxis=dict(
            title='Week Number',
            tickmode='array',
            tickvals=[],
            showline=False
        )
    )
    heatmap = go.Figure(data=data, layout=layout)
    return heatmap


def serve_layout():
    df = get_data()
    return html.Div([
        dbc.Container([
            dbc.Row(
                dbc.Col(
                    html.Div(
                        html.H3(
                            '🏃‍♂️ Fitness Challenge 2021 Dashboard 🏋️‍♂️'
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
                            id='line-graph',
                            figure=weight(df)
                        ),
                        className='card p-2'
                    ),
                    lg=6,
                    className='mb-2'
                ),
                dbc.Col(
                    html.Div(
                        dcc.Graph(
                            id='bar-graph',
                            figure=delta(df)
                        ),
                        className='card p-2'
                    ),
                    lg=6,
                    className='mb-2'
                )
                ],
                className='gx-2'
            ),
            dbc.Row([
                dbc.Col(
                    html.Div(
                        dcc.Graph(
                            id='three-graph',
                            figure=calendar()
                        ),
                        className='card p-2'
                    ),
                    lg=6,
                    className='mb-2'
                ),
                dbc.Col(
                    html.Div(
                        html.Div([
                            html.Div(
                                'Most Recent Entries',
                                className='mb-1'
                            ),
                            table(df)],
                            className='table'
                        ),
                        className='card p-2'
                    ),
                    lg=6,
                    className='mb-2'
                )],
                className='gx-2'
            )]
        )]
    )

app.layout = serve_layout

if __name__ == '__main__':
    app.run_server(debug=True)

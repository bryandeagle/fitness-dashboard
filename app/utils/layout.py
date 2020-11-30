import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px
from . import get_data


def calendar(data, column, title):
    """A heatmap calendar showing exercise"""
    data = data.tail(7 * 15)  # Get last 15 weeks
    x = [int(i.strftime('%V')) for i in data.index]
    y = [i.weekday() for i in data.index]
    text = [i.strftime('%m/%d') for i in data.index]
    data = [
        go.Heatmap(
            x=x,
            y=y,
            z=data[column],
            text=text,
            hoverinfo='text',
            xgap=4,
            ygap=4,
            colorscale='Viridis'
        )
    ]
    layout = go.Layout(
        title=title,
        yaxis=dict(
            showgrid=False,
            tickmode='array',
            ticktext=['Sun', 'Sat', 'Fri', 'Thu', 'Wed', 'Tue', 'Mon'],
            tickvals=[0, 1, 2, 3, 4, 5, 6],
        ),
        xaxis=dict(
            title='',
            tickmode='array',
            tickvals=[],
            showline=False
        )
    )
    heatmap = go.Figure(data=data, layout=layout)
    return heatmap


def layout():
    df = get_data()
    return html.Div([
        dbc.Container([
            dbc.Row(
                dbc.Col(
                    html.Div(
                        html.H4(
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
                            id='body-weight',
                            figure=px.line(df.tail(30),
                                           x=df.tail(30).index,
                                           y='Weight',
                                           title='Body Weight (Lbs)',
                                           line_shape='spline')
                        ),
                        className='card p-2'
                    ),
                    lg=6,
                    className='mb-2'
                ),
                dbc.Col(
                    html.Div(
                        dcc.Graph(
                            id='weight-delta',
                            figure=px.bar(df.tail(30),
                                          x=df.tail(30).index,
                                          y='Delta',
                                          title='Daily Weight Loss/Gain (Lbs)')
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
                            id='body-fat',
                            figure=px.line(df.tail(30),
                                           x=df.tail(30).index,
                                           y='Fat',
                                           title='Body Fat (%)',
                                           line_shape='spline')
                        ),
                        className='card p-2'
                    ),
                    lg=6,
                    className='mb-2'
                ),
                dbc.Col(
                    html.Div(
                        dcc.Graph(
                            id='body-bmi',
                            figure=px.line(df.tail(30),
                                           x=df.tail(30).index,
                                           y='Bmi',
                                           title='Body Mass Index (BMI)',
                                           line_shape='spline')
                        ),
                        className='card p-2'
                    ),
                    lg=6,
                    className='mb-2'
                )],
                className='gx-2'
            ),
            dbc.Row([
                dbc.Col(
                    html.Div(
                        dcc.Graph(
                            id='calories',
                            figure=calendar(data=df,
                                            column='Calories',
                                            title='Daily Calories Burned')
                        ),
                        className='card p-2'
                    ),
                    lg=6,
                    className='mb-2'
                ),
                dbc.Col(
                    html.Div(
                        dcc.Graph(
                            id='distance',
                            figure=calendar(data=df,
                                            column='Distance',
                                            title='Daily Distance (miles)')
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

from utils import line, bar, calendar
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from . import get_data


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
                            figure=line(data=df,
                                        column='Weight',
                                        title='Body Weight (Lbs)')
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
                            figure=bar(data=df,
                                       column='Delta',
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
                            figure=line(data=df,
                                        column='Fat',
                                        title='Body Fat (%)')
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
                            figure=line(data=df,
                                        column='Bmi',
                                        title='Body Mass Index (BMI)')
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

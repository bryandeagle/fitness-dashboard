
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import pandas as pd
import dash_table
import dash


bootstrap = 'https://stackpath.bootstrapcdn.com/bootstrap/5.0.0-alpha2/css/bootstrap.min.css'

app = dash.Dash(__name__, external_stylesheets=[bootstrap])

# Dummy data
df = pd.DataFrame({
    'Weight': [180,
               177,
               179,
               176,
               178,
               175,
               174,
               172],
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


# Default template for graphs
pio.templates['dashboard'] = dict(
    layout=go.Layout(
        dict(
            height=250,
            margin=dict(l=20, r=20, b=20, t=20),
            hovermode="closest",
            bargap=0.25,
            plot_bgcolor="#F9F9F9",
            paper_bgcolor="#F9F9F9",
            title=dict(
                x=0.5,
                xanchor='center',
                yanchor='top'
            ),
            xaxis=dict(
                automargin=True,
                showgrid=False,
                showline=False,
                dtick='D1',
                tickformat='%m/%d'
            ),
            yaxis=dict(
                automargin=True,
                gridcolor='#e9e9e9'
            )
        )
    )
)
pio.templates.default = 'dashboard'

# Create line graph figure
fig_line = px.line(df,
                   x='Date',
                   y='Weight',
                   title='Weight Over Time',
                   line_shape='spline')

# Create bar graph figure
fig_bar = px.bar(df,
                 x='Date',
                 y='Weight',
                 title='Daily Weight Loss/Gain')
fig_bar.update_layout({'xaxis': {'showline': False}})

# Create bar graph figure
fig_the = px.bar(df,
                 x='Date',
                 y='Weight',
                 title='Daily Weight Loss/Gain')

# Create bootstrap table in bottom-right
table = dbc.Table.from_dataframe(df[['Date', 'Weight']].head(4),
                                 striped=False,
                                 bordered=True,
                                 hover=True)  #pylint: disable=E1101

# Layout
app.layout = html.Div([
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
                        figure=fig_line
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
                        figure=fig_bar
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
                        figure=fig_the
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
                        table],
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

if __name__ == '__main__':
    app.run_server(debug=True)

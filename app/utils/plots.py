import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import datetime


def line(data, column, title):
    """A line chart showing historical weight"""
    data = data.tail(30)
    return px.line(data,
                   x=data.index,
                   y=column,
                   title=title,
                   line_shape='spline')


def bar(data, column, title):
    """A bar chart showing daily weight deltas"""
    data = data.tail(30)
    return px.bar(data,
                  x=data.index,
                  y=column,
                  title=title)


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

from utils import template, layout
import plotly.io as pio
import json
import dash
import os

# Default template from utils/template.py
pio.templates['dashboard'] = template
pio.templates.default = 'dashboard'

# Use Bootstrap 5 and initiatlize app
bootstrap = 'https://stackpath.bootstrapcdn.com/bootstrap/5.0.0-alpha2/css/bootstrap.min.css'
app = dash.Dash(__name__, external_stylesheets=[bootstrap])
app.layout = layout


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=False)

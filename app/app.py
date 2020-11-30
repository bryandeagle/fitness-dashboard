from utils import template, layout, get_oauth_token
import plotly.io as pio
import dash
import os

# Default template from utils/template.py
pio.templates['dashboard'] = template
pio.templates.default = 'dashboard'

# Use Bootstrap 5 and initiatlize app
bootstrap = 'https://stackpath.bootstrapcdn.com/bootstrap/5.0.0-alpha2/css/bootstrap.min.css'


if __name__ == '__main__':
    get_oauth_token()
    app = dash.Dash(__name__, external_stylesheets=[bootstrap])
    app.layout = layout
    app.run_server(host='0.0.0.0', debug=False)

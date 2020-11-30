from oauthlib.oauth2.rfc6749.errors import MismatchingStateError
from oauthlib.oauth2.rfc6749.errors import MissingTokenError
from urllib.parse import urlparse
from datetime import timedelta
from fitbit.api import Fitbit
from datetime import datetime
import pandas as pd
import webbrowser
import threading
import traceback
import cherrypy
import fitbit
import json
import json
import sys


RESOURCES = ['body/bmi',
             'body/fat',
             'body/weight',
             'activities/tracker/calories',
             'activities/tracker/distance']


class OAuth:
    def __init__(self, client_id, client_secret,
                 redirect_uri='http://127.0.0.1:8080/'):
        """ Initialize the FitbitOauth2Client """
        self.success_html = """
            <h1>You are now authorized to access the Fitbit API!</h1>
            <br/><h3>You can close this window</h3>"""
        self.failure_html = """
            <h1>ERROR: %s</h1><br/><h3>You can close this window</h3>%s"""
        self.fitbit = Fitbit(
            client_id,
            client_secret,
            redirect_uri=redirect_uri,
            timeout=10,
        )
        self.redirect_uri = redirect_uri
        url, _ = self.fitbit.client.authorize_token_url()
        # Open the web browser in a new thread for command-line browser support
        threading.Timer(1, webbrowser.open, args=(url,)).start()

        # Same with redirect_uri hostname and port.
        urlparams = urlparse(self.redirect_uri)
        cherrypy.config.update({'server.socket_host': urlparams.hostname,
                                'server.socket_port': urlparams.port})
        cherrypy.quickstart(self)

    @cherrypy.expose
    def index(self, state, code=None, error=None):
        """
        Receive a Fitbit response containing a verification code. Use the code
        to fetch the access_token.
        """
        error = None
        if code:
            try:
                self.fitbit.client.fetch_access_token(code)
            except MissingTokenError:
                error = self._fmt_failure(
                    'Missing access token parameter.</br>Please check that '
                    'you are using the correct client_secret')
            except MismatchingStateError:
                error = self._fmt_failure('CSRF Warning! Mismatching state')
        else:
            error = self._fmt_failure('Unknown error while authenticating')
        # Use a thread to shutdown cherrypy so we can return HTML first
        self._shutdown_cherrypy()
        return error if error else self.success_html

    def _fmt_failure(self, message):
        tb = traceback.format_tb(sys.exc_info()[2])
        tb_html = '<pre>%s</pre>' % ('\n'.join(tb)) if tb else ''
        return self.failure_html % (message, tb_html)

    @staticmethod
    def _shutdown_cherrypy():
        """ Shutdown cherrypy in one second, if it's running """
        if cherrypy.engine.state == cherrypy.engine.states.STARTED:
            threading.Timer(1, cherrypy.engine.exit).start()


class Fit:
    """Nice class to organize Fitbit API"""
    def __init__(self):
        self.period = '6m'

        # Open self.secrets JSON file
        with open('secrets.json', 'rt') as f:
            self.secrets = json.load(f)

        # Get a token from oauth as a global
        server = OAuth(client_id=self.secrets['client_id'],
                       client_secret=self.secrets['client_secret'])
        self.token = server.fitbit.client.session.token

        print('TOKEN={}'.format(self.token))

        # Initialize Fitbit client
        self.client = fitbit.Fitbit(client_secret=self.secrets['client_secret'],
                                    refresh_token=self.token['refresh_token'],
                                    access_token=self.token['access_token'],
                                    expires_at=self.token['expires_at'],
                                    client_id=self.secrets['client_id'],
                                    redirect_uri='http://localhost/',
                                    refresh_cb=self.refresh_cb)

    def refresh_cb(self, new_token):
        self.token = new_token

    def get_resource(self, resource):
        results = self.client.time_series(resource=resource,
                                          user_id=self.secrets['user_id'],
                                          base_date='today',
                                          period=self.period)

        # Get key name and proper name from resource
        key = resource.replace('/', '-')
        name = resource.split('/')[-1].capitalize()

        data = [{'Date': datetime.strptime(x['dateTime'], '%Y-%m-%d'),
                 name: float(x['value'])} for x in results[key]]

        # Convert list of dicts into dataframe
        df = pd.DataFrame(data)
        df.columns = ['Date', name]
        df.set_index('Date', inplace=True)
        return df


fitbit_api = Fit()


def get_data():
    df = fitbit_api.get_resource(RESOURCES[0])
    for resource in RESOURCES[1:]:
        df = df.merge(fitbit_api.get_resource(resource), on='Date')
    df['Delta'] = df['Weight'].diff(1)
    return df

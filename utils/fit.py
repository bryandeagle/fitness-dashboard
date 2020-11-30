from datetime import timedelta
from datetime import datetime
import pandas as pd
import fitbit
import json


class Fit:
    """Nice class to organize Fitbit API"""
    def __init__(self):
        self.period = '6m'
        with open('secrets.json', 'rt') as f:
            self.secrets = json.load(f)

        self.client = fitbit.Fitbit(client_secret=self.secrets['client_secret'],
                                    refresh_token=self.secrets['refresh_token'],
                                    access_token=self.secrets['access_token'],
                                    expires_at=self.secrets['expires_at'],
                                    client_id=self.secrets['client_id'],
                                    redirect_uri='http://localhost/',
                                    refresh_cb=self.refresh_cb)

    @staticmethod
    def refresh_cb(new_secrets):
        """Callback function to refresh data in secrets.json"""
        with open('secrets.json', 'rt') as f:
            old_secrets = json.load(f)
        with open('secrets.json', 'wt') as f:
            json.dump({**old_secrets, **new_secrets}, f)

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


def get_data():
    resources = ['body/bmi',
                 'body/fat',
                 'body/weight',
                 'activities/tracker/calories',
                 'activities/tracker/distance']
    fit = Fit()
    df = fit.get_resource(resources[0])
    for resource in resources[1:]:
        df = df.merge(fit.get_resource(resource), on='Date')
    df['Delta'] = df['Weight'].diff(1)
    return df


if __name__ == '__main__':
    x = get_data()

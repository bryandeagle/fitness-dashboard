import urllib
import fitbit
import json
import os


def refresh_cb(token):
    with open('secrets.json', 'rt') as f:
        secrets = json.load(f)
    with open('secrets.json', 'wt') as f:
        json.dump({**secrets, **token}, f)


if __name__ == '__main__':

    with open('secrets.json', 'rt') as f:
        secrets = json.load(f)

    # Initialize fitbit API
    client = fitbit.Fitbit(client_secret=secrets['client_secret'],
                           refresh_token=secrets['refresh_token'],
                           access_token=secrets['access_token'],
                           expires_at=secrets['expires_at'],
                           client_id=secrets['client_id'],
                           redirect_uri='http://localhost/',
                           refresh_cb=refresh_cb)

    # Get current weight from fitbit API
    weight = client.get_bodyweight(user_id=secrets['user_id'], period='1m')
    print(weight)

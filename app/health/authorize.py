from fitbit.api import Fitbit
import json


if __name__ == '__main__':

    with open('config.json', 'rt') as f:
        config = json.load(f)

    fitbit = Fitbit(client_id=config['client_id'],
                    client_secret=config['client_secret'],
                    redirect_uri=config['redirect_uri'],
                    timeout=10)

    url, _ = fitbit.client.authorize_token_url()
    url = url.replace('response_type=code', 'response_type=token')
    print('Please visit: {}'.format(url))
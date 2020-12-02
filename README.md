Fitness Dashboard
=================

A light-weight dashboard project for displaying Fitbit data

## Installing

From the `app` directory:

```sh
if [ ! -d "env" ]; then
        python3 -m venv env
fi
source env/bin/activate
pip install -r requirements.txt
```

## Deploying

Create a `secrets.json` in the working directory with the following format:

```json
{
    "user_id": "",
    "client_id": "",
    "client_secret": ""
}
```

Get your Fitbit `user_id` by going to [fitbit.com](https://fitbit.com/) and clicking your profile in the top-right and looking at the url. it should be of the format `https://fitbit.com/user/<user_id>`. Get your app's `client_id` and `client_secret` from [dev.fitbit.com/apps](https://dev.fitbit.com/apps).

When the app first runs, it uses the `client_id` and `client_secret` to obtain an *access token* via Oauth2. You have to authorize the app to access your user account by going to the link printed to the console.

## Contributing

The `requirements.txt` file was generated using the following command:

```
pipreqs --encoding=utf8 --force
```

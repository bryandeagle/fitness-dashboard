Dashboard
=========

A light-weight dashboard project for displaying Fitbit data

## Installing

```
if [ ! -d "env" ]; then
        python3 -m venv env
fi
source env/bin/activate
pip install -r requirements.txt
```

## Deploying

Create `secrets.json` with the following format

```
{
    "user_id": "",
    "client_id": "",
    "client_secret": ""
}
```

Get your Fitbit `user_id` by going to [fitbit.com](https://fitbit.com/) and clicking your profile in the top-right and looking at the url. it should be of the format `https://fitbit.com/user/<user_id>`. Get your app's `client_id` and `client_secret` from [dev.fitbit.com/apps](https://dev.fitbit.com/apps).

Then authorize the app by running `get-token.py`. It will add more necessary keys to the `secrets.json` file.

## Contributing

The `requirements.txt` file was generated using the following command:

```
pipreqs --encoding=utf8 --force
```
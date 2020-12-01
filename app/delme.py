from health import Health
import json


if __name__ == '__main__':
    with open('secrets.json', 'rt') as f:
        health = Health(**json.load(f))

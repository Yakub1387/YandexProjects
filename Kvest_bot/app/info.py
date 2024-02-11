import json


def get_data():
    with open('data.json', 'r') as f:
        try:
            r = json.load(f)
        except json.JSONDecodeError:
            r = {}
        return r


def push_data(a):
    with open('data.json', 'w') as f:
        json.dump(a, f)


def result():
    pass
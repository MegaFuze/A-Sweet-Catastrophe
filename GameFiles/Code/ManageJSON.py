import json

def import_json(path):
    with open(path) as file:
        data = json.load(file)
    return data
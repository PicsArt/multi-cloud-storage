import json


def populate_store(data_path, store):

    with open(data_path) as f:
        data = json.load(f)

    for entry in data:
        store.insert(entry)

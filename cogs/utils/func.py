import json
def read(file):
    with open(file=file, mode='r') as f:
        data = json.load(f)
        return data

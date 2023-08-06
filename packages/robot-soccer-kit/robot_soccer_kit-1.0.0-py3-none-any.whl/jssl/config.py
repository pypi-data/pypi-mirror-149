import os
import json

config = {}
filename = 'config.json'

if os.path.exists(filename):
    with open(filename, 'r') as file:
        config = json.load(file)

def save():
    with open(filename, 'w') as file:
        json.dump(config, file)



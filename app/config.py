import json

p = "../config.json"

def load():
    with open(p) as cfg :
        return load(cfg)

cfg = load()

host = cfg["host"]
port = cfg["port"]
key = cfg["password"]
up = cfg["upload_dir"]
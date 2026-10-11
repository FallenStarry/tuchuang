import json

p = "../config.json"

def load1():
    with open(p) as cfg :
        return json.load(cfg)

cfg = load1()

host = cfg["host"]
port = cfg["port"]
key = cfg["password"]
up = cfg["upload_dir"]
url = cfg["url"]
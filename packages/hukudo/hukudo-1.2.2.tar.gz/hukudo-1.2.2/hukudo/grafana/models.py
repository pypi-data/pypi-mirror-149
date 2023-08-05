import json
from pathlib import Path


class JSONThing:
    def __init__(self, raw):
        self.raw = raw

    def __repr__(self):
        return str(self.raw)[:30]

    @property
    def id(self):
        return self.raw['id']

    @property
    def uid(self):
        return self.raw['uid']


class Dashboard(JSONThing):
    def export(self, path):
        path = Path(path)
        path.write_text(json.dumps(self.raw))

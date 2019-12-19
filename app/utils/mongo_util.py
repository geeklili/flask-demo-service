from pymongo import MongoClient
from flask import g, current_app


class MongoBase:
    def __init__(self, uri):
        self.uri = uri

    def client(self):
        if 'client' not in g:
            g.client = MongoClient(self.uri)
        return g.client

    def close(self):
        client = g.pop('client', None)
        if client is not None:
            client.close()


class MongoJDAli(MongoBase):
    def __init__(self):
        uri = current_app.config['MONGO_JD_ALI_URI']
        super().__init__(uri)

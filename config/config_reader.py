import os
import json
import codecs


class Config:
    def __init__(self, stand):
        self.stand = stand

    @staticmethod
    def get_config():
        full_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config', 'config.json'))
        with codecs.open(full_path, 'r', encoding='utf-8') as config:
            data = json.load(config)
        return Config(data['stand'])

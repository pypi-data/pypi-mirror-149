import toml
import json


def get_authentications(filename, content):
    if filename.endswith('.json'):
        return json.loads(content)
    if filename.endswith('.toml'):
        return toml.loads(content)


class Config(object):
    def __init__(self, path):
        self.configs = {}
        self.path = path
        self.file_format = None

    def load(self):
        data = {}

        if self.path.name.endswith('.json'):
            self.file_format = 'json'
        elif self.path.name.endswith('.toml'):
            self.file_format = 'toml'

        if not self.path.exists():
            return

        if self.file_format == 'toml':
            data = toml.load(self.path.open('r'))
        elif self.file_format == 'json':
            data = json.load(self.path.open('r'))

        for key, value in data.items():
            self.configs[key] = value

    def login(self, hostname, username, password):
        creds = self.configs.get('credentials', {})
        creds[hostname] = {
            "username": username,
            "password": password,
        }
        self.configs['credentials'] = creds

    def save(self):
        if self.file_format == 'toml':
            toml.dump(self.configs, self.path.open('w'))
        elif self.file_format == 'json':
            json.dump(self.configs, self.path.open('w'))

    def get(self, hostname):
        return self.configs['credentials'][hostname]

    def __contains__(self, key):
        creds = self.configs.get('credentials', {})
        return key in creds

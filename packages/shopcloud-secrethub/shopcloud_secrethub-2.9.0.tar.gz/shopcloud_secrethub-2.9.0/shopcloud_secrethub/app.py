import configparser
import requests
from typing import List
import os


class ConfigFile:
    def __init__(self, path, **kwargs):
        self.path = path
        self._token = kwargs.get('api_token')

        if self._token is None:
            self._load_from_env()
            if self._token is None:
                self._load_from_config()

    def _load_from_env(self):
        token = os.environ.get('SECRETHUB_TOKEN')
        if token is not None:
            self._token = token

    def _load_from_config(self):
        config = configparser.ConfigParser()
        config.read(self.path)
        if 'default' not in config:
            raise Exception(f'Error loading file {self.path} use auth to generate')

        self._token = config['default']['token']

    @property
    def token(self) -> str:
        if self._token is None:
            raise Exception('No Auth Token exists')
        return self._token

    @staticmethod
    def generate(path: str, token: str):
        config = configparser.ConfigParser()
        config.add_section('default')
        config['default']['token'] = token

        with open(path, 'w') as configfile:
            config.write(configfile)


class App:
    def __init__(self, path, **kwargs):
        self.config = ConfigFile(path, api_token=kwargs.get('api_token'))
        self.endpoint = kwargs.get('endpoint', 'shopcloud-secrethub.ey.r.appspot.com')
    
    def read(self, secretname, **kwargs) -> List:
        headers = {
            'Authorization': self.config.token.strip(),
            'User-Agent': kwargs.get('user_agent', 'secrethub-cli'),
            'User-App': kwargs.get('user_app')
        }
        response = requests.get(
            f'https://{self.endpoint}/hub/api/secrets/',
            headers=headers,
            params={
                'q': secretname,
            }
        )
        if not (200 <= response.status_code <= 299):
            raise Exception('API wrong answer')

        return response.json().get('results', [])

    def write(self, secretname, value, **kwargs):
        headers = {
            'Authorization': self.config.token,
            'User-Agent': kwargs.get('user_agent', 'secrethub-cli'),
            'User-App': kwargs.get('user_app')
        }
        response = requests.post(
            f'https://{self.endpoint}/hub/api/secrets/write/',
            headers=headers,
            json={
                'name': secretname,
                'value': value
            }
        )

        if not (200 <= response.status_code <= 299):
            raise Exception('API wrong answer')

        return response.json()
    
    def token_refresh(self, **kwargs) -> str:
        headers = {
            'Authorization': self.config.token,
            'User-Agent': kwargs.get('user_agent', 'secrethub-cli'),
            'User-App': kwargs.get('user_app')
        }
        response = requests.post(
            f'https://{self.endpoint}/hub/api/tokens/refresh/',
            headers=headers,
            json={}
        )

        if not (200 <= response.status_code <= 299):
            raise Exception('API wrong answer')

        return response.json().get('token', {}).get('value')



class SecretHub:
    def __init__(self, **kwargs):
        path = os.path.expanduser('~/.secrethub')
        self.app = App(path, api_token=kwargs.get('api_token'))
        self.secrets = {}
        self.user_app = kwargs.get('user_app')

    def read(self, secretname: str):
        secret = self.secrets.get(secretname)
        if secret is not None:
            return secret.get('value')
        
        secrets = self.app.read(
            secretname, 
            user_agent='secrethub-code',
            user_app=self.user_app
        )
        if len(secrets) == 0:
            raise Exception('can not access secret `{}`'.format(secretname))
        secret = secrets[0]
        self.secrets[secret.get('name')] = secret
        return secrets[0].get('value')

import requests
from config.config_reader import Config


class Auth:
    def __init__(self):
        self.BASE_URL = Config.get_config().stand

    def login(self, login, password):
        body = {
            "login": login,
            "password": password
        }
        response = requests.post(self.BASE_URL + '/api/v1/auth/login', json=body)
        return response

    def get_auth_header(self, login, password):
        token = self.login(login, password).json()['token']
        return {"Authorization": "Bearer %s" % token}


if __name__ == '__main__':
    response = Auth().login('testlogin123', 'testlogin123')
    print(response.json()['token'])
    header = Auth().get_auth_header('testlogin123', 'testlogin123')
    print(header)

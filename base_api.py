import json
import requests
from decouple import config

class BaseApi():
    def __init__(self, url, username, password, web):
        self.url = url
        self.token = self.authenticate(username, password, web)


    def authenticate(self, username, password, web):
        url = f'{self.url}/login2'
        body = {
            'username': username,
            'password': password,
            'web': web
        }

        try:
            response = requests.post(
                url=url,
                data=body
            )

            if response.status_code == 200:
                content = json.loads(response.text)
                token = content.get('token')
                self.access_token = f'Bearer {token}'

                contexto = content.get('contexto', [])
                self.contexto = contexto[0]

                dados_pessoais = content.get('dadosPessoais', {})
                self.cod_pessoa = dados_pessoais.get('codpessoa')
        except Exception as e:
            print(e)

    def get_emprestimo_renovavel(self):
        url = f'{self.url}/api/biblioteca/listaemprestimorenovavel'
        headers = {
            'Authorization': self.access_token
        }

        body = {
            'contextoaluno': self.contexto,
            'codpessoa': self.cod_pessoa
        }

        try:
            response = requests.post(
                url,
                body,
                headers=headers
            )

            if response.status_code == 200:
                content = json.loads(response.text)
                print(content)
        except Exception as e:
            print(e)


url = config('URL')
username = config('USERNAME')
password = config('PASSWORD')
web = config('WEB')

base_api = BaseApi(
    url,
    username,
    password,
    web
)

base_api.get_emprestimo_renovavel()
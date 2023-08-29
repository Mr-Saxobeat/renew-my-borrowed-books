import json
import requests

class BaseApi():
    def __init__(self, url, username, password, web):
        self.url = url
        self.authenticate(username, password, web)


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


    def request(self, method, path, **kwargs):
        headers = {
            'Authorization': self.access_token
        }

        body = {
            'contextoaluno': self.contexto,
            'codpessoa': self.cod_pessoa
        }

        if kwargs.get('body'):
            kbody = kwargs.get('body')
            body.update(**kbody)

        url = f'{self.url}{path}'
        response = requests.request(
                method,
                url,
                body=body,
                headers=headers
            )
        
        return response

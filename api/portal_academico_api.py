import json
from api.base_api import BaseApi
from decouple import config


class PortalAcademicoApi(BaseApi):
    def __init__(self):
        super().__init__(
            config('URL'),
            config('USERNAME'),
            config('PASSWORD'),
            config('WEB'),
        )


    def lista_emprestimo_renovavel(self):
        path = f'/api/biblioteca/listaemprestimorenovavel'
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
            'Host': 'portal.multivix.edu.br',
            'Content-Length': '144'
        }

        try:
            response = self.request('POST', path, headers=headers)

            if response.status_code == 200:
                content = json.loads(response.text)
                return content
        except Exception as e:
            print(e)


    def renova_obra(self, code):
        path = f'/api/biblioteca/renovaobra'

        body = {
            'codigo': code
        }

        try:
            response = self.request(
                'POST',
                path,
                body=body,
            )
            return response
        except Exception as e:
            print(e)
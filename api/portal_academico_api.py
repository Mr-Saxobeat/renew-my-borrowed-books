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

        try:
            response = self.request(
                path,
            )

            response = self.request('GET', path)

            if response.status_code == 200:
                content = json.loads(response.text)
                print(content)
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
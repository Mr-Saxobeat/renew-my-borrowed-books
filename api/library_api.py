import json
from api.base_api import BaseApi
from decouple import config


class LibraryApi(BaseApi):
    def __init__(self):
        super().__init__(
            config('URL'),
            config('USERNAME'),
            config('PASSWORD'),
            config('WEB'),
        )


    def list_borrowed_books(self):
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
                borrowed_books = content.get('renovaveis')
                return borrowed_books
        except Exception as e:
            print(e)


    def renew_book(self, book_code):
        path = f'/api/biblioteca/renovaobra'

        body = {
            'codigo': book_code
        }

        try:
            response = self.request('POST', path, body=body)
            return response
        except Exception as e:
            print(e)
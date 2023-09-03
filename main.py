from api.portal_academico_api import PortalAcademicoApi
from datetime import datetime
from api.logger_api import ApiLogger


class Event():
    def __init__(self):
        self.api = PortalAcademicoApi()
        self.logger = ApiLogger(__name__)
        self.now = datetime.now()


    def process(self):
        borrowed_books = self.api.list_borrowed_books()

        self.logger.info(f'Livros renováveis: {borrowed_books}')

        for book in borrowed_books:
            self.renew_if_reached_due_date(book)


    def renew_if_reached_due_date(self, book: dict):
        due_date = self.get_due_date(book)

        self.logger.info(f'Data de devolução do livro {book["ttl_nome"]}: {due_date}')

        if self.now < due_date:
            self.logger.info(f'Renovando livro: {book["ttl_nome"]}')

            book_code = book['codigo']
            self.api.renew_book(book_code)


    def get_due_date(self, livro: dict):
        unformatted_due_date = livro.get('dtdevolucaoestimada')
        due_date = datetime.strptime(unformatted_due_date, '%Y-%m-%dT%H:%M:%S')
        return due_date


# def handler(event, context):
event = Event()
event.process()
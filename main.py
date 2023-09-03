from api.portal_academico_api import PortalAcademicoApi
from datetime import datetime
from api.logger_api import ApiLogger


class Main():
    def __init__(self):
        self.api = PortalAcademicoApi()


    def process(self):
        logger = ApiLogger(__name__)

        logger.info("Listando livros renováveis...")
        livros_renovavies = self.lista_livros_renovaveis()
        agora = datetime.now()

        logger.info(f'Livros renováveis: {livros_renovavies}')
        for livro in livros_renovavies:
            data_devolucao = self.get_data_devolucao(livro)
            logger.info(f'Data de devolução do livro {livro["ttl_nome"]}: {data_devolucao}')

            if agora > data_devolucao:
                logger.info(f'Renovando livro {livro["ttl_nome"]}')
                self.renova(livro)


    def lista_livros_renovaveis(self):
        try:
            response = self.api.lista_emprestimo_renovavel()
            renovaveis = response.get('renovaveis')
            return renovaveis
        except Exception as e:
            print(e)


    def get_data_devolucao(self, livro):
        dtdevolucaoestimada = livro.get('dtdevolucaoestimada')
        data_devolucao = datetime.strptime(dtdevolucaoestimada, '%Y-%m-%dT%H:%M:%S')
        return data_devolucao


    def renova(self, livro):
        return self.api.renova_obra(livro['codigo'])


def handler(event, context):
    main = Main()
    main.process()


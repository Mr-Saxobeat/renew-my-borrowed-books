from api.portal_academico_api import PortalAcademicoApi
from datetime import datetime


class Main():
    def __init__(self):
        self.api = PortalAcademicoApi()


    def main(self):
        livros_renovavies = self.lista_livros_renovaveis()
        agora = datetime.now()

        for livro in livros_renovavies:
            data_devolucao = self.get_data_devolucao(livro)

            if agora > data_devolucao:
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

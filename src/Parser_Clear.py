import camelot
import os
from os import listdir
from src.Transacao import Transacao
from src.Parser_Nota import ParserNota
from src.Nota import Nota

class ParserClear(ParserNota):


    def __init__(self, path_pdf:str):
        """
        Execute o parser da nota de corretagem em PDF da Clear

        Args:
            path_pdf (str): Caminho completo do arquivo PDF que possui os dados da nota
        """
        self.path_pdf = path_pdf
        self.refactor_path_pdf = self.refactor_pdf(self.path_pdf)
        self.tables = self.extract(self.refactor_path_pdf)
        # Remover o arquivo temporário
        # os.remove(self.refactor_path_pdf)
        
    def extract(self, refactor_path_pdf):
        tables = camelot.read_pdf(refactor_path_pdf, flavor='stream')
        return tables

    def parse_data_pregao(self, table):
        """
        Processa a tabela com os dados da nota e retorna a data do pregão

        Args:
            table (PandasDataframe): Dataframe com os dados da nota
        """        
        return table[2][2]

    def parse_taxa_liquidacao(self, table):
        """
        Processa a tabela com os dados da nota e retorna a taxa de liquidacao

        Args:
            table (PandasDataframe): Dataframe com os dados da nota
        """
        return float(table[4][3].replace(",","."))

    def parse_emolumentos(self, table):
        """
        Processa a tabela com os dados da nota e retorna o valor dos emolumentos

        Args:
            table (PandasDataframe): Dataframe com os dados da nota
        """        
        return float(table[4][9].replace(",","."))

    def parse_valor_total_operacoes(self, table):
        """
        Processa a tabela com os dados da nota e retorna o valor total das operações da nota

        Args:
            table (PandasDataframe): Dataframe com os dados da nota
        """        
        return float(table[2][8].replace(".","").replace(",","."))

    def parse_transacoes(self, table):
        """
        Processa a tabela e extrai as transacoes
        """
        table = table.iloc[4: , :]
        transacoes = []
        for aux in table.iterrows():
            # Extrair o ativo, a string vem da seguinte forma 
            # "    FII MAXI REN          MXRF11          CI"
            nome_ativo = aux[1][3].split("          ")
            tipo = aux[1][1]
            ativo = nome_ativo[1]
            qtd = int(aux[1][6])
            preco_medio = float(aux[1][7].replace(",","."))
            nova_trasacao = Transacao(tipo, ativo, qtd, preco_medio)
            transacoes.append(nova_trasacao)

        return transacoes
    
    def cria_nota(self):
        """
        Cria uma nota a partir do arquivo enviado
        """

        data_pregao = self.parse_data_pregao()
        taxa_liquidacao = self.parse_taxa_liquidacao()
        emolumentos = self.parse_emolumentos()
        valor_total_operacoes = self.parse_valor_total_operacoes()

        nota = Nota(data_pregao, taxa_liquidacao, emolumentos, valor_total_operacoes)

        transacoes = self.parse_transacoes()

        for transacao in transacoes:            
            nota.add_transcao(transacao)

        nota.calc_preco_medio_ajustado()

        return nota
from datetime import date
import camelot
from src.Parser_Nota import ParserNota
from src.Nota import Nota
from src.Transacao import Transacao
from src.Utils import Utils
import numpy as np
import os


class ParserClear(ParserNota):


    def __init__(self, path_pdf:str):
        """
        Execute o parser da nota de corretagem em PDF da Clear

        Args:
            path_pdf (str): Caminho completo do arquivo PDF que possui os dados da nota
        """
        self.path_pdf = path_pdf
        self.refactor_path_pdf = self.refactor_pdf(self.path_pdf)

        # # Remover o arquivo temporário
        # os.remove(self.refactor_path_pdf)
        
    def extract(self, refactor_path_pdf):

        # não conseguiu achar as três tabelas
        dados = {
            "cabecalho": "",
            "transacoes": "",
            "resumo": "",
        }
        # Tabela com os dados da nota e com o resumo
        dados_nota = camelot.read_pdf(refactor_path_pdf, flavor='stream')

        # Tabela com as Transações
        transacaoes = camelot.read_pdf(refactor_path_pdf, flavor='stream', table_areas=['0,600,600,400'],
                                       columns=['91,105,167,180,305,345,402,445,543'])

        # areas [x1,y1,y2,x2] = x1 = sempre 0, y1 = altura que vai começar a ler y2 = altura que vai parar de ler x1 =
        resumo = camelot.read_pdf(refactor_path_pdf, flavor='stream', table_areas=['0,380,600,0'])

        dados["cabecalho"] = dados_nota[0].df
        dados["transacoes"] = transacaoes[0].df.iloc[1:, :]
        dados["resumo"] = resumo[0].df

        return dados

    def parse_data_pregao(self, table):
        """
        Processa a tabela com os dados da nota e retorna a data do pregão

        Args:
            table (PandasDataframe): Dataframe com os dados da nota
        """
        data_pregao = table[1][2].split('\n')
        data_pregao = data_pregao[2]
        data_pregao_formatada = date(int(data_pregao[6:10]), int(data_pregao[3:5]), int(data_pregao[0:2]))
        return data_pregao_formatada

    def parse_taxa_liquidacao(self, table):
        """
        Processa a tabela com os dados da nota e retorna a taxa de liquidacao

        Args:
            table (PandasDataframe): Dataframe com os dados da nota
        """
        return float(table[4][2].replace(",","."))

    def parse_emolumentos(self, table):
        """
        Processa a tabela com os dados da nota e retorna o valor dos emolumentos

        Args:
            table (PandasDataframe): Dataframe com os dados da nota
        """        
        return float(table[4][8].replace(",","."))

    def parse_valor_total_operacoes(self, table):
        """
        Processa a tabela com os dados da nota e retorna o valor total das operações da nota

        Args:
            table (PandasDataframe): Dataframe com os dados da nota
        """        
        return float(table[2][7].replace(".","").replace(",","."))

    def parse_transacoes(self, table, data_pregao: date, nome_ativos_clear: dict):
        """
        Processa a tabela e extrai as transacoes

        @Args:
            nome_ativos_clear (dict): Dicionário com os nomes dos ativos na clear
        """        
        transacoes = []        
        
        for aux in table.iterrows():
            aux[1].replace('', np.nan, inplace=True)
            
            # Tipo, compra ou venda (C / V)
            tipo = aux[1][1][:1]            
            qtd = 0
            preco_medio = 0.0

            if type(aux[1][3]) == str:            
                ativo = aux[1][3]
            else:
                ativo = aux[1][4]

            if len(aux[1]) == 8:
                qtd = int(aux[1][4])
                preco_medio = float(aux[1][5].replace(",","."))

            if len(aux[1]) == 9:                
                qtd = int(aux[1][5])
                preco_medio = float(aux[1][6].replace(",","."))

            if len(aux[1]) == 10 or len(aux[1]) == 11:                                                    
                if aux[1][4] == "":
                    qtd = int(aux[1][5])
                    preco_medio = float(aux[1][6].replace(",","."))                
                else:
                    qtd = int(aux[1][6])
                    preco_medio = float(aux[1][7].replace(",","."))                

            ativo = Utils.formata_nome_ativo_clear(ativo)
            nome_ativo_clear = ativo
            if ativo in nome_ativos_clear:
                nome_ativo_clear = nome_ativos_clear[ativo]
            else:
                print("O ativo {} não está cadastrado na lista com os nomes dos ativos da clear".format(ativo))

            nova_trasacao = Transacao(data_pregao, tipo, ativo, nome_ativo_clear, qtd, preco_medio)
            transacoes.append(nova_trasacao)

        return transacoes
    
    def cria_nota(self, nome_ativos_clear):
        """
        Cria uma nota a partir do arquivo enviado

        Args:
            nome_ativos_clear (dict): Dicionário com o nome dos ativos utilizados pela clear
        """
        tables = self.extract(self.refactor_path_pdf)
        data_pregao = self.parse_data_pregao(tables["cabecalho"])
        taxa_liquidacao = self.parse_taxa_liquidacao(tables["resumo"])
        emolumentos = self.parse_emolumentos(tables["resumo"])

        valor_total_operacoes = self.parse_valor_total_operacoes(tables["resumo"])

        nota = Nota(data_pregao, taxa_liquidacao, emolumentos, valor_total_operacoes, self.path_pdf)

        transacoes = self.parse_transacoes(tables["transacoes"], data_pregao, nome_ativos_clear)

        for transacao in transacoes:            
            nota.add_transcao(transacao)

        nota.calc_preco_medio_ajustado()

        return nota
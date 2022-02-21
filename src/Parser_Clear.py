from datetime import date
import camelot
from camelot import utils
import os
from os import listdir

from matplotlib.pyplot import table
from src.Transacao import Transacao
from src.Parser_Nota import ParserNota
from src.Nota import Nota

import pandas as pd
import numpy as np
import re

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
        # # Remover o arquivo temporário
        # os.remove(self.refactor_path_pdf)
        
    def extract(self, refactor_path_pdf):

        tables = camelot.read_pdf(refactor_path_pdf, flavor='stream')
        
        # não conseguiu achar as três tabelas
        dados = {
            "cabecalho": "",
            "transacoes": "",
            "resumo": "",
        }
        
        if tables.n == 2:

            # topo
            dados_nota = camelot.read_pdf(refactor_path_pdf, flavor='stream')            
            
            # transacoes
            transacaoes = camelot.read_pdf(refactor_path_pdf , flavor='stream', table_areas = ['0,600,600,400'],
                                columns=['91,105,167,180,305,345,402,445,543'])

            dados["cabecalho"] = dados_nota[0].df
            dados["transacoes"] = transacaoes[0].df.iloc[1: , :]
            dados["resumo"] = dados_nota[1].df
            
        else:
            dados["cabecalho"] = tables[0].df
            dados["transacoes"] = tables[1].df.iloc[4: , :]
            dados["resumo"] = tables[2].df            

        return dados

    def parse_data_pregao(self, table):
        """
        Processa a tabela com os dados da nota e retorna a data do pregão

        Args:
            table (PandasDataframe): Dataframe com os dados da nota
        """     
        data_pregao = table[2][2]    
        data_pregao_formatada = date(int(data_pregao[6:10]), int(data_pregao[3:5]), int(data_pregao[0:2]))
        return data_pregao_formatada

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
        transacoes = []        
        
        for aux in table.iterrows():
            
            # aux[1].dropna(inplace=True)
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
            
                        

            nova_trasacao = Transacao(tipo, ativo, qtd, preco_medio)
            transacoes.append(nova_trasacao)

            # if len(aux[1]) == 9:
            #     qtd = int(aux[1][6])
            #     preco_medio = float(aux[1][7].replace(",","."))


            # if len(aux[1]) == 8:
                
                
            #     preco_medio = float(aux[1][5].replace(",","."))

            #     if aux[1][5] == "" or aux[1][5][:1] == "#" :
            #         qtd = int(aux[1][6])
            #         preco_medio = float(aux[1][7].replace(",","."))
            #     else:
            #         qtd = int(aux[1][5])
            #         preco_medio = float(aux[1][6].replace(",","."))                   

            # if len(aux[1])== 9:
            #     tipo = aux[1][1][:1]
            #     ativo = aux[1][3]

            #     if aux[1][5] == "" or aux[1][5][:1] == "#" :
            #         qtd = int(aux[1][6])
            #         preco_medio = float(aux[1][7].replace(",","."))
            #     else:
            #         qtd = int(aux[1][5])
            #         preco_medio = float(aux[1][6].replace(",","."))                                    
                
            #     preco_medio = float(aux[1][5].replace(",","."))

            # if len(aux[1]) == 10:
                
            #     tipo = aux[1][1][:1]

            #     if aux[1][3] == "":
            #         ativo = aux[1][4]
            #     else:
            #         ativo = aux[1][3]

            #     if aux[1][5] == "" or aux[1][5][:1] == "#" :
            #         qtd = int(aux[1][6])
            #         preco_medio = float(aux[1][7].replace(",","."))
            #     else:
            #         qtd = int(aux[1][5])
            #         preco_medio = float(aux[1][6].replace(",","."))            

            # if len(aux[1])== 11:
            #     tipo = aux[1][1][:1]
            #     ativo = aux[1][4]
            #     qtd = int(aux[1][6])
            #     preco_medio = float(aux[1][7].replace(",","."))
            

        return transacoes
    
    def cria_nota(self):
        """
        Cria uma nota a partir do arquivo enviado
        """
        tables = self.extract(self.refactor_path_pdf)

        data_pregao = self.parse_data_pregao(tables["cabecalho"])
        taxa_liquidacao = self.parse_taxa_liquidacao(tables["resumo"])
        emolumentos = self.parse_emolumentos(tables["resumo"])
        valor_total_operacoes = self.parse_valor_total_operacoes(tables["resumo"])

        nota = Nota(data_pregao, taxa_liquidacao, emolumentos, valor_total_operacoes, self.path_pdf)

        transacoes = self.parse_transacoes(tables["transacoes"])

        for transacao in transacoes:            
            nota.add_transcao(transacao)

        nota.calc_preco_medio_ajustado()

        return nota
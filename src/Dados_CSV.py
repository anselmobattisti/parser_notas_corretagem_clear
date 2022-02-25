from src.Nota import Nota
from src.Transacao import Transacao
from src.Ativo import Ativo
import datetime
from typing import List
import csv
from src.Imprimir import Imprimir
from datetime import date

class DadosCSV:


    @staticmethod
    def exportar_notas(notas: List[Nota], filename:str):
        """
        Exporta as notas para um arquivo CSV

        Args:
            notas (List[Nota]): Lista de notas que devem ser salvas
            filename (str): Path do arquivo que será gerado
        """

        try:
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                        "Data_Pregao",
                        "Emolumentos",
                        "Taxa_Liquidacao",
                        "Valor_Total_Operacao",
                        "Arquivo"
                    ])

                for nota in notas:
                    writer.writerow([
                            nota.data_pregao,
                            nota.emolumentos,
                            nota.taxa_liquidacao,
                            nota.valor_total_operacoes,
                            nota.path_pdf
                        ])

        except Exception as e:
            print('Error:', e)

    @staticmethod
    def exportar_transacoes(transacoes: List[Transacao], filename:str):
        """
        Exporta as transacoes para um arquivo CSV

        Args:
            transacoes (List[Nota]): Lista de notas que devem ser salvas
            filename (str): Path do arquivo que será gerado
        """

        try:
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    "Data_Pregao",
                    "Tipo",
                    "Ativo",
                    "Qtd",
                    "Preco_Medio",
                    "Preco_Medio_Ajustado",
                    "Valor_Transacao",
                    "Valor_Transacao_Ajustada"
                ])

                for transacao in transacoes:
                    writer.writerow([
                        transacao.data_pregao,
                        transacao.tipo,
                        transacao.ativo,
                        transacao.qtd,
                        transacao.preco_medio,
                        transacao.preco_medio_ajustado,
                        transacao.calc_valor_transacao(),
                        transacao.calc_valor_transacao_ajustada()
                    ])

        except Exception as e:
            print('Error:', e)

    @staticmethod
    def importar_transacoes(filename:str):
        """
        Importar as transacoes que estão em um arquivo CSV.

        O processo de extração das informações do PDF é demorada então a ideia é executar a extração, salvar em um
        CSV e depois usar os dados do CSV para gerar os relatórios para o imposto de renda.

        Args:
            filename (str): Path do arquivo que será lido
        """
        try:
            transacaoes = []
            with open(filename, 'r', newline='') as f:
                spamreader = csv.reader(f, delimiter=",")
                next(spamreader)
                for row in spamreader:
                    dt = row[0].split("-")
                    data_pregao = date(int(dt[0]), int(dt[1]), int(dt[2]))
                    t = Transacao(data_pregao, row[1], row[2], int(row[3]), float(row[4]), float(row[5]))
                    transacaoes.append(t)

            return transacaoes

        except Exception as e:
            print('Error:', e)
            return []

    @staticmethod
    def importar_notas(filename:str):
        """
        Importar as notas que estão em um arquivo CSV.

        Args:
            filename (str): Path do arquivo que será lido
        """
        try:
            notas = []
            with open(filename, 'r', newline='') as f:
                spamreader = csv.reader(f, delimiter=",")
                next(spamreader)
                for row in spamreader:
                    # Data,Emolumentos,Taxa_Liquidacao,Valor_Total_Operacao,Arquivo
                    dt = row[0].split("-")
                    n = Nota(date(int(dt[0]), int(dt[1]), int(dt[2])), float(row[1]), float(row[2]), float(row[3]), row[4])
                    notas.append(n)

            return notas

        except Exception as e:
            print('Error:', e)
            return []


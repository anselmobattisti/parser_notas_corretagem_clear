from src.Nota import Nota
from src.Transacao import Transacao
from src.Ativo import Ativo
import datetime
from typing import List
import csv

class Exportar:

    @staticmethod
    def notas(notas: List[Nota], filename:str):
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
                        "Data",
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
    def transacoes(transacoes: List[Transacao], filename:str):
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


from beautifultable import BeautifulTable
from src.Nota import Nota
from src.Transacao import Transacao
from src.Ativo import Ativo

import datetime

class Imprimir:

    @staticmethod
    def nota(nota:Nota):
        """
        Imprime os dados de uma nota

        Args:
            nota (Nota): Nota
        """
        table = BeautifulTable()

        table.rows.append(["{}/{}/{}".format(nota.data_pregao.day,nota.data_pregao.month, nota.data_pregao.year)])
        table.rows.append(["R$ {}".format(nota.taxa_liquidacao)])
        table.rows.append(["R$ {}".format(nota.emolumentos)])
        table.rows.append(["R$ {}".format(nota.valor_total_operacoes)])
        table.rows.header = [
            "Data_Pregao",
            "Taxa_Liquidacao",
            "Emolumentos",
            "Valor_Total"            
        ]
        print(table)
        print("Transações ================")
        for transacao in nota.transacoes:
            Imprimir.transacao(transacao)
                        
        print("=======================")
        print("\n")        
                    

    @staticmethod
    def transacao(transacao:Transacao):
        """
        Imprime uma transação
        Args:
            transacao (Transacao): Transacao
        """
        table = BeautifulTable()
        table.rows.append(["{}/{}/{}".format(transacao.data_pregao.day,transacao.data_pregao.month, transacao.data_pregao.year)])
        table.rows.append([transacao.tipo])
        table.rows.append([transacao.ativo])
        table.rows.append([transacao.qtd])
        table.rows.append([transacao.preco_medio])
        table.rows.append([transacao.preco_medio_ajustado])
        table.rows.append([transacao.calc_valor_transacao()])
        table.rows.append([transacao.calc_valor_transacao_ajustada()])
        table.rows.header = [
            "Data_Pregao",
            "Tipo",
            "Ativo",
            "Qtd",
            "Preco_Medio",
            "Preco_Medio_Ajustado",
            "Valor_Transacao",
            "Valor_Transacao_Ajustada",
        ]
        print(table)
        print("\n")        
            

    @staticmethod
    def ativo(ativo:Ativo):
        """
        Imprime um ativo

        Args:
            ativo (Ativo): Ativo
        """
        table = BeautifulTable()
        table.rows.append([ativo.tipo])
        table.rows.append([ativo.nome])
        table.rows.append([ativo.qtd])
        table.rows.append([ativo.preco_medio])        
        table.rows.append([ativo.calc_valor_investido()])

        table.rows.header = [
            "Tipo",
            "Ativo",
            "Qtd",
            "Preco_Medio",
            "Valor_Investido",            
        ]
        print(table)
        print("\n")        
                        
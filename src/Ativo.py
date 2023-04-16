from typing import List
import re
import math
from beautifultable import BeautifulTable
from src.Transacao import Transacao


class Ativo:

    def __init__(self, tipo: str, nome: str, qtd: int, preco_medio: float):
        """
        Ativo (FII, BDR ou Ação)

        Args:
            tipo (str): ACAO, FII, BDR
            nome (str): Nome do ativo na clear
            qtd (int): Quantas unidades do ativo você possui atualmente
            preco_medio (float): Valor do preco médio pago nos ativos
        """
        self.tipo = tipo
        self.nome = nome
        self.qtd = qtd
        self.preco_medio = preco_medio

        self.qtd_inicial = qtd
        self.preco_medio_inicial = preco_medio

    @property
    def tipo(self):
        """
        Tipo do ativo
        """
        return self._tipo
    
    @tipo.setter
    def tipo(self, valor: str):
        """
        Seta o tipo do ativo
        """
        if not type(valor) == str:
            raise TypeError("O tipo deve ser uma string")
        
        self._tipo = valor

    @property
    def nome(self):
        """
        Nome do ativo na clear
        """
        return self._nome
    
    @nome.setter
    def nome(self, valor: str):
        """
        Seta o nome do ativo
        """
        valor = " ".join(re.split("\s+", valor, flags=re.UNICODE)).strip()
        self._nome = valor

    @property
    def qtd(self):
        """
        Quantas unidades você tem
        """
        return self._qtd
    
    @qtd.setter
    def qtd(self, valor: float):
        """
        Seta a quantidade 
        """
        if valor < 0:
            valor = 0

        self._qtd = valor

    @property
    def preco_medio(self):
        """
        Preço médio
        """
        return round(self._preco_medio, 2)

    @preco_medio.setter
    def preco_medio(self, valor: float):
        """
        Seta o preço médio
        """
        self._preco_medio = valor

    def calc_valor_investido(self):
        """
        Calcula o valor já investido no ativo
        """
        return self.qtd * self._preco_medio

    def imprimir_discriminacao(self):
        """
        Gera o texto que será colado no formulário do imposto de renda com base no total de ações e o seu preço médio
        ajustado

        :return:
        """
        valor_investido = round(self.qtd * self.preco_medio, 2)
        preco_medio = "{}".format(self.preco_medio).replace(".", ",")
        # valor_investido = "{}".format(valor_investido).replace(".", ",")

        # texto = "ACOES: {} QTD: {} PRECO MEDIO COMPRA: R$: {} \t TOTAL\t TOTAL INVESTIDO R$ {} \n".format(self.nome, self.qtd, preco_medio, valor_investido)
        texto = "ACOES: {} QTD: {} PRECO MEDIO COMPRA: R$: {}".format(self.nome, self.qtd, preco_medio)
        return texto

    def recalcular_preco_medio(self, transacoes:List[Transacao]):
        """
        A partir de uma lista de transações, atualiza o preço médio e também a nova quantidade de ativos

        Args:
            transacoes (list[Transacao]): Lista de transações para serem processadas            
        """
        qtd_compra = 0
        qtd_venda = 0

        total_investido = 0

        for transacao in transacoes:
            if transacao.ativo == self.nome:
                if transacao.tipo == "C":

                    total_investido += transacao.calc_valor_transacao_ajustada()

                    qtd_compra += transacao.qtd

                else:
                    qtd_venda += transacao.qtd

        total = qtd_compra + self.qtd
        if total == 0:
            self.preco_medio = 0
        else:
            self.preco_medio = ((self.preco_medio * self.qtd) + total_investido) / (total )
        self.qtd = self.qtd + (qtd_compra - qtd_venda)
        return self.preco_medio



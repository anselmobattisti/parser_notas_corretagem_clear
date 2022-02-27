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
        return math.floor(self._preco_medio)

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
        texto = "ACOES: {} QTD: {} PRECO MEDIO COMPRA: R$: {:.2f} \t R$ {:.2f} \t R$ {:.2f}\n".format(self.nome, self.qtd, self.preco_medio, (self.qtd_inicial*self.preco_medio_inicial), self.calc_valor_investido())
        return texto

    def recalcular_preco_medio(self, transacoes:List[Transacao]):
        """
        A partir de uma lista de transações, atualiza o preço médio e também a nova quantidade de ativos

        Args:
            transacoes (list[Transacao]): Lista de transações para serem processadas            
        """

        # Se não tem quantidade o preço médio é zero
        if self.qtd == 0:
            return 0
        total_investido = self.calc_valor_investido()

        qtd_total_novas_acoes = 0

        valor_total_aplicado_nas_transacaoes = 0

        for transacao in transacoes:
            if transacao.ativo == self.nome and transacao.tipo == "C":
                qtd_total_novas_acoes += transacao.qtd
                valor_total_aplicado_nas_transacaoes += transacao.calc_valor_transacao_ajustada()

        # a) Soma o valor_atual com o valor ajustado da nova transacao
        self.qtd += qtd_total_novas_acoes

        # b) Divide pela soma do valor atual com a quantidade de ações compradas
        self.preco_medio = (total_investido + valor_total_aplicado_nas_transacaoes) / self.qtd

        return self.preco_medio



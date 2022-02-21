from datetime import date
from src.Transacao import Transacao

class Nota:

    def __init__(self, data_pregao:date, taxa_liquidacao:float, emolumentos:float, valor_total_operacoes:float, path_pdf:str):
        """
        Estrutura da nota de corretagem

        Args:
            data_pregao (date): Data do pregão
            taxa_liquidacao (float): Taxa de liquidação
            emolumentos (float): Taxa de emolumentos
            valor_total_operacoes (float): Valor total da soma de todas as transações da nota
            path_pdf (str): Arquivo PDF que gerou a nota
        """
        self.data_pregao = data_pregao
        self.taxa_liquidacao = taxa_liquidacao
        self.emolumentos = emolumentos
        self.valor_total_operacoes = valor_total_operacoes
        self.path_pdf = path_pdf
        self.transacoes = []

    @property
    def data_pregao(self):
        """
        Data do pregão
        """
        return self._data_pregao
    
    @data_pregao.setter
    def data_pregao(self, valor:date):
        """
        Seta a data do pregão
        """
        if not type(valor) == date:
            raise TypeError("A data do pregão deve ser um date")
        
        self._data_pregao = valor

    @property
    def path_pdf(self):
        """
        Caminho do PDF que gerou a nota
        """
        return self._data_pregao
    
    @path_pdf.setter
    def path_pdf(self, valor:date):
        """
        Seta o caminho do arquvio que gerou a nota
        """
        self._path_pdf = valor

    @property
    def taxa_liquidacao(self):
        """
        Taxa de liquidação
        """
        return self._taxa_liquidacao
    
    @taxa_liquidacao.setter
    def taxa_liquidacao(self, valor:float):
        """
        Seta a taxa de liquidação
        """
        if(valor < 0):
            valor = 0

        self._taxa_liquidacao = valor

    @property
    def emolumentos(self):
        """
        Emolumentos
        """
        return self._emolumentos
    
    @emolumentos.setter
    def emolumentos(self, valor:float):
        """
        Seta a taxa de liquidação
        """
        if(valor < 0):
            valor = 0

        self._emolumentos = valor

    @property
    def valor_total_operacoes(self):
        """
        Emolumentos
        """
        return self._valor_total_operacoes

    @property
    def transacoes(self):
        """
        Transações da nota
        """
        return self._transacoes

    @transacoes.setter
    def transacoes(self, transacoes:list):
        self._transacoes = transacoes

    @valor_total_operacoes.setter
    def valor_total_operacoes(self, valor:float):
        """
        Seta o valor total de todas as operações
        """
        if(valor < 0):
            valor = 0

        self._valor_total_operacoes = valor

    def add_transcao(self, transacao:Transacao):
        """
        Adiciona uma transcação a nota
        """
        if not type(transacao) == Transacao:
            raise TypeError("A transcao deve ser do tipo Transação")
        
        self.transacoes.append(transacao)

    def calc_preco_medio_ajustado(self):
        """        
        Calcula o preço médio ajustado dos ativos da nota

        a) Soma os valores da taxa de liquidação com os valores de emolumentos
        b) Calcula o percentual de cada transação no valor total da nota
        c) Subtrai do preço médio o valor pago em tarifas
        """
        total_taxas = self.taxa_liquidacao + self.emolumentos

        for transacao in self.transacoes:            
            percentual_da_transacao = transacao.calc_valor_transacao() / self.valor_total_operacoes
            desconto_taxas = total_taxas * percentual_da_transacao            
            novo_preco_medio = transacao.preco_medio - (desconto_taxas / transacao.qtd)
            transacao.preco_medio_ajustado = novo_preco_medio
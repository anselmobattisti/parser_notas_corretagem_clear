from datetime import date
from src.Utils import Utils


class Transacao:

    def __init__(self, data_pregao: date, tipo: str, ativo: str, nome_ativo_clear: str, qtd: int, preco_medio: float,
                 preco_medio_ajustado: float = 0):
        """
        Estrutura da nota de corretagem

        Args:
            data_pregao (date): Data do pregão
            tipo (str): Tipo da operação, (Compra = C / Venda = V)
            ativo (str): Nome do ativo
            nome_ativo_clear (str): Nome extraído da nota
            qtd (int): Quantidade de unidades transacionadas
            preco_medio (float): Preço médio de cada unidade
            preco_medio_ajustado (float): Preço médio ajustado descontando as taxas
        """
        self.data_pregao = data_pregao
        self.tipo = tipo
        self.ativo = ativo
        self.nome_ativo_clear = nome_ativo_clear
        self.qtd = qtd
        self.preco_medio = preco_medio

        if preco_medio_ajustado > 0:
            self.preco_medio_ajustado = preco_medio_ajustado
        else:
            self.preco_medio_ajustado = preco_medio

    @property
    def data_pregao(self):
        """
        Data do pregão
        """
        return self._data_pregao

    @data_pregao.setter
    def data_pregao(self, valor: date):
        """
        Seta a data do pregão
        """
        if not type(valor) == date:
            raise TypeError("A data do pregão deve ser um date")

        self._data_pregao = valor

    @property
    def tipo(self):
        """
        Tipo da operação, (Compra = C / Venda = V)
        """
        return self._tipo

    @tipo.setter
    def tipo(self, valor: str):
        """
        Seta a data do pregão
        """
        if valor != "C" and valor != "V":
            raise TypeError("O tipo deve ser C ou V")

        self._tipo = valor

    @property
    def ativo(self):
        """
        Nome do ativo
        """
        return self._ativo

    @ativo.setter
    def ativo(self, valor: str):
        """
        Seta o nome do ativo
        """
        self._ativo = valor

    @property
    def nome_ativo_clear(self):
        """
        Nome do ativo
        """
        return self._nome_ativo_clear

    @nome_ativo_clear.setter
    def nome_ativo_clear(self, valor: str):
        """
        Seta o nome do ativo
        """
        self._nome_ativo_clear = Utils.formata_nome_ativo_clear(valor)

    @property
    def qtd(self):
        """
        Quantidade de unidades transacionadas
        """
        return self._qtd

    @qtd.setter
    def qtd(self, valor: int):
        """
        Seta o nome do ativo
        """
        if not type(valor) == int:
            raise TypeError("A QTD deve ser um int")

        self._qtd = valor

    @property
    def preco_medio(self):
        """
        Preço médio pago pelo ativo nessa operação
        """
        return self._preco_medio

    @preco_medio.setter
    def preco_medio(self, valor: float):
        """
        Seta o preço médio de cada unidade
        """
        if not type(valor) == float:
            raise TypeError("O prevo_medio deve ser um float")

        self._preco_medio = valor

    @property
    def preco_medio_ajustado(self):
        """
        Preço médio ajustado
        """
        return self._preco_medio_ajustado

    @preco_medio_ajustado.setter
    def preco_medio_ajustado(self, valor: float):
        """
        Seta o preço médio ajustado com base nas taxas
        """
        if not type(valor) == float:
            raise TypeError("O preco_medio_ajustado deve ser um float")

        self._preco_medio_ajustado = valor

    def calc_valor_transacao(self):
        """
        Calcula o valor total da operação
        """
        return self.qtd * self.preco_medio

    def calc_valor_transacao_ajustada(self):
        """
        Calcula o valor total da operação ajustada com as taxas pagas
        """
        return self.qtd * self.preco_medio_ajustado


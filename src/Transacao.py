import re

class Transacao:

    def __init__(self, tipo:str, ativo:str, qtd:int, preco_medio:float, preco_medio_ajustado:float=0):
        """
        Estrutura da nota de corretagem

        Args:
            tipo (str): Tipo da operação, (Compra = C / Venda = V)
            ativo (str): Nome do ativo
            qtd (int): Quantidade de unidades transacionadas
            preco_medio (float): Preço médio de cada unidade
            preco_medio_ajustado (float): Preço médio ajustado descontando as taxas
        """                
        self.tipo = tipo
        self.ativo = ativo
        self.qtd = qtd
        self.preco_medio = preco_medio

        if preco_medio_ajustado > 0:
            self.preco_medio_ajustado = preco_medio_ajustado
        else:
            self.preco_medio_ajustado = preco_medio


    @property
    def tipo(self):
        """
        Tipo da operação, (Compra = C / Venda = V)
        """
        return self._tipo
    
    @tipo.setter
    def tipo(self, valor:str):
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
    def ativo(self, valor:str):
        """
        Seta o nome do ativo
        """
        valor = " ".join(re.split("\s+", valor, flags=re.UNICODE)).strip()
        self._ativo = valor

    @property
    def qtd(self):
        """
        Quantidade de unidades transacionadas
        """
        return self._qtd
    
    @qtd.setter
    def qtd(self, valor:int):
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
    def preco_medio(self, valor:float):
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
    def preco_medio_ajustado(self, valor:float):
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

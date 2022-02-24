from datetime import date


class Bonificacao:

    def __init__(self, ativo: str, data_base: date, proporcao: float, custo_aquisicao: float):
        """
        Evento de bonificação de ações

        Args:
            ativo (str): Código do ativo
            data_base (date): Data em que o evento irá ocorre
            proporcao (float): Proporcao da bonificação
            custo_aquisicao (float): valor da aquisição para fins contáveis
        """
        self.ativo = ativo
        self.data_base = data_base
        self.proposcao = proporcao
        self.custo_aquisicao = custo_aquisicao

    @property
    def ativo(self):
        """
        Código do ativo
        """
        return self._ativo

    @ativo.setter
    def ativo(self, valor: str):
        """
        Seta o ativo
        """
        if not type(valor) == str:
            raise TypeError("O ativo deve ser uma string")

        self._ativo = valor

    @property
    def data_base(self):
        """
        Data base do evento
        """
        return self._data_base

    @data_base.setter
    def data_base(self, valor: date):
        """
        Seta a data do pregão
        """
        if not type(valor) == date:
            raise TypeError("A data base deve ser um date")

        self._data_base = valor

    @property
    def proposcao(self):
        """
        Proporção da bonificação
        """
        return self._proposcao

    @proposcao.setter
    def proposcao(self, valor: float):
        """
        Seta a quantidade
        """
        if valor < 0:
            valor = 0

        self._proposcao = valor

    @property
    def custo_aquisicao(self):
        """
        Custo de aquisição
        """
        return self._custo_aquisicao

    @custo_aquisicao.setter
    def custo_aquisicao(self, valor: float):
        """
        Seta o custo de aquisição
        """
        if valor < 0:
            valor = 0

        self._custo_aquisicao = valor

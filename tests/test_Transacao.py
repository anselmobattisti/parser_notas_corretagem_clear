import unittest
from src.Transacao import Transacao
from datetime import date

class TransacaoTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tipo = "C"
        cls.ativo = "KNRI11"
        cls.qtd = 10
        cls.preco_medio = 135.25
        cls.transacao = Transacao(cls.tipo, cls.ativo, cls.qtd, cls.preco_medio)

    def test_tipo(self):
        """
        Verifica se o atributo tipo está sendo setado corretamente
        """
        self.assertEqual(self.transacao.tipo, self.tipo)

    def test_ativo(self):
        """
        Verifica se o atributo ativo está sendo setado corretamente
        """        
        self.assertEqual(self.transacao.ativo, self.ativo)

    def test_qtd(self):
        """
        Verifica se o atributo qtd está sendo setado corretamente
        """        
        self.assertEqual(self.transacao.qtd, self.qtd)

    def test_preco_medio(self):
        """
        Verifica se o atributo preco_medio está sendo setado corretamente
        """        
        self.assertEqual(self.transacao.preco_medio, self.preco_medio)

    def test_calc_valor_transacao(self):
        """
        Verifica se a função que calcula o valor total da transacao está funcionando corretamente
        """        
        valor_transacao = self.qtd * self.preco_medio
        self.assertEqual(self.transacao.calc_valor_transacao(), valor_transacao)    

    def test_preco_medio_ajustado_na_craicao(self):
        t1 = Transacao("C", "KNRI11", 10, 20.0, 19.0)
        self.assertEqual(t1.preco_medio_ajustado, 19.0)

if __name__ == '__main__':
    unittest.main()

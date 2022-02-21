import unittest
from src.Imprimir import Imprimir
from src.Ativo import Ativo
from src.Transacao import Transacao

class AtivoTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.tipo = "ACAO"
        cls.nome = "ENERGIAS BR ON NM"
        cls.qtd_anterior = 500
        cls.preco_medio_anterior = 10.00
        
        cls.ativo = Ativo(cls.tipo, cls.nome, cls.qtd_anterior, cls.preco_medio_anterior)
    
    def test_tipo(self):
        self.assertEqual(self.ativo.tipo, self.tipo)

    def test_nome(self):
        self.assertEqual(self.ativo.nome, self.nome)

    def test_qtd_anterior(self):
        self.assertEqual(self.ativo.qtd_anterior, self.qtd_anterior)

    def test_preco_medio_anterior(self):
        self.assertEqual(self.ativo.preco_medio_anterior, self.preco_medio_anterior)

    def test_recalcular_preco_medio(self):

        transacoes = []
        transacoes.append(Transacao("C", "ENERGIAS BR ON NM ", 300, 20.00))
        transacoes.append(Transacao("V", "KNRI11",2, 135.25))
        transacoes.append(Transacao("V", "KNRI11",2, 135.25))
        transacoes.append(Transacao("C", "ENERGIAS BR ON NM ", 200, 20.00))

        preco_medio = self.ativo.recalcular_preco_medio(transacoes)        
        self.assertEqual(preco_medio, 15.00)
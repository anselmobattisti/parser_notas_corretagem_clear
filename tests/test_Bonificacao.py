import unittest
from src.Bonificacao import Bonificacao
from datetime import date


class BonificacaoTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ativo = "PSSA3"
        cls.data_base = date(2021, 10, 25)
        cls.proporcao = 1
        cls.custo_aquisicao = 12.37

        cls.bonificacao = Bonificacao(cls.ativo, cls.data_base, cls.proporcao, cls.custo_aquisicao)

    def test_ativo(self):
        self.assertEqual(self.bonificacao.ativo, self.ativo)

    def test_data_base(self):
        self.assertEqual(self.bonificacao.data_base, self.data_base)

    def test_proporcao(self):
        self.assertEqual(self.bonificacao.proposcao, self.proporcao)

    def test_custo_aquisicao(self):
        self.assertEqual(self.bonificacao.custo_aquisicao, self.custo_aquisicao)
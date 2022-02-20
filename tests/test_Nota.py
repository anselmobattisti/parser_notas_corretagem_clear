import unittest
from src.Nota import Nota
from datetime import date

from src.Transacao import Transacao

class NotaTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.taxa_liquidacao = 1.09
        cls.emolumentos = 0.21
        cls.data_pregao = date(2022, 12, 25)
        cls.valor_total_operacoes = 4345.86
        cls.nota = Nota(cls.data_pregao, cls.taxa_liquidacao, cls.emolumentos,cls.valor_total_operacoes)
    
    @unittest.skip
    def test_data_pregao(self):
        self.assertEqual(self.nota.data_pregao, self.data_pregao)

    @unittest.skip
    def test_taxa_liquidacao(self):
        self.assertEqual(self.nota.taxa_liquidacao, self.taxa_liquidacao)
    
    @unittest.skip
    def test_emolumentos(self):
        self.assertEqual(self.nota.emolumentos, self.emolumentos)
    
    @unittest.skip
    def test_valor_total_operacoes(self):
        self.assertEqual(self.nota.valor_total_operacoes, self.valor_total_operacoes)
    
    @unittest.skip
    def test_add_transacao(self):
        """
        Verifica se uma transacao está sendo adicionada a nota
        """
        t1 = Transacao("C", "KNRI11",2, 135.25)        
        self.nota.add_transcao(t1)
        self.assertEqual(len(self.nota.transacoes), 1)

    def test_calc_preco_medio_ajustado(self):
        """
        Verifica se a operação de ajuste do preço médio está correta
        """

        n1 = Nota(date(2022, 2, 11), 1.09, 0.21, 4345.89)

        t1 = Transacao("C", "KNRI11",2, 135.25)
        t2 = Transacao("C", "KNRI11",8, 135.25)
        t3 = Transacao("V", "MALL11",21, 98.16)
        t4 = Transacao("C", "MXRF11",50, 9.36)
        t5 = Transacao("C", "MXRF11",50, 9.36)
        
        n1.add_transcao(t1)
        n1.add_transcao(t2)
        n1.add_transcao(t3)
        n1.add_transcao(t4)
        n1.add_transcao(t5)

        n1.calc_preco_medio_ajustado()
        
        self.assertAlmostEqual(t1.preco_medio_ajustado, 135.20954223415686)

if __name__ == '__main__':
    unittest.main()

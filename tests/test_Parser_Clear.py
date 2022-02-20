import unittest
from src.Parser_Clear import ParserClear
from src.Nota import Nota
from src.Transacao import Transacao
from datetime import date

class ParserClearTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.path_pdf = "/home/battisti/versionado/nota-corretagem-clear/notas/teste.pdf"
        cls.parser_clear = ParserClear(cls.path_pdf)

    @unittest.skip
    def test_extract_text(self):
        """
        Extrai as três tabelas do PDF
        0 = Dados da nota
        1 = Transações
        2 - Taxas
        """
        tables = self.parser_clear.extract(self.parser_clear.refactor_path_pdf)
        self.assertEqual(tables.n, 3)

    @unittest.skip
    def test_data_pregao(self):
        """
        Extrai a data do pregão do PDF
        """
        tables = self.parser_clear.extract(self.parser_clear.refactor_path_pdf)
        data_pregao = self.parser_clear.parse_data_pregao(tables[0].df)        
        self.assertEqual(data_pregao, "11/02/2022")

    @unittest.skip
    def test_taxa_liquidacao(self):
        """
        Extrai a taxa de liquidação do PDF
        """
        tables = self.parser_clear.extract(self.parser_clear.refactor_path_pdf)
        taxa_liquidacao = self.parser_clear.parse_taxa_liquidacao(tables[2].df)
        self.assertEqual(taxa_liquidacao, 1.09)

    @unittest.skip
    def test_parse_emolumentos(self):
        """
        Extrai a taxa de liquidação do PDF
        """
        tables = self.parser_clear.extract(self.parser_clear.refactor_path_pdf)
        emolumentos = self.parser_clear.parse_emolumentos(tables[2].df)
        self.assertEqual(emolumentos, 0.21)

    @unittest.skip
    def test_parse_valor_total_operacoes(self):
        """
        Extrai o valor total das operações da nota
        """
        tables = self.parser_clear.extract(self.parser_clear.refactor_path_pdf)
        emolumentos = self.parser_clear.parse_valor_total_operacoes(tables[2].df)
        self.assertEqual(emolumentos, 4345.86)

    @unittest.skip
    def test_transacoes(self):
        """
        Extrai as transacoes do PDF
        """
        tables = self.parser_clear.extract(self.parser_clear.refactor_path_pdf)
        transacoes = self.parser_clear.parse_transacoes(tables[1].df)
        self.assertEqual(len(transacoes), 5)

    # @unittest.skip
    def test_cria_nota(self):
        """
        Cria uma nota a partir do PDF
        """
        nota = self.parser_clear.cria_nota()
        print(nota)
        # self.assertEqual(len(transacoes), 5)



if __name__ == '__main__':
    unittest.main()

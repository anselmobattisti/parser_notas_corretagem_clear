import unittest
from src.Parser_Clear import ParserClear
from src.Nota import Nota
from src.Transacao import Transacao
from datetime import date

class ParserClearTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.path_pdf = "/home/battisti/versionado/parser_notas_corretagem_clear/notas/teste.pdf"
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
        # print(tables['cabecalho'])
        # print("-----")
        # print(tables['transacoes'])
        # print("-----")
        # print(tables['resumo'])
        # print()
        # 9 linhas de cabecalho
        self.assertEqual(tables['cabecalho'].shape[0], 9)

        # 5 linhas de transacoes
        self.assertEqual(tables["transacoes"].shape[0], 5)

        # 28 linhas de resumo
        self.assertEqual(tables["resumo"].shape[0], 28)

    @unittest.skip
    def test_extract_text_one_transaction(self):
        """
        Caso o sistema não consiga extrair as três tabelas então ele deve fazer uma operação manual 
        para recuperar as tabelas
        """
        path_pdf = "/home/battisti/versionado/nota-corretagem-clear/notas/teste_1_transacao.pdf"        
        parser_clear2 = ParserClear(path_pdf)
        tables = parser_clear2.extract(parser_clear2.refactor_path_pdf)

        self.assertEqual(tables['cabecalho'].shape[0], 9)

        # 5 linhas de transacoes
        self.assertEqual(tables["transacoes"].shape[0], 1)

        # 28 linhas de resumo
        self.assertEqual(tables["resumo"].shape[0], 28)

    @unittest.skip
    def test_data_pregao(self):
        """
        Extrai a data do pregão do PDF
        """
        tables = self.parser_clear.extract(self.parser_clear.refactor_path_pdf)
        data_pregao = self.parser_clear.parse_data_pregao(tables["cabecalho"])        
        self.assertEqual(data_pregao, date(2022, 2, 11))

    @unittest.skip
    def test_taxa_liquidacao(self):
        """
        Extrai a taxa de liquidação do PDF
        """
        tables = self.parser_clear.extract(self.parser_clear.refactor_path_pdf)
        taxa_liquidacao = self.parser_clear.parse_taxa_liquidacao(tables["resumo"])
        self.assertEqual(taxa_liquidacao, 1.09)

    @unittest.skip
    def test_parse_emolumentos(self):
        """
        Extrai a taxa de liquidação do PDF
        """
        tables = self.parser_clear.extract(self.parser_clear.refactor_path_pdf)
        emolumentos = self.parser_clear.parse_emolumentos(tables["resumo"])
        self.assertEqual(emolumentos, 0.21)

    @unittest.skip
    def test_parse_valor_total_operacoes(self):
        """
        Extrai o valor total das operações da nota
        """
        tables = self.parser_clear.extract(self.parser_clear.refactor_path_pdf)
        emolumentos = self.parser_clear.parse_valor_total_operacoes(tables["resumo"])
        self.assertEqual(emolumentos, 4345.86)

    @unittest.skip
    def test_transacoes(self):
        """
        Extrai as transacoes do PDF
        """
        tables = self.parser_clear.extract(self.parser_clear.refactor_path_pdf)
        transacoes = self.parser_clear.parse_transacoes(tables["transacoes"])
        self.assertEqual(len(transacoes), 5)

    @unittest.skip
    def test_transacoes_unica(self):
        """
        Verifica se ele extrai uma única transacao
        """
        path_pdf = "/home/battisti/versionado/nota-corretagem-clear/notas/teste_1_transacao.pdf"        
        parser_clear2 = ParserClear(path_pdf)
        tables = parser_clear2.extract(parser_clear2.refactor_path_pdf)

        transacoes = self.parser_clear.parse_transacoes(tables["transacoes"])
        self.assertEqual(len(transacoes), 1)


    # @unittest.skip
    def test_cria_nota_5_transacoes(self):
        """
        Cria uma nota a partir do PDF
        """
        nota = self.parser_clear.cria_nota()   

        self.assertEqual(nota.taxa_liquidacao, 1.09)
        self.assertEqual(len(nota.transacoes), 5)

    # @unittest.skip
    def test_cria_nota_1_transacoes(self):
        """
        Cria uma nota a partir do PDF
        """
        path_pdf = "/home/battisti/versionado/nota-corretagem-clear/notas/teste_1_transacao.pdf"        
        parser_clear2 = ParserClear(path_pdf)        
        nota = parser_clear2.cria_nota()

        self.assertEqual(nota.taxa_liquidacao, 0.12)
        self.assertEqual(len(nota.transacoes), 1)


if __name__ == '__main__':
    unittest.main()


import unittest
from src.Dados_CSV import DadosCSV
from src.Nota import Nota
from src.Transacao import Transacao
from src.Imprimir import Imprimir
from datetime import date
import os

class NotaTest(unittest.TestCase):

    def test_exportarnotas(self):
        filename = "arquivos_teste/notas.csv"

        notas = []
        notas.append(Nota(date(2021,10,10),0.10,1.15,200,"Arquivo1"))
        notas.append(Nota(date(2021,11,11),0.10,1.15,200,"Arquivo2"))
        notas.append(Nota(date(2021,12,12),0.10,1.15,200,"Arquivo3"))
        notas.append(Nota(date(2021,2,13),0.10,1.15,250,"Arquivo4"))
        DadosCSV.exportar_notas(notas, filename)
        self.assertTrue(os.path.isfile(filename))
        #os.remove(filename)

    # @unittest.skip
    def test_exportartransacoes(self):
        filename = "arquivos_teste/transacoes.csv"

        transacoes = []
        transacoes.append(Transacao(date(2021,10,10), "C", "ENERGIAS BR ON NM ", 300, 20.00))
        transacoes.append(Transacao(date(2021,11,10), "V", "KNRI11",2, 135.25))
        transacoes.append(Transacao(date(2021,12,2), "V", "KNRI11",2, 135.25))
        transacoes.append(Transacao(date(2021,2,13), "C", "ENERGIAS BR ON NM ", 200, 20.00))

        DadosCSV.exportar_transacoes(transacoes, filename)

        self.assertTrue(os.path.isfile(filename))
        # os.remove(filename)

    def test_importartransacoes(self):
        filename = "arquivos_teste/transacoes.csv"
        transacoes = DadosCSV.importar_transacoes(filename)
        Imprimir.transacao(transacoes[0])
        self.assertTrue(len(transacoes), 4)
        # os.remove(filename)

    def test_importarnotas(self):
        filename = "arquivos_teste/notas.csv"
        notas = DadosCSV.importar_notas(filename)

        for n in notas:
            Imprimir.nota(n)

        self.assertTrue(len(notas), 4)

        # os.remove(filename)

    def test_importarativos(self):
        filename = "arquivos_teste/ativos.csv"
        ativos = DadosCSV.importar_ativos(filename)

        self.assertTrue(len(ativos), 3)
        self.assertTrue(ativos[1].nome == "BBDC3")


if __name__ == '__main__':
    unittest.main()


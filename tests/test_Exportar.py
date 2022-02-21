import unittest
from src.Exportar import Exportar
from src.Nota import Nota
from src.Transacao import Transacao
from datetime import date
import os

class NotaTest(unittest.TestCase):

    # @unittest.skip
    def test_notas(self):
        filename = "notas.csv"

        notas = []
        notas.append(Nota(date(2021,10,10),0.10,1.15,200,"Arquivo1"))
        notas.append(Nota(date(2021,11,11),0.10,1.15,200,"Arquivo2"))
        notas.append(Nota(date(2021,12,12),0.10,1.15,200,"Arquivo3"))
        notas.append(Nota(date(2021,2,13),0.10,1.15,250,"Arquivo4"))
        Exportar.notas(notas, filename)
        self.assertTrue(os.path.isfile(filename))
        os.remove(filename)

    # @unittest.skip
    def test_transacoes(self):
        filename = "transacoes.csv"

        transacoes = []
        transacoes.append(Transacao("C", "ENERGIAS BR ON NM ", 300, 20.00))
        transacoes.append(Transacao("V", "KNRI11",2, 135.25))
        transacoes.append(Transacao("V", "KNRI11",2, 135.25))
        transacoes.append(Transacao("C", "ENERGIAS BR ON NM ", 200, 20.00))

        Exportar.transacoes(transacoes, filename)

        self.assertTrue(os.path.isfile(filename))
        os.remove(filename)


if __name__ == '__main__':
    unittest.main()


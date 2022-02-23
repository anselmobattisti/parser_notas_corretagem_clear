from importlib.resources import path
from src.Ativo import Ativo
from src.Nota import Nota
from src.Parser_Clear import ParserClear
import os
from src.Imprimir import Imprimir
from src.Dados_CSV import DadosCSV
"""
Exemplo de uso

a) Ler várias notas
b) Criar uma lista com todas as notas
c) Salvar em um arquivo do Excel o resultado
"""

def main():

    meus_ativos = {}
    meus_ativos["ENERGIAS BR ON NM"] = Ativo("ACAO", "ENERGIAS BR ON NM", 500, 19.46)

    # Define qual é o diretório onde estão os arquivos
    path_notas = "/home/battisti/versionado/nota-corretagem-clear/minhas_notas/ENBR3"
    # path_notas = "/home/battisti/versionado/nota-corretagem-clear/minhas_notas/"

    notas = []
    for f in os.listdir(path_notas):        
        file_path = "{}/{}".format(path_notas,f)
        if os.path.isfile(file_path) and file_path.endswith('.pdf'):
            if file_path.find("resaved") == -1:      
                # if file_path.find("NotaNegociacao_596745_20210119.pdf") > 0:            
                # debug
                print(f)
                parser = ParserClear(file_path)
                nota = parser.cria_nota()
                notas.append(nota)

    total = 0    

    transacoes = []
    for nota in notas:
        transacoes += nota.transacoes
        meus_ativos["ENERGIAS BR ON NM"].recalcular_preco_medio(nota.transacoes)
        # print("Nota ========== ")
        # Imprimir.nota(nota)
        # total += nota.valor_total_operacoes

    Imprimir.ativo(meus_ativos["ENERGIAS BR ON NM"])
    DadosCSV.exportar_notas(notas, "./minhas_notas/notas.csv")
    DadosCSV.exportar_transacoes(transacoes, "./minhas_notas/transacoes.csv")

    # print(total)

if __name__ == "__main__":
    main()

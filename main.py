from importlib.resources import path
from src.Nota import Nota
from src.Parser_Clear import ParserClear
import os

"""
Exemplo de uso

a) Ler vários arquivos de notas
b) Criar uma lista com todas as notas
c) Salvar em um arquivo do Excel o resultado
"""

def main():

    # Define qual é o diretório onde estão os arquivos
    path_notas = "/home/battisti/versionado/nota-corretagem-clear/minhas_notas/"

    notas = []
    for f in os.listdir(path_notas):
        print(f)
        file_path = "{}/{}".format(path_notas,f)
        if os.path.isfile(file_path) and file_path.endswith('.pdf'):
            print(file_path)
        
            parser = ParserClear(file_path)
            nota = parser.criar_nota()
        
if __name__ == "__main__":
    main()

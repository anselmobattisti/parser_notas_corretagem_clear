from src.Parser_Clear import ParserClear
import os
from src.Dados_CSV import DadosCSV
from src.Imprimir import Imprimir
from src.Ativo import Ativo

def carregar_transacoes_manuais(filetransacaoes: str):
    """
    Carrega as transações que foram manualmente inseridas devido a emissão de cotas ou então processo de bonificação
    de ações.

    Dados sobre cada emissão de FII pode ser achada no site: https://www.clubefii.com.br/ofertas-publicas-fundos-imobiliarios/quinta-emissao-XPLG11

    :param filetransacaoes: caminho onde está o arquivo das transações manuais
    :return:
    """
    transacoes = []

    transacoes += DadosCSV.importar_transacoes(filetransacaoes)

    return transacoes

def processar_notas(meses: [], ano:int , nome_ativos_clear: dict):
    """
    Processa as notas em pdf de uma pasta e gera o CSV com as notas e as transações,
    os arquivos CSV serão salvos na mesma pasta onde está o PDF com o nome de notas.csv e transacoes.csv

    :param meses: lista com os meses que devem ser processados
    :param ano: ano do imposto
    :param nome_ativos_clear: dicionário com os nomes de ativos da clear
    :return:
    """

    for mes in meses:
        notas = []
        print("Processando as notas do mês {}:".format(mes))
        path_notas = "/home/battisti/versionado/parser_notas_corretagem_clear/minhas_notas/{}-{}".format(mes, ano)
        list_files = os.listdir(path_notas)
        list_files = sorted(list_files)
        for f in list_files:
            file_path = "{}/{}".format(path_notas, f)
            if os.path.isfile(file_path) and file_path.endswith('.pdf'):
                if file_path.find("resaved") == -1:
                    print("Processando o arquivo {}".format(f))
                    parser = ParserClear(file_path)
                    nota = parser.cria_nota(nome_ativos_clear)
                    notas.append(nota)

        transacoes = []
        for nota in notas:
            transacoes += nota.transacoes

        DadosCSV.exportar_notas(notas, "{}/notas.csv".format(path_notas))
        DadosCSV.exportar_transacoes(transacoes, "{}/transacoes.csv".format(path_notas))


def executa_processamento_anual_notas(nome_ativos_clear, ano):
    """
    Executa o processamento de todas todos os PDFs das notas que estão nas pastas de cada mes
    :return:
    """
    # meses = ["teste"]
    meses = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    # meses = ["11"]
    processar_notas(meses, ano, nome_ativos_clear)


def carregar_notas(path_csv: str, ano: int, meses: []):
    """
    Carreta os dados da notas que foram precisamente processadas.

    :param path_notas: caminho onde estão as notas
    :param ano: Ano onde as notas foram geradas
    :param meses: arquivos de quais meses devem ser importados
    :return:
    """
    notas = []

    for mes in meses:
        print("Importando as notas do mês {}/:".format(mes, ano))
        path_notas = "{}/{}-{}".format(path_csv, mes, ano, "notas.csv")
        path_notas_csv = "{}/{}-{}/{}".format(path_csv, mes, ano, "notas.csv")
        notas = notas + DadosCSV.importar_notas(path_notas_csv)

    return notas


def carregar_transacaoes(path_csv: str, ano: int, meses: []):
    """
    Carreta os dados das transacoes que foram previamente processadas.

    :param path_csv: caminho onde estão as notas
    :param ano: Ano onde as notas foram geradas
    :param meses: arquivos de quais meses devem ser importados
    :return:
    """
    transacoes = []

    for mes in meses:
        path_transacoes_csv = "{}{}-{}/{}".format(path_csv, mes, ano, "transacoes.csv")
        transacoes += DadosCSV.importar_transacoes(path_transacoes_csv)

    # carregar transações manuais
    transacaoes_manuais = carregar_transacoes_manuais("{}/transacoes_manuais.csv".format(path_csv))

    return transacoes + transacaoes_manuais


def carregar_ativos(path_arquvio: str, nome_ativos_clear: dict):
    """
    Carrega os ativos que estão no arquivo de ativos, pegar info na declaração do ano anterior

    :param path_arquvio: 
    :param nome_ativos_clear:
    :return: dicionários com os ativos
    """
    ativos = DadosCSV.importar_ativos(path_arquvio)

    ativos_ja_importados = []

    for ativo in ativos:
        ativos_ja_importados.append(ativo.nome)

    # Adiciona todos os ativos que foram negociados no ano mas que ainda não estão na lista
    for ativo in nome_ativos_clear:
        nome_ativo = nome_ativos_clear[ativo]
        if nome_ativo not in ativos_ja_importados:
            ativos_ja_importados.append(ativo)
            ativos.append(Ativo("ACAO",nome_ativo, 0, 0.0))

    return ativos


def main():
    ano = 2022

    path_sys = "/home/battisti/versionado/parser_notas_corretagem_clear/"

    path_data = "{}data/".format(path_sys)

    path_csv = "{}minhas_notas/".format(path_sys)

    nome_ativos_clear = DadosCSV.carregar_nome_ativos("{}nome_ativos.csv".format(path_data))

    # # Executa o processamento atual das notas
    # executa_processamento_anual_notas(nome_ativos_clear, ano)
    # quit()

    meses = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    ativos = carregar_ativos("{}ativos.csv".format(path_data), nome_ativos_clear)

    transacoes = carregar_transacaoes(path_csv, ano, meses)

    DadosCSV.exportar_transacoes(transacoes, "{}{}-transacoes.csv".format(path_csv, ano))
    # quit()

    for ativo in ativos:
        ativo.recalcular_preco_medio(transacoes)
        print(ativo.imprimir_discriminacao())

    posicao_acoes = "{}{}-posicao.csv".format(path_csv,ano)
    DadosCSV.exportar_posicao_acoes(ativos, posicao_acoes)
    # notas = carregar_notas(path_csv,2021,meses)
    # for nota in notas:
    #     Imprimir.nota(nota)

    # transacoes = carregar_transacaoes(path_csv, 2021, meses)
    # for transacao in transacoes:
    #     Imprimir.transacao(transacao)

# Fora de contexto
# Carrega todas as notas e transações do ano
# meus_ativos = {}
# meus_ativos["ENERGIAS BR ON NM"] = Ativo("ACAO", "ENERGIAS BR ON NM", 500, 19.46)
#
# # Define qual é o diretório onde estão os arquivos
# path_notas = "/home/battisti/versionado/nota-corretagem-clear/minhas_notas/ENBR3"
# # path_notas = "/home/battisti/versionado/nota-corretagem-clear/minhas_notas/"
#
# notas = []
# for f in os.listdir(path_notas):
#     file_path = "{}/{}".format(path_notas,f)
#     if os.path.isfile(file_path) and file_path.endswith('.pdf'):
#         if file_path.find("resaved") == -1:
#             # if file_path.find("NotaNegociacao_596745_20210119.pdf") > 0:
#             # debug
#             print(f)
#             parser = ParserClear(file_path)
#             nota = parser.cria_nota()
#             notas.append(nota)
#
# total = 0
#
# transacoes = []
# for nota in notas:
#     transacoes += nota.transacoes
#     meus_ativos["ENERGIAS BR ON NM"].recalcular_preco_medio(nota.transacoes)
#     # print("Nota ========== ")
#     # Imprimir.nota(nota)
#     # total += nota.valor_total_operacoes
#
# Imprimir.ativo(meus_ativos["ENERGIAS BR ON NM"])
# DadosCSV.exportar_notas(notas, "./minhas_notas/notas.csv")
# DadosCSV.exportar_transacoes(transacoes, "./minhas_notas/transacoes.csv")
#
# # print(total)


if __name__ == "__main__":
    main()

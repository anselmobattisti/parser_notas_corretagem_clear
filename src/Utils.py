import re


class Utils:

    @staticmethod
    def formata_nome_ativo_clear(nome_ativo):
        return " ".join(re.split("\s+", nome_ativo, flags=re.UNICODE)).strip()
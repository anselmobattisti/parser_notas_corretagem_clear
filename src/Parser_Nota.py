import os
import pikepdf
from abc import ABC, abstractmethod

class ParserNota(ABC):


    def __init__(self):
        super().__init__()

    def refactor_pdf(self, path_pdf):
        """
        Abre o PDF e salva ele novamente, por alguma razão as notas da clear vem com PDF corrompido e o camelot não 
        consegue ler corretamente
        """
        modified_pdf_name = os.path.basename(path_pdf).split('.')
        modified_pdf_name = modified_pdf_name[0]+'_resaved.pdf'
        dir_name = os.path.dirname(path_pdf)
        path_pdf_resaved = os.path.join(dir_name,modified_pdf_name)
        pdf_resaved = pikepdf.Pdf.open(path_pdf)            
        pdf_resaved.save(path_pdf_resaved)
        return path_pdf_resaved

    @abstractmethod
    def extract(self, refactor_path_pdf):
        pass

    @abstractmethod
    def parse_data_pregao(self, table):
        pass
    
    @abstractmethod
    def parse_taxa_liquidacao(self, table):
        pass
    
    @abstractmethod
    def parse_emolumentos(self, table):
        pass
    
    @abstractmethod    
    def parse_valor_total_operacoes(self, table):
        pass
    
    @abstractmethod
    def parse_transacoes(self, table):
        pass

    @abstractmethod
    def cria_nota(self):
        pass
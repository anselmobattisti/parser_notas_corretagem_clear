import os
import pikepdf
from abc import ABC, abstractmethod
from PyPDF4 import PdfFileWriter, PdfFileReader
import PyPDF4

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

        # Teste de marca d'agua
        # self.put_watermark(path_pdf_resaved, path_pdf_resaved, "grade.pdf")

        return path_pdf_resaved

    def put_watermark(self, input_pdf, output_pdf, watermark):
        # reads the watermark pdf file through
        # PdfFileReader
        watermark_instance = PdfFileReader(watermark)

        # fetches the respective page of
        # watermark(1st page)
        watermark_page = watermark_instance.getPage(0)

        # reads the input pdf file
        pdf_reader = PdfFileReader(input_pdf)

        # It creates a pdf writer object for the
        # output file
        pdf_writer = PdfFileWriter()

        # iterates through the original pdf to
        # merge watermarks
        for page in range(pdf_reader.getNumPages()):
            page = pdf_reader.getPage(page)

            # will overlay the watermark_page on top
            # of the current page.
            page.mergePage(watermark_page)

            # add that newly merged page to the
            # pdf_writer object.
            pdf_writer.addPage(page)

        with open(output_pdf, 'wb') as out:
            # writes to the respective output_pdf provided
            pdf_writer.write(out)

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
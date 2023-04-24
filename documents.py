import os
import shutil
import docx
import logging

class Documents:

    def __init__(self, cnpj, root_cnpj, corporate_name, trade_name, registration_status):
        self.cnpj = cnpj
        self.root_cnpj = root_cnpj
        self.corporate_name = corporate_name
        self.trade_name = trade_name
        self.registration_status = registration_status
        
        self.formatted_cnpj = self.format_cnpj(self.cnpj)

        self.error = False
        self.source_document_path = "./doc-matriz.docx" 
        self.final_document_path = f"./Docs/Documento Gerado de {self.trade_name}.docx"

        logging.basicConfig(filename='logs_general.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')

    def create_directory_if_not_exists(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def format_cnpj(self, cnpj):
        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
      
    def replace_phrases(self, doc, guide):
        for paragraph in doc.paragraphs:
            for run in paragraph.runs:
                for key, value in guide.items():
                    if value["indice"] in run.text:
                        text = run.text.replace(value["indice"], value["replace"])
                        run.clear()
                        run.add_text(text)

    def create_document(self):
        logging.debug("entrou no create")
        dir_path = os.path.dirname(self.final_document_path)
        logging.debug("dir path")
        self.create_directory_if_not_exists(dir_path)

        if os.path.exists(self.final_document_path):
            self.error = True
            logging.info("O arquivo de destino já existe.")
            pass
        else:
            shutil.copy(self.source_document_path, self.final_document_path)

        doc = docx.Document(self.final_document_path)
        guide = self.guide()
        self.replace_phrases(doc, guide)
        doc.save(self.final_document_path)

    def guide(self):
        guide = {
            "CNPJ": {
                "indice" : "TTT",
                "replace": str(self.formatted_cnpj)
                #Saida ex: 00.000.000/0001-00
            },
            "CNPJ_RAIZ": {
                "indice" : "QQQ",
                "replace": str(self.root_cnpj)
                #Saida ex: 12345678
            },
            "RAZAO_SOCIAL": {
                "indice" : "WWW",
                "replace": str(self.corporate_name),
                #Saida ex: Teste LTDA
            },
            "NOME_FANTASIA": {
                "indice" : "EEE",
                "replace": str(self.trade_name),
                #Saida ex: Testes meus 
            },
            "SITUACAO_CADASTRAL": {
                "indice" : "RRR",
                "replace": str(self.registration_status),
                #Saida ex: Ativa
            }
        }

        return guide
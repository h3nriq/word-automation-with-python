import PySimpleGUI as simpleGui
from documents import Documents
from request import CNPJData
import logging

class Interface:
    def __init__(self):

        simpleGui.theme('Dark')
        #Layout
        layout = [
            [simpleGui.Text('CNPJ.', size=(10,0)), simpleGui.Input(size=(14,0), key=('cnpj'),  enable_events=True)],
            [simpleGui.Text('Deseja buscar a situação cadastral?')],
            [simpleGui.Radio('Sim', 'option', key='sim'), simpleGui.Radio('Não', 'option', key='nao')],
            [simpleGui.Button('Gerar Documento')],
            [simpleGui.Output(size=(20,5))]
        ]
        #Janela
        self.window = simpleGui.Window('Gerar Docx Formatado').layout(layout)

        logging.basicConfig(filename='logs_general.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')

        self.error = False
    
    def set_cnpj_data(self, cnpj):
        cnpj_class = CNPJData(cnpj)

        if cnpj_class.error is True: 
            self.error = True
            logging.error(f"Erro ao fazer requisição. Status code: {cnpj_class.status_code}")
        
        else:
            self.root_cnpj = cnpj_class.root_cnpj
            self.corporate_name = cnpj_class.corporate_name
            self.trade_name = cnpj_class.trade_name
            self.registration_status = self.get_registration_status(cnpj_class.registration_status)
        
    def set_document(self, cnpj, root_cnpj, corporate_name, trade_name, registration_status):

        self.document = Documents(cnpj, root_cnpj, corporate_name, trade_name, registration_status)
        self.document.create_document()
        if self.document.error is True:
            print("Error: Aconteceu algum erro ao gerar seu documento, veja se ele já não está criado no destino")
        else:
            print("Sucesso: Documento gerado! Acesse em /Docs")

    def loop_system(self):
        while True:
            self.button, self.values = self.window.Read()

            # Valida o campo CNPJ
            self.validations(self.values['cnpj'])

            if self.button == "Gerar Documento":
                self.set_input_values()
                self.set_cnpj_data(self.cnpj)

                if self.error is True: 
                    print(f"ERRO: Por Favor busque um CNPJ válido")
                else: 
                    self.set_document(self.cnpj, self.root_cnpj, self.corporate_name, self.trade_name, self.registration_status)

    def set_input_values(self):
        self.cnpj = self.values['cnpj']

        if self.values['sim']:
            self.option = True
        elif self.values['nao']:
            self.option = False

    def get_registration_status(self, cnpj_registration_status):
        if self.option is True: 
            return cnpj_registration_status
        else: 
            return ""
        
    def run(self):
        self.loop_system()

    def validations(self, cnpj):

        # Validações: Somente numero
        if self.button == 'cnpj' and cnpj and cnpj[-1] not in ('0123456789'): self.window['cnpj'].update(cnpj[:-1])

        # Validações: Quantiedade de caracteres
        if len(cnpj) > 14: self.window.Element('cnpj').Update(cnpj[:-1])            

win = Interface()
win.run()
import requests

class CNPJData:
    def __init__(self, cnpj):
        self.cnpj = cnpj
        self.url_cnpj = f"https://publica.cnpj.ws/cnpj/{cnpj}"
        self.error = False
        self._get_data()

    def _get_data(self):
        response = requests.get(self.url_cnpj)
        
        if response.status_code == 200:
            data = response.json()
            
            self.root_cnpj = data['cnpj_raiz']
            self.corporate_name = data['razao_social']
            self.trade_name = data['estabelecimento']['nome_fantasia']
            self.registration_status = data['estabelecimento']['situacao_cadastral']
        else:
            self.error = True
            self.status_code = response.status_code
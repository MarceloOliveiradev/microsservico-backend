import requests
from flask_restx import Namespace, Resource

frete_ns = Namespace('frete', description='Cálculo de frete baseado em CEP')

@frete_ns.route('/<string:cep>')
class Frete(Resource):
    def get(self, cep):
        # Consulta ViaCEP
        url = f'https://viacep.com.br/ws/{cep}/json/'
        response = requests.get(url)

        if response.status_code != 200:
            return {'erro': 'Erro ao consultar o ViaCEP'}, 400

        data = response.json()

        if 'erro' in data:
            return {'erro': 'CEP inválido'}, 404

        uf = data.get('uf')

        # Tabela simples de frete por estado
        tabela_frete = {
            "SP": 7.50, "RJ": 5.50, "MG": 6.00, "ES": 6.50,
            "RS": 8.00, "SC": 7.00, "PR": 7.00,
            "BA": 9.00, "PE": 10.00,
        }

        frete = tabela_frete.get(uf, 12.00)

        return {
            "cep": cep,
            "logradouro": data.get("logradouro"),
            "bairro": data.get("bairro"),
            "localidade": data.get("localidade"),
            "uf": uf,
            "frete": round(frete, 2)
        }

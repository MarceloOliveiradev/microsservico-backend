from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from resources.ima import ns as imas_ns
from resources.frete import frete_ns


app = Flask(__name__)
CORS(app)

api = Api(app, version='1.0', title='API de Imãs',
          description='Uma API para gerenciar um estoque de uma loja imãs de neodímio')

api.add_namespace(imas_ns)
api.add_namespace(frete_ns)


if __name__ == '__main__':
    from banco_de_dados.database import init_db # Inicializar o banco de dados apenas se o app.py for executado diretamente 
    init_db()
    
    app.run(debug=True, host='0.0.0.0')


# http://localhost:5000/frete/01001000 - RETORNO EM JSON SIMPLES
# http://127.0.0.1:5000/ - SWAGGER
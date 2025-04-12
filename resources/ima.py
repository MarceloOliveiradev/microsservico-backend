from flask_restx import Namespace, Resource, fields, reqparse
from sqlalchemy.exc import IntegrityError
from banco_de_dados.database import SessionLocal, Ima

# Definir o namespace
ns = Namespace('imas', description='Operações relacionadas aos imãs')

# Definir o modelo (schema) para o imã
ima_model = ns.model('Imã', {
    'ima_id': fields.String(required=False, description="ID do imã"),
    'medida': fields.String(required=True, description="Medida do imã"),
    'formato': fields.String(required=True, description="Formato do imã"),
    'forca_N': fields.String(required=True, description="Força do imã em Mega-Gauss Oersteds (MGOe)"),
    'preco': fields.Float(required=True, description="Preço do imã")
})

# Rotas
@ns.route('/')
class Imas(Resource):
    @ns.marshal_list_with(ima_model) 
    def get(self):
        """
        Retorna o estoque de imãs.
        """
        session = SessionLocal()
        imas = session.query(Ima).all()
        session.close()
        return imas

    @ns.expect(ima_model)  # Espera que a requisição seja no formato do modelo
    @ns.marshal_with(ima_model)  # Retorna a resposta usando o modelo
    def post(self):
        """
        Cria um novo imã e o salva no banco de dados.
        """
        parser = reqparse.RequestParser()
        parser.add_argument('medida', required=True, type=str, help="Medida do imã")
        parser.add_argument('formato', required=True, type=str, help="Formato do imã")
        parser.add_argument('forca_N', required=True, type=str, help="Força do imã")
        parser.add_argument('preco', required=True, type=float, help="Preço do imã")
        args = parser.parse_args()

        # Valores permitidos para força_N
        valores_permitidos = ['N35', 'N42', 'N50', 'N52']
        if args['forca_N'] not in valores_permitidos:
            return {'message': f"Valor inválido para força_N. Deve ser um dos: {', '.join(valores_permitidos)}."}, 400 # Bad Request

        # Valores permitidos para formato
        valores_formato_permitidos = ['cilindro', 'cubo', 'anel']
        if args['formato'].lower() not in valores_formato_permitidos:
            return {'message': f"Valor inválido para formato. Deve ser um dos: {', '.join(valores_formato_permitidos)}."}, 400  # Bad Request
    
        # Cria um novo objeto Imã
        new_ima = Ima(
            medida=args['medida'],
            formato=args['formato'],
            forca_N=args['forca_N'],
            preco=args['preco']
        )

        session = SessionLocal()
        try:
            session.add(new_ima)
            session.commit()
            session.refresh(new_ima)
        except IntegrityError:
            session.rollback()
            return {'message': 'ID do imã já existe.'}, 400 # Bad Request
        except Exception as e:
            session.rollback()
            return {'message': f'Erro ao salvar o imã: {str(e)}'}, 500  # Internal Server Error
        finally:
            session.close()

        return new_ima, 201 # Created


@ns.route('/search/<string:medida>')
class ImasById(Resource):
    @ns.marshal_with(ima_model)
    def get(self, medida):
        """
        Retorna um imã específico do estoque pela medida.
        """
        session = SessionLocal()
        ima = session.query(Ima).filter(Ima.medida == medida).first()
        session.close()

        if ima:
            return ima
        return {'message': 'Imã não encontrado'}, 404 # Not found

@ns.route('/<string:ima_id>')
class ImasById(Resource):
    @ns.expect(ima_model) 
    @ns.marshal_with(ima_model) 
    def put(self, ima_id):
        """
        Atualiza um imã específico pelo ID.
        """
        parser = reqparse.RequestParser()
        parser.add_argument('medida', type=str, help="Medida do imã")
        parser.add_argument('formato', type=str, help="Formato do imã")
        parser.add_argument('forca_N', type=str, help="Força do imã")
        parser.add_argument('preco', type=float, help="Preço do imã")
        args = parser.parse_args()

        session = SessionLocal()
        ima = session.query(Ima).filter(Ima.ima_id == ima_id).first()
        if ima:
            if args['medida']: ima.medida = args['medida']
            if args['formato']: ima.formato = args['formato']
            if args['forca_N']is not None: ima.forca_N = args['forca_N']
            if args['preco'] is not None: ima.preco = args['preco']

            session.commit()
            session.refresh(ima)
            session.close()
            return ima
        session.close()
        return {'message': 'Imã não encontrado'}, 404 # Not found

    def delete(self, ima_id):
        """
        Deleta um imã específico pelo ID.
        """
        session = SessionLocal()
        ima = session.query(Ima).filter(Ima.ima_id == ima_id).first()
        if ima:
            session.delete(ima)
            session.commit()
            session.close()
            return {'message': f'Imã com ID {ima_id} deletado'}, 200 # Sucess
        session.close()
        return {'message': 'Imã não encontrado'}, 404 # Not Found

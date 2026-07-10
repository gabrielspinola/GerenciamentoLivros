from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token

from models.usuario_model import usuario_existe, criar_usuario, validar_credenciais

api = Namespace("auth", description="Autenticação (usuários mockados em memória, sem banco de dados)")

# --- Modelos (schemas) usados no Swagger ---

registro_model = api.model(
    "Registro",
    {
        "username": fields.String(required=True, description="Nome de usuário", example="joao"),
        "senha": fields.String(required=True, description="Senha do usuário", example="senha123"),
    },
)

login_model = api.model(
    "Login",
    {
        "username": fields.String(required=True, description="Nome de usuário", example="admin"),
        "senha": fields.String(required=True, description="Senha do usuário", example="admin123"),
    },
)

token_model = api.model(
    "Token",
    {
        "access_token": fields.String(description="Token JWT de acesso"),
    },
)

mensagem_model = api.model(
    "Mensagem",
    {
        "mensagem": fields.String(description="Mensagem de retorno"),
    },
)


@api.route("/registro")
class Registro(Resource):
    @api.expect(registro_model, validate=True)
    @api.marshal_with(mensagem_model, code=201)
    @api.response(409, "Usuário já existe")
    def post(self):
        """Cria um novo usuário (mock, mantido apenas em memória)."""
        dados = api.payload

        if usuario_existe(dados["username"]):
            api.abort(409, "Usuário já existe.")

        criar_usuario(dados["username"], dados["senha"])
        return {"mensagem": "Usuário criado com sucesso."}, 201


@api.route("/login")
class Login(Resource):
    @api.expect(login_model, validate=True)
    @api.marshal_with(token_model, code=200)
    @api.response(401, "Credenciais inválidas")
    def post(self):
        """Autentica o usuário mock e retorna um token JWT.

        Usuário de exemplo já cadastrado: **admin** / **admin123**
        """
        dados = api.payload

        if not validar_credenciais(dados["username"], dados["senha"]):
            api.abort(401, "Usuário ou senha inválidos.")

        access_token = create_access_token(identity=dados["username"])
        return {"access_token": access_token}, 200

from flask import Flask, Blueprint
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import NoAuthorizationError
from jwt.exceptions import PyJWTError

from config.config import Config
from controllers.AuthController import api as auth_ns
from controllers.LivroController import api as livro_ns


# Configuração do cadeado (Authorize) no Swagger, para permitir enviar o Bearer token.
authorizations = {
    "Bearer": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "Digite **Bearer &lt;seu_token&gt;** para autenticar. Ex: Bearer eyJhbGciOi...",
    }
}

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    JWTManager(app)

    # --- Blueprint principal da API ---
    # Toda a API (Swagger + rotas de auth e livros) é registrada dentro
    # deste Blueprint, e depois o Blueprint é registrado na aplicação Flask.
    api_bp = Blueprint("api", __name__)

    api = Api(
        api_bp,
        version="1.0",
        title="API de Cadastro de Livros (mock)",
        description=(
            "API RESTful organizada com Blueprint, autenticação via JWT e dados vindos do MySql"
        ),
        doc="/swagger",  # URL onde o Swagger UI ficará disponível
        authorizations=authorizations,
        security="Bearer",
    )

    api.add_namespace(auth_ns, path="/auth")
    api.add_namespace(livro_ns, path="/livros")

    app.register_blueprint(api_bp)

    # Trata erros de autenticação JWT retornando 401 (em vez do 500 padrão).
    @api.errorhandler(NoAuthorizationError)
    def handle_no_authorization_error(e):
        return {"mensagem": "Token de acesso ausente. Envie o header Authorization: Bearer <token>."}, 401

    @api.errorhandler(PyJWTError)
    def handle_jwt_error(e):
        return {"mensagem": "Token inválido ou expirado."}, 401

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

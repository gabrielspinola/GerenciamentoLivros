from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from repositories.LivroRepository import LivroRepository

api = Namespace("livros", description="Cadastro de livros (dados mockados em memória, sem banco de dados)")

# --- Modelo (schema) usado no Swagger ---

livro_model = api.model(
    "Livro",
    {
        "idlivro": fields.Integer(readonly=True, description="Identificador único do livro"),
        "titulo": fields.String(required=True, description="Título do livro", example="Dom Casmurro"),
        "autor": fields.String(required=True, description="Autor do livro", example="Machado de Assis"),
        "ano_publicacao": fields.Integer(required=True, description="Ano de publicação", example=1899),
        "genero": fields.String(required=True, description="Gênero literário", example="Romance"),
        "bloqueado": fields.String(description="Indica se o livro está bloqueado para empréstimo", example="N"),
    },
)

# Modelo para criação/atualização (sem o idlivro, que é gerado pelo servidor)
livro_input_model = api.model(
    "LivroInput",
    {
        "titulo": fields.String(required=True, description="Título do livro", example="Dom Casmurro"),
        "autor": fields.String(required=True, description="Autor do livro", example="Machado de Assis"),
        "ano_publicacao": fields.Integer(required=True, description="Ano de publicação", example=1899),
        "genero": fields.String(required=True, description="Gênero literário", example="Romance"),
        "bloqueado": fields.String(description="Indica se o livro está bloqueado para empréstimo", example="N", default="N"),
    },
)


@api.route("")
class LivroLista(Resource):
    @jwt_required()
    @api.doc(security="Bearer")
    @api.marshal_list_with(livro_model)
    def get(self):
        livros = LivroRepository().listar_all()
        return livros

    @jwt_required()
    @api.doc(security="Bearer")
    @api.expect(livro_input_model, validate=True)
    @api.marshal_with(livro_model, code=201)
    def post(self):
        dados = api.payload
        livro = LivroRepository().create(dados)
        return livro, 201


@api.route("/<int:idlivro>")
@api.param("idlivro", "Identificador do livro")
@api.response(404, "Livro não encontrado")
class LivroItem(Resource):
    @jwt_required()
    @api.doc(security="Bearer")
    @api.marshal_with(livro_model)
    def get(self, idlivro):
        """Busca um livro pelo ID."""
        #livro = buscar_livro(idlivro)
        #if not livro:
        #    api.abort(404, "Livro não encontrado.")
        #return livro

    @jwt_required()
    @api.doc(security="Bearer")
    @api.expect(livro_input_model, validate=True)
    @api.marshal_with(livro_model)
    def put(self, idlivro):
        """Atualiza um livro existente."""
        dados = api.payload
        #livro = atualizar_livro(idlivro, dados)
        #if not livro:
        #    api.abort(404, "Livro não encontrado.")
        #return livro

    @jwt_required()
    @api.doc(security="Bearer")
    @api.response(204, "Livro removido com sucesso")
    def delete(self, idlivro):
        """Remove um livro pelo ID."""
        #removido = remover_livro(idlivro)
        #if not removido:
        #    api.abort(404, "Livro não encontrado.")
        #return "", 204

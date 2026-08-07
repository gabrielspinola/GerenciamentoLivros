from flask import request, render_template, flash, redirect, session

from routes.Routes import Routes
from services.LivrosServices import LivroServices
from model.LivroModel import LivroModel, LivroModelVazio

class LivroRoute(Routes):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.register_routes()
        
    def register_routes(self):
        @self.app.route("/livros", methods=["POST"])
        @Routes.login_required
        def create_livro():
            livro = LivroModel(titulo = request.form.get("titulo"), 
                               autor = request.form.get("autor"), 
                               ano_publicacao = request.form.get("ano_publicacao"), 
                               genero = request.form.get("genero"),
                               bloqueado = request.form.get("bloqueado"))

            livro_service = LivroServices(username=session.get('username'), password=session.get('usuario_pass'))
            livro_service.create(livro)

            flash('Livro criado com sucesso!', 'success')
            return redirect('/livros')

        @self.app.route("/livros", methods=["GET"])
        @Routes.login_required
        def listar_livros():
            livro = LivroServices(username=session.get('username'), password=session.get('usuario_pass'))
            livros = livro.listar_all()
            return render_template("pages/ListLivros.html", livros=livros), 200

        @self.app.route("/livro", methods=["GET"])
        @Routes.login_required
        def livro():
            livro_data = LivroModelVazio()
            return render_template("pages/Livro.html", livro=livro_data, acao="novo"), 200

        @self.app.route("/livro/<int:id>/editar", methods=["GET"])
        @Routes.login_required
        def atualizar_livro(id):
            livro_service = LivroServices(username=session.get('username'), password=session.get('usuario_pass'))
            livro_data = livro_service.consultar_id(id)
            return render_template("pages/Livro.html", livro=livro_data, acao="alterar"), 200

        @self.app.route("/livro/<int:id>", methods=["POST", "GET"])
        @Routes.login_required
        def consultar_livro(id):
            altLivro = LivroModel(idlivro = id,
                                   titulo = request.form.get("titulo"), 
                                   autor = request.form.get("autor"), 
                                   ano_publicacao = request.form.get("ano_publicacao"), 
                                   genero = request.form.get("genero"),
                                   bloqueado = request.form.get("bloqueado"))

            livro_service = LivroServices(username=session.get('username'), password=session.get('usuario_pass'))
            livro_service.atualizar(altLivro)
            flash('Livro atualizado com sucesso!', 'success')
            return redirect('/livros')
        
        @self.app.route("/livro/<int:id>/deletar", methods=["GET", "DELETE"])
        @Routes.login_required
        def deletar_livro(id):
            livro_service = LivroServices(username=session.get('username'), password=session.get('usuario_pass'))
            livro_service.deletar(id)
            flash('Livro deletado com sucesso!', 'success')
            return redirect('/livros')
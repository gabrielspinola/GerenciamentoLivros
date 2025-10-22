from conexao import DatabaseConnection
from flask import request, render_template, flash, redirect
from routes.Routes import Routes
from services.LivrosServices import LivroServices
from model.LivroModel import LivroModel

class LivroRoute(Routes):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.db = DatabaseConnection()
        self.register_routes()
        
    def register_routes(self):
        @self.app.route("/livros", methods=["POST"])
        @Routes.login_required
        def create_livro():
            livro = LivroModel(titulo = request.form.get("titulo"), 
                               autor = request.form.get("autor"), 
                               ano_publicacao = request.form.get("ano_publicacao"), 
                               genero = request.form.get("genero"))
            self.db.connect()
            livro_service = LivroServices(self.db)
            livro_service.create(livro)
            self.db.close()
            flash('Livro criado com sucesso!', 'success')
            return redirect('/livros')

        @self.app.route("/livros", methods=["GET"])
        @Routes.login_required
        def listar_livros():
            self.db.connect()
            livro = LivroServices(self.db)
            livros = livro.listar_all()
            
            self.db.close()
            return render_template("pages/ListLivros.html", livros=livros), 200

        @self.app.route("/livro", methods=["GET"])
        @Routes.login_required
        def livro():
            livro_data = LivroModel(idlivro=0, titulo="", autor="", ano_publicacao="", genero="")
            return render_template("pages/Livro.html", livro=livro_data, acao="novo"), 200

        @self.app.route("/livro/<int:id>/editar", methods=["GET"])
        @Routes.login_required
        def consultar_livro(id):
            self.db.connect()
            livro_service = LivroServices(self.db)
            livro_data = livro_service.consultar_id(id)
            self.db.close()
            return render_template("pages/Livro.html", livro=livro_data, acao="alterar"), 200

        @self.app.route("/livro/<int:id>", methods=["POST", "GET"])
        @Routes.login_required
        def atualizar_livro(id):
            altLivro = LivroModel(idlivro = id,
                                   titulo = request.form.get("titulo"), 
                                   autor = request.form.get("autor"), 
                                   ano_publicacao = request.form.get("ano_publicacao"), 
                                   genero = request.form.get("genero"))

            self.db.connect()
            livro_service = LivroServices(self.db)
            livro_service.atualizar(altLivro)
            self.db.close()
            flash('Livro atualizado com sucesso!', 'success')
            return redirect('/livros')
        
        @self.app.route("/livro/<int:id>/deletar", methods=["GET", "DELETE"])
        @Routes.login_required
        def deletar_livro(id):
            self.db.connect()
            livro_service = LivroServices(self.db)
            livro_service.deletar(id)
            self.db.close()
            flash('Livro deletado com sucesso!', 'success')
            return redirect('/livros')
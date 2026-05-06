from conexao import DatabaseConnection
from flask import request, render_template, flash, redirect
from routes.Routes import Routes
from services.LivrosAlugadosServices import LivrosAlugadosServices
from services.LivrosServices import LivroServices
from services.UsuarioServices import UsuarioServices
from model.LivrosAlugadosModel import LivrosAlugadosModel

class LivrosAlugadosRoute(Routes):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.db = DatabaseConnection()
        self.register_routes()
        
    def register_routes(self):
        @self.app.route("/alugarLivro", methods=["POST"])
        @Routes.login_required
        def alugar_Livro():
            livroAlugado = LivrosAlugadosModel(
                idusuario = request.form.get("idusuario"),
                idlivro = request.form.get("idlivro"),
                dataAluguel = request.form.get("dataAluguel"),
                dataDevolucao = request.form.get("dataDevolucao")
            )
            self.db.connect()
            livroAlugado = LivrosAlugadosServices(self.db)
            livroAlugado.create(livroAlugado)
            
            # Bloquear o livro alugado
            livro = LivroServices(self.db)
            livro.bloquear_livro(livroAlugado.idlivro)
            
            self.db.close()
            flash('Livro alugado com sucesso!', 'success')
            return redirect("/livrosAlugados")

        @self.app.route("/livrosAlugados", methods=["GET"])
        @Routes.login_required
        def listar_LivrosAlugados():
            self.db.connect()
            livroAlugado = LivrosAlugadosServices(self.db)
            livrosAlugados = livroAlugado.listar_all()
            
            self.db.close()
            return render_template("pages/ListLivrosAlugados.html", livrosAlugados=livrosAlugados), 200
        
        @self.app.route("/alugarLivro", methods=["GET"])
        @Routes.login_required
        def alugDevolLivro():
            self.db.connect()
            livroAlugado_data = LivrosAlugadosModel(idLivrosAlugados=0, idlivro=0, idusuario=0, nome="", titulo="", dataAluguel="", dataDevolucao="", dataEntrega="")
            listaLivros_disponiveis = LivroServices(self.db).listar_livros_disponiveis()
            listaUsuarios = UsuarioServices(self.db).listar_allAtivos()
            self.db.close()
            return render_template("pages/alugDevolLivro.html", livroAlugado=livroAlugado_data, livrosDisponiveis=listaLivros_disponiveis, usuarios=listaUsuarios, acao="novo"), 200
        
        @self.app.route("/livro/<int:id>", methods=["POST", "GET"])
        @Routes.login_required
        def consultar_LivroAlugado(id):
            altLivroAlugado = LivrosAlugadosModel(idLivrosAlugados = id,
                                                  idlivro = request.form.get("idlivro"),
                                                  idusuario = request.form.get("idusuario"),
                                                  dataAluguel = request.form.get("dataAluguel"),
                                                  dataDevolucao = request.form.get("dataDevolucao"),
                                                  dataEntrega = request.form.get("dataEntrega"))
            self.db.connect()
            livroAlugado_service = LivrosAlugadosServices(self.db)
            livroAlugado_service.atualizar(altLivroAlugado)
            
            # Desbloquear o livro alugado
            livro = LivroServices(self.db)
            livro.desbloquear_livro(altLivroAlugado.idlivro)
            
            self.db.close()
            flash('Aluguel atualizado com sucesso!', 'success')
            return redirect('/livrosAlugados')
        
        @self.app.route("/livrosAlugado/<int:id>/editar", methods=["GET"])
        @Routes.login_required
        def atualizar_LivroAlugado(id):
            self.db.connect()
            atualizar_livro_service = LivrosAlugadosServices(self.db)
            livro_Alugado_Data = atualizar_livro_service.consultar_id(id)
            self.db.close()
            return render_template("pages/alugDevolLivro.html", livroAlugado=livro_Alugado_Data, acao="alterar"), 200
        
        @self.app.route("/livrosAlugado/<int:id>/deletar", methods=["GET", "DELETE"])
        @Routes.login_required
        def deletar_LivroAlugado(id):
            self.db.connect()
            livroAlugado_service = LivrosAlugadosServices(self.db)
            livroAlugado_service.deletar(id)
            self.db.close()
            flash('Aluguel deletado com sucesso!', 'success')
            return redirect('/livrosAlugados')
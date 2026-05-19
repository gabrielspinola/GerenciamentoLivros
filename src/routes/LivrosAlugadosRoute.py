from conexao import DatabaseConnection
from flask import request, render_template, flash, redirect
from datetime import datetime, date
from routes.Routes import Routes
from utils.utils import adicionar_dias_uteis
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
        @self.app.context_processor
        def inject_now():
            return {'datetime': datetime}        
        
        #Grava o aluguel realizado   
        @self.app.route("/alugarLivro", methods=["POST"])
        @Routes.login_required
        def alugar_Livro():
            livroAlugado = LivrosAlugadosModel(
                idusuario = request.form.get("idusuario"),
                idlivro = request.form.get("idlivro"),
                dataAluguel = request.form.get("dataAluguel"),
                dataDevolucao = request.form.get("dataDevolucao")
            )
            
            # Validar dados
            if not livroAlugado.idusuario or livroAlugado.idusuario == "0":
                flash('Selecione um usuário válido!', 'error')
                return redirect("/alugarLivro")
            
            if not livroAlugado.idlivro or livroAlugado.idlivro == "0":
                flash('Selecione um livro válido!', 'error')
                return redirect("/alugarLivro")
                        
            self.db.connect()
            livroAlugado_service = LivrosAlugadosServices(self.db)
            livroAlugado_service.create(livroAlugado)
            
            # Bloquear o livro alugado
            livro_services = LivroServices(self.db)
            livro_services.BloqueiaLivroID(livroAlugado.idlivro)
            
            self.db.close()
            flash('Livro alugado com sucesso!', 'success')
            return redirect("/livrosAlugados")

        @self.app.route("/livrosAlugados", methods=["GET"])
        @Routes.login_required
        def listar_LivrosAlugados():
            self.db.connect()
            livroAlugado = LivrosAlugadosServices(self.db)
            livrosAlugados = livroAlugado.listar_all_nao_entregues()
            
            self.db.close()
            return render_template("pages/ListLivrosAlugados.html", livrosAlugados=livrosAlugados), 200
        
        #Abre a tela para realizar um novo aluguel
        @self.app.route("/alugarLivro", methods=["GET"])
        @Routes.login_required
        def novoAluguel():
            self.db.connect()
            livroAlugado_data = LivrosAlugadosModel(idLivrosAlugados=0, idlivro=0, idusuario=0, nome="", titulo="", dataAluguel="", dataDevolucao="", dataEntrega="")
            listaLivros_disponiveis = LivroServices(self.db).listar_livros_disponiveis()
            listaUsuarios = UsuarioServices(self.db).listar_allAtivos()
            data_Prev_Devolucao = adicionar_dias_uteis(date.today(), 7).strftime('%Y-%m-%d')
            self.db.close()
            return render_template("pages/alugDevolLivro.html", livroAlugado=livroAlugado_data, livrosDisponiveis=listaLivros_disponiveis, 
                                                                usuarios=listaUsuarios, data_Prev_Devolucao=data_Prev_Devolucao, 
                                                                acao="novo"), 200
        
        @self.app.route("/alugarLivro/<int:id>", methods=["POST", "GET"])
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
            #LivroServices(self.db).DesbloqueiaLivroID(altLivroAlugado.idlivro)
            
            self.db.close()
            flash('Aluguel atualizado com sucesso!', 'success')
            return redirect('/livrosAlugados')
        
        #Abre a tela para editar um livro alugado
        @self.app.route("/livroAlugado/<int:id>/editar", methods=["GET"])
        @Routes.login_required
        def atualizar_LivroAlugado(id):
            self.db.connect()
            livroAlugado_Data = LivrosAlugadosServices(self.db).consultar_id(id)
            listaLivros_disponiveis = LivroServices(self.db).listar_all()
            listaUsuarios = UsuarioServices(self.db).listar_allAtivos()
            self.db.close()
            return render_template("pages/alugDevolLivro.html", livroAlugado=livroAlugado_Data, livrosDisponiveis=listaLivros_disponiveis, 
                                                                usuarios=listaUsuarios, acao="alterar"), 200
        
        @self.app.route("/livroAlugado/<int:id>/deletar", methods=["GET", "DELETE"])
        @Routes.login_required
        def deletar_LivroAlugado(id):
            self.db.connect()
            livroAlugado_service = LivrosAlugadosServices(self.db)
            aluguel = livroAlugado_service.consultar_id(id)  # Consulta para obter o ID do livro alugado antes de deletar
            livroAlugado_service.deletar(id)
            
            # Desbloquear o livro alugado
            LivroServices(self.db).DesbloqueiaLivroID(aluguel.idlivro)
            
            self.db.close()
            flash('Aluguel disfeito!', 'success')
            return redirect('/livrosAlugados')
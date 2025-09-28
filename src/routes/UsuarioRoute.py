from conexao import DatabaseConnection
from flask import Flask, request, jsonify, render_template, flash, url_for, redirect, session
from functools import wraps
from werkzeug.security import generate_password_hash
from services.UsuarioServices import UsuarioServices
from model.UsuarioModel import UsuarioModel


class UsuarioRoute:
    def __init__(self, app):
        self.app = app
        self.db = DatabaseConnection()
        self.register_routes()

    def register_routes(self):
        def login_required(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if 'username' not in session:
                    flash('Você precisa fazer login primeiro!', 'warning')
                    return redirect(url_for('login'))
                return f(*args, **kwargs)
            return decorated_function
        
        
        @self.app.route("/usuarios", methods=["POST"])
        @login_required
        def create_usuario():
            usuario = UsuarioModel(nome = request.form.get("nome"), 
                                   login = request.form.get("login"), 
                                   password = generate_password_hash(request.form.get("password")), 
                                   dataAniversario = request.form.get("dataAniversario"))
            self.db.connect()
            usuario_service = UsuarioServices(self.db)
            usuario_service.create(usuario)
            self.db.close()
            flash('Usuário criado com sucesso!', 'success')
            return redirect('/usuarios')

        @self.app.route("/usuarios", methods=["GET"])
        @login_required
        def listar_usuarios():
            self.db.connect()
            usuario = UsuarioServices(self.db)
            usuarios = usuario.listar_all()
            
            self.db.close()
            return render_template("pages/ListUsuarios.html", usuarios=usuarios), 200
        
        @self.app.route("/usuario", methods=["GET"])
        @login_required
        def usuario():
            usuario_data = UsuarioModel(idusuario=0, nome="", login="", password="", dataAniversario="", ativo=1)
            return render_template("pages/Usuario.html", usuario=usuario_data, acao="novo"), 200

        @self.app.route("/usuario/<int:id>/editar", methods=["GET"])
        @login_required
        def consultar_usuario(id):
            self.db.connect()
            usuario = UsuarioServices(self.db)
            usuario_data = usuario.consultar_id(id)
            self.db.close()
            return render_template("pages/Usuario.html", usuario=usuario_data, acao="alterar"), 200
        

        @self.app.route("/usuario/<int:id>", methods=["POST", "GET"])
        @login_required
        def atualizar_usuario(id):
            altUsuario = UsuarioModel(idusuario = id,
                                   nome = request.form.get("nome"), 
                                   login = request.form.get("login"), 
                                   password = generate_password_hash(request.form.get("password")), 
                                   dataAniversario = request.form.get("dataAniversario"))

            self.db.connect()
            usuario = UsuarioServices(self.db)
            usuario.atualizar(altUsuario)
            self.db.close()
            flash('Usuário atualizado com sucesso!', 'success')
            return redirect('/usuarios')

        @self.app.route("/usuario/<int:id>/deletar", methods=["DELETE", "GET"])
        @login_required
        def deletar_usuario(id):
            self.db.connect()
            usuario = UsuarioServices(self.db)
            usuario.deletar_id(id)
            self.db.close()
            flash('Usuário deletado com sucesso!', 'success')
            return redirect('/usuarios')
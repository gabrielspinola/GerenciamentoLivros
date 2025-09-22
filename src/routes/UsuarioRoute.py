from conexao import DatabaseConnection
from flask import Flask, request, jsonify, render_template, flash, url_for, redirect, session
from functools import wraps
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
            data = request.json
            usuario = UsuarioModel(nome=data.get("nome"), login=data.get("login"), password=data.get("password"), dataAniversario=data.get("dataAniversario"))

            self.db.connect()
            usuario_service = UsuarioServices(self.db)
            usuario_service.create(usuario)
            self.db.close()
            return jsonify({"message": "Usuário criado com sucesso."}), 201

        @self.app.route("/usuarios", methods=["GET"])
        @login_required
        def listar_usuarios():
            self.db.connect()
            usuario = UsuarioServices(self.db)
            usuarios = usuario.listar_all()
            
            self.db.close()
            return render_template("pages/ListUsuarios.html", usuarios=usuarios), 200

        @self.app.route("/usuarios/<int:id>", methods=["GET"])
        @login_required
        def consultar_usuario(id):
            self.db.connect()
            usuario = UsuarioServices(self.db)
            usuario_data = usuario.consultar_id(id)
            self.db.close()
            return jsonify(usuario_data), 200

        @self.app.route("/usuarios/<int:id>", methods=["PUT"])
        @login_required
        def atualizar_usuario(id):
            data = request.json
            nome = data.get("nome")
            login = data.get("login")
            password = data.get("password")
            dataAniversario = data.get("dataAniversario")

            self.db.connect()
            usuario = UsuarioServices(self.db)
            usuario.atualizar(id, nome, login, password, dataAniversario)
            self.db.close()
            return jsonify({"message": "Usuário atualizado com sucesso."}), 200

        @self.app.route("/usuarios/<int:id>", methods=["DELETE"])
        @login_required
        def deletar_usuario(id):
            self.db.connect()
            usuario = UsuarioServices(self.db)
            usuario.deletar_id(id)
            self.db.close()
            return jsonify({"message": "Usuário deletado com sucesso."}), 200
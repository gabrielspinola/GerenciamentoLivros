from conexao import DatabaseConnection
from flask import Flask, request, jsonify
from services.UsuarioServices import UsuarioServices


class UsuarioRoute:
    def __init__(self, app):
        self.app = app
        self.db = DatabaseConnection()
        self.register_routes()

    def register_routes(self):
        @self.app.route("/usuarios", methods=["POST"])
        def create_usuario():
            data = request.json
            nome = data.get("nome")
            login = data.get("login")
            password = data.get("password")
            dataAniversario = data.get("dataAniversario")

            self.db.connect()
            usuario = UsuarioServices(self.db)
            usuario.create(nome, login, password, dataAniversario)
            self.db.close()
            return jsonify({"message": "Usuário criado com sucesso."}), 201

        @self.app.route("/usuarios", methods=["GET"])
        def listar_usuarios():
            self.db.connect()
            usuario = UsuarioServices(self.db)
            usuarios = usuario.listar_all()
            self.db.close()
            return jsonify(usuarios), 200

        @self.app.route("/usuarios/<int:id>", methods=["GET"])
        def consultar_usuario(id):
            self.db.connect()
            usuario = UsuarioServices(self.db)
            usuario_data = usuario.consultar_id(id)
            self.db.close()
            return jsonify(usuario_data), 200

        @self.app.route("/usuarios/<int:id>", methods=["PUT"])
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
        def deletar_usuario(id):
            self.db.connect()
            usuario = UsuarioServices(self.db)
            usuario.deletar_id(id)
            self.db.close()
            return jsonify({"message": "Usuário deletado com sucesso."}), 200
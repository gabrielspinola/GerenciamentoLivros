import os
from conexao import DatabaseConnection
from flask import Flask, request, render_template #jsonify

class PrincRoute:
    def __init__(self, app):
        self.app = app
        self.db = DatabaseConnection()
        self.register_routes()

    def register_routes(self):
        @self.app.route("/", methods=["GET"])
        def carregar_principal():
            template_dir = os.path.join(self.app.root_path, 'templates')
            return render_template("pages/home.html", template_dir=template_dir), 200
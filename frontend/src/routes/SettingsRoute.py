from flask import request, render_template, flash, redirect, session
from routes.Routes import Routes
from services.SettingsServices import SettingsServices
from model.SettingsModel import SettingsModel

class SettingsRoute(Routes):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.register_routes()
        
    def register_routes(self):
        @self.app.route("/settings", methods=["POST"])
        @Routes.login_required
        def create_settings():            
            settings = SettingsModel(idsettings = request.form.get("idsettings"),
                                     diasLivroEmprestado = request.form.get("diasLivroEmprestado"))

            settings_service = SettingsServices(username=session.get('username'), password=session.get('usuario_pass'))
            settings_data = settings_service.criar_atualizar(settings)
        
            flash('Configurações salvas com sucesso!', 'success')
            return render_template("pages/Settings.html", settings=settings_data), 200

        @self.app.route("/settings", methods=["GET"])
        @Routes.login_required
        def listar_settings():
            settings_service = SettingsServices(username=session.get('username'), password=session.get('usuario_pass'))
            settings = settings_service.listar_config()
            
            return render_template("pages/Settings.html", settings=settings), 200
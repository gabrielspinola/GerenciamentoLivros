from conexao import DatabaseConnection
from flask import request, render_template, flash, redirect
from routes.Routes import Routes
from services.SettingsServices import SettingsServices
from model.SettingsModel import SettingsModel

class SettingsRoute(Routes):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.db = DatabaseConnection()
        self.register_routes()
        
    def register_routes(self):
        @self.app.route("/settings", methods=["POST"])
        @Routes.login_required
        def create_settings():
            
            settings = SettingsModel(idsettings = request.form.get("idsettings"),
                                     diasLivroEmprestado = request.form.get("diasLivroEmprestado"))
            self.db.connect()
            
            if settings.idsettings == "": 
                settings_service_gravar = SettingsServices(self.db)
                settings_service_gravar.create(settings)            
            else:
                settings_service_atualizar = SettingsServices(self.db)
                settings_service_atualizar.update(settings)
            
            settings_service_consulta = SettingsServices(self.db)
            settings_data = settings_service_consulta.listar_all()
            self.db.close()
            
            flash('Configurações salvas com sucesso!', 'success')
            return render_template("pages/Settings.html", settings=settings_data), 200

        @self.app.route("/settings", methods=["GET"])
        @Routes.login_required
        def listar_settings():
            self.db.connect()
            settings_service = SettingsServices(self.db)
            settings = settings_service.listar_config()
            
            self.db.close()
            return render_template("pages/Settings.html", settings=settings), 200
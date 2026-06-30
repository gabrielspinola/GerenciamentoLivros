from conexao import DatabaseConnection
from flask import request, render_template, flash, redirect
from routes.Routes import Routes
from werkzeug.security import generate_password_hash
from services.UsuarioServices import UsuarioServices
from model.UsuarioModel import UsuarioModel
from utils.email_utils import generate_confirmation_token, send_confirmation_email, verify_confirmation_token

class UsuarioRoute(Routes):
    def __init__(self, app):
        self.app = app
        self.db = DatabaseConnection()
        self.register_routes()

    def register_routes(self):
        @self.app.route("/usuarios", methods=["POST"])
        @Routes.login_required
        def create_usuario():
            usuario = UsuarioModel(nome = request.form.get("nome"), 
                                   login = request.form.get("login"), 
                                   password = generate_password_hash(request.form.get("password")), 
                                   dataAniversario = request.form.get("dataAniversario"),
                                   email = request.form.get("email"))
            self.db.connect()
            usuario_service = UsuarioServices(self.db)
            usuario_service.create(usuario)
            self.db.close()
            flash('Usuário criado com sucesso!', 'success')
            return redirect('/usuarios')

        @self.app.route("/usuarios", methods=["GET"])
        @Routes.login_required
        def listar_usuarios():
            self.db.connect()
            usuario = UsuarioServices(self.db)
            usuarios = usuario.listar_all()
            
            self.db.close()
            return render_template("pages/ListUsuarios.html", usuarios=usuarios), 200
        
        @self.app.route("/usuario", methods=["GET"])
        @Routes.login_required
        def usuario():
            usuario_data = UsuarioModel(idusuario=0, nome="", login="", password="", dataAniversario="", ativo=1, email="")
            return render_template("pages/Usuario.html", usuario=usuario_data, acao="novo"), 200

        @self.app.route("/usuario/<int:id>/editar", methods=["GET"])
        @Routes.login_required
        def consultar_usuario(id):
            self.db.connect()
            usuario = UsuarioServices(self.db)
            usuario_data = usuario.consultar_id(id)
            self.db.close()
            return render_template("pages/Usuario.html", usuario=usuario_data, acao="alterar"), 200
        

        @self.app.route("/usuario/<int:id>", methods=["POST", "GET"])
        @Routes.login_required
        def atualizar_usuario(id):
            altUsuario = UsuarioModel(idusuario = id,
                                   nome = request.form.get("nome"), 
                                   login = request.form.get("login"), 
                                   password = generate_password_hash(request.form.get("password")), 
                                   dataAniversario = request.form.get("dataAniversario"),
                                   email = request.form.get("email"))

            self.db.connect()
            usuario = UsuarioServices(self.db)
            usuario.atualizar(altUsuario)
            self.db.close()
            flash('Usuário atualizado com sucesso!', 'success')
            return redirect('/usuarios')

        @self.app.route("/usuario/<int:id>/deletar", methods=["DELETE", "GET"])
        @Routes.login_required
        def deletar_usuario(id):
            self.db.connect()
            usuario = UsuarioServices(self.db)
            usuario.deletar_id(id)
            self.db.close()
            flash('Usuário deletado com sucesso!', 'success')
            return redirect('/usuarios')
        
        @self.app.route('/cadastro', methods=['GET', 'POST'])
        def cadastro():
            if request.method == 'POST':
                nome = request.form.get('nome', '').strip()
                login = request.form.get('login', '').strip()
                password = request.form.get('password', '')
                email = request.form.get('email', '').strip()
                dataAniversario = request.form.get('dataAniversario', '').strip()

                if not nome or not login or not password or not email:
                    flash('Preencha todos os campos.', 'error')
                    return render_template('pages/cadastro.html')

                self.db.connect()
                usuario_service = UsuarioServices(self.db)
                usuario_existente = usuario_service.consultar_login(login)
                if usuario_existente is not None:
                    self.db.close()
                    flash('Já existe um usuário com este login.', 'warning')
                    return render_template('pages/cadastro.html')

                from werkzeug.security import generate_password_hash
                usuario = UsuarioModel(nome=nome, login=login, password=generate_password_hash(password), dataAniversario=dataAniversario, email=email, ativo='I')
                usuario_service.create(usuario)
                self.db.close()

                token = generate_confirmation_token(email, login)
                send_confirmation_email(email, nome, token)
                flash('Conta criada! Verifique seu e-mail para confirmar o cadastro.', 'success')
                return redirect('/login')

            return render_template('pages/cadastro.html')
        
        @self.app.route('/confirmar-email/<token>')
        def confirmar_email(token):
            data = verify_confirmation_token(token)
            if not data:
                flash('Link inválido ou expirado.', 'error')
                return redirect('/login')

            self.db.connect()
            usuario_service = UsuarioServices(self.db)
            usuario = usuario_service.consultar_login(data.get('login'))
            if usuario is None:
                self.db.close()
                flash('Usuário não encontrado.', 'error')
                return redirect('/login')

            if usuario.email == data.get('email'):
                self.db.cursor.execute("UPDATE usuarios SET ativo = 'A' WHERE login = %s", (data.get('login'),))
                self.db.connection.commit()
                flash('E-mail confirmado com sucesso! Você já pode entrar.', 'success')
            else:
                flash('Não foi possível confirmar este e-mail.', 'error')
            self.db.close()
            return redirect('/login')

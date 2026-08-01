from flask import request, render_template, flash, redirect, session
from routes.Routes import Routes
from werkzeug.security import generate_password_hash
from services.UsuarioServices import UsuarioServices
from model.UsuarioModel import UsuarioModel, UsuarioModelVazio

class UsuarioRoute(Routes):
    def __init__(self, app):
        self.app = app
        self.register_routes()

    def register_routes(self):
        @self.app.route("/usuarios", methods=["POST"])
        @Routes.login_required
        def create_usuario():
            usuario = UsuarioModel(nome = request.form.get("nome"), 
                                   login = request.form.get("login"), 
                                   password = generate_password_hash(request.form.get("password")), 
                                   dataAniversario = request.form.get("dataAniversario"),
                                   ativo="A",
                                   email = request.form.get("email"))

            usuario_service = UsuarioServices(username=session.get('username'), password=session.get('usuario_pass'))
            usuario_service.create(usuario)
            flash('Usuário criado com sucesso!', 'success')
            return redirect('/usuarios')

        @self.app.route("/usuarios", methods=["GET"])
        @Routes.login_required
        def listar_usuarios():
            usuario = UsuarioServices(username=session.get('username'), password=session.get('usuario_pass'))
            usuarios = usuario.listar_all()
            
            return render_template("pages/ListUsuarios.html", usuarios=usuarios), 200
        
        @self.app.route("/usuario", methods=["GET"])
        @Routes.login_required
        def usuario():
            usuario_data = UsuarioModelVazio()
            return render_template("pages/Usuario.html", usuario=usuario_data, acao="novo"), 200

        @self.app.route("/usuario/<int:id>/editar", methods=["GET"])
        @Routes.login_required
        def consultar_usuario(id):
            usuario = UsuarioServices(username=session.get('username'), password=session.get('usuario_pass'))
            usuario_data = usuario.consultar_id(id)
            return render_template("pages/Usuario.html", usuario=usuario_data, acao="alterar"), 200
        

        @self.app.route("/usuario/<int:id>", methods=["POST", "GET"])
        @Routes.login_required
        def atualizar_usuario(id):
            altUsuario = UsuarioModel(idusuario = id,
                                      nome = request.form.get("nome"), 
                                      login = request.form.get("login"), 
                                      password = generate_password_hash(request.form.get("password")), 
                                      dataAniversario = request.form.get("dataAniversario"),
                                      ativo="A",
                                      email = request.form.get("email"))


            usuario = UsuarioServices(username=session.get('username'), password=session.get('usuario_pass'))
            usuario.atualizar(altUsuario)
            flash('Usuário atualizado com sucesso!', 'success')
            return redirect('/usuarios')

        @self.app.route("/usuario/<int:id>/deletar", methods=["DELETE", "GET"])
        @Routes.login_required
        def deletar_usuario(id):
            usuario = UsuarioServices(username=session.get('username'), password=session.get('usuario_pass'))
            usuario.deletar_id(id)
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

                usuario_service = UsuarioServices(username="", password="")
                usuario_existente = usuario_service.validar_login(login)
                if usuario_existente:
                    flash('Já existe um usuário com este login.', 'warning')
                    return render_template('pages/cadastro.html')

                from werkzeug.security import generate_password_hash
                usuario = UsuarioModel(nome=nome, login=login, password=generate_password_hash(password), dataAniversario=dataAniversario, email=email, ativo='I')
                usuario_service.create_com_email(usuario)

                flash('Conta criada! Verifique seu e-mail para confirmar o cadastro.', 'success')
                return redirect('/login')

            return render_template('pages/cadastro.html')
        
        @self.app.route('/confirmar-email/<token>')
        def confirmar_email(token):
            if not token:
                flash('Token inválido.', 'error')
                return redirect('/login')

            usuario_service = UsuarioServices(username="", password="")
            usuario_Validado = usuario_service.valida_token(token)
            if usuario_Validado:
                flash('E-mail confirmado com sucesso! Você já pode entrar.', 'success')
                return redirect('/login')                
            else:
                flash('Não foi possível confirmar este e-mail.', 'error')
            return redirect('/login')

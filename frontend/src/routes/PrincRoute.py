import os
from flask import request, render_template, flash, redirect, session 
from werkzeug.security import check_password_hash

from routes.Routes import Routes
from services.UsuarioServices import UsuarioServices

class PrincRoute(Routes):
    def __init__(self, app):
        self.app = app
        self.register_routes()

    def register_routes(self):
        @self.app.route('/')
        def inicio():
            if 'username' in session:
                return redirect("/home")
            return redirect("/login")

        @self.app.route("/home", methods=["GET"])
        @Routes.login_required
        def home():
            template_dir = os.path.join(self.app.root_path, 'templates')
            return render_template("pages/home.html", template_dir=template_dir), 200
        
        @self.app.route("/about", methods=["GET"])
        @Routes.login_required
        def about():
            template_dir = os.path.join(self.app.root_path, 'templates')
            return render_template("pages/about.html", template_dir=template_dir), 200
        
        
        @self.app.route('/login', methods=['GET', 'POST'])
        def login():
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                
                # self.db.connect()
                usuario = UsuarioServices(username, password)
                usu = usuario.consultar_login(username, password)
                                
                if usu != None:
                    if username == usu.login and check_password_hash(usu.password, password):
                        if usu.ativo != 'A':
                            flash('Confirme seu cadastro antes de entrar.', 'warning')
                            return render_template('pages/login.html')
                        session['username'] = username
                        session['usuario_pass'] = password
                        session['name'] = usu.nome
                        flash(f'Bem-vindo, {usu.nome}!', 'success')
                        return redirect('/home')
                    else:
                        flash('Usuário ou senha incorretos!', 'error')
                        return render_template('pages/login.html')
                else:
                    flash('Usuário ou senha incorretos!', 'error')
                    return render_template('pages/login.html')
                    
            return render_template('pages/login.html')
        
        @self.app.route('/logout')
        def logout():
            session.pop('username', None)
            session.pop('name', None)
            session.pop('usuario_completo', None)
            session.clear()
            #flash('Você saiu com sucesso!', 'success')
            return redirect('/login')
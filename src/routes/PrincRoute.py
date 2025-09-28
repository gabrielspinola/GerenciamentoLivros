import os
from conexao import DatabaseConnection
from flask import Flask, request, render_template, flash, redirect, session 
from werkzeug.security import check_password_hash
from functools import wraps
from services.UsuarioServices import UsuarioServices

class PrincRoute:
    def __init__(self, app):
        self.app = app
        self.db = DatabaseConnection()
        self.register_routes()    

    def register_routes(self):
        # Decorator para rotas que precisam de autenticação
        def login_required(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if 'username' not in session:
                    flash('Você precisa fazer login primeiro!', 'warning')
                    return redirect("/login")
                return f(*args, **kwargs)
            return decorated_function

        @self.app.route('/')
        def inicio():
            if 'username' in session:
                return redirect("/home")
            return redirect("/login")

        
        @self.app.route("/home", methods=["GET"])
        @login_required
        def home():
            template_dir = os.path.join(self.app.root_path, 'templates')
            return render_template("pages/home.html", template_dir=template_dir), 200
        
        @self.app.route("/about", methods=["GET"])
        @login_required
        def about():
            template_dir = os.path.join(self.app.root_path, 'templates')
            return render_template("pages/about.html", template_dir=template_dir), 200
        
        
        @self.app.route('/login', methods=['GET', 'POST'])
        def login():
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                
                self.db.connect()
                usuario = UsuarioServices(self.db)
                usu = usuario.consultar_login(username)
                
                self.db.close()
                
                # Verificar se o usuário existe e a senha está correta
                if usu != None:
                    if username == usu.login and check_password_hash(usu.password, password):
                        session['username'] = username
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
            session.clear()
            #flash('Você saiu com sucesso!', 'success')
            return redirect('/login')
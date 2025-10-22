from functools import wraps
from flask import session, flash, redirect, url_for

class Routes:
    def __init__(self):
        pass

    # Decorator para rotas que precisam de autenticação
    @staticmethod
    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'username' not in session:
                flash('Você precisa fazer login primeiro!', 'warning')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function
    
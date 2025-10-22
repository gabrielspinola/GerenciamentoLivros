from flask import Flask, request, redirect
from routes.UsuarioRoute import UsuarioRoute
from routes.LivroRoute import LivroRoute
from routes.PrincRoute import PrincRoute

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui_mude_em_producao'
app.permanent_session_lifetime = 600  # Sessão expira após 10 minutos de inatividade

if __name__ == "__main__":
    principal = PrincRoute(app)
    user = UsuarioRoute(app)
    livro = LivroRoute(app)
    app.run(host="localhost",port=8080,debug=True) #(host="0.0.0.0", port=5000, debug=True)


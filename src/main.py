from flask import Flask, request
from routes.UsuarioRoute import UsuarioRoute
from routes.PrincRoute import PrincRoute

app = Flask(__name__)

if __name__ == "__main__":
    user = UsuarioRoute(app)
    principal = PrincRoute(app)
    app.run(host="localhost",port=8080,debug=True) #(host="0.0.0.0", port=5000, debug=True)

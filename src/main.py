from flask import Flask, request, jsonify
from routes.UsuarioRoute import UsuarioRoute


app = Flask(__name__)

if __name__ == "__main__":
    pass 
    #db = DatabaseConnection()
    #db.connect()
    #usuario = Usuario(db)
    #usuario.create("Sem nome", "s.nome", "123456", "2000-01-01")
    #usuario.deletar_id(4)
    #usuario.atualizar(5, nome="Maria da Silva", login="mar.silva", password="456321", dataAniversario="2001-03-25")
    #usuario.listar_all()
    #db.close()

    user = UsuarioRoute(app)    
    app.run(debug=True)
    
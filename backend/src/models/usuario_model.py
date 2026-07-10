from typing import List, Dict, Optional

_usuarios: List[Dict[str, str]] = [
    {"username": "admin", "senha": "admin123"},
]


def usuario_existe(username: str) -> bool:
    return any(u["username"] == username for u in _usuarios)


def criar_usuario(username: str, senha: str) -> Dict[str, str]:
    usuario = {"username": username, "senha": senha}
    _usuarios.append(usuario)
    return usuario


def validar_credenciais(username: str, senha: str) -> bool:
    return any(u["username"] == username and u["senha"] == senha for u in _usuarios)

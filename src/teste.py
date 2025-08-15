from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional
import mysql.connector
from mysql.connector import Error

@dataclass
class Usuario:
    id: Optional[int] = None
    nome: str = ""
    email: str = ""
    senha: str = ""
    created_at: Optional[datetime] = None
    status: str = "ativo"
    
    def to_dict(self) -> dict:
        """Converte para dicionário"""
        data = asdict(self)
        if self.created_at:
            data['created_at'] = self.created_at.isoformat()
        return data
    
    @classmethod
    def from_row(cls, row: tuple) -> 'Usuario':
        """Cria instância a partir de uma linha do banco"""
        return cls(
            id=row[0],
            nome=row[1],
            email=row[2],
            senha=row[3],
            created_at=row[4],
            status=row[5]
        )

class DatabaseConnection:
    def __init__(self, host='localhost', database='nome_do_banco', 
                 user='usuario', password='senha'):
        self.config = {
            'host': host,
            'database': database,
            'user': user,
            'password': password
        }
        self.connection = None
    
    def __enter__(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
            return self.connection
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")
            raise
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection and self.connection.is_connected():
            self.connection.close()

class UsuarioService:
    def __init__(self, db_config: dict):
        self.db_config = db_config
    
    def buscar_todos(self) -> List[Usuario]:
        """Busca todos os usuários e retorna lista de objetos Usuario"""
        with DatabaseConnection(**self.db_config) as conn:
            cursor = conn.cursor()
            
            query = """
                SELECT id, nome, email, senha, created_at, status 
                FROM usuarios 
                ORDER BY id
            """
            
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            
            # Converte cada linha em objeto Usuario
            return [Usuario.from_row(row) for row in rows]
    
    def buscar_por_id(self, usuario_id: int) -> Optional[Usuario]:
        """Busca usuário por ID"""
        with DatabaseConnection(**self.db_config) as conn:
            cursor = conn.cursor()
            
            query = """
                SELECT id, nome, email, senha, created_at, status 
                FROM usuarios 
                WHERE id = %s
            """
            
            cursor.execute(query, (usuario_id,))
            row = cursor.fetchone()
            cursor.close()
            
            return Usuario.from_row(row) if row else None
    
    def buscar_ativos(self) -> List[Usuario]:
        """Busca apenas usuários ativos"""
        with DatabaseConnection(**self.db_config) as conn:
            cursor = conn.cursor()
            
            query = """
                SELECT id, nome, email, senha, created_at, status 
                FROM usuarios 
                WHERE status = 'ativo'
                ORDER BY nome
            """
            
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            
            return [Usuario.from_row(row) for row in rows]
    
    def criar_usuario(self, usuario: Usuario) -> Optional[Usuario]:
        """Cria novo usuário no banco"""
        with DatabaseConnection(**self.db_config) as conn:
            cursor = conn.cursor()
            
            query = """
                INSERT INTO usuarios (nome, email, senha, created_at, status)
                VALUES (%s, %s, %s, %s, %s)
            """
            
            values = (
                usuario.nome,
                usuario.email,
                usuario.senha,
                usuario.created_at or datetime.now(),
                usuario.status
            )
            
            cursor.execute(query, values)
            conn.commit()
            
            # Busca o usuário recém criado
            usuario_id = cursor.lastrowid
            cursor.close()
            
            return self.buscar_por_id(usuario_id)
    
    def atualizar_usuario(self, usuario_id: int, **kwargs) -> Optional[Usuario]:
        """Atualiza campos específicos do usuário"""
        campos_validos = ['nome', 'email', 'senha', 'status']
        updates = []
        values = []
        
        for campo, valor in kwargs.items():
            if campo in campos_validos:
                updates.append(f"{campo} = %s")
                values.append(valor)
        
        if not updates:
            return self.buscar_por_id(usuario_id)
        
        with DatabaseConnection(**self.db_config) as conn:
            cursor = conn.cursor()
            
            query = f"""
                UPDATE usuarios 
                SET {', '.join(updates)}
                WHERE id = %s
            """
            
            values.append(usuario_id)
            cursor.execute(query, values)
            conn.commit()
            cursor.close()
            
            return self.buscar_por_id(usuario_id)

# Exemplo de uso
def exemplo_uso():
    # Configuração do banco
    db_config = {
        'host': 'localhost',
        'database': 'meu_banco',
        'user': 'usuario',
        'password': 'senha'
    }
    
    service = UsuarioService(db_config)
    
    # Buscar todos os usuários como objetos
    usuarios = service.buscar_todos()
    print("Usuários encontrados:")
    for usuario in usuarios:
        print(f"- {usuario.nome} ({usuario.email}) - Status: {usuario.status}")
    
    # Buscar usuário específico
    usuario = service.buscar_por_id(1)
    if usuario:
        print(f"\nUsuário ID 1: {usuario.to_dict()}")
    
    # Criar novo usuário
    novo_usuario = Usuario(
        nome="Maria Silva",
        email="maria@email.com",
        senha="senha123"
    )
    
    usuario_criado = service.criar_usuario(novo_usuario)
    if usuario_criado:
        print(f"\nUsuário criado: {usuario_criado.to_dict()}")

if __name__ == "__main__":
    exemplo_uso()
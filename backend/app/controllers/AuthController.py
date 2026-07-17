from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from models.token import Token, UserLogin, UserInDB
from repositories.UsuarioRepository import UsuarioRepository
from utils.security import Security
import jwt

router = APIRouter(prefix="/auth", tags=["Autenticação"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
security = Security()

@router.post("/login", response_model=Token)
async def login(dados: UserLogin):
    usuario_repository = UsuarioRepository()
    usuario = usuario_repository.get_by_username(dados.login)

    if not usuario or not security.verify_password(usuario.password, dados.password ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )    
    
    access_token = security.create_access_token(data={"sub": usuario.login})
    return Token(access_token=access_token)


def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = security.decode_access_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado, faça login novamente",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise credentials_exception

    usuario_repository = UsuarioRepository()
    user = usuario_repository.get_by_username(username)
    if user is None:
        raise credentials_exception

    return user

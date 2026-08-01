from fastapi import APIRouter, Depends, status

from models.setting import Settings
from repositories.SettingRepository import SettingRepository
from models.token import UserInDB
from controllers.AuthController import get_current_user

router = APIRouter(prefix="/settings", tags=["Settings"])

@router.get("/", response_model=Settings, summary="Retorna a configuração", description="Retorna todas as configurações do sistema. Requer autenticação.")
async def listar_settings(usuario_atual: UserInDB = Depends(get_current_user)):
    return SettingRepository().obter_settings()

@router.post("/", response_model=Settings, status_code=status.HTTP_201_CREATED, summary="Cria ou atualiza as configurações", description="Realiza a criação ou atualização das configurações. Requer autenticação.")
async def criar_configuracao(settings: Settings, usuario_atual: UserInDB = Depends(get_current_user)):
    if settings.idsettings == "":
        SettingRepository().criar(settings)    
    else:
        SettingRepository().atualizar(settings)
    return SettingRepository().obter_settings()
import logging
import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.trustedhost import TrustedHostMiddleware
from controllers import LivroController, UsuarioController, AuthController, SettingsController, LivrosAlugadosController
from utils.middleware import RequestIDMiddleware, ProcessTimeMiddleware

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()  # continua mostrando no terminal também
    ]
)
logging.getLogger("watchfiles").setLevel(logging.WARNING)

app = FastAPI(
    title="API de Livros",
    description="API para gestão de livros com autenticação JWT",
    version="1.0.2",
)

app.include_router(LivroController.router)
app.include_router(UsuarioController.router)
app.include_router(AuthController.router)
app.include_router(SettingsController.router)
app.include_router(LivrosAlugadosController.router)

app.add_middleware(ProcessTimeMiddleware)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["127.0.0.1", "localhost"])
#Rejeita requisições que cheguem com um header Host forjado/diferente do esperado — proteção simples contra um tipo de ataque de manipulação de host. Em produção, você trocaria pelos domínios reais

# app.add_middleware(AuthController.JWTBearerMiddleware) 
# Realiza a autenticação JWT para todas as rotas, 
# mas não é necessário pois cada rota já possui a dependência de autenticação. 
# Caso seja usada essa linha as rotas de login e cadastro de usuário não funcionam, pois não possuem autenticação.

#@app.get("/")
#async def root():
#    return {"message": "Bem-vindo à API de Livros! Acesse /docs para o Swagger."}

#Rota criada temporariamente para testar o middleware de tratamento de erros. A rota gera um erro 500 propositalmente.
#@app.get("/testar-erro-500")
#async def testar_erro_500():
#    return 1 / 0  #

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    request_id = get_request_id(request)
    logger.error(f"[{request_id}] Erro não tratado em {request.url}: {exc}", exc_info=True)
 
    response = JSONResponse(
        status_code=500,
        content={"detail": "Erro interno no servidor.", "request_id": request_id},
    )
    # Ver docstring do RequestIDMiddleware: exceções genéricas não passam pelos
    # middlewares customizados, então os headers precisam ser adicionados aqui.
    response.headers["X-Request-ID"] = request_id
    start_time = request.scope.get("state", {}).get("start_time")
    if start_time is not None:
        response.headers["X-Process-Time"] = f"{time.perf_counter() - start_time:.4f}"
    return response


def get_request_id(request: Request) -> str:
    return request.scope.get("state", {}).get("request_id", "sem-id")
 

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging

from controllers import LivroController
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
    version="1.0.0",
)

app.include_router(LivroController.router)

#@app.get("/")
#async def root():
#    return {"message": "Bem-vindo à API de Livros! Acesse /docs para o Swagger."}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Erro não tratado em {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno no servidor."},
    )
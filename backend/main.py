from fastapi import FastAPI
from controllers import auth_controller, livro_controller

app = FastAPI(
    title="API de Livros",
    description="API para gestão de livros com autenticação JWT",
    version="1.0.0",
)

app.include_router(auth_controller.router)
app.include_router(livro_controller.router)

@app.get("/")
async def root():
    return {"message": "Bem-vindo à API de Livros! Acesse /docs para o Swagger."}
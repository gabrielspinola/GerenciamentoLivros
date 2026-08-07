import time
import uuid

class RequestIDMiddleware:
    """
    Middleware ASGI puro (não usa BaseHTTPMiddleware) para evitar um bug conhecido
    do Starlette, onde cabeçalhos adicionados após call_next() não aparecem em
    respostas geradas por exception_handlers de exceções genéricas (essas passam
    pelo ServerErrorMiddleware, que fica FORA dos middlewares de add_middleware()).
 
    Guarda um ID único por requisição em request.state.request_id, disponível
    inclusive dentro do global_exception_handler, e devolve esse ID no header
    X-Request-ID — útil pra rastrear uma requisição específica nos logs.
    """
 
    def __init__(self, app):
        self.app = app
 
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
 
        request_id = str(uuid.uuid4())
        scope["state"] = scope.get("state", {})
        scope["state"]["request_id"] = request_id
 
        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                headers = message.setdefault("headers", [])
                headers.append((b"x-request-id", request_id.encode()))
            await send(message)
 
        await self.app(scope, receive, send_wrapper)
 
 
class ProcessTimeMiddleware:
    """
    Middleware ASGI puro. Mede o tempo de resposta de cada requisição e devolve
    no header X-Process-Time (em segundos) — útil pra identificar endpoints lentos
    sem precisar instrumentar ferramenta externa.
    """
 
    def __init__(self, app):
        self.app = app
 
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
 
        start = time.perf_counter()
        scope["state"] = scope.get("state", {})
        scope["state"]["start_time"] = start
 
        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                duration = time.perf_counter() - start
                headers = message.setdefault("headers", [])
                headers.append((b"x-process-time", f"{duration:.4f}".encode()))
            await send(message)
 
        await self.app(scope, receive, send_wrapper)

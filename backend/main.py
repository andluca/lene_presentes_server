from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
from auth.jwt import verify_token
from auth.routes import auth_router
from users.routes import users_router
from products.routes import products_router

app = FastAPI()

@app.middleware("http")
async def jwt_middleware(request: Request, call_next):
    public_paths = [
        "/auth/login",
        "/docs",
        "/openapi.json",
        "/products/",
    ]

    is_public = (
        request.url.path == "/products/" or
        request.url.path == "/products" or
        any(request.url.path.startswith(path) for path in ["/auth/login", "/docs", "/openapi.json"])
    )

    if request.method == "GET" and is_public:
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"detail": "Token não enviado"})

    token = auth_header.split(" ")[1]
    payload = verify_token(token)
    if not payload:
        return JSONResponse(status_code=401, content={"detail": "Token inválido ou expirado"})

    request.state.user = payload

    return await call_next(request)
        
app.include_router(users_router)
app.include_router(products_router)
app.include_router(auth_router)
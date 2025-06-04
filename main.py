from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from backend.auth.jwt import verify_token
from backend.auth.routes import auth_router
from backend.users.routes import users_router
from backend.products.routes import products_router
import backend.config

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def jwt_middleware(request: Request, call_next):
    public_paths = [
        "/auth/login",
        "/docs",
        "/openapi.json",
        "/products/",
        "/products"
    ]
    is_public = any(request.url.path.startswith(path) for path in public_paths)

    if is_public:
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
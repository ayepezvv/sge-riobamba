from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth, users, roles, permissions, parametros, territorio, ciudadanos, comercial

app = FastAPI(
    title="SGE API",
    version="1.0.0",
    description="Backend del Sistema de Gestión Empresarial"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "Servidor SGE activo y funcionando."}

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(roles.router, prefix="/api/roles", tags=["roles"])
app.include_router(permissions.router, prefix="/api/permissions", tags=["permissions"])
app.include_router(parametros.router, prefix="/api/parametros", tags=["parametros"])
app.include_router(territorio.router, prefix="/api/territorio", tags=["territorio"])
app.include_router(ciudadanos.router, prefix="/api/ciudadanos", tags=["ciudadanos"])
app.include_router(comercial.router, prefix="/api/comercial", tags=["comercial"])


import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth, users, roles, permissions, parametros, territorio, ciudadanos, comercial, contratacion, administrativo, informatica, rrhh
from app.db.seed import run_startup_seed


@asynccontextmanager
async def lifespan(app: FastAPI):
    run_startup_seed()
    yield


app = FastAPI(
    title="SGE API",
    version="1.0.0",
    description="Backend del Sistema de Gestión Empresarial",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get("SGE_CORS_ORIGIN", "http://192.168.1.15:3000")],
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
app.include_router(contratacion.router, prefix="/api/contratacion", tags=["contratacion"])
app.include_router(administrativo.router, prefix="/api/administrativo", tags=["administrativo"])
app.include_router(informatica.router, prefix="/api/informatica", tags=["informatica"])
app.include_router(rrhh.router, prefix="/api/rrhh", tags=["RRHH V3"])
from app.api.routes import bodega
app.include_router(bodega.router, prefix="/api/bodega", tags=["bodega"])


from app.api.routes import contabilidad
app.include_router(contabilidad.router, prefix="/api/contabilidad", tags=["Contabilidad"])

from app.api.routes import tesoreria
app.include_router(tesoreria.router, prefix="/api/tesoreria", tags=["Tesorería"])

from app.api.routes import financiero
app.include_router(financiero.router, prefix="/api/financiero", tags=["Financiero"])

from app.api.routes import presupuesto
app.include_router(presupuesto.router, prefix='/api/presupuesto', tags=['Presupuesto'])

from app.api.routes import compras_publicas
app.include_router(compras_publicas.router, prefix='/api/compras', tags=['Compras Públicas'])

from app.api.routes import nomina
app.include_router(nomina.router, prefix='/api/rrhh/nomina', tags=['Nómina / Rol de Pagos'])

from app.api.routes import inventario
app.include_router(inventario.router, prefix="/api/inventario", tags=["Inventario / Existencias"])

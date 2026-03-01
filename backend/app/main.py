from fastapi import FastAPI

app = FastAPI(
    title="SGE API",
    version="1.0.0",
    description="Backend del Sistema de Gestión Empresarial"
)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "Servidor SGE activo y funcionando."}

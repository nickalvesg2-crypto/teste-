from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.core.database import Base, engine
from backend.core.middleware import ExceptionHandlerMiddleware
from backend.reunioes.controller import router as reuniao_router
from backend.usuario.controller import router as usuario_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Sistema de Gestão de Reuniões Escolares",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


# ==========================================
# CORS
# ==========================================

origins = [
    "https://teste-frontend-j16d.onrender.com",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "http://localhost:5175",
    "http://127.0.0.1:5175",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# TRATAMENTO DE EXCEÇÕES
# ==========================================

app.add_middleware(ExceptionHandlerMiddleware)


# ==========================================
# ROUTERS
# ==========================================

app.include_router(usuario_router)
app.include_router(reuniao_router)


# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/", tags=["Health"])
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
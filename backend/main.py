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

# 1. Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Middleware Customizado
# Middleware de tratamento de exceções
app.add_middleware(ExceptionHandlerMiddleware)

# CORS deve ficar por último para ficar "por fora" dos demais middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra os Routers
app.include_router(usuario_router)
app.include_router(reuniao_router)


@app.get("/health", tags=["Health"])
def health_check():
  return {"status": "ok"}
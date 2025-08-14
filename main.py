from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import events  

app = FastAPI(
    title="Dashboard API",
    version="0.1.0",
    description="API para recopilar y gestionar actividad del navegador"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(events.router)

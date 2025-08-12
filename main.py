from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.core.db import init_db
from app.routers import events

app = FastAPI(title="Smart Monitor API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


@app.get("/health")
def health():
    return {"status": "ok"}

app = FastAPI(lifespan=lifespan)
app.include_router(events.router, prefix="/v1")

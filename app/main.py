from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

from .database import engine, Base
from .routers import containers, items, search

# create db tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Storage Assistant", version="1.0.0")

# mount static files
STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# add routers
app.include_router(containers.router, prefix="/containers", tags=["containers"])
app.include_router(items.router, prefix="/items", tags=["items"])
app.include_router(search.router, prefix="/search", tags=["search"])

@app.get("/")
async def root():
    return {"message": "Storage Assistant API", "docs": "/docs"}

@app.get("/health")
async def health():
    return {"status": "ok"}
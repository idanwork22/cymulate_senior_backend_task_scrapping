import FastAPI as FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes import *

def get_app():
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # include all the routes
    return app

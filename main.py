from fastapi import FastAPI
from application.routes import router
from fastapi.middleware.cors import CORSMiddleware
from application.load_config import config
import logging


# Logging setup
logging.basicConfig(
    format=config["logging"]["format"],
    level=config["logging"]["level"],
)

application = FastAPI()

# CORS
application.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

application.include_router(router)

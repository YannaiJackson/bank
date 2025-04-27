from fastapi import FastAPI
from app.routes import router
from fastapi.middleware.cors import CORSMiddleware
from app.logger import logger
import uvicorn


def create_application():
    """
    Creates and returns the FastAPI application instance.
    Configures middlewares, logging, and includes routers.
    """
    application = FastAPI()
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(router)
    logger.get_logger().info("Application starting...")

    return application


if __name__ == "__main__":
    application = create_application()
    uvicorn.run(application, host="0.0.0.0", port=8080)

from os import environ


class Config:
    HOST = environ.get("SERVICE_HOST", "0.0.0.0")
    PORT = int(environ.get("SERVICE_PORT", 5002))
    CONCURRENCY = int(environ.get("CONCURRENCY")) if environ.get("CONCURRENCY") else None

    ENV = environ.get("ENV", "development")
    DEBUG = int(environ.get("DEBUG", 0))
    LOG_LEVEL = environ.get("LOG_LEVEL", "INFO")

    # TENANT_ID = environ.get("TENANT_ID", "")
    # DATASOURCE_BASE_URL = environ.get("DATASOURCE_BASE_URL", "http://192.168.0.128:5000/datasource/api/v1/")
    # FLASHCORPBE_BASE_URL = environ.get("FLASHCORPBE_BASE_URL", "http://127.0.0.1:3001/flashcorp/api/v1/")
    # VISUAL_PROGRAMMING_BASE_URL = environ.get("VISUAL_PROGRAMMING_BASE_URL", "http://127.0.0.1:8000/vp/")

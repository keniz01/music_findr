from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from uuid import uuid4
import time

from src.config.log_config import logger
from src.routes.search.api import search_router


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Try to get correlation ID from headers or generate new one
        correlation_id = request.headers.get("X-Request-ID", str(uuid4()))
        start_time = time.time()

        # Bind correlation ID to the logger for this request
        with logger.contextualize(correlation_id=correlation_id):
            logger.info(f"📥 Request | {request.method} {request.url.path}")

            try:
                response: Response = await call_next(request)
            except Exception as e:
                logger.exception(f"❌ Error during request: {e}")
                raise

            process_time = (time.time() - start_time) * 1000
            logger.info(f"📤 Response | Status: {response.status_code} | Time: {process_time:.2f}ms")

            # Add correlation ID to response headers
            response.headers["X-Request-ID"] = correlation_id

            return response


app = FastAPI(
    title="Postgres SQL MCP Client",
    description="FastApi Postgres SQL MCP Client.",
    version="1.0.0"
)

# CORS settings
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom logging middleware
app.add_middleware(LoggingMiddleware)

# Exception Handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"⚠️ HTTPException: {exc.detail} | Path: {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTPException",
            "message": exc.detail,
            "path": request.url.path
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"🛑 ValidationError at {request.url.path}: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "message": "Invalid request data",
            "details": exc.errors(),
            "path": request.url.path
        }
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting FastAPI application...")
    yield
    logger.info("🛑 Shutting down FastAPI application...")

app = FastAPI(lifespan=lifespan)

# Include the router with prefix
app.include_router(search_router)

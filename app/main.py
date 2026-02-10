from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.api.product_routes import router as product_router
from app.api.category_routes import router as category_router
from app.api.health import router as health_router
from app.config import APP_NAME

from app.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables (for demo / assignment purposes)
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=APP_NAME,
    version="1.0.0",
    lifespan=lifespan,
)


app.include_router(product_router)
app.include_router(category_router)
app.include_router(health_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "error": "Validation Error",
            "details": exc.errors(),
        },
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc),
        },
    )

"""
CosmicLens API - Main FastAPI Application

A RESTful API for NASA's Astronomy Picture of the Day dataset
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import uvicorn

from app.config import settings
from app.database import init_database
from app.routers import pictures_router, collections_router, analytics_router, auth_router

# Create FastAPI application
app = FastAPI(
    title="CosmicLens API",
    description="""
    ## CosmicLens API

    A RESTful API for exploring NASA's iconic Astronomy Picture of the Day (APOD) collection.

    ### Features

    * **Astronomy Pictures**: Full CRUD operations for NASA's APOD dataset (30+ years of cosmic imagery)
    * **Collections**: Create and manage personal collections of favorite astronomy pictures
    * **Analytics**: Statistics, trends, and insights from the APOD dataset
    * **Search**: Advanced filtering and search capabilities
    * **Authentication**: User registration and login with JWT tokens

    ### Dataset

    This API uses the NASA Astronomy Picture of the Day dataset from Kaggle:
    - **Records**: 11,186+ images spanning from June 1995 to present
    - **Source**: [NASA APOD on Kaggle](https://www.kaggle.com/datasets/ahsanneural/nasa-astronomy-picture-of-the-day-1995-2026)

    ### Technology Stack

    * **Framework**: FastAPI (Python)
    * **Database**: PostgreSQL with SQLAlchemy ORM
    * **Documentation**: Swagger UI & ReDoc
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with better messages"""
    errors = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"])
        errors.append({
            "field": field,
            "message": error["msg"],
            "type": error["type"]
        })
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "errors": errors
        }
    )


# Include routers
app.include_router(pictures_router, prefix=settings.API_V1_PREFIX)
app.include_router(collections_router, prefix=settings.API_V1_PREFIX)
app.include_router(analytics_router, prefix=settings.API_V1_PREFIX)
app.include_router(auth_router, prefix=settings.API_V1_PREFIX)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_database()


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API information"""
    return {
        "name": "CosmicLens API",
        "version": "1.0.0",
        "description": "A RESTful API for NASA's Astronomy Picture of the Day",
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc",
            "openapi_json": "/openapi.json"
        },
        "endpoints": {
            "pictures": f"{settings.API_V1_PREFIX}/pictures",
            "collections": f"{settings.API_V1_PREFIX}/collections",
            "analytics": f"{settings.API_V1_PREFIX}/analytics",
            "auth": f"{settings.API_V1_PREFIX}/auth"
        },
        "dataset_source": "https://www.kaggle.com/datasets/ahsanneural/nasa-astronomy-picture-of-the-day-1995-2026"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "CosmicLens API",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

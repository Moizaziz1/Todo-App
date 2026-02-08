from fastapi import FastAPI
from .config.settings import settings
from .services.database import create_db_and_tables
from .api.routes import tasks, auth
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events
    """
    # Startup
    print("Initializing database...")
    try:
        create_db_and_tables()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Warning: Database initialization failed: {e}")
        print("Database tables will be created on first request.")
    yield
    # Shutdown
    print("Application shutdown")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application
    """
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan
    )

    # Add CORS middleware - configured for frontend origin
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://tode-app.vercel.app/"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type", "Accept"],
    )

    # Include API routes
    app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
    app.include_router(tasks.router, prefix="/api/v1", tags=["tasks"])

    @app.get("/health")
    def health_check():
        """
        Health check endpoint
        """
        return {"status": "healthy", "version": settings.app_version}

    return app


# Create the main application instance
app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
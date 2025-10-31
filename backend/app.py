"""
Main FastAPI application
"""

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi import Request
from pathlib import Path

from backend.config import settings
from backend.routes import protocol_router, evolution_router, social_router

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Recursive AI Consciousness Simulator",
    debug=settings.DEBUG
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Templates
templates = Jinja2Templates(directory="frontend/templates")

# Include routers
app.include_router(protocol_router)
app.include_router(evolution_router)
app.include_router(social_router)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Serve main page"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/demo", response_class=HTMLResponse)
async def demo_page(request: Request):
    """Serve interactive demo page"""
    return templates.TemplateResponse("demo.html", {"request": request})


@app.get("/evolution", response_class=HTMLResponse)
async def evolution_page(request: Request):
    """Serve evolution visualization page"""
    return templates.TemplateResponse("evolution.html", {"request": request})


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "service": settings.APP_NAME
    }


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} starting...")
    print(f"📡 Server running on {settings.HOST}:{settings.PORT}")
    print(f"🧠 LLM Provider: {settings.DEFAULT_LLM_PROVIDER}")
    
    # Create necessary directories
    Path("logs").mkdir(exist_ok=True)
    Path("models").mkdir(exist_ok=True)


def main():
    """Run the application"""
    uvicorn.run(
        "backend.app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )


if __name__ == "__main__":
    main()
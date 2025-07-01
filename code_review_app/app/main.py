from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import analyze, webhook
from app.services.database import init_db

app = FastAPI(
    title="AI Code Review App",
    description="An AI-powered code review application that analyzes code for bugs, vulnerabilities, and quality issues",
    version="1.0.0"
)

# Add CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://localhost:8080",      # Added for Vite/other dev servers
        "http://127.0.0.1:8080"       # Added for Vite/other dev servers
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    init_db()  # Initialize SQLite (optional)

app.include_router(analyze.router, prefix="/api", tags=["analysis"])
app.include_router(webhook.router, prefix="/api", tags=["webhooks"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "AI Code Review API is running"}

@app.get("/")
async def root():
    return {
        "message": "AI Code Review API",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "/api/analyze",
            "analyze-file": "/api/analyze-file",
            "supported-languages": "/api/supported-languages",
            "webhook": "/api/webhook",
            "health": "/health"
        }
    } 
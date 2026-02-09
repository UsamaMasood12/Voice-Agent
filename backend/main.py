"""
RoomiAI - FastAPI Backend Server

This is the main FastAPI application that provides REST API endpoints for the
hotel reservation system. It connects to MongoDB for data storage and is used
by both the voice agent and any external applications.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.database.connection import connect_to_mongodb, close_mongodb_connection
from backend.routers import booking, rooms


# Lifespan handler for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongodb()
    yield
    # Shutdown
    await close_mongodb_connection()


# Create FastAPI app
app = FastAPI(
    title="RoomiAI - Hotel Reservation API",
    description="REST API for hotel room reservations and guest services",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(booking.router, prefix="/api/v1")
app.include_router(rooms.router, prefix="/api/v1")


# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to RoomiAI Hotel Reservation API",
        "version": "1.0.0",
        "docs": "/docs"
    }


# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)

"""
Routers Package - RoomiAI FastAPI API Endpoints

This package contains all FastAPI router modules that define the REST API endpoints.
Each router file handles a specific domain area (rooms, bookings, guests, services).
Routers receive HTTP requests, validate input using Pydantic models, call services
for business logic, and return JSON responses. They are registered in main.py.
"""

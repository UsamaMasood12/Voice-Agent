"""
Service Requests API Routes - FastAPI Endpoints for Hotel Services

This file defines REST API endpoints for in-stay service requests including:
POST /services/requests - Create a new service request (housekeeping, room service, etc.)
GET /services/requests/{request_id} - Get status of a service request
PUT /services/requests/{request_id} - Update request status (for staff)
These endpoints handle guest service needs during their stay at the hotel.
"""

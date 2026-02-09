"""
Guest API Routes - FastAPI Endpoints for Guest Profile Operations

This file defines REST API endpoints for guest management including:
POST /guests - Create a new guest profile
GET /guests/{guest_id} - Retrieve guest profile and history
GET /guests/search - Search guests by name, email, or phone
PUT /guests/{guest_id}/preferences - Update guest preferences
These endpoints manage guest data collected during voice conversations.
"""

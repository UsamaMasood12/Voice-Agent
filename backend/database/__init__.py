"""
Database Package - RoomiAI MongoDB Configuration

This package handles all database-related functionality including MongoDB connection
setup, collection access, and database schemas. It uses Motor (async MongoDB driver)
for non-blocking database operations. The connection is shared across all services
and routers for efficient database access throughout the application.
"""

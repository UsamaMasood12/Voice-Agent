"""
Database Connection Manager - RoomiAI MongoDB Setup

This file establishes and manages the MongoDB connection using Motor async driver.
It reads the MONGODB_URL from environment variables, creates the client connection,
and provides the database instance to other modules.
"""

import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection string
MONGODB_URL = os.getenv(
    "MONGODB_URL",
    "mongodb+srv://asadullahmasood1005:o6JMETlQXlGKy8T5@cluster0.nio7sh8.mongodb.net/"
)
DATABASE_NAME = "roomiai"

# Global database client and database instance
client: AsyncIOMotorClient = None
db = None


async def connect_to_mongodb():
    """Connect to MongoDB on application startup."""
    global client, db
    print(f"Connecting to MongoDB...")
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    
    # Test connection
    try:
        await client.admin.command('ping')
        print(f"✅ Connected to MongoDB database: {DATABASE_NAME}")
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        raise e


async def close_mongodb_connection():
    """Close MongoDB connection on application shutdown."""
    global client
    if client:
        client.close()
        print("MongoDB connection closed.")


def get_database():
    """Get the database instance."""
    return db


# Collection getters
def get_bookings_collection():
    """Get the bookings collection."""
    return db["bookings"]


def get_guests_collection():
    """Get the guests collection."""
    return db["guests"]


def get_rooms_collection():
    """Get the rooms collection."""
    return db["rooms"]


def get_room_types_collection():
    """Get the room_types collection."""
    return db["room_types"]


def get_service_requests_collection():
    """Get the service_requests collection."""
    return db["service_requests"]

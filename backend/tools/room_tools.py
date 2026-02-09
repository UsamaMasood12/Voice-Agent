"""
Room Tools - Business Logic for Room Operations

This file contains the business logic functions for room operations.
These functions call the FastAPI backend.
"""

import os
import httpx

# FastAPI backend URL
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")


async def get_all_room_types(filter_type: str = "all") -> dict:
    """
    Get all available room types from the FastAPI backend.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{API_BASE_URL}/rooms/types",
                params={"filter_type": filter_type},
                timeout=10.0
            )
            if response.status_code == 200:
                return response.json()
            else:
                return _fallback_room_types(filter_type)
    except Exception as e:
        print(f"API call failed: {e}")
        return _fallback_room_types(filter_type)


def _fallback_room_types(filter_type: str) -> dict:
    """Fallback room types when API is not available."""
    room_types = [
        {"type": "Standard Room", "rate": 120, "description": "Comfortable room, 300 sq ft"},
        {"type": "Deluxe Room", "rate": 150, "description": "Spacious room with views, 400 sq ft"},
        {"type": "Junior Suite", "rate": 220, "description": "Suite with living area, 550 sq ft"},
        {"type": "Executive Suite", "rate": 350, "description": "Premium suite, 800 sq ft"},
        {"type": "Family Room", "rate": 250, "description": "Large family room, 600 sq ft"}
    ]
    
    if filter_type.lower() == "budget":
        room_types = [r for r in room_types if r["rate"] <= 150]
    elif filter_type.lower() == "premium":
        room_types = [r for r in room_types if r["rate"] > 150]
    
    return {
        "room_types": room_types,
        "message": "We have Standard Rooms at $120, Deluxe Rooms at $150, Suites from $220 per night."
    }


async def get_hotel_information(info_type: str = "all") -> dict:
    """
    Get hotel information from the FastAPI backend.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{API_BASE_URL}/rooms/info",
                params={"info_type": info_type},
                timeout=10.0
            )
            if response.status_code == 200:
                return response.json()
            else:
                return _fallback_hotel_info(info_type)
    except Exception as e:
        print(f"API call failed: {e}")
        return _fallback_hotel_info(info_type)


def _fallback_hotel_info(info_type: str) -> dict:
    """Fallback hotel info when API is not available."""
    return {
        "hotel_name": "Grand Hotel",
        "address": "123 Main Street, Downtown, City 12345",
        "check_in_time": "3:00 PM",
        "check_out_time": "11:00 AM",
        "cancellation_policy": "Free cancellation up to 24 hours before check-in",
        "message": "Check-in is at 3 PM and checkout is at 11 AM. Free cancellation up to 24 hours before."
    }

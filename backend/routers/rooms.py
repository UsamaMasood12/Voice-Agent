"""
Room API Routes - FastAPI Endpoints for Room Operations

GET /rooms/types - List all room types with amenities and pricing
GET /rooms/availability - Check room availability for specific dates
"""

from fastapi import APIRouter
from typing import Optional

from backend.database.connection import get_room_types_collection, get_rooms_collection

router = APIRouter(prefix="/rooms", tags=["Rooms"])

# Sample room type data (will be used if DB is empty)
DEFAULT_ROOM_TYPES = [
    {
        "type": "Standard Room",
        "code": "STD",
        "rate": 120,
        "description": "Comfortable room with modern amenities, 300 sq ft",
        "max_guests": 3,
        "amenities": ["WiFi", "TV", "Safe", "Coffee Maker"],
        "total_rooms": 20
    },
    {
        "type": "Deluxe Room",
        "code": "DLX",
        "rate": 150,
        "description": "Spacious room with premium views, 400 sq ft",
        "max_guests": 3,
        "amenities": ["WiFi", "TV", "Safe", "Coffee Maker", "Bathrobe", "Work Desk"],
        "total_rooms": 20
    },
    {
        "type": "Junior Suite",
        "code": "STE-J",
        "rate": 220,
        "description": "Luxurious suite with separate living area, 550 sq ft",
        "max_guests": 3,
        "amenities": ["WiFi", "TV", "Safe", "Living Area", "Mini Bar"],
        "total_rooms": 6
    },
    {
        "type": "Executive Suite",
        "code": "STE-E",
        "rate": 350,
        "description": "Premium suite with panoramic city views, 800 sq ft",
        "max_guests": 4,
        "amenities": ["WiFi", "TV", "Safe", "Living Area", "Dining Table", "Kitchenette"],
        "total_rooms": 3
    },
    {
        "type": "Family Room",
        "code": "FAM",
        "rate": 250,
        "description": "Large room perfect for families, 600 sq ft",
        "max_guests": 5,
        "amenities": ["WiFi", "TV", "Safe", "Extra Beds", "Kids Pack"],
        "total_rooms": 1
    }
]


@router.get("/types")
async def get_room_types(filter_type: str = "all"):
    """Get all available room types with descriptions and pricing."""
    
    collection = get_room_types_collection()
    
    # Check if room types exist in DB, if not use defaults
    count = await collection.count_documents({})
    
    if count == 0:
        # Insert default room types
        await collection.insert_many(DEFAULT_ROOM_TYPES)
        room_types = DEFAULT_ROOM_TYPES
    else:
        cursor = collection.find({})
        room_types = await cursor.to_list(length=100)
        # Remove MongoDB _id fields
        for room in room_types:
            room.pop("_id", None)
    
    # Apply filter
    if filter_type.lower() == "budget":
        room_types = [r for r in room_types if r["rate"] <= 150]
    elif filter_type.lower() == "premium":
        room_types = [r for r in room_types if r["rate"] > 150]
    
    rates_message = ", ".join([f"{r['type']} at ${r['rate']}" for r in room_types])
    
    return {
        "room_types": room_types,
        "count": len(room_types),
        "message": f"We have {rates_message} per night."
    }


@router.get("/availability")
async def check_availability(
    check_in: str,
    check_out: str,
    room_type: str = "any",
    guests: str = "2"
):
    """Check room availability for given dates."""
    
    # TODO: Implement actual availability logic based on bookings
    # For now, return all room types as available
    
    collection = get_room_types_collection()
    
    if room_type.lower() == "any":
        cursor = collection.find({})
    else:
        cursor = collection.find({"code": room_type.upper()})
    
    rooms = await cursor.to_list(length=100)
    
    # If no rooms found, use defaults
    if not rooms:
        rooms = DEFAULT_ROOM_TYPES
        if room_type.lower() != "any":
            rooms = [r for r in rooms if room_type.lower() in r["type"].lower()]
    
    # Remove MongoDB _id fields
    for room in rooms:
        room.pop("_id", None)
    
    return {
        "available": True,
        "check_in": check_in,
        "check_out": check_out,
        "rooms": rooms,
        "message": f"We have rooms available from {check_in} to {check_out}."
    }


@router.get("/info")
async def get_hotel_info(info_type: str = "all"):
    """Get general hotel information."""
    
    hotel_info = {
        "hotel_name": "Grand Hotel",
        "address": "123 Main Street, Downtown, City 12345",
        "phone": "+1-555-HOTEL-00",
        "check_in_time": "3:00 PM",
        "check_out_time": "11:00 AM",
        "early_check_in_fee": 50,
        "late_check_out_fee": 50,
        "parking_self": 15,
        "parking_valet": 25,
        "cancellation_policy": "Free cancellation up to 24 hours before check-in",
        "tax_rate": 12.5
    }
    
    if info_type.lower() == "timings":
        return {
            "check_in_time": hotel_info["check_in_time"],
            "check_out_time": hotel_info["check_out_time"],
            "message": f"Check-in is at {hotel_info['check_in_time']} and checkout is at {hotel_info['check_out_time']}."
        }
    elif info_type.lower() == "location":
        return {
            "hotel_name": hotel_info["hotel_name"],
            "address": hotel_info["address"],
            "phone": hotel_info["phone"],
            "message": f"We are located at {hotel_info['address']}."
        }
    elif info_type.lower() == "policies":
        return {
            "cancellation_policy": hotel_info["cancellation_policy"],
            "parking_self": hotel_info["parking_self"],
            "parking_valet": hotel_info["parking_valet"],
            "message": hotel_info["cancellation_policy"]
        }
    
    hotel_info["message"] = f"Check-in is at {hotel_info['check_in_time']} and checkout is at {hotel_info['check_out_time']}. {hotel_info['cancellation_policy']}."
    return hotel_info

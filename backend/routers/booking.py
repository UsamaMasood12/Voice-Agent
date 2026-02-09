"""
Booking API Routes - FastAPI Endpoints for Reservation Operations

POST /bookings - Create a new reservation
GET /bookings/{confirmation_number} - Retrieve booking details
DELETE /bookings/{confirmation_number} - Cancel a booking
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
import random
import string

from backend.database.connection import get_bookings_collection
from backend.models.booking import (
    BookingCreate,
    BookingResponse,
    CancelBookingRequest,
    CancelBookingResponse,
    BookingInDB
)

router = APIRouter(prefix="/bookings", tags=["Bookings"])

# Room rates
ROOM_RATES = {
    "standard": 120,
    "deluxe": 150,
    "suite": 220,
    "executive": 350,
    "family": 250
}


@router.post("/", response_model=BookingResponse)
async def create_booking(booking: BookingCreate):
    """Create a new room reservation."""
    
    # Generate confirmation number
    random_suffix = ''.join(random.choices(string.digits, k=4))
    date_part = datetime.now().strftime("%Y%m%d")
    confirmation_number = f"ROOMI-{date_part}-{random_suffix}"
    
    # Calculate pricing
    rate_per_night = ROOM_RATES.get(booking.room_type.lower(), 150)
    nights = 5  # TODO: Calculate from actual dates
    room_total = rate_per_night * nights
    taxes = round(room_total * 0.125, 2)
    grand_total = room_total + taxes
    
    # Create booking document
    booking_doc = {
        "confirmation_number": confirmation_number,
        "guest_name": booking.guest_name,
        "email": booking.email,
        "phone": booking.phone,
        "check_in": booking.check_in,
        "check_out": booking.check_out,
        "nights": nights,
        "room_type": booking.room_type,
        "guests": booking.guests,
        "rate_per_night": rate_per_night,
        "room_total": room_total,
        "taxes": taxes,
        "grand_total": grand_total,
        "special_requests": booking.special_requests,
        "status": "confirmed",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    # Save to MongoDB
    collection = get_bookings_collection()
    await collection.insert_one(booking_doc)
    
    return BookingResponse(
        success=True,
        confirmation_number=confirmation_number,
        guest_name=booking.guest_name,
        check_in=booking.check_in,
        check_out=booking.check_out,
        nights=nights,
        room_type=booking.room_type,
        rate_per_night=rate_per_night,
        room_total=room_total,
        taxes=taxes,
        grand_total=grand_total,
        status="confirmed",
        message=f"Booking confirmed! Confirmation number is {confirmation_number}"
    )


@router.get("/{confirmation_number}")
async def get_booking(confirmation_number: str):
    """Retrieve booking details by confirmation number."""
    
    collection = get_bookings_collection()
    booking = await collection.find_one({"confirmation_number": confirmation_number})
    
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Remove MongoDB _id field
    booking.pop("_id", None)
    
    return {
        "found": True,
        "booking": booking
    }


@router.get("/search/by-name")
async def search_booking_by_name(guest_name: str):
    """Search bookings by guest name."""
    
    collection = get_bookings_collection()
    cursor = collection.find({"guest_name": {"$regex": guest_name, "$options": "i"}})
    bookings = await cursor.to_list(length=10)
    
    # Remove MongoDB _id fields
    for booking in bookings:
        booking.pop("_id", None)
    
    return {
        "found": len(bookings) > 0,
        "count": len(bookings),
        "bookings": bookings
    }


@router.delete("/{confirmation_number}")
async def cancel_booking(confirmation_number: str, reason: str = ""):
    """Cancel an existing booking."""
    
    collection = get_bookings_collection()
    
    # Find the booking
    booking = await collection.find_one({"confirmation_number": confirmation_number})
    
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Update status to cancelled
    cancellation_ref = f"CXL-{confirmation_number}"
    
    await collection.update_one(
        {"confirmation_number": confirmation_number},
        {
            "$set": {
                "status": "cancelled",
                "cancellation_reference": cancellation_ref,
                "cancellation_reason": reason,
                "cancelled_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    return CancelBookingResponse(
        success=True,
        confirmation_number=confirmation_number,
        cancellation_reference=cancellation_ref,
        refund_eligible=True,
        message=f"Booking cancelled. Reference: {cancellation_ref}. Full refund in 5-7 business days."
    )


@router.get("/")
async def list_bookings(status: str = None, limit: int = 20):
    """List all bookings with optional status filter."""
    
    collection = get_bookings_collection()
    
    query = {}
    if status:
        query["status"] = status
    
    cursor = collection.find(query).sort("created_at", -1).limit(limit)
    bookings = await cursor.to_list(length=limit)
    
    # Remove MongoDB _id fields
    for booking in bookings:
        booking.pop("_id", None)
    
    return {
        "count": len(bookings),
        "bookings": bookings
    }

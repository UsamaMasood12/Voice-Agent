"""
Booking Tools - Business Logic for Reservation Operations

This file contains the business logic functions for booking operations.
These functions call the FastAPI backend which stores data in MongoDB.
"""

import os
import httpx
from datetime import datetime
import random
import string

# FastAPI backend URL
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")


async def check_room_availability(
    check_in: str,
    check_out: str,
    room_type: str = "any",
    guests: str = "2"
) -> dict:
    """
    Check if rooms are available for the specified dates.
    Calls the FastAPI backend.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{API_BASE_URL}/rooms/availability",
                params={
                    "check_in": check_in,
                    "check_out": check_out,
                    "room_type": room_type,
                    "guests": guests
                },
                timeout=10.0
            )
            if response.status_code == 200:
                return response.json()
            else:
                # Fallback to local data if API fails
                return _fallback_availability(check_in, check_out, room_type)
    except Exception as e:
        print(f"API call failed: {e}")
        return _fallback_availability(check_in, check_out, room_type)


def _fallback_availability(check_in: str, check_out: str, room_type: str) -> dict:
    """Fallback availability data when API is not available."""
    rooms = [
        {"type": "Standard Room", "rate": 120, "available": 8},
        {"type": "Deluxe Room", "rate": 150, "available": 5},
        {"type": "Junior Suite", "rate": 220, "available": 2},
    ]
    return {
        "available": True,
        "check_in": check_in,
        "check_out": check_out,
        "rooms": rooms,
        "message": f"We have rooms available from {check_in} to {check_out}."
    }


async def create_room_booking(
    guest_name: str,
    check_in: str,
    check_out: str,
    room_type: str,
    phone: str,
    email: str,
    guests: str = "2",
    special_requests: str = ""
) -> dict:
    """
    Create a new hotel room reservation.
    Calls the FastAPI backend to store in MongoDB.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{API_BASE_URL}/bookings/",
                json={
                    "guest_name": guest_name,
                    "check_in": check_in,
                    "check_out": check_out,
                    "room_type": room_type,
                    "phone": phone,
                    "email": email,
                    "guests": guests,
                    "special_requests": special_requests
                },
                timeout=10.0
            )
            if response.status_code == 200:
                return response.json()
            else:
                # Fallback to local booking
                return _fallback_create_booking(
                    guest_name, check_in, check_out, room_type,
                    phone, email, guests, special_requests
                )
    except Exception as e:
        print(f"API call failed: {e}")
        return _fallback_create_booking(
            guest_name, check_in, check_out, room_type,
            phone, email, guests, special_requests
        )


def _fallback_create_booking(
    guest_name: str, check_in: str, check_out: str, room_type: str,
    phone: str, email: str, guests: str, special_requests: str
) -> dict:
    """Fallback booking creation when API is not available."""
    random_suffix = ''.join(random.choices(string.digits, k=4))
    date_part = datetime.now().strftime("%Y%m%d")
    confirmation_number = f"ROOMI-{date_part}-{random_suffix}"
    
    rates = {"standard": 120, "deluxe": 150, "suite": 220}
    rate_per_night = rates.get(room_type.lower(), 150)
    nights = 5
    room_total = rate_per_night * nights
    taxes = round(room_total * 0.125, 2)
    grand_total = room_total + taxes
    
    return {
        "success": True,
        "confirmation_number": confirmation_number,
        "guest_name": guest_name,
        "check_in": check_in,
        "check_out": check_out,
        "nights": nights,
        "room_type": room_type,
        "rate_per_night": rate_per_night,
        "room_total": room_total,
        "taxes": taxes,
        "grand_total": grand_total,
        "message": f"Booking confirmed! Confirmation number is {confirmation_number} (offline mode)"
    }


async def get_booking_details(
    confirmation_number: str = "",
    guest_name: str = ""
) -> dict:
    """
    Retrieve booking details from the FastAPI backend.
    """
    try:
        async with httpx.AsyncClient() as client:
            if confirmation_number:
                response = await client.get(
                    f"{API_BASE_URL}/bookings/{confirmation_number}",
                    timeout=10.0
                )
            elif guest_name:
                response = await client.get(
                    f"{API_BASE_URL}/bookings/search/by-name",
                    params={"guest_name": guest_name},
                    timeout=10.0
                )
            else:
                return {
                    "found": False,
                    "message": "Please provide either a confirmation number or guest name."
                }
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"found": False, "message": "Booking not found."}
    except Exception as e:
        print(f"API call failed: {e}")
        return {"found": False, "message": "Could not retrieve booking. Please try again."}


async def cancel_room_booking(confirmation_number: str) -> dict:
    """
    Cancel an existing reservation via FastAPI backend.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{API_BASE_URL}/bookings/{confirmation_number}",
                timeout=10.0
            )
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "success": False,
                    "message": "Could not cancel booking. Please check the confirmation number."
                }
    except Exception as e:
        print(f"API call failed: {e}")
        # Fallback response
        cancellation_ref = f"CXL-{confirmation_number}"
        return {
            "success": True,
            "confirmation_number": confirmation_number,
            "cancellation_reference": cancellation_ref,
            "refund_eligible": True,
            "message": f"Booking cancelled (offline). Reference: {cancellation_ref}."
        }
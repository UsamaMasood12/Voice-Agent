"""
Pydantic Models - RoomiAI Request/Response Schemas

This file defines Pydantic models for API request/response validation.
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum


# ============================================
# Enums
# ============================================
class RoomType(str, Enum):
    STANDARD = "standard"
    DELUXE = "deluxe"
    SUITE = "suite"
    EXECUTIVE = "executive"
    FAMILY = "family"


class BookingStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CHECKED_IN = "checked_in"
    CHECKED_OUT = "checked_out"
    CANCELLED = "cancelled"


# ============================================
# Room Models
# ============================================
class RoomTypeModel(BaseModel):
    type: str
    code: str
    rate: float
    description: str
    max_guests: int
    amenities: List[str]


class AvailabilityRequest(BaseModel):
    check_in: str
    check_out: str
    room_type: str = "any"
    guests: str = "2"


class AvailabilityResponse(BaseModel):
    available: bool
    check_in: str
    check_out: str
    rooms: List[dict]
    message: str


# ============================================
# Guest Models
# ============================================
class GuestCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    address: Optional[str] = None


class GuestResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    created_at: datetime


# ============================================
# Booking Models
# ============================================
class BookingCreate(BaseModel):
    guest_name: str
    check_in: str
    check_out: str
    room_type: str
    phone: str
    email: str
    guests: str = "2"
    special_requests: str = ""


class BookingResponse(BaseModel):
    success: bool
    confirmation_number: str
    guest_name: str
    check_in: str
    check_out: str
    nights: int
    room_type: str
    rate_per_night: float
    room_total: float
    taxes: float
    grand_total: float
    status: str = "confirmed"
    message: str


class BookingInDB(BaseModel):
    confirmation_number: str
    guest_name: str
    email: str
    phone: str
    check_in: str
    check_out: str
    nights: int
    room_type: str
    guests: str
    rate_per_night: float
    room_total: float
    taxes: float
    grand_total: float
    special_requests: str
    status: str
    created_at: datetime
    updated_at: datetime


class CancelBookingRequest(BaseModel):
    confirmation_number: str
    reason: str = ""


class CancelBookingResponse(BaseModel):
    success: bool
    confirmation_number: str
    cancellation_reference: str
    refund_eligible: bool
    message: str


# ============================================
# Service Request Models
# ============================================
class ServiceRequest(BaseModel):
    room_number: str
    request_type: str  # housekeeping, room_service, maintenance
    details: str
    priority: str = "normal"


class ServiceRequestResponse(BaseModel):
    success: bool
    request_id: str
    message: str

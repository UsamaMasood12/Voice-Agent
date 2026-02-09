# RoomiAI - Technical Architecture Document
## AI Voice Agent for Hotel Reservation System

---

## Table of Contents
1. [System Architecture Overview](#system-architecture-overview)
2. [Technology Stack](#technology-stack)
3. [Database Schemas (MongoDB)](#database-schemas-mongodb)
4. [API Endpoints (FastAPI)](#api-endpoints-fastapi)
5. [Voice Agent Architecture](#voice-agent-architecture)
6. [Integration Details](#integration-details)
7. [Deployment Configuration](#deployment-configuration)
8. [Security Considerations](#security-considerations)

---

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              GUEST (Phone Call)                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          LiveKit Cloud (SFU)                                 │
│                    Real-time Audio/Video Infrastructure                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                    ┌─────────────────┴─────────────────┐
                    ▼                                   ▼
┌───────────────────────────────┐     ┌───────────────────────────────────────┐
│         Deepgram STT          │     │           Deepgram TTS                │
│   (Speech-to-Text Engine)     │     │     (Text-to-Speech Engine)           │
│   - Real-time transcription   │     │   - Natural voice synthesis           │
│   - Multi-language support    │     │   - Low latency responses             │
└───────────────────────────────┘     └───────────────────────────────────────┘
                    │                                   ▲
                    ▼                                   │
┌─────────────────────────────────────────────────────────────────────────────┐
│                         RoomiAI Agent (Python)                               │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    Conversation Manager                              │   │
│  │  - State tracking    - Context management   - Intent handling        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                      │                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      Groq LLM Integration                           │   │
│  │  - Natural language understanding    - Response generation          │   │
│  │  - Intent classification             - Entity extraction            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                      │                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     Business Logic Layer                            │   │
│  │  - Reservation handling    - Availability checks   - Pricing        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        FastAPI Backend Server                                │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐                │
│  │ Reservation API│  │   Room API     │  │   Guest API    │                │
│  └────────────────┘  └────────────────┘  └────────────────┘                │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐                │
│  │ Payment API    │  │  Service API   │  │   Admin API    │                │
│  └────────────────┘  └────────────────┘  └────────────────┘                │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          MongoDB Database                                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐         │
│  │  rooms   │ │  guests  │ │bookings  │ │ payments │ │services  │         │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                                     │
│  │room_types│ │  rates   │ │call_logs │                                     │
│  └──────────┘ └──────────┘ └──────────┘                                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Runtime** | Python 3.11+ | Core application language |
| **Backend Framework** | FastAPI | REST API server |
| **Database** | MongoDB | Data storage (NoSQL) |
| **Real-time Audio** | LiveKit | Audio streaming & SFU |
| **Speech-to-Text** | Deepgram | Voice transcription |
| **Text-to-Speech** | Deepgram | Voice synthesis |
| **LLM Provider** | Groq (LLaMA/Mixtral) | NLU & response generation |
| **Containerization** | Docker + Docker Compose | Deployment |
| **Async Library** | asyncio | Concurrent operations |
| **ODM** | Motor (async MongoDB) | Database operations |

---

## Database Schemas (MongoDB)

### Collection: `room_types`
Defines the types of rooms available in the hotel.

```javascript
{
  "_id": ObjectId,
  "type_code": String,           // "STD", "DLX", "STE", "FAM"
  "name": String,                // "Standard Room"
  "description": String,         // "Comfortable room with..."
  "base_occupancy": Number,      // 2
  "max_occupancy": Number,       // 4
  "extra_person_charge": Number, // 50.00
  "bed_configurations": [        // Available bed options
    {
      "code": String,            // "KING", "TWIN", "QUEEN"
      "description": String      // "One King Bed"
    }
  ],
  "amenities": [String],         // ["WiFi", "TV", "Mini Bar", "Safe"]
  "size_sqft": Number,           // 350
  "view_options": [String],      // ["city", "garden", "pool", "ocean"]
  "is_smoking_available": Boolean,
  "is_accessible": Boolean,
  "images": [String],            // URL array
  "created_at": ISODate,
  "updated_at": ISODate
}
```

### Collection: `rooms`
Individual room inventory.

```javascript
{
  "_id": ObjectId,
  "room_number": String,         // "405"
  "floor": Number,               // 4
  "room_type_id": ObjectId,      // Reference to room_types
  "bed_configuration": String,   // "KING"
  "view": String,                // "city"
  "status": String,              // "available", "occupied", "maintenance", "blocked"
  "is_smoking": Boolean,
  "is_accessible": Boolean,
  "features": [String],          // ["corner_room", "near_elevator", "connecting"]
  "connecting_room": String,     // Room number if applicable
  "notes": String,               // Internal notes
  "created_at": ISODate,
  "updated_at": ISODate
}
```

### Collection: `rates`
Pricing configuration.

```javascript
{
  "_id": ObjectId,
  "rate_code": String,           // "BAR", "AAA", "CORP", "PKG_BB"
  "name": String,                // "Best Available Rate"
  "description": String,         // "Flexible rate with free cancellation"
  "room_type_id": ObjectId,      // Reference to room_types
  "base_rate": Number,           // 150.00
  "currency": String,            // "USD"
  "rate_type": String,           // "per_night", "per_stay"
  "includes": [String],          // ["breakfast", "parking", "wifi"]
  "valid_from": ISODate,
  "valid_to": ISODate,
  "day_of_week_rates": {         // Optional day-specific pricing
    "friday": Number,            // 180.00
    "saturday": Number           // 200.00
  },
  "min_stay": Number,            // 1
  "max_stay": Number,            // 30
  "advance_booking_days": Number, // 0 for same-day
  "cancellation_policy": {
    "type": String,              // "flexible", "moderate", "strict"
    "free_cancellation_hours": Number,  // 24
    "penalty_amount": Number,    // One night or percentage
    "penalty_type": String       // "first_night", "percentage", "flat"
  },
  "is_refundable": Boolean,
  "is_active": Boolean,
  "created_at": ISODate,
  "updated_at": ISODate
}
```

### Collection: `guests`
Guest profiles and history.

```javascript
{
  "_id": ObjectId,
  "guest_id": String,            // "G-2026-00001"
  "title": String,               // "Mr", "Mrs", "Ms", "Dr"
  "first_name": String,          // "John"
  "last_name": String,           // "Smith"
  "email": String,               // "john.smith@email.com"
  "phone": {
    "country_code": String,      // "+1"
    "number": String             // "5551234567"
  },
  "alternate_phone": {
    "country_code": String,
    "number": String
  },
  "address": {
    "street": String,
    "city": String,
    "state": String,
    "postal_code": String,
    "country": String
  },
  "date_of_birth": ISODate,
  "nationality": String,
  "id_document": {
    "type": String,              // "passport", "drivers_license", "national_id"
    "number": String,
    "expiry_date": ISODate,
    "issuing_country": String
  },
  "preferences": {
    "room_type": String,
    "floor_preference": String,   // "high", "low", "any"
    "bed_preference": String,     // "KING", "TWIN"
    "view_preference": String,
    "smoking": Boolean,
    "dietary_restrictions": [String],
    "accessibility_needs": [String],
    "special_requests": [String]  // Common requests for this guest
  },
  "loyalty": {
    "member_id": String,
    "tier": String,              // "bronze", "silver", "gold", "platinum"
    "points": Number,
    "join_date": ISODate
  },
  "communication_preferences": {
    "email_marketing": Boolean,
    "sms_notifications": Boolean,
    "preferred_language": String  // "en", "ur"
  },
  "stay_history": {
    "total_stays": Number,
    "total_nights": Number,
    "total_revenue": Number,
    "first_stay": ISODate,
    "last_stay": ISODate
  },
  "notes": String,               // VIP notes, complaints, etc.
  "tags": [String],              // ["VIP", "frequent_guest", "wedding_party"]
  "created_at": ISODate,
  "updated_at": ISODate
}
```

### Collection: `bookings`
Core reservation data.

```javascript
{
  "_id": ObjectId,
  "confirmation_number": String,  // "ROOMI-20260120-001"
  "status": String,               // "confirmed", "checked_in", "checked_out", 
                                  // "cancelled", "no_show", "pending"
  "booking_source": String,       // "voice_agent", "website", "phone", "walk_in"
  "booking_channel": String,      // "direct", "ota", "corporate"
  
  // Dates
  "check_in_date": ISODate,       // 2026-01-20
  "check_out_date": ISODate,      // 2026-01-25
  "nights": Number,               // 5
  "actual_check_in": ISODate,     // Actual arrival time
  "actual_check_out": ISODate,    // Actual departure time
  
  // Guest Information
  "primary_guest_id": ObjectId,   // Reference to guests
  "additional_guests": [
    {
      "first_name": String,
      "last_name": String,
      "is_adult": Boolean,
      "age": Number              // For children
    }
  ],
  "guest_count": {
    "adults": Number,            // 2
    "children": Number,          // 0
    "infants": Number            // 0
  },
  
  // Room Details
  "rooms": [
    {
      "room_type_id": ObjectId,
      "room_number": String,     // Assigned at check-in (null if not yet)
      "bed_configuration": String,
      "view": String,
      "rate_code": String,
      "rate_per_night": Number,
      "special_requests": [String]
    }
  ],
  
  // Pricing
  "pricing": {
    "room_total": Number,        // 750.00
    "taxes": Number,             // 93.75
    "fees": Number,              // 25.00 (resort fee, etc.)
    "packages": [
      {
        "name": String,          // "Romance Package"
        "price": Number          // 75.00
      }
    ],
    "discounts": [
      {
        "code": String,          // "SUMMER20"
        "amount": Number,        // -50.00
        "type": String           // "percentage", "flat"
      }
    ],
    "grand_total": Number,       // 893.75
    "currency": String           // "USD"
  },
  
  // Payment
  "payment_status": String,      // "pending", "partial", "paid", "refunded"
  "payment_method": {
    "type": String,              // "credit_card", "debit_card", "cash"
    "card_last_four": String,    // "4567"
    "card_type": String,         // "visa", "mastercard"
    "token": String              // Payment token for charges
  },
  "deposit_amount": Number,
  "deposit_paid": Boolean,
  
  // Special Info
  "special_occasion": String,    // "anniversary", "birthday", "honeymoon"
  "estimated_arrival": String,   // "18:00"
  "special_requests": [String],  // ["high floor", "extra pillows"]
  "room_preferences": {
    "floor": String,             // "high", "low", "specific"
    "floor_number": Number,      // 10
    "near_elevator": Boolean,
    "connecting_rooms": Boolean,
    "quiet_room": Boolean,
    "other": [String]
  },
  
  // Policies
  "cancellation_policy": {
    "type": String,
    "deadline": ISODate,
    "penalty": Number
  },
  "policies_accepted": Boolean,
  "policies_accepted_at": ISODate,
  
  // Tracking
  "created_by": String,          // "voice_agent", "staff_id"
  "created_at": ISODate,
  "updated_at": ISODate,
  "modification_history": [
    {
      "action": String,          // "created", "modified", "cancelled"
      "timestamp": ISODate,
      "modified_by": String,
      "changes": Object,         // What was changed
      "reason": String
    }
  ],
  
  // Voice Agent Specific
  "voice_session": {
    "session_id": String,
    "call_start": ISODate,
    "call_end": ISODate,
    "call_duration_seconds": Number,
    "transcript_id": String      // Reference to call_logs
  }
}
```

### Collection: `availability`
Room availability cache for quick lookups.

```javascript
{
  "_id": ObjectId,
  "date": ISODate,               // 2026-01-20
  "room_type_id": ObjectId,
  "total_rooms": Number,         // 20
  "booked": Number,              // 15
  "available": Number,           // 5
  "blocked": Number,             // 0 (maintenance, etc.)
  "min_rate": Number,            // Lowest available rate
  "rates_available": [           // Which rate codes have inventory
    {
      "rate_code": String,
      "available": Number,
      "rate": Number
    }
  ],
  "updated_at": ISODate
}
```

### Collection: `payments`
Payment transactions.

```javascript
{
  "_id": ObjectId,
  "payment_id": String,          // "PAY-2026-00001"
  "booking_id": ObjectId,        // Reference to bookings
  "guest_id": ObjectId,          // Reference to guests
  "amount": Number,              // 893.75
  "currency": String,            // "USD"
  "payment_type": String,        // "deposit", "full_payment", "refund", "charge"
  "payment_method": {
    "type": String,              // "credit_card"
    "card_last_four": String,
    "card_type": String
  },
  "status": String,              // "pending", "completed", "failed", "refunded"
  "transaction_id": String,      // From payment processor
  "processor": String,           // "stripe", "square"
  "processor_response": Object,  // Raw response
  "refund_reason": String,       // If refunded
  "created_at": ISODate,
  "processed_at": ISODate
}
```

### Collection: `service_requests`
Guest service requests during stay.

```javascript
{
  "_id": ObjectId,
  "request_id": String,          // "SRV-2026-00001"
  "booking_id": ObjectId,
  "room_number": String,
  "guest_id": ObjectId,
  "request_type": String,        // "housekeeping", "room_service", "maintenance",
                                 // "concierge", "amenity"
  "request_details": {
    "category": String,          // "extra_towels", "food_order", "repair"
    "items": [String],           // ["towels", "pillows"]
    "quantity": Number,
    "description": String,
    "priority": String           // "normal", "urgent"
  },
  "status": String,              // "pending", "in_progress", "completed", "cancelled"
  "assigned_to": String,         // Staff member
  "estimated_completion": ISODate,
  "completed_at": ISODate,
  "guest_rating": Number,        // 1-5 satisfaction
  "notes": String,
  "created_at": ISODate,
  "updated_at": ISODate
}
```

### Collection: `call_logs`
Voice agent call recordings and transcripts.

```javascript
{
  "_id": ObjectId,
  "session_id": String,          // LiveKit session ID
  "call_type": String,           // "inbound", "outbound"
  "caller_phone": String,        // Masked: "+1555***4567"
  "call_start": ISODate,
  "call_end": ISODate,
  "duration_seconds": Number,
  "outcome": String,             // "booking_completed", "booking_failed",
                                 // "inquiry_only", "transferred", "abandoned"
  "booking_id": ObjectId,        // If booking was created
  "guest_id": ObjectId,          // If guest was identified
  "transcript": [
    {
      "timestamp": ISODate,
      "speaker": String,         // "agent", "guest"
      "text": String,
      "confidence": Number       // STT confidence
    }
  ],
  "intents_detected": [
    {
      "intent": String,          // "book_room", "check_availability"
      "confidence": Number,
      "timestamp": ISODate
    }
  ],
  "entities_extracted": {
    "dates": [ISODate],
    "guest_count": Number,
    "room_type": String,
    "guest_name": String,
    "contact_info": Object
  },
  "agent_version": String,
  "errors": [
    {
      "timestamp": ISODate,
      "type": String,
      "message": String
    }
  ],
  "audio_recording_url": String, // If recorded
  "created_at": ISODate
}
```

### Collection: `hotel_settings`
Hotel configuration and settings.

```javascript
{
  "_id": ObjectId,
  "hotel_id": String,            // "HOTEL-001"
  "name": String,                // "Grand Hotel"
  "brand": String,
  "address": Object,
  "phone": String,
  "email": String,
  "timezone": String,            // "America/New_York"
  "currency": String,            // "USD"
  "check_in_time": String,       // "15:00"
  "check_out_time": String,      // "11:00"
  "early_check_in": {
    "available": Boolean,
    "fee": Number,
    "earliest_time": String      // "12:00"
  },
  "late_check_out": {
    "available": Boolean,
    "fee": Number,
    "latest_time": String        // "14:00"
  },
  "policies": {
    "cancellation_default": Object,
    "deposit_required": Boolean,
    "deposit_percentage": Number,
    "children_policy": String,
    "pet_policy": String,
    "smoking_policy": String
  },
  "taxes": [
    {
      "name": String,            // "City Tax"
      "type": String,            // "percentage", "flat_per_night"
      "amount": Number
    }
  ],
  "fees": [
    {
      "name": String,            // "Resort Fee"
      "amount": Number,
      "per": String              // "night", "stay"
    }
  ],
  "voice_agent_settings": {
    "greeting_name": String,     // "Roomi"
    "voice_id": String,          // Deepgram voice
    "language": String,          // "en-US"
    "backup_language": String,   // "ur"
    "max_call_duration": Number, // seconds
    "transfer_number": String    // For human handoff
  },
  "updated_at": ISODate
}
```

---

## API Endpoints (FastAPI)

### Base URL
```
Production: https://api.roomiai.hotel.com/v1
Development: http://localhost:8000/v1
```

### Authentication
All endpoints require JWT authentication header:
```
Authorization: Bearer <token>
```

---

### Room Endpoints

#### GET `/rooms/availability`
Check room availability for dates.

**Request:**
```json
{
  "check_in": "2026-01-20",
  "check_out": "2026-01-25",
  "adults": 2,
  "children": 0,
  "rooms_needed": 1,
  "room_type": "DLX"  // Optional filter
}
```

**Response:**
```json
{
  "available": true,
  "date_range": {
    "check_in": "2026-01-20",
    "check_out": "2026-01-25",
    "nights": 5
  },
  "options": [
    {
      "room_type_id": "65a1b2c3...",
      "room_type": "Deluxe Room",
      "available_count": 5,
      "views_available": ["city", "garden"],
      "beds_available": ["KING", "TWIN"],
      "rates": [
        {
          "rate_code": "BAR",
          "name": "Best Available Rate",
          "per_night": 150.00,
          "total": 750.00,
          "includes": [],
          "cancellation": "Free cancellation until 24 hours before"
        },
        {
          "rate_code": "PKG_BB",
          "name": "Bed & Breakfast",
          "per_night": 175.00,
          "total": 875.00,
          "includes": ["breakfast"],
          "cancellation": "Free cancellation until 24 hours before"
        }
      ]
    }
  ]
}
```

#### GET `/rooms/types`
Get all room types.

**Response:**
```json
{
  "room_types": [
    {
      "id": "65a1b2c3...",
      "code": "STD",
      "name": "Standard Room",
      "description": "Comfortable room with modern amenities",
      "base_occupancy": 2,
      "max_occupancy": 3,
      "amenities": ["WiFi", "TV", "Safe"],
      "size_sqft": 300,
      "images": ["url1", "url2"]
    }
  ]
}
```

#### GET `/rooms/{room_type_id}/rates`
Get rates for a specific room type.

---

### Booking Endpoints

#### POST `/bookings`
Create a new reservation.

**Request:**
```json
{
  "check_in": "2026-01-20",
  "check_out": "2026-01-25",
  "room_type_id": "65a1b2c3...",
  "rate_code": "BAR",
  "bed_configuration": "KING",
  "view": "city",
  "guests": {
    "adults": 2,
    "children": 0
  },
  "primary_guest": {
    "title": "Mr",
    "first_name": "John",
    "last_name": "Smith",
    "email": "john.smith@email.com",
    "phone": {
      "country_code": "+1",
      "number": "5551234567"
    }
  },
  "special_requests": ["high floor", "extra pillows"],
  "special_occasion": "anniversary",
  "estimated_arrival": "18:00",
  "packages": ["romance_package"],
  "payment": {
    "card_number": "4111111111111111",
    "expiry": "12/27",
    "cvv": "123",
    "name_on_card": "John Smith"
  },
  "accept_policies": true,
  "voice_session_id": "session_abc123"  // If from voice agent
}
```

**Response:**
```json
{
  "success": true,
  "booking": {
    "confirmation_number": "ROOMI-20260120-001",
    "status": "confirmed",
    "check_in": "2026-01-20T15:00:00",
    "check_out": "2026-01-25T11:00:00",
    "nights": 5,
    "room_type": "Deluxe Room",
    "view": "city",
    "bed": "King",
    "guest_name": "Mr. John Smith",
    "pricing": {
      "room_total": 750.00,
      "packages": 75.00,
      "taxes": 103.13,
      "grand_total": 928.13,
      "currency": "USD"
    },
    "special_requests": ["high floor", "extra pillows"],
    "special_occasion": "anniversary"
  },
  "confirmation_email_sent": true
}
```

#### GET `/bookings/{confirmation_number}`
Retrieve booking details.

#### PUT `/bookings/{confirmation_number}`
Modify an existing booking.

**Request:**
```json
{
  "check_in": "2026-01-22",
  "check_out": "2026-01-25",
  "modification_reason": "Schedule change"
}
```

#### DELETE `/bookings/{confirmation_number}`
Cancel a booking.

**Request:**
```json
{
  "cancellation_reason": "Change of plans"
}
```

**Response:**
```json
{
  "success": true,
  "cancellation_reference": "CXL-ROOMI-20260120-001",
  "refund": {
    "eligible": true,
    "amount": 928.13,
    "status": "processing",
    "estimated_days": 5
  }
}
```

#### GET `/bookings/search`
Search bookings by guest name, phone, or email.

**Query Parameters:**
- `guest_name`: String
- `email`: String  
- `phone`: String
- `date_from`: Date
- `date_to`: Date

---

### Guest Endpoints

#### POST `/guests`
Create a new guest profile.

#### GET `/guests/{guest_id}`
Get guest profile.

#### GET `/guests/search`
Search guests.

**Query Parameters:**
- `name`: String
- `email`: String
- `phone`: String

#### PUT `/guests/{guest_id}/preferences`
Update guest preferences.

---

### Service Request Endpoints

#### POST `/services/requests`
Create a service request.

**Request:**
```json
{
  "booking_id": "65a1b2c3...",
  "room_number": "405",
  "request_type": "housekeeping",
  "details": {
    "category": "extra_amenities",
    "items": ["towels", "pillows"],
    "quantity": 2
  },
  "priority": "normal"
}
```

#### GET `/services/requests/{request_id}`
Get service request status.

---

### Voice Agent Internal Endpoints

#### POST `/voice/session/start`
Initialize a voice session.

**Request:**
```json
{
  "caller_id": "+15551234567",
  "livekit_room": "room_abc123"
}
```

**Response:**
```json
{
  "session_id": "session_abc123",
  "greeting": "Thank you for calling Grand Hotel...",
  "settings": {
    "voice_id": "aura-asteria-en",
    "language": "en-US"
  }
}
```

#### POST `/voice/session/{session_id}/transcript`
Store transcript chunk.

#### POST `/voice/session/{session_id}/intent`
Log detected intent.

#### POST `/voice/session/{session_id}/end`
End voice session and finalize logs.

---

### Admin Endpoints

#### GET `/admin/dashboard`
Get dashboard statistics.

**Response:**
```json
{
  "today": {
    "arrivals": 15,
    "departures": 12,
    "in_house": 85,
    "available_rooms": 23,
    "occupancy_rate": 0.79
  },
  "voice_agent": {
    "calls_today": 47,
    "bookings_completed": 23,
    "conversion_rate": 0.49,
    "avg_call_duration": 185
  },
  "revenue": {
    "today": 12500.00,
    "mtd": 245000.00
  }
}
```

#### GET `/admin/calls`
Get call logs with filtering.

#### PUT `/admin/settings`
Update hotel settings.

---

## Voice Agent Architecture

### Agent Core Components

```
┌─────────────────────────────────────────────────────────────────┐
│                     VoiceAgentCore                              │
│  ├── SessionManager         - Manages call sessions             │
│  ├── ConversationState      - Tracks conversation context       │
│  ├── IntentClassifier       - Identifies user intents           │
│  ├── EntityExtractor        - Extracts booking details          │
│  ├── DialogueManager        - Controls conversation flow        │
│  ├── ResponseGenerator      - Creates natural responses         │
│  └── ActionExecutor         - Performs booking operations       │
└─────────────────────────────────────────────────────────────────┘
```

### Conversation State Machine

```python
class ConversationState(Enum):
    GREETING = "greeting"
    INTENT_DETECTION = "intent_detection"
    COLLECT_DATES = "collect_dates"
    COLLECT_GUESTS = "collect_guests"
    CHECK_AVAILABILITY = "check_availability"
    ROOM_SELECTION = "room_selection"
    COLLECT_GUEST_INFO = "collect_guest_info"
    RATE_SELECTION = "rate_selection"
    COLLECT_PAYMENT = "collect_payment"
    CONFIRM_BOOKING = "confirm_booking"
    CLOSING = "closing"
    MODIFICATION = "modification"
    CANCELLATION = "cancellation"
    TRANSFER = "transfer"
    ERROR = "error"
```

### Intent Classification

| Intent | Description | Example Utterances |
|--------|-------------|-------------------|
| `book_room` | New reservation | "I want to book a room", "Make a reservation" |
| `check_availability` | Check if rooms available | "Do you have rooms?", "What's available?" |
| `modify_booking` | Change existing booking | "I need to change my dates", "Modify reservation" |
| `cancel_booking` | Cancel booking | "Cancel my booking", "I need to cancel" |
| `get_info` | General inquiry | "What time is checkout?", "Do you have parking?" |
| `confirm` | Affirmative response | "Yes", "Correct", "That's right" |
| `deny` | Negative response | "No", "That's wrong", "Not that" |
| `request_human` | Transfer request | "Speak to someone", "Talk to a person" |

### Entity Extraction

| Entity | Type | Examples |
|--------|------|----------|
| `check_in_date` | Date | "January 20th", "next Friday", "tomorrow" |
| `check_out_date` | Date | "the 25th", "for 3 nights", "next Monday" |
| `guest_count` | Number | "2 adults", "just me", "4 people" |
| `children_count` | Number | "2 kids", "no children" |
| `room_type` | RoomType | "deluxe", "suite", "standard" |
| `bed_preference` | BedType | "king bed", "two beds", "twin" |
| `guest_name` | PersonName | "John Smith", "Sarah Johnson" |
| `phone_number` | Phone | "555-123-4567" |
| `email` | Email | "john@email.com" |
| `confirmation_number` | BookingRef | "ROOMI-20260120-001" |
| `special_request` | String | "high floor", "late checkout" |

---

## Integration Details

### LiveKit Integration

```python
# LiveKit Room Configuration
LIVEKIT_CONFIG = {
    "url": "wss://your-livekit-server.com",
    "api_key": "your_api_key",
    "api_secret": "your_api_secret",
    "room_options": {
        "auto_subscribe": True,
        "adaptive_stream": True,
        "dynacast": True
    },
    "audio_options": {
        "sample_rate": 16000,
        "channels": 1,
        "echo_cancellation": True,
        "noise_suppression": True,
        "auto_gain_control": True
    }
}
```

### Deepgram Integration

```python
# Speech-to-Text Configuration
DEEPGRAM_STT_CONFIG = {
    "model": "nova-2",
    "language": "en-US",
    "punctuate": True,
    "diarize": False,
    "smart_format": True,
    "filler_words": False,
    "profanity_filter": True,
    "numerals": True,
    "interim_results": True,
    "endpointing": 500,  # ms
    "vad_events": True
}

# Text-to-Speech Configuration
DEEPGRAM_TTS_CONFIG = {
    "model": "aura-asteria-en",  # Female voice
    # "model": "aura-orion-en",  # Male voice
    "encoding": "linear16",
    "sample_rate": 16000,
    "container": "none"
}
```

### Groq LLM Integration

```python
# LLM Configuration
GROQ_CONFIG = {
    "api_key": "your_groq_api_key",
    "model": "llama-3.1-70b-versatile",  # or "mixtral-8x7b-32768"
    "temperature": 0.7,
    "max_tokens": 500,
    "top_p": 0.9,
    "stream": True
}

# System Prompt Template
SYSTEM_PROMPT = """
You are Roomi, an AI receptionist for {hotel_name}. Your role is to:
1. Help guests make room reservations
2. Answer questions about the hotel
3. Process service requests

Current conversation state: {state}
Guest information collected: {context}
Available room types: {room_types}

Respond naturally and professionally. Keep responses concise for voice.
Always confirm information before proceeding.
"""
```

---

## Deployment Configuration

### Docker Compose

```yaml
version: '3.8'

services:
  # FastAPI Backend
  api:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URL=mongodb://mongodb:27017/roomiai
      - GROQ_API_KEY=${GROQ_API_KEY}
      - DEEPGRAM_API_KEY=${DEEPGRAM_API_KEY}
      - LIVEKIT_URL=${LIVEKIT_URL}
      - LIVEKIT_API_KEY=${LIVEKIT_API_KEY}
      - LIVEKIT_API_SECRET=${LIVEKIT_API_SECRET}
      - JWT_SECRET=${JWT_SECRET}
    depends_on:
      - mongodb
    restart: unless-stopped

  # Voice Agent Service
  voice-agent:
    build:
      context: ./voice-agent
      dockerfile: Dockerfile
    environment:
      - API_URL=http://api:8000
      - DEEPGRAM_API_KEY=${DEEPGRAM_API_KEY}
      - GROQ_API_KEY=${GROQ_API_KEY}
      - LIVEKIT_URL=${LIVEKIT_URL}
      - LIVEKIT_API_KEY=${LIVEKIT_API_KEY}
      - LIVEKIT_API_SECRET=${LIVEKIT_API_SECRET}
    depends_on:
      - api
    restart: unless-stopped

  # MongoDB Database
  mongodb:
    image: mongo:7.0
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    restart: unless-stopped

  # Redis (for session caching)
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    restart: unless-stopped

volumes:
  mongodb_data:
```

### Environment Variables

```env
# Database
MONGODB_URL=mongodb://localhost:27017/roomiai

# API Keys
GROQ_API_KEY=your_groq_api_key
DEEPGRAM_API_KEY=your_deepgram_api_key

# LiveKit
LIVEKIT_URL=wss://your-livekit-cloud.livekit.cloud
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret

# Security
JWT_SECRET=your_secure_jwt_secret
ENCRYPTION_KEY=your_encryption_key

# Hotel Settings
HOTEL_ID=HOTEL-001
HOTEL_NAME=Grand Hotel
```

---

## Security Considerations

### Data Protection

1. **PCI Compliance**
   - Never store full card numbers
   - Use tokenization for payment data
   - Encrypt sensitive data at rest

2. **Personal Data**
   - Mask phone numbers in logs
   - Encrypt guest PII in database
   - Implement data retention policies

3. **Voice Data**
   - Inform callers about recording
   - Store transcripts securely
   - Auto-delete recordings after X days

### API Security

1. **Authentication**
   - JWT tokens with short expiry
   - Refresh token rotation
   - Rate limiting per endpoint

2. **Input Validation**
   - Sanitize all inputs
   - Validate date ranges
   - Check for injection attacks

3. **Network Security**
   - HTTPS only
   - CORS configuration
   - WAF protection

---

## Project Structure

```
roomiai/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app
│   │   ├── config.py            # Configuration
│   │   ├── database.py          # MongoDB connection
│   │   ├── models/
│   │   │   ├── booking.py
│   │   │   ├── guest.py
│   │   │   ├── room.py
│   │   │   └── payment.py
│   │   ├── schemas/
│   │   │   ├── booking.py
│   │   │   ├── guest.py
│   │   │   └── room.py
│   │   ├── routers/
│   │   │   ├── bookings.py
│   │   │   ├── rooms.py
│   │   │   ├── guests.py
│   │   │   ├── services.py
│   │   │   ├── voice.py
│   │   │   └── admin.py
│   │   ├── services/
│   │   │   ├── availability.py
│   │   │   ├── pricing.py
│   │   │   ├── email.py
│   │   │   └── payment.py
│   │   └── utils/
│   │       ├── auth.py
│   │       └── helpers.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── voice-agent/
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── core.py              # Main agent logic
│   │   ├── session.py           # Session management
│   │   ├── conversation.py      # Conversation state machine
│   │   ├── intents.py           # Intent classification
│   │   ├── entities.py          # Entity extraction
│   │   ├── dialogue.py          # Dialogue management
│   │   ├── responses.py         # Response templates
│   │   └── actions.py           # Booking actions
│   ├── integrations/
│   │   ├── livekit_client.py    # LiveKit integration
│   │   ├── deepgram_stt.py      # Speech-to-text
│   │   ├── deepgram_tts.py      # Text-to-speech
│   │   └── groq_llm.py          # LLM client
│   ├── Dockerfile
│   └── requirements.txt
│
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Summary

This technical document provides a complete blueprint for the RoomiAI hotel reservation voice agent, including:

1. **System Architecture** - Complete component diagram and data flow
2. **Database Schemas** - 10 MongoDB collections with detailed field definitions
3. **API Endpoints** - 25+ REST endpoints for all operations
4. **Voice Agent Design** - State machine, intent classification, entity extraction
5. **Integrations** - LiveKit, Deepgram, Groq configurations
6. **Deployment** - Docker Compose setup and environment configuration
7. **Security** - PCI compliance, data protection, API security

The system is designed to be:
- **Scalable** - Containerized microservices architecture
- **Cost-effective** - Uses free/affordable API tiers
- **Maintainable** - Clean separation of concerns
- **Secure** - Industry-standard security practices

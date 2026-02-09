# RoomiAI - Core Room Booking Conversation
## Complete Happy Path Flow (Foundation Build)

---

## Overview

This document contains the **complete core conversation flow** for a standard room booking. This is the foundation that covers 80% of all booking calls. Focus on implementing this perfectly before adding edge cases.

**Scope:** New room reservation from start to finish (happy path with basic alternatives)

---

## Hotel Configuration (Sample Data for Development)

### Hotel Information

| Field | Value |
|-------|-------|
| **Hotel Name** | Grand Hotel |
| **Address** | 123 Main Street, Downtown, City 12345 |
| **Phone** | +1-555-HOTEL-00 |
| **Email** | reservations@grandhotel.com |
| **Check-in Time** | 3:00 PM |
| **Check-out Time** | 11:00 AM |
| **Currency** | USD ($) |
| **Tax Rate** | 12.5% |

---

### Room Inventory (Total: 50 Rooms)

| Room Type | Code | Total Rooms | Bed Options | Max Guests | Views Available |
|-----------|------|-------------|-------------|------------|-----------------|
| **Standard Room** | STD | 20 rooms | King / 2 Queens | 3 adults | City, Courtyard |
| **Deluxe Room** | DLX | 20 rooms | King / 2 Queens | 3 adults | City, Garden, Pool |
| **Junior Suite** | STE-J | 6 rooms | King | 3 adults | City, Garden |
| **Executive Suite** | STE-E | 3 rooms | King | 4 adults | City Panoramic |
| **Family Room** | FAM | 1 room | 2 Queens + Sofa | 5 adults | Garden |

---

### Room Pricing (Per Night)

| Room Type | Weekday Rate | Weekend Rate | Holiday Rate |
|-----------|--------------|--------------|--------------|
| **Standard Room** | $120 | $140 | $180 |
| **Deluxe Room** | $150 | $180 | $220 |
| **Junior Suite** | $220 | $260 | $320 |
| **Executive Suite** | $350 | $400 | $500 |
| **Family Room** | $250 | $300 | $380 |

> **Note:** Weekend = Friday & Saturday nights. Holiday = Peak seasons & holidays.

---

### Room Amenities

| Room Type | Size (sq ft) | Amenities |
|-----------|--------------|-----------|
| **Standard** | 300 | WiFi, TV, Safe, Coffee Maker, Mini Fridge |
| **Deluxe** | 400 | All Standard + Bathrobe, Premium Toiletries, Workspace |
| **Junior Suite** | 550 | All Deluxe + Living Area, Sofa, 2 TVs |
| **Executive Suite** | 800 | All Junior + Dining Table, Kitchenette, Premium Mini Bar |
| **Family Room** | 600 | All Deluxe + Extra Beds, Kids Amenity Pack |

---

### Rate Plans Available

| Rate Code | Name | Description | Cancellation | Discount |
|-----------|------|-------------|--------------|----------|
| **BAR** | Best Available Rate | Flexible booking | Free cancel 24h before | - |
| **ADV** | Advance Purchase | Book 7+ days ahead | Non-refundable | 15% off |
| **PKG-BB** | Bed & Breakfast | Includes daily breakfast | Free cancel 48h before | +$25/night |
| **PKG-ROM** | Romance Package | Champagne + roses + late checkout | Free cancel 48h before | +$75 total |
| **AAA** | AAA/Senior Rate | Valid ID required | Free cancel 24h before | 10% off |

---

### Additional Services & Fees

| Service | Price | Notes |
|---------|-------|-------|
| **Parking (Self)** | $15/night | Uncovered |
| **Parking (Valet)** | $25/night | Covered garage |
| **Early Check-in** | $50 | Subject to availability (from 12 PM) |
| **Late Check-out** | $50 | Subject to availability (until 2 PM) |
| **Extra Person** | $30/night | Beyond base occupancy |
| **Rollaway Bed** | $25/night | Subject to availability |
| **Crib** | Free | Request in advance |
| **Pet Fee** | $50/stay | Small pets only, max 25 lbs |
| **Airport Shuttle** | $40/trip | One-way, book 24h ahead |

---

### Policies

| Policy | Details |
|--------|---------|
| **Standard Cancellation** | Free cancellation up to 24 hours before check-in. Late cancellation or no-show = 1 night charge. |
| **Deposit** | First night charged at booking to guarantee reservation. |
| **Payment Methods** | Visa, Mastercard, American Express, Discover |
| **Minimum Age** | Guest must be 21+ to check in |
| **Smoking** | Non-smoking hotel. $250 cleaning fee if violated. |
| **Pets** | Allowed with fee in designated rooms only |

---

### Sample Availability (For Testing)

For development/testing, assume these rooms are available:

| Date Range | Standard | Deluxe | Jr. Suite | Exec Suite | Family |
|------------|----------|--------|-----------|------------|--------|
| Jan 10-15 | 8 | 5 | 2 | 1 | 1 |
| Jan 15-20 | 12 | 10 | 4 | 2 | 1 |
| Jan 20-25 | 5 | 3 | 1 | 0 | 1 |
| Jan 25-30 | 15 | 12 | 5 | 3 | 1 |

---

## Complete Booking Conversation Script

### PHASE 1: GREETING & INTENT

```
[Call Connected]

AGENT: "Thank you for calling Grand Hotel. This is Roomi, your virtual 
        reservation assistant. How may I help you today?"

GUEST: "Hi, I'd like to book a room."

AGENT: "I'd be happy to help you make a reservation. 
        Let me get a few details from you."
```

---

### PHASE 2: CHECK-IN DATE

```
AGENT: "What date would you like to check in?"

GUEST: "January 20th"

AGENT: "January 20th, perfect."
```

**Alternative Responses to Handle:**
```
GUEST: "Next Friday"
AGENT: "That would be Friday, January 17th. Is that correct?"
GUEST: "Yes"
AGENT: "Great, January 17th."

GUEST: "The 20th"
AGENT: "January 20th, perfect."

GUEST: "Tomorrow"
AGENT: "That would be January 9th."
```

---

### PHASE 3: CHECK-OUT DATE

```
AGENT: "And what date would you like to check out?"

GUEST: "January 25th"

AGENT: "January 25th. So that's 5 nights, from January 20th to 25th. 
        Is that correct?"

GUEST: "Yes"

AGENT: "Perfect."
```

**Alternative Responses to Handle:**
```
GUEST: "For 3 nights"
AGENT: "Three nights would have you checking out on January 23rd. 
        Is that correct?"

GUEST: "On the 25th"
AGENT: "January 25th, so 5 nights total."
```

---

### PHASE 4: NUMBER OF GUESTS

```
AGENT: "How many guests will be staying?"

GUEST: "Two adults"

AGENT: "Two adults, perfect."
```

**Alternative Responses to Handle:**
```
GUEST: "Just me"
AGENT: "One adult, noted."

GUEST: "4 people"
AGENT: "4 guests. How many adults and how many children?"

GUEST: "2 adults and 2 kids"
AGENT: "2 adults and 2 children. What are the ages of the children?"

GUEST: "8 and 12"
AGENT: "Ages 8 and 12, noted."
```

---

### PHASE 5: ROOM TYPE PREFERENCE

```
AGENT: "What type of room would you prefer? 
        We have Standard Rooms, Deluxe Rooms, and Suites available."

GUEST: "Deluxe room"

AGENT: "A Deluxe Room, excellent choice."
```

**Alternative Responses to Handle:**
```
GUEST: "What's the difference?"
AGENT: "Our Standard Rooms are comfortable with basic amenities at $120 per night.
        Deluxe Rooms are larger with premium views at $150 per night.
        Suites include a separate living area at $220 per night.
        Which would you prefer?"

GUEST: "Something nice but not too expensive"
AGENT: "I'd recommend our Deluxe Room at $150 per night. 
        It offers a great balance of comfort and value."
```

---

### PHASE 6: ROOM PREFERENCES (BED & VIEW)

```
AGENT: "Would you prefer a king bed or two queen beds?"

GUEST: "King bed"

AGENT: "King bed, noted. And for the view, 
        we have city view and garden view available. 
        Which would you prefer?"

GUEST: "City view"

AGENT: "Deluxe Room with king bed and city view, perfect."
```

---

### PHASE 7: AVAILABILITY CHECK

```
AGENT: "Let me check availability for you...

        Great news! I have a Deluxe Room with king bed and city view 
        available from January 20th to 25th.
        
        The rate is $150 per night, totaling $750 for 5 nights, 
        plus taxes of approximately $94.
        
        Would you like to proceed with this booking?"

GUEST: "Yes"

AGENT: "Excellent! Let me collect your details."
```

**If Room Not Available (Basic Alternative):**
```
AGENT: "I apologize, but the Deluxe Room with city view is fully booked 
        for those dates. However, I have these options available:
        
        1. Deluxe Room with garden view at the same rate of $150 per night
        2. A Suite with city view at $220 per night
        
        Which would you prefer?"

GUEST: "The garden view is fine"

AGENT: "Deluxe Room with garden view at $150 per night. 
        Your total for 5 nights would be $750 plus taxes.
        Shall I proceed?"
```

---

### PHASE 8: GUEST NAME

```
AGENT: "May I have the name for the reservation?"

GUEST: "John Smith"

AGENT: "John Smith. Could you spell your last name for me, please?"

GUEST: "S-M-I-T-H"

AGENT: "S-M-I-T-H, thank you Mr. Smith."
```

---

### PHASE 9: CONTACT INFORMATION

```
AGENT: "What's the best phone number to reach you?"

GUEST: "555-123-4567"

AGENT: "555-123-4567. And your email address for the confirmation?"

GUEST: "john.smith@email.com"

AGENT: "john.smith@email.com. I'll send your confirmation there."
```

---

### PHASE 10: SPECIAL REQUESTS

```
AGENT: "Do you have any special requests for your stay? 
        For example, high floor, extra pillows, or any special occasion?"

GUEST: "It's our anniversary, and we'd like a high floor if possible"

AGENT: "How wonderful! Congratulations! I'll note your anniversary 
        and request a high floor room for you."
```

**Alternative Responses:**
```
GUEST: "No, nothing special"
AGENT: "No problem. Let me proceed with the booking."

GUEST: "Late checkout if possible"
AGENT: "I'll add a late checkout request. These are subject to availability 
        on the day of departure."
```

---

### PHASE 11: PAYMENT INFORMATION

```
AGENT: "To secure your reservation, I'll need a credit card. 
        This will only be charged according to our cancellation policy.
        
        May I have the card number, please?"

GUEST: "4111 2222 3333 4444"

AGENT: "And the expiration date?"

GUEST: "December 2027"

AGENT: "12/27. And the 3-digit security code on the back?"

GUEST: "789"

AGENT: "And the name exactly as it appears on the card?"

GUEST: "John Smith"

AGENT: "Thank you. Your card has been securely recorded."
```

---

### PHASE 12: POLICIES & ESTIMATED ARRIVAL

```
AGENT: "Our cancellation policy allows free cancellation up to 24 hours 
        before check-in. Cancellations within 24 hours will be charged 
        one night's stay.
        
        Do you accept this policy?"

GUEST: "Yes, that's fine"

AGENT: "Thank you. What time do you expect to arrive?"

GUEST: "Around 6 PM"

AGENT: "6 PM, noted. Check-in begins at 3 PM, so your room will be ready."
```

---

### PHASE 13: BOOKING CONFIRMATION

```
AGENT: "Let me confirm your reservation:

        Guest Name: Mr. John Smith
        Check-in: Monday, January 20th, 2026
        Check-out: Saturday, January 25th, 2026
        Duration: 5 nights
        
        Room: Deluxe Room with King Bed and City View
        Guests: 2 adults
        
        Room Rate: $150 per night
        Total: $750 plus $94 taxes
        Grand Total: $844
        
        Special Notes: Anniversary celebration, high floor request
        Arrival Time: 6 PM
        
        Is everything correct?"

GUEST: "Yes, that's correct"

AGENT: "Excellent!"
```

---

### PHASE 14: FINAL CONFIRMATION & CLOSING

```
AGENT: "Your reservation is confirmed!
        
        Your confirmation number is R-O-O-M-I-2-0-2-6-0-1-2-0-0-1.
        That's ROOMI-20260120-01.
        
        I'm sending a confirmation email to john.smith@email.com right now.
        
        Just a reminder:
        - Check-in is at 3 PM
        - Our address is 123 Main Street, Downtown
        - Parking is available at $20 per night if needed
        
        We look forward to celebrating your anniversary with you, Mr. Smith!
        
        Is there anything else I can help you with today?"

GUEST: "No, that's all. Thank you!"

AGENT: "Thank you for choosing Grand Hotel. 
        Have a wonderful day, and we'll see you on January 20th. Goodbye!"

[Call Ends]
```

---

## Data Collected Summary

By the end of this conversation, the agent has collected:

| Field | Value | Phase |
|-------|-------|-------|
| Check-in Date | 2026-01-20 | 2 |
| Check-out Date | 2026-01-25 | 3 |
| Nights | 5 | 3 |
| Adults | 2 | 4 |
| Children | 0 | 4 |
| Room Type | Deluxe | 5 |
| Bed Type | King | 6 |
| View | City | 6 |
| Rate per Night | $150 | 7 |
| Guest First Name | John | 8 |
| Guest Last Name | Smith | 8 |
| Phone | 555-123-4567 | 9 |
| Email | john.smith@email.com | 9 |
| Special Occasion | Anniversary | 10 |
| Room Preference | High Floor | 10 |
| Card Last 4 | 4444 | 11 |
| Card Expiry | 12/27 | 11 |
| Card Name | John Smith | 11 |
| Policies Accepted | Yes | 12 |
| Arrival Time | 18:00 | 12 |
| Confirmation # | ROOMI-20260120-01 | 14 |

---

## API Calls Made During Conversation

| Phase | API Endpoint | Purpose |
|-------|--------------|---------|
| 7 | `GET /rooms/availability` | Check room availability |
| 13 | `POST /bookings` | Create reservation |
| 14 | `POST /notifications/email` | Send confirmation |

---

## Conversation State Flow

```
GREETING
    ↓
COLLECT_CHECK_IN_DATE
    ↓
COLLECT_CHECK_OUT_DATE
    ↓
COLLECT_GUESTS
    ↓
COLLECT_ROOM_TYPE
    ↓
COLLECT_ROOM_PREFERENCES
    ↓
CHECK_AVAILABILITY
    ↓ (if not available → offer alternatives)
COLLECT_GUEST_NAME
    ↓
COLLECT_CONTACT_INFO
    ↓
COLLECT_SPECIAL_REQUESTS
    ↓
COLLECT_PAYMENT
    ↓
CONFIRM_POLICIES
    ↓
REVIEW_BOOKING
    ↓
FINALIZE_BOOKING
    ↓
CLOSING
```

---

## Agent Prompts Summary (For LLM)

### Prompt Structure for Each Phase:

```python
PHASE_PROMPTS = {
    "greeting": "Greet the guest warmly and ask how you can help.",
    
    "collect_check_in": "Ask for the check-in date. Confirm the date back to the guest.",
    
    "collect_check_out": "Ask for check-out date. Calculate nights and confirm.",
    
    "collect_guests": "Ask number of guests. If more than 2, ask adults/children breakdown.",
    
    "collect_room_type": "Ask room type preference. Offer Standard, Deluxe, or Suite.",
    
    "collect_preferences": "Ask bed preference (King/Queen) and view preference.",
    
    "check_availability": "Check availability and present rate. If unavailable, offer alternatives.",
    
    "collect_name": "Ask for guest name. Confirm spelling of last name.",
    
    "collect_contact": "Ask for phone number and email address.",
    
    "collect_requests": "Ask for special requests or occasions.",
    
    "collect_payment": "Collect card number, expiry, CVV, and name on card.",
    
    "confirm_policies": "Explain cancellation policy. Ask for acceptance. Get arrival time.",
    
    "review_booking": "Read back all booking details. Ask for confirmation.",
    
    "finalize": "Provide confirmation number. Mention email sent. Offer additional help.",
    
    "closing": "Thank guest warmly. Mention looking forward to their stay. Say goodbye."
}
```

---

## Implementation Priority

### Build in This Order:

1. **Phase 1-3**: Greeting + Date Collection
2. **Phase 4-6**: Guest Count + Room Selection
3. **Phase 7**: Availability Check + Basic Alternative Handling
4. **Phase 8-9**: Guest Name + Contact Info
5. **Phase 10**: Special Requests
6. **Phase 11**: Payment Collection
7. **Phase 12-14**: Policies + Confirmation + Closing

### Test Each Phase Before Moving to Next

---

## Notes for Development

1. **Keep responses short** - Voice interactions need concise replies
2. **Always confirm back** - Repeat important info (dates, spelling, numbers)
3. **Use natural transitions** - "Perfect", "Great", "Noted" between phases
4. **Don't ask too many questions at once** - One question per turn
5. **Handle "yes/no" smoothly** - Move forward on confirmation

---

This core flow forms the foundation. Once this works perfectly, add edge cases layer by layer.

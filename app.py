"""
RoomiAI - Hotel Reservation Voice Agent

This is the main entry point for the AI voice agent. It connects to LiveKit for
real-time audio, uses Deepgram for STT/TTS, and Groq LLM for natural language understanding.
The agent can handle room reservations, check availability, and answer hotel questions.

Note: @function_tool decorated methods MUST be inside the Agent class (LiveKit requirement).
The business logic is organized in backend/tools/ and called from here.
"""

import os
from typing import Any

from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions, RunContext, function_tool
from livekit.plugins import silero, deepgram, groq

# Import business logic from tools folder
from backend.tools.booking_tools import (
    check_room_availability,
    create_room_booking,
    get_booking_details,
    cancel_room_booking
)
from backend.tools.room_tools import (
    get_all_room_types,
    get_hotel_information
)

load_dotenv()


# ============================================
# Hotel Receptionist Agent with Tools
# ============================================
class HotelAssistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are Roomi, a friendly hotel receptionist for Grand Hotel. Help guests book rooms.

Flow: Ask check-in date, check-out date, guests count, then room type, then name, phone, email. Use tools to check availability and create bookings.

Keep responses SHORT (1-2 sentences). Ask ONE thing at a time. Be warm and helpful.""",
        )

    # ============================================
    # TOOL: Check Room Availability
    # ============================================
    @function_tool(
        description="Check room availability for given check-in and check-out dates. Call this when guest asks about availability or wants to book a room."
    )
    async def check_availability(
        self,
        context: RunContext,
        check_in: str,
        check_out: str,
        room_type: str = "any",
        guests: str = "2"
    ) -> dict[str, Any]:
        """
        Check if rooms are available for the specified dates.
        
        Args:
            check_in: Check-in date (e.g., 'January 20' or '2026-01-20')
            check_out: Check-out date (e.g., 'January 25' or '2026-01-25')
            room_type: Type of room (standard, deluxe, suite, any). Default is 'any'
            guests: Number of guests staying as text. Default is '2'
        """
        # Call business logic from tools folder
        return await check_room_availability(check_in, check_out, room_type, guests)

    # ============================================
    # TOOL: Create Booking
    # ============================================
    @function_tool(
        description="Create a new room reservation. IMPORTANT: Only call this AFTER you have collected ALL of the following from the guest: 1) guest_name (real name, not null), 2) phone number, 3) email address, 4) room type, 5) dates. If any info is missing, ask the guest first before calling this tool."
    )
    async def create_booking(
        self,
        context: RunContext,
        guest_name: str,
        check_in: str,
        check_out: str,
        room_type: str,
        phone: str,
        email: str,
        guests: str = "2",
        special_requests: str = ""
    ) -> dict[str, Any]:
        """
        Create a new hotel room reservation.
        
        Args:
            guest_name: Full name of the guest - REQUIRED, must be a real name
            check_in: Check-in date - REQUIRED
            check_out: Check-out date - REQUIRED
            room_type: Type of room - REQUIRED
            phone: Guest phone number - REQUIRED
            email: Guest email address - REQUIRED
            guests: Number of guests as text (default '2')
            special_requests: Any special requests
        """
        # Handle "null" string that LLM sometimes passes
        if guest_name.lower() in ["null", "none", ""]:
            return {"success": False, "message": "Please collect the guest's name first before creating a booking."}
        if phone.lower() in ["null", "none", ""]:
            return {"success": False, "message": "Please collect the guest's phone number first before creating a booking."}
        if email.lower() in ["null", "none", ""]:
            return {"success": False, "message": "Please collect the guest's email address first before creating a booking."}
        
        # Call business logic from tools folder
        return await create_room_booking(
            guest_name, check_in, check_out, room_type,
            phone, email, guests, special_requests
        )

    # ============================================
    # TOOL: Get Room Types
    # ============================================
    @function_tool(
        description="Get all available room types with their descriptions, amenities and pricing. Call this when guest asks about room options or what types of rooms are available."
    )
    async def get_room_types(
        self,
        context: RunContext,
        filter_type: str = "all"
    ) -> dict[str, Any]:
        """
        Get all available room types with descriptions and base pricing.
        
        Args:
            filter_type: Filter by room category - 'all', 'budget', 'premium'. Default is 'all'
        """
        # Call business logic from tools folder
        return await get_all_room_types(filter_type)

    # ============================================
    # TOOL: Get Hotel Info
    # ============================================
    @function_tool(
        description="Get general hotel information like check-in time, checkout time, address, and policies. Call this when guest asks about hotel policies or timings."
    )
    async def get_hotel_info(
        self,
        context: RunContext,
        info_type: str = "all"
    ) -> dict[str, Any]:
        """
        Get general hotel information and policies.
        
        Args:
            info_type: Type of info needed - 'all', 'timings', 'policies', 'location'. Default is 'all'
        """
        # Call business logic from tools folder
        return await get_hotel_information(info_type)

    # ============================================
    # TOOL: Get Booking Details
    # ============================================
    @function_tool(
        description="Retrieve details of an existing booking. Call this when guest wants to check their reservation status."
    )
    async def get_booking(
        self,
        context: RunContext,
        confirmation_number: str = "",
        guest_name: str = ""
    ) -> dict[str, Any]:
        """
        Retrieve booking details by confirmation number or guest name.
        
        Args:
            confirmation_number: The booking confirmation number
            guest_name: Guest name to search for
        """
        # Call business logic from tools folder
        return await get_booking_details(confirmation_number, guest_name)

    # ============================================
    # TOOL: Cancel Booking
    # ============================================
    @function_tool(
        description="Cancel an existing booking. Call this when guest wants to cancel their reservation."
    )
    async def cancel_booking(
        self,
        context: RunContext,
        confirmation_number: str
    ) -> dict[str, Any]:
        """
        Cancel an existing reservation.
        
        Args:
            confirmation_number: The booking confirmation number to cancel
        """
        # Call business logic from tools folder
        return await cancel_room_booking(confirmation_number)


# ============================================
# Main Entrypoint
# ============================================
async def entrypoint(ctx: agents.JobContext):
    # Get API keys
    groq_api_key = os.getenv("GROQ_API_KEY")
    deepgram_api_key = os.getenv("DEEPGRAM_API_KEY")
    
    if not groq_api_key:
        raise RuntimeError("GROQ_API_KEY not found in environment variables!")
    if not deepgram_api_key:
        raise RuntimeError("DEEPGRAM_API_KEY not found in environment variables!")

    # Initialize LLM (Groq)
    # Note: llama-3.3-70b-versatile has 12000 TPM limit (higher than 8b's 6000 TPM)
    llm_instance = groq.LLM(
        model="llama-3.3-70b-versatile",
        api_key=groq_api_key,
        temperature=0.3,
    )
    
    # Initialize TTS (Deepgram)
    tts = deepgram.TTS(
        model="aura-asteria-en",
        api_key=deepgram_api_key,
    )

    # Create agent session
    session = AgentSession(
        stt=deepgram.STT(
            model="nova-2",
            language="en",
            api_key=deepgram_api_key
        ),
        llm=llm_instance,
        tts=tts,
        vad=silero.VAD.load(),
    )
    
    # Start the session with the agent
    await session.start(
        room=ctx.room,
        agent=HotelAssistant(),
        room_input_options=RoomInputOptions(),
    )

    # Initial greeting
    await session.say(
        "Thank you for calling Grand Hotel. This is Roomi, your virtual reservation assistant. How may I help you today?"
    )


# ============================================
# Run the Agent
# ============================================
if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
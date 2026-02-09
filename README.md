# 🏨 RoomiAI - AI Voice Agent for Hotel Reservations

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.100+-green.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/MongoDB-Atlas-brightgreen.svg" alt="MongoDB">
  <img src="https://img.shields.io/badge/LiveKit-Voice-red.svg" alt="LiveKit">
  <img src="https://img.shields.io/badge/LLM-Groq-purple.svg" alt="Groq">
</p>

RoomiAI is an intelligent AI-powered voice agent designed to handle hotel room reservations through natural conversation. It uses real-time audio streaming, speech recognition, and natural language understanding to provide a seamless booking experience.

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture Overview](#-architecture-overview)
- [Project Structure](#-project-structure)
- [Technology Stack](#-technology-stack)
- [File Descriptions](#-file-descriptions)
- [Installation & Setup](#-installation--setup)
- [Environment Variables](#-environment-variables)
- [API Endpoints](#-api-endpoints)
- [How It Works](#-how-it-works)
- [Documentation](#-documentation)

---

## ✨ Features

- **🎙️ Real-time Voice Interaction** - Natural conversation using LiveKit audio streaming
- **🗣️ Speech Recognition** - Deepgram-powered Speech-to-Text (STT)
- **🔊 Voice Synthesis** - Natural Text-to-Speech (TTS) with Deepgram Aura voices
- **🧠 AI-Powered Understanding** - Groq LLM (LLaMA 3.3 70B) for natural language understanding
- **📅 Room Booking** - Complete reservation workflow with availability checking
- **📞 Booking Management** - Create, retrieve, and cancel reservations
- **💾 MongoDB Storage** - Persistent data storage using MongoDB Atlas
- **🔧 RESTful API** - FastAPI backend for all operations

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    GUEST (Phone/Web Call)                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   LiveKit Cloud (SFU)                       │
│              Real-time Audio/Video Infrastructure           │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
┌─────────────────────────┐   ┌─────────────────────────────┐
│     Deepgram STT        │   │       Deepgram TTS          │
│  (Speech-to-Text)       │   │    (Text-to-Speech)         │
└─────────────────────────┘   └─────────────────────────────┘
              │                               ▲
              ▼                               │
┌─────────────────────────────────────────────────────────────┐
│                   RoomiAI Voice Agent                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              HotelAssistant (app.py)                │   │
│  │  - check_availability()  - create_booking()         │   │
│  │  - get_room_types()      - get_hotel_info()         │   │
│  │  - get_booking()         - cancel_booking()         │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Groq LLM (LLaMA 3.3 70B)               │   │
│  │  Natural Language Understanding & Response Gen      │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  FastAPI Backend Server                     │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐   │
│  │ /api/bookings │  │  /api/rooms   │  │  /api/info    │   │
│  └───────────────┘  └───────────────┘  └───────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     MongoDB Atlas                           │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐   │
│  │ bookings │ │  rooms   │ │  guests  │ │ room_types   │   │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
FYP-Agent/
│
├── 📄 app.py                           # Main voice agent entry point
├── 📄 .env                             # Environment variables (API keys)
├── 📄 .gitignore                       # Git ignore file
│
├── 📂 backend/                         # FastAPI backend server
│   ├── 📄 main.py                      # FastAPI application entry point
│   │
│   ├── 📂 database/                    # Database layer
│   │   ├── 📄 __init__.py
│   │   ├── 📄 connection.py            # MongoDB connection manager
│   │   └── 📄 schemas.py               # Database schema definitions
│   │
│   ├── 📂 models/                      # Pydantic models for validation
│   │   ├── 📄 __init__.py
│   │   ├── 📄 booking.py               # Booking request/response models
│   │   ├── 📄 room.py                  # Room models
│   │   ├── 📄 guest.py                 # Guest models
│   │   └── 📄 service.py               # Service request models
│   │
│   ├── 📂 routers/                     # API route handlers
│   │   ├── 📄 __init__.py
│   │   ├── 📄 booking.py               # Booking CRUD endpoints
│   │   ├── 📄 rooms.py                 # Room availability endpoints
│   │   ├── 📄 guests.py                # Guest management endpoints
│   │   └── 📄 services.py              # Service request endpoints
│   │
│   ├── 📂 services/                    # Business logic services
│   │   ├── 📄 __init__.py
│   │   ├── 📄 booking_service.py       # Booking business logic
│   │   └── 📄 room_service.py          # Room business logic
│   │
│   └── 📂 tools/                       # Voice agent tool functions
│       ├── 📄 __init__.py
│       ├── 📄 booking_tools.py         # Booking operations for agent
│       ├── 📄 room_tools.py            # Room operations for agent
│       ├── 📄 guest_tools.py           # Guest operations for agent
│       └── 📄 service_tools.py         # Service operations for agent
│
├── 📄 RoomiAI_Technical_Architecture.md    # Detailed technical documentation
├── 📄 RoomiAI_Conversation_Flow.md         # Complete conversation scripts
└── 📄 RoomiAI_Core_Conversation.md         # Core booking flow documentation
```

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Runtime** | Python 3.11+ | Core application language |
| **Voice Agent** | LiveKit Agents SDK | Real-time voice interaction |
| **Speech-to-Text** | Deepgram Nova-2 | Voice transcription |
| **Text-to-Speech** | Deepgram Aura | Voice synthesis |
| **LLM** | Groq (LLaMA 3.3 70B) | Natural language understanding |
| **Backend** | FastAPI | REST API server |
| **Database** | MongoDB Atlas | Data persistence |
| **Async Driver** | Motor | Async MongoDB operations |
| **VAD** | Silero | Voice Activity Detection |

---

## 📚 File Descriptions

### Root Files

| File | Description |
|------|-------------|
| `app.py` | **Main Voice Agent** - Contains the `HotelAssistant` class with all `@function_tool` decorated methods for voice interactions. Initializes LiveKit session with Deepgram STT/TTS and Groq LLM. |
| `.env` | **Environment Configuration** - Stores API keys for LiveKit, MongoDB, Groq, and Deepgram. |
| `.gitignore` | Git ignore rules for `.env` and virtual environment |

### Backend - Database Layer (`backend/database/`)

| File | Description |
|------|-------------|
| `connection.py` | **MongoDB Connection Manager** - Async connection using Motor driver. Provides `connect_to_mongodb()`, `close_mongodb_connection()`, and collection getters (`get_bookings_collection()`, `get_rooms_collection()`, etc.) |
| `schemas.py` | Database schema placeholder definitions |

### Backend - Models (`backend/models/`)

| File | Description |
|------|-------------|
| `booking.py` | **Booking Pydantic Models** - Includes `BookingCreate`, `BookingResponse`, `BookingInDB`, `CancelBookingRequest`, `CancelBookingResponse`, and enums for `RoomType` and `BookingStatus` |
| `room.py` | Room type model definitions |
| `guest.py` | Guest data models (`GuestCreate`, `GuestResponse`) |
| `service.py` | Service request models |

### Backend - Routers (`backend/routers/`)

| File | Description |
|------|-------------|
| `booking.py` | **Booking API Endpoints** - `POST /bookings` (create), `GET /bookings/{id}` (retrieve), `DELETE /bookings/{id}` (cancel), `GET /bookings/search/by-name` (search) |
| `rooms.py` | **Room API Endpoints** - `GET /rooms/types` (list room types), `GET /rooms/availability` (check availability), `GET /rooms/info` (hotel information) |
| `guests.py` | Guest management endpoints |
| `services.py` | Service request endpoints |

### Backend - Tools (`backend/tools/`)

| File | Description |
|------|-------------|
| `booking_tools.py` | **Booking Business Logic** - Functions called by voice agent: `check_room_availability()`, `create_room_booking()`, `get_booking_details()`, `cancel_room_booking()`. Includes fallback logic when API is unavailable. |
| `room_tools.py` | **Room Business Logic** - `get_all_room_types()`, `get_hotel_information()`. Contains fallback data for offline operation. |
| `guest_tools.py` | Guest management functions |
| `service_tools.py` | Service request functions |

### Backend - Main Entry (`backend/main.py`)

**FastAPI Application** with:
- CORS middleware configured
- Lifespan handler for MongoDB connection management
- Routers included at `/api/v1` prefix
- Health check endpoint at `/health`
- Swagger docs at `/docs`

### Documentation Files

| File | Description |
|------|-------------|
| `RoomiAI_Technical_Architecture.md` | Complete technical architecture including MongoDB schemas, API endpoint specifications, system integration details |
| `RoomiAI_Conversation_Flow.md` | Full conversation scripts covering all reservation scenarios, edge cases, and error handling |
| `RoomiAI_Core_Conversation.md` | Core booking flow with phase-by-phase breakdown, sample hotel data, and implementation priorities |

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.11 or higher
- MongoDB Atlas account (or local MongoDB)
- API keys for: LiveKit, Deepgram, Groq

### 1. Clone the Repository

```bash
git clone https://github.com/UsamaMasood12/Voice-Agent.git
cd Voice-Agent
```

### 2. Create Virtual Environment

```bash
python -m venv myenv
# Windows
myenv\Scripts\activate
# Linux/Mac
source myenv/bin/activate
```

### 3. Install Dependencies

```bash
pip install livekit-agents livekit-plugins-deepgram livekit-plugins-groq livekit-plugins-silero
pip install fastapi uvicorn motor python-dotenv httpx pydantic
```

### 4. Configure Environment Variables

Create a `.env` file with the following:

```env
# LiveKit Configuration
LIVEKIT_URL=wss://your-livekit-url.livekit.cloud
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret

# MongoDB Configuration
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/
DB_NAME=roomiai

# FastAPI Backend
API_BASE_URL=http://localhost:8000/api/v1

# AI API Keys
GROQ_API_KEY=your_groq_api_key
DEEPGRAM_API_KEY=your_deepgram_api_key
```

### 5. Run the Backend Server

```bash
python -m backend.main
```

The API will be available at `http://localhost:8000`

### 6. Run the Voice Agent

```bash
python app.py dev
```

---

## 🔐 Environment Variables

| Variable | Description |
|----------|-------------|
| `LIVEKIT_URL` | LiveKit Cloud WebSocket URL |
| `LIVEKIT_API_KEY` | LiveKit API Key |
| `LIVEKIT_API_SECRET` | LiveKit API Secret |
| `MONGODB_URL` | MongoDB Atlas connection string |
| `DB_NAME` | MongoDB database name |
| `API_BASE_URL` | FastAPI backend URL |
| `GROQ_API_KEY` | Groq API key for LLM |
| `DEEPGRAM_API_KEY` | Deepgram API key for STT/TTS |

---

## 🔌 API Endpoints

### Bookings

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/bookings/` | Create a new reservation |
| `GET` | `/api/v1/bookings/{confirmation_number}` | Get booking details |
| `GET` | `/api/v1/bookings/search/by-name` | Search by guest name |
| `GET` | `/api/v1/bookings/` | List all bookings |
| `DELETE` | `/api/v1/bookings/{confirmation_number}` | Cancel a booking |

### Rooms

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/rooms/types` | Get all room types |
| `GET` | `/api/v1/rooms/availability` | Check room availability |
| `GET` | `/api/v1/rooms/info` | Get hotel information |

### Health

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/` | API welcome message |

---

## ⚙️ How It Works

### Voice Agent Flow

1. **Call Initiation**: Guest connects via LiveKit to the voice agent
2. **Speech Recognition**: Deepgram STT transcribes guest speech in real-time
3. **Intent Understanding**: Groq LLM (LLaMA 3.3 70B) processes the transcription
4. **Tool Execution**: Agent calls appropriate `@function_tool` methods
5. **API Communication**: Tools make async HTTP calls to FastAPI backend
6. **Database Operations**: FastAPI interacts with MongoDB for data persistence
7. **Response Generation**: LLM generates natural language response
8. **Voice Synthesis**: Deepgram TTS converts response to speech

### Agent Tools

The `HotelAssistant` class in `app.py` includes these tools:

| Tool | Function | Description |
|------|----------|-------------|
| `check_availability` | `check_room_availability()` | Check room availability for dates |
| `create_booking` | `create_room_booking()` | Create a new reservation |
| `get_room_types` | `get_all_room_types()` | Get available room types and prices |
| `get_hotel_info` | `get_hotel_information()` | Get hotel policies and information |
| `get_booking` | `get_booking_details()` | Retrieve existing booking |
| `cancel_booking` | `cancel_room_booking()` | Cancel a reservation |

---

## 📖 Documentation

Detailed documentation is available in the repository:

- **[Technical Architecture](./RoomiAI_Technical_Architecture.md)** - System design, MongoDB schemas, API specifications
- **[Conversation Flow](./RoomiAI_Conversation_Flow.md)** - Complete conversation scripts and scenarios
- **[Core Conversation](./RoomiAI_Core_Conversation.md)** - Core booking flow and implementation guide

---

## 👨‍💻 Author

**Usama Masood**

---

## 📄 License

This project is part of a Final Year Project (FYP) at UMT.

---

<p align="center">Made with ❤️ for seamless hotel reservations</p>

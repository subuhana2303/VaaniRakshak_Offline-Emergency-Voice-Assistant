# VaaniRakshak - Offline Emergency Voice Assistant

## Overview

VaaniRakshak is an offline voice assistant designed for disaster emergency situations. The application provides voice-activated emergency assistance without requiring internet connectivity, making it ideal for disaster scenarios where network infrastructure may be compromised. The system combines speech recognition, natural language processing, and text-to-speech capabilities to help users find emergency shelters, get medical assistance, and access critical information during crisis situations.

## System Architecture

### Core Architecture Pattern
The application follows a modular architecture with clear separation of concerns:

- **Voice Assistant Core**: Central coordinator managing all components
- **Speech Processing**: Handles speech-to-text and text-to-speech operations
- **Emergency Handler**: Processes emergency requests and provides appropriate responses
- **GUI Interface**: Provides accessible graphical interface for users
- **Configuration Management**: Centralized configuration system

### Technology Stack
- **Language**: Python 3.11
- **Speech Recognition**: Vosk (offline speech recognition)
- **Text-to-Speech**: pyttsx3 (cross-platform TTS)
- **Audio Processing**: PyAudio for real-time audio handling
- **GUI Framework**: Tkinter for cross-platform desktop interface
- **Data Storage**: JSON files for emergency data (phrases, shelters, locations)

### Architecture Rationale
The offline-first architecture was chosen to ensure reliability during disasters when internet connectivity is unavailable. Vosk was selected over cloud-based solutions for its offline capabilities, while pyttsx3 provides reliable TTS without external dependencies.

## Key Components

### Voice Assistant (`voice_assistant.py`)
- **Purpose**: Main orchestrator coordinating all system components
- **Responsibilities**: 
  - Initialize and manage speech processor and emergency handler
  - Coordinate listening sessions and response generation
  - Provide callbacks for GUI integration

### Speech Processor (`speech_processor.py`)
- **Purpose**: Handle all speech-related operations
- **Key Features**:
  - Real-time speech recognition using Vosk
  - Text-to-speech synthesis with pyttsx3
  - Audio stream management with PyAudio
  - Configurable speech parameters (rate, volume, voice preference)

### Emergency Handler (`emergency_handler.py`)
- **Purpose**: Process emergency requests and generate appropriate responses
- **Capabilities**:
  - Parse emergency phrases and intents
  - Locate nearby emergency shelters
  - Provide medical and fire emergency guidance
  - Calculate distances and provide location-based assistance

### GUI Interface (`gui_interface.py`)
- **Purpose**: Provide accessible graphical interface
- **Features**:
  - Real-time conversation display
  - Manual text input option
  - Visual status indicators
  - Control buttons for start/stop operations

### Configuration System (`config.py`)
- **Purpose**: Centralized configuration management
- **Settings**: Audio parameters, recognition thresholds, GUI dimensions, emergency response delays

## Data Flow

### Speech Recognition Flow
1. Audio input captured via PyAudio
2. Real-time processing through Vosk speech recognition model
3. Recognized text passed to Emergency Handler for intent analysis
4. Response generated based on emergency type and location data
5. Text-to-speech synthesis for audio response
6. GUI updated with conversation history

### Emergency Response Flow
1. User voice input recognized and processed
2. Emergency Handler analyzes text for emergency phrases
3. Location-based shelter search performed using distance calculations
4. Appropriate emergency response generated
5. Response delivered via both audio and visual channels

## External Dependencies

### Core Dependencies
- **Vosk**: Offline speech recognition model (requires model download)
- **pyttsx3**: Cross-platform text-to-speech engine
- **PyAudio**: Real-time audio I/O library
- **tkinter**: GUI framework (included with Python)

### System Dependencies
- **espeak-ng**: Text-to-speech backend (installed via Nix)
- **Python 3.11**: Runtime environment
- **Audio system**: Microphone and speakers for voice interaction

### Data Dependencies
- Emergency phrases database (`data/emergency_phrases.json`)
- Shelter locations database (`data/shelters.json`)
- Geographic locations database (`data/locations.json`)

## Deployment Strategy

### Local Development
- Uses Replit with Nix package management
- Automatic dependency installation via pip
- Vosk model downloaded on first run (fallback mode available)

### Production Considerations
- Offline operation is primary requirement
- Local model storage for speech recognition
- JSON-based data storage for emergency information
- Cross-platform compatibility (Windows, macOS, Linux)

### Deployment Commands
```bash
pip install vosk pyttsx3 pyaudio
python main.py
```

## Changelog
- June 14, 2025. Initial setup

## User Preferences
Preferred communication style: Simple, everyday language.
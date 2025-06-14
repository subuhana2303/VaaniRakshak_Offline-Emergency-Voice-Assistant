"""
Configuration settings for VaaniRakshak
Contains all application configuration and constants
"""

import os
from pathlib import Path

class Config:
    """Application configuration class"""
    
    # Application Info
    APP_NAME = "VaaniRakshak"
    APP_VERSION = "1.0.0"
    APP_DESCRIPTION = "Offline Emergency Voice Assistant"
    
    # Audio Configuration
    SAMPLE_RATE = 16000  # Sample rate for audio recording
    CHUNK_SIZE = 4000    # Audio chunk size for processing
    AUDIO_FORMAT = "paInt16"  # Audio format
    CHANNELS = 1         # Mono audio
    
    # Vosk Model Configuration
    VOSK_MODEL_PATH = os.path.join("models", "vosk-model-small-en-us-0.15")
    VOSK_FALLBACK_MODE = True  # Enable fallback when model is not available
    
    # Text-to-Speech Configuration
    TTS_RATE = 150       # Speech rate (words per minute)
    TTS_VOLUME = 0.9     # Volume level (0.0 to 1.0)
    TTS_VOICE_PREFERENCE = "female"  # Preferred voice type
    
    # Recognition Configuration
    RECOGNITION_TIMEOUT = 5.0    # Timeout for speech recognition
    PHRASE_TIMEOUT = 1.0         # Timeout between phrases
    ENERGY_THRESHOLD = 1000      # Energy threshold for voice detection
    
    # Emergency Configuration
    EMERGENCY_RESPONSE_DELAY = 0.5   # Delay before emergency response
    MAX_SHELTER_RESULTS = 5          # Maximum shelter results to return
    LOCATION_ACCURACY_METERS = 50    # Mock GPS accuracy
    
    # GUI Configuration
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 700
    WINDOW_TITLE = f"{APP_NAME} - {APP_DESCRIPTION}"
    
    # Colors (Emergency Theme)
    COLOR_PRIMARY = "#d32f2f"      # Emergency red
    COLOR_SECONDARY = "#f44336"    # Light red
    COLOR_SUCCESS = "#4caf50"      # Green
    COLOR_WARNING = "#ffa726"      # Orange
    COLOR_INFO = "#2196f3"         # Blue
    COLOR_BACKGROUND = "#f0f0f0"   # Light gray
    COLOR_TEXT = "#333333"         # Dark gray
    
    # File Paths
    DATA_DIR = "data"
    MODELS_DIR = "models"
    LOGS_DIR = "logs"
    
    # Data Files
    SHELTERS_FILE = os.path.join(DATA_DIR, "shelters.json")
    PHRASES_FILE = os.path.join(DATA_DIR, "emergency_phrases.json")
    LOCATIONS_FILE = os.path.join(DATA_DIR, "locations.json")
    
    # Logging Configuration
    LOG_LEVEL = "INFO"
    LOG_FILE = "vaanirakshak.log"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Emergency Numbers (India)
    EMERGENCY_NUMBERS = {
        "police": "100",
        "fire": "101",
        "ambulance": "108",
        "disaster_management": "1070",
        "women_helpline": "1091",
        "child_helpline": "1098",
        "national_emergency": "112"
    }
    
    # SMS Configuration (Mock)
    SMS_ENABLED = True
    SMS_EMERGENCY_CONTACTS = [
        "+91-9999999999",  # Replace with actual emergency contacts
        "+91-8888888888"
    ]
    
    # Network Configuration
    OFFLINE_MODE = True          # Force offline operation
    INTERNET_CHECK_TIMEOUT = 5   # Timeout for internet connectivity check
    
    # Performance Configuration
    MAX_CONVERSATION_HISTORY = 100  # Maximum conversation entries to keep
    AUDIO_BUFFER_SIZE = 8192       # Audio buffer size
    THREAD_POOL_SIZE = 4           # Number of worker threads
    
    # Safety Configuration
    PANIC_WORD = "panic"           # Special panic word for immediate help
    SILENT_MODE_ENABLED = False    # Enable silent emergency mode
    AUTO_LOCATION_SHARING = True   # Automatically share location in emergencies
    
    @classmethod
    def create_directories(cls):
        """Create necessary directories if they don't exist"""
        directories = [cls.DATA_DIR, cls.MODELS_DIR, cls.LOGS_DIR]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def validate_configuration(cls):
        """Validate configuration settings"""
        errors = []
        
        # Check sample rate
        if cls.SAMPLE_RATE not in [8000, 16000, 22050, 44100]:
            errors.append(f"Invalid sample rate: {cls.SAMPLE_RATE}")
        
        # Check TTS settings
        if not (0.0 <= cls.TTS_VOLUME <= 1.0):
            errors.append(f"Invalid TTS volume: {cls.TTS_VOLUME}")
        
        if cls.TTS_RATE <= 0:
            errors.append(f"Invalid TTS rate: {cls.TTS_RATE}")
        
        # Check GUI dimensions
        if cls.WINDOW_WIDTH <= 0 or cls.WINDOW_HEIGHT <= 0:
            errors.append("Invalid window dimensions")
        
        return errors
    
    @classmethod
    def get_emergency_number(cls, service_type: str) -> str:
        """Get emergency number for specific service"""
        return cls.EMERGENCY_NUMBERS.get(service_type.lower(), "112")
    
    @classmethod
    def is_development_mode(cls) -> bool:
        """Check if running in development mode"""
        return os.getenv("VAANIRAKSHAK_DEV", "false").lower() == "true"
    
    @classmethod
    def get_log_level(cls) -> str:
        """Get logging level from environment or config"""
        return os.getenv("VAANIRAKSHAK_LOG_LEVEL", cls.LOG_LEVEL)

# Create directories on import
Config.create_directories()

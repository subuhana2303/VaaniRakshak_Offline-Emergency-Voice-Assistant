"""
Utility functions for VaaniRakshak
Contains helper functions for various operations
"""

import math
import json
import logging
import os
import re
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any

logger = logging.getLogger(__name__)

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points on Earth
    using the Haversine formula
    
    Args:
        lat1, lon1: Latitude and longitude of first point
        lat2, lon2: Latitude and longitude of second point
    
    Returns:
        Distance in kilometers
    """
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of Earth in kilometers
    earth_radius_km = 6371.0
    
    # Calculate the result
    distance = earth_radius_km * c
    
    return distance

def format_distance(distance_km: float) -> str:
    """
    Format distance for human-readable display
    
    Args:
        distance_km: Distance in kilometers
    
    Returns:
        Formatted distance string
    """
    if distance_km < 1.0:
        meters = int(distance_km * 1000)
        return f"{meters} meters"
    elif distance_km < 10.0:
        return f"{distance_km:.1f} km"
    else:
        return f"{distance_km:.0f} km"

def format_time_ago(timestamp: datetime) -> str:
    """
    Format timestamp as time ago string
    
    Args:
        timestamp: DateTime object
    
    Returns:
        Human-readable time ago string
    """
    now = datetime.now()
    delta = now - timestamp
    
    if delta.total_seconds() < 60:
        return "just now"
    elif delta.total_seconds() < 3600:
        minutes = int(delta.total_seconds() / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif delta.total_seconds() < 86400:
        hours = int(delta.total_seconds() / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    else:
        days = delta.days
        return f"{days} day{'s' if days != 1 else ''} ago"

def clean_text(text: str) -> str:
    """
    Clean and normalize text for processing
    
    Args:
        text: Input text string
    
    Returns:
        Cleaned text string
    """
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower().strip()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove common filler words that might interfere with recognition
    filler_words = ['um', 'uh', 'er', 'ah', 'well']
    words = text.split()
    words = [word for word in words if word not in filler_words]
    
    return ' '.join(words)

def extract_emergency_keywords(text: str) -> List[str]:
    """
    Extract emergency-related keywords from text
    
    Args:
        text: Input text to analyze
    
    Returns:
        List of emergency keywords found
    """
    emergency_keywords = [
        'help', 'emergency', 'urgent', 'danger', 'rescue', 'fire', 'flood',
        'earthquake', 'medical', 'injured', 'bleeding', 'unconscious',
        'shelter', 'evacuation', 'trapped', 'collapsed', 'burning'
    ]
    
    text_lower = text.lower()
    found_keywords = []
    
    for keyword in emergency_keywords:
        if keyword in text_lower:
            found_keywords.append(keyword)
    
    return found_keywords

def validate_coordinates(latitude: float, longitude: float) -> bool:
    """
    Validate GPS coordinates
    
    Args:
        latitude: Latitude value
        longitude: Longitude value
    
    Returns:
        True if coordinates are valid
    """
    return (-90 <= latitude <= 90) and (-180 <= longitude <= 180)

def load_json_file(file_path: str, default_value: Any = None) -> Any:
    """
    Safely load JSON file with error handling
    
    Args:
        file_path: Path to JSON file
        default_value: Default value if file can't be loaded
    
    Returns:
        Loaded JSON data or default value
    """
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            logger.warning(f"JSON file not found: {file_path}")
            return default_value
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in file {file_path}: {e}")
        return default_value
    except Exception as e:
        logger.error(f"Error loading JSON file {file_path}: {e}")
        return default_value

def save_json_file(file_path: str, data: Any) -> bool:
    """
    Safely save data to JSON file
    
    Args:
        file_path: Path to save JSON file
        data: Data to save
    
    Returns:
        True if saved successfully
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Successfully saved JSON file: {file_path}")
        return True
        
    except Exception as e:
        logger.error(f"Error saving JSON file {file_path}: {e}")
        return False

def get_system_info() -> Dict[str, Any]:
    """
    Get system information for debugging
    
    Returns:
        Dictionary with system information
    """
    import platform
    import sys
    
    return {
        'platform': platform.platform(),
        'system': platform.system(),
        'machine': platform.machine(),
        'python_version': sys.version,
        'timestamp': datetime.now().isoformat()
    }

def create_emergency_log_entry(event_type: str, message: str, 
                              location: Optional[Dict] = None,
                              additional_data: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Create structured emergency log entry
    
    Args:
        event_type: Type of emergency event
        message: Event message
        location: Location information
        additional_data: Additional event data
    
    Returns:
        Structured log entry
    """
    entry = {
        'timestamp': datetime.now().isoformat(),
        'event_type': event_type,
        'message': message,
        'severity': determine_severity(event_type),
        'location': location or {},
        'additional_data': additional_data or {},
        'system_info': get_system_info()
    }
    
    return entry

def determine_severity(event_type: str) -> str:
    """
    Determine severity level based on event type
    
    Args:
        event_type: Type of emergency event
    
    Returns:
        Severity level string
    """
    high_severity = ['fire', 'medical', 'earthquake', 'flood', 'collapse']
    medium_severity = ['shelter', 'evacuation', 'weather']
    
    event_lower = event_type.lower()
    
    for high_event in high_severity:
        if high_event in event_lower:
            return 'HIGH'
    
    for medium_event in medium_severity:
        if medium_event in event_lower:
            return 'MEDIUM'
    
    return 'LOW'

def generate_emergency_id() -> str:
    """
    Generate unique emergency ID
    
    Returns:
        Unique emergency identifier
    """
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_suffix = str(int(time.time() * 1000) % 10000).zfill(4)
    return f"EMG-{timestamp}-{random_suffix}"

def parse_coordinates_from_text(text: str) -> Optional[Tuple[float, float]]:
    """
    Extract GPS coordinates from text if present
    
    Args:
        text: Text that might contain coordinates
    
    Returns:
        Tuple of (latitude, longitude) if found, None otherwise
    """
    # Pattern for coordinates like "28.6139, 77.2090" or "28.6139°N, 77.2090°E"
    coord_pattern = r'(-?\d+\.?\d*)[°\s]*[NS]?,?\s*(-?\d+\.?\d*)[°\s]*[EW]?'
    
    match = re.search(coord_pattern, text)
    if match:
        try:
            lat = float(match.group(1))
            lon = float(match.group(2))
            
            if validate_coordinates(lat, lon):
                return (lat, lon)
        except ValueError:
            pass
    
    return None

def format_emergency_message(message_type: str, details: Dict[str, Any]) -> str:
    """
    Format emergency message for consistent display
    
    Args:
        message_type: Type of emergency message
        details: Message details
    
    Returns:
        Formatted message string
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if message_type == 'shelter_info':
        return f"""SHELTER INFORMATION ({timestamp})
Name: {details.get('name', 'Unknown')}
Address: {details.get('address', 'Unknown')}
Distance: {details.get('distance', 'Unknown')}
Capacity: {details.get('capacity', 'Unknown')}
Facilities: {', '.join(details.get('facilities', []))}
Contact: {details.get('contact', 'Emergency Hotline: 108')}"""
    
    elif message_type == 'emergency_alert':
        return f"""EMERGENCY ALERT ({timestamp})
Type: {details.get('type', 'General Emergency')}
Message: {details.get('message', 'Emergency assistance needed')}
Location: {details.get('location', 'Location not available')}
Contact: {details.get('contact', 'Emergency Services: 108')}"""
    
    else:
        return f"{message_type.upper()} ({timestamp}): {details.get('message', 'No details available')}"

def is_audio_device_available() -> bool:
    """
    Check if audio input device is available
    
    Returns:
        True if audio device is available
    """
    try:
        import pyaudio
        audio = pyaudio.PyAudio()
        
        # Check for input devices
        device_count = audio.get_device_count()
        has_input = False
        
        for i in range(device_count):
            device_info = audio.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                has_input = True
                break
        
        audio.terminate()
        return has_input
        
    except Exception as e:
        logger.error(f"Error checking audio device: {e}")
        return False

def normalize_emergency_phrase(phrase: str) -> str:
    """
    Normalize emergency phrase for better matching
    
    Args:
        phrase: Input emergency phrase
    
    Returns:
        Normalized phrase
    """
    # Convert to lowercase and clean
    phrase = clean_text(phrase)
    
    # Common phrase normalizations
    normalizations = {
        'i need help': 'help',
        'please help': 'help',
        'help me': 'help',
        'emergency situation': 'emergency',
        'medical emergency': 'medical',
        'fire emergency': 'fire',
        'nearest shelter': 'shelter',
        'safe place': 'shelter',
        'evacuation center': 'shelter'
    }
    
    for original, normalized in normalizations.items():
        if original in phrase:
            return normalized
    
    return phrase

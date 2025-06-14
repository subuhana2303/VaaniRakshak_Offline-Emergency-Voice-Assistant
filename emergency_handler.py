"""
Emergency Handler Module for VaaniRakshak
Processes emergency requests and provides appropriate responses
"""

import json
import logging
import os
import random
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from config import Config
from utils import calculate_distance, format_distance

logger = logging.getLogger(__name__)

class EmergencyHandler:
    """Handles emergency requests and responses"""
    
    def __init__(self):
        self.emergency_phrases = {}
        self.shelters = []
        self.locations = {}
        self.current_location = None
        
        self._load_data()
        self._set_mock_location()
    
    def _load_data(self):
        """Load emergency data from JSON files"""
        try:
            # Load emergency phrases
            with open('data/emergency_phrases.json', 'r') as f:
                self.emergency_phrases = json.load(f)
            
            # Load shelter data
            with open('data/shelters.json', 'r') as f:
                self.shelters = json.load(f)
            
            # Load location data
            with open('data/locations.json', 'r') as f:
                self.locations = json.load(f)
            
            logger.info("Emergency data loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load emergency data: {e}")
            # Create default data if files don't exist
            self._create_default_data()
    
    def _create_default_data(self):
        """Create default emergency data"""
        # Default emergency phrases
        self.emergency_phrases = {
            "help_phrases": ["help", "emergency", "need help", "assist", "rescue"],
            "shelter_phrases": ["shelter", "safe place", "refuge", "evacuation center"],
            "medical_phrases": ["medical", "doctor", "hospital", "injured", "hurt"],
            "fire_phrases": ["fire", "burning", "smoke", "flames"],
            "flood_phrases": ["flood", "water", "drowning", "trapped by water"],
            "earthquake_phrases": ["earthquake", "tremor", "shaking", "collapsed"]
        }
        
        # Default shelters (example data for demonstration)
        self.shelters = [
            {
                "name": "Community Center Shelter",
                "address": "123 Main Street",
                "capacity": 200,
                "latitude": 28.6139,
                "longitude": 77.2090,
                "facilities": ["Food", "Medical", "Communications"],
                "contact": "Emergency Hotline: 108"
            },
            {
                "name": "School Emergency Shelter",
                "address": "456 Oak Avenue",
                "capacity": 150,
                "latitude": 28.6129,
                "longitude": 77.2080,
                "facilities": ["Food", "Basic Medical", "Childcare"],
                "contact": "Emergency Hotline: 108"
            }
        ]
        
        # Default locations
        self.locations = {
            "default": {
                "latitude": 28.6139,
                "longitude": 77.2090,
                "city": "New Delhi",
                "country": "India"
            }
        }
        
        logger.info("Created default emergency data")
    
    def _set_mock_location(self):
        """Set mock GPS location"""
        # Simulate current location (in real app, this would come from GPS)
        self.current_location = {
            "latitude": 28.6139 + random.uniform(-0.01, 0.01),  # Add some randomness
            "longitude": 77.2090 + random.uniform(-0.01, 0.01),
            "accuracy": "50 meters",
            "timestamp": datetime.now().isoformat()
        }
        logger.info(f"Mock location set: {self.current_location}")
    
    def process_request(self, text: str) -> Optional[str]:
        """Process emergency request and return appropriate response"""
        if not text:
            return None
        
        text_lower = text.lower()
        logger.info(f"Processing request: {text}")
        
        # Identify request type
        request_type = self._identify_request_type(text_lower)
        
        if request_type == "help":
            return self._handle_general_help()
        elif request_type == "shelter":
            return self._handle_shelter_request()
        elif request_type == "medical":
            return self._handle_medical_emergency()
        elif request_type == "fire":
            return self._handle_fire_emergency()
        elif request_type == "flood":
            return self._handle_flood_emergency()
        elif request_type == "earthquake":
            return self._handle_earthquake_emergency()
        else:
            return self._handle_unknown_request(text)
    
    def _identify_request_type(self, text: str) -> str:
        """Identify the type of emergency request"""
        for category, phrases in self.emergency_phrases.items():
            for phrase in phrases:
                if phrase in text:
                    return category.replace('_phrases', '')
        
        return "unknown"
    
    def _handle_general_help(self) -> str:
        """Handle general help requests"""
        response = ("I'm here to help you in this emergency. "
                   "I can help you find the nearest shelter, provide medical guidance, "
                   "or connect you with emergency services. "
                   "Say 'nearest shelter' to find safe places, "
                   "or 'medical emergency' if you need medical assistance.")
        
        # Simulate SMS alert
        self._send_mock_sms_alert("General emergency assistance requested")
        
        return response
    
    def _handle_shelter_request(self) -> str:
        """Handle shelter/safe place requests"""
        if not self.shelters:
            return "I don't have shelter information available right now. Please contact emergency services at 108."
        
        # Find nearest shelters
        nearest_shelters = self._find_nearest_shelters(limit=2)
        
        if not nearest_shelters:
            return "I couldn't find nearby shelters. Please contact emergency services at 108."
        
        response = "Here are the nearest emergency shelters:\n\n"
        
        for i, (shelter, distance) in enumerate(nearest_shelters, 1):
            response += f"{i}. {shelter['name']}\n"
            response += f"   Address: {shelter['address']}\n"
            response += f"   Distance: {format_distance(distance)}\n"
            response += f"   Capacity: {shelter['capacity']} people\n"
            response += f"   Facilities: {', '.join(shelter['facilities'])}\n"
            response += f"   Contact: {shelter['contact']}\n\n"
        
        response += "Stay safe and move to the nearest shelter if possible."
        
        # Simulate SMS with shelter info
        self._send_mock_sms_alert(f"Shelter information sent: {nearest_shelters[0][0]['name']}")
        
        return response
    
    def _handle_medical_emergency(self) -> str:
        """Handle medical emergency requests"""
        response = ("Medical emergency detected. "
                   "If someone is seriously injured, call emergency services immediately at 108. "
                   "For minor injuries: "
                   "1. Keep the person calm and still "
                   "2. Apply pressure to stop bleeding "
                   "3. Do not move someone with possible spinal injury "
                   "4. Check for breathing and pulse "
                   "The nearest medical facilities will be contacted.")
        
        self._send_mock_sms_alert("Medical emergency - immediate assistance needed")
        
        return response
    
    def _handle_fire_emergency(self) -> str:
        """Handle fire emergency requests"""
        response = ("Fire emergency detected. "
                   "Safety instructions: "
                   "1. Get out of the building immediately "
                   "2. Stay low to avoid smoke "
                   "3. Feel doors before opening them "
                   "4. Don't use elevators "
                   "5. Call fire department at 101 "
                   "6. Go to your designated meeting point "
                   "Emergency services are being notified.")
        
        self._send_mock_sms_alert("Fire emergency - evacuation required")
        
        return response
    
    def _handle_flood_emergency(self) -> str:
        """Handle flood emergency requests"""
        response = ("Flood emergency detected. "
                   "Safety instructions: "
                   "1. Move to higher ground immediately "
                   "2. Avoid walking or driving through flood water "
                   "3. Stay away from electrical equipment "
                   "4. If trapped, signal for help from upper floors "
                   "5. Don't drink flood water "
                   "Emergency rescue teams are being alerted.")
        
        self._send_mock_sms_alert("Flood emergency - move to higher ground")
        
        return response
    
    def _handle_earthquake_emergency(self) -> str:
        """Handle earthquake emergency requests"""
        response = ("Earthquake emergency detected. "
                   "If shaking continues: Drop, Cover, and Hold On. "
                   "After shaking stops: "
                   "1. Check for injuries "
                   "2. Look for hazards like gas leaks or structural damage "
                   "3. Exit carefully if building is damaged "
                   "4. Stay away from damaged structures "
                   "5. Be prepared for aftershocks "
                   "Emergency teams are being mobilized.")
        
        self._send_mock_sms_alert("Earthquake detected - following safety protocols")
        
        return response
    
    def _handle_unknown_request(self, text: str) -> str:
        """Handle unrecognized requests"""
        return ("I didn't recognize that emergency request. "
                "You can say things like: "
                "'I need help', 'nearest shelter', 'medical emergency', "
                "'fire emergency', or 'earthquake'. "
                "For immediate assistance, call emergency services at 108.")
    
    def _find_nearest_shelters(self, limit: int = 3) -> List[Tuple[Dict, float]]:
        """Find nearest shelters based on current location"""
        if not self.current_location or not self.shelters:
            return []
        
        shelters_with_distance = []
        
        for shelter in self.shelters:
            distance = calculate_distance(
                self.current_location['latitude'],
                self.current_location['longitude'],
                shelter['latitude'],
                shelter['longitude']
            )
            shelters_with_distance.append((shelter, distance))
        
        # Sort by distance and return top results
        shelters_with_distance.sort(key=lambda x: x[1])
        return shelters_with_distance[:limit]
    
    def _send_mock_sms_alert(self, message: str):
        """Simulate sending SMS alert to emergency contacts"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        location_str = f"Lat: {self.current_location['latitude']:.4f}, Lon: {self.current_location['longitude']:.4f}"
        
        sms_content = f"[VaaniRakshak Alert] {message}\nTime: {timestamp}\nLocation: {location_str}"
        
        # In a real implementation, this would send actual SMS
        logger.info(f"Mock SMS Alert: {sms_content}")
        
        # Simulate SMS delivery confirmation
        return True
    
    def get_current_location(self) -> Dict:
        """Get current mock location"""
        return self.current_location.copy() if self.current_location else {}
    
    def is_ready(self) -> bool:
        """Check if emergency handler is ready"""
        return (len(self.emergency_phrases) > 0 and 
                len(self.shelters) > 0 and 
                self.current_location is not None)

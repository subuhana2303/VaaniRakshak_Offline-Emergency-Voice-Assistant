"""
VaaniRakshak Voice Assistant Core Module
Handles speech recognition and text-to-speech functionality
"""

import json
import logging
import threading
import time
from typing import Callable, Optional

from speech_processor import SpeechProcessor
from emergency_handler import EmergencyHandler
from config import Config

logger = logging.getLogger(__name__)

class VoiceAssistant:
    """Main voice assistant class"""
    
    def __init__(self):
        self.config = Config()
        self.speech_processor = None
        self.emergency_handler = None
        self.listening = False
        self.initialized = False
        
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize speech processor and emergency handler"""
        try:
            # Initialize speech processor
            self.speech_processor = SpeechProcessor(
                model_path=self.config.VOSK_MODEL_PATH,
                sample_rate=self.config.SAMPLE_RATE
            )
            
            # Initialize emergency handler
            self.emergency_handler = EmergencyHandler()
            
            self.initialized = True
            logger.info("Voice assistant components initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize voice assistant: {e}")
            raise
    
    def start_listening(self, status_callback: Optional[Callable] = None, 
                       response_callback: Optional[Callable] = None):
        """Start continuous listening for emergency phrases"""
        if not self.initialized:
            raise RuntimeError("Voice assistant not properly initialized")
        
        self.listening = True
        logger.info("Starting voice recognition...")
        
        if status_callback:
            status_callback("Listening for emergency phrases...", "listening")
        
        try:
            # Start speech recognition loop
            self.speech_processor.start_recognition()
            
            while self.listening:
                # Get recognized text
                recognized_text = self.speech_processor.get_recognized_text()
                
                if recognized_text:
                    logger.info(f"Recognized: {recognized_text}")
                    
                    # Process emergency request
                    response = self.emergency_handler.process_request(recognized_text)
                    
                    if response:
                        logger.info(f"Response: {response}")
                        
                        # Speak response
                        self.speech_processor.speak(response)
                        
                        # Update GUI if callback provided
                        if response_callback:
                            response_callback(f"You: {recognized_text}", f"VaaniRakshak: {response}")
                
                # Small delay to prevent excessive CPU usage
                time.sleep(0.1)
                
        except Exception as e:
            error_msg = f"Voice recognition error: {e}"
            logger.error(error_msg)
            if status_callback:
                status_callback(error_msg, "error")
        
        finally:
            self.speech_processor.stop_recognition()
            if status_callback:
                status_callback("Voice recognition stopped", "stopped")
    
    def stop_listening(self):
        """Stop voice recognition"""
        self.listening = False
        if self.speech_processor:
            self.speech_processor.stop_recognition()
        logger.info("Voice recognition stopped")
    
    def process_manual_input(self, text: str) -> str:
        """Process manual text input (for GUI text input)"""
        if not self.emergency_handler:
            return "Emergency handler not initialized"
        
        response = self.emergency_handler.process_request(text)
        if response:
            self.speech_processor.speak(response)
        
        return response or "I didn't understand that request."
    
    def is_listening(self) -> bool:
        """Check if assistant is currently listening"""
        return self.listening
    
    def get_status(self) -> dict:
        """Get current status of voice assistant"""
        return {
            'initialized': self.initialized,
            'listening': self.listening,
            'speech_processor_ready': self.speech_processor.is_ready() if self.speech_processor else False,
            'emergency_handler_ready': self.emergency_handler.is_ready() if self.emergency_handler else False
        }

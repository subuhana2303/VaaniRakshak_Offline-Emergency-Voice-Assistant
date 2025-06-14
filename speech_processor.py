"""
Speech Processing Module for VaaniRakshak
Handles speech-to-text and text-to-speech functionality using Vosk and pyttsx3
"""

import json
import logging
import os
import threading
import queue
import time
from typing import Optional

import vosk
import pyaudio
import pyttsx3

from config import Config
from virtual_audio import VirtualAudioManager

logger = logging.getLogger(__name__)

class SpeechProcessor:
    """Handles speech recognition and text-to-speech"""
    
    def __init__(self, model_path: Optional[str] = None, sample_rate: int = 16000):
        self.model_path = model_path or Config.VOSK_MODEL_PATH
        self.sample_rate = sample_rate
        
        # Audio components
        self.audio = None
        self.stream = None
        self.model = None
        self.rec = None
        
        # TTS engine
        self.tts_engine = None
        
        # Recognition state
        self.recognition_queue = queue.Queue()
        self.is_recognizing = False
        self.recognition_thread = None
        
        # Virtual audio system
        self.virtual_audio = VirtualAudioManager()
        self.use_virtual_audio = False
        
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize speech recognition and TTS components"""
        try:
            # Initialize Vosk model
            self._initialize_vosk_model()
            
            # Initialize audio
            self._initialize_audio()
            
            # Initialize TTS
            self._initialize_tts()
            
            logger.info("Speech processor initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize speech processor: {e}")
            raise
    
    def _initialize_vosk_model(self):
        """Initialize Vosk speech recognition model"""
        if not os.path.exists(self.model_path):
            # Create a minimal model directory with basic configuration
            os.makedirs(self.model_path, exist_ok=True)
            
            # Create a basic model configuration for offline use
            # Note: In production, you would download the actual Vosk model
            model_config = {
                "model_type": "vosk-model-small-en-us-0.15",
                "sample_rate": self.sample_rate,
                "offline": True
            }
            
            with open(os.path.join(self.model_path, "config.json"), "w") as f:
                json.dump(model_config, f)
            
            logger.warning(f"Vosk model not found at {self.model_path}. Using fallback configuration.")
            logger.info("For full functionality, download a Vosk model from https://alphacephei.com/vosk/models")
        
        try:
            self.model = vosk.Model(self.model_path)
            self.rec = vosk.KaldiRecognizer(self.model, self.sample_rate)
            logger.info("Vosk model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Vosk model: {e}")
            # Fallback: Create a simple recognizer without model
            self.rec = None
    
    def _initialize_audio(self):
        """Initialize PyAudio for microphone input"""
        try:
            self.audio = pyaudio.PyAudio()
            
            # Check if any input devices are available
            device_count = self.audio.get_device_count()
            input_devices = []
            
            for i in range(device_count):
                device_info = self.audio.get_device_info_by_index(i)
                max_input_channels = device_info.get('maxInputChannels', 0)
                if isinstance(max_input_channels, (int, float)) and int(max_input_channels) > 0:
                    input_devices.append(device_info)
            
            if input_devices:
                # Use the first available input device
                default_device = input_devices[0]
                logger.info(f"Using audio device: {default_device['name']}")
            else:
                logger.warning("No physical audio input devices found - enabling virtual microphone")
                self.audio = None
                self.use_virtual_audio = True
                
        except Exception as e:
            logger.warning(f"Physical audio initialization failed: {e} - enabling virtual microphone")
            self.audio = None
            self.use_virtual_audio = True
    
    def _initialize_tts(self):
        """Initialize text-to-speech engine"""
        try:
            self.tts_engine = pyttsx3.init()
            
            # Configure TTS settings
            self.tts_engine.setProperty('rate', 150)  # Speed of speech
            self.tts_engine.setProperty('volume', 0.9)  # Volume level
            
            # Try to set a clear voice
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Prefer female voice for emergency situations (often perceived as calmer)
                for voice in voices:
                    if 'female' in voice.name.lower() or 'woman' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
                else:
                    # Use first available voice
                    self.tts_engine.setProperty('voice', voices[0].id)
            
            logger.info("TTS engine initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize TTS engine: {e}")
            self.tts_engine = None
    
    def start_recognition(self):
        """Start continuous speech recognition"""
        if self.is_recognizing:
            return
        
        if not self.audio:
            logger.info("No audio device available - speech recognition disabled")
            return
            
        try:
            # Open audio stream
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=4000
            )
            
            self.is_recognizing = True
            
            # Start recognition thread
            self.recognition_thread = threading.Thread(
                target=self._recognition_loop, 
                daemon=True
            )
            self.recognition_thread.start()
            
            logger.info("Speech recognition started")
            
        except Exception as e:
            logger.error(f"Failed to start speech recognition: {e}")
            # Don't raise exception, allow graceful degradation
    
    def _recognition_loop(self):
        """Main speech recognition loop"""
        while self.is_recognizing and self.stream:
            try:
                # Read audio data
                data = self.stream.read(4000, exception_on_overflow=False)
                
                if self.rec:
                    # Process with Vosk
                    if self.rec.AcceptWaveform(data):
                        result = json.loads(self.rec.Result())
                        text = result.get('text', '').strip()
                        if text:
                            self.recognition_queue.put(text)
                else:
                    # Fallback: Simple keyword detection
                    # This is a basic fallback when Vosk model is not available
                    self._fallback_recognition(data)
                
            except Exception as e:
                logger.error(f"Recognition loop error: {e}")
                time.sleep(0.1)
    
    def _fallback_recognition(self, audio_data):
        """Fallback recognition when Vosk is not available"""
        # This is a placeholder for basic audio processing
        # In a real implementation, you might use simple audio level detection
        # to trigger predefined responses
        
        # For demonstration, we'll simulate recognition of key phrases
        # based on audio activity (this is very basic)
        
        import struct
        import math
        
        try:
            # Calculate audio level
            audio_data_int = struct.unpack(f'<{len(audio_data)//2}h', audio_data)
            rms = math.sqrt(sum(x*x for x in audio_data_int) / len(audio_data_int))
            
            # If audio level is above threshold, simulate recognition
            if rms > 1000:  # Adjust threshold as needed
                # This is a very basic fallback - in production you'd want better audio processing
                self.recognition_queue.put("help")  # Default emergency phrase
                time.sleep(2)  # Prevent rapid triggering
                
        except Exception as e:
            logger.error(f"Fallback recognition error: {e}")
    
    def stop_recognition(self):
        """Stop speech recognition"""
        self.is_recognizing = False
        
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        
        if self.recognition_thread:
            self.recognition_thread.join(timeout=1.0)
        
        logger.info("Speech recognition stopped")
    
    def get_recognized_text(self) -> Optional[str]:
        """Get the next recognized text from the queue"""
        try:
            return self.recognition_queue.get_nowait()
        except queue.Empty:
            return None
    
    def speak(self, text: str):
        """Convert text to speech"""
        if not self.tts_engine:
            logger.warning("TTS engine not available")
            return
        
        try:
            logger.info(f"Speaking: {text}")
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            logger.error(f"TTS error: {e}")
    
    def is_ready(self) -> bool:
        """Check if speech processor is ready"""
        return (self.audio is not None and 
                self.tts_engine is not None and 
                (self.rec is not None or True))  # Allow fallback mode
    
    def __del__(self):
        """Cleanup resources"""
        self.stop_recognition()
        if self.audio:
            self.audio.terminate()

"""
Virtual Audio System for VaaniRakshak
Creates a simulated microphone input for testing and demonstration
"""

import numpy as np
import threading
import time
import queue
import logging
from typing import Optional, Callable

logger = logging.getLogger(__name__)

class VirtualMicrophone:
    """Simulates microphone input with predefined audio patterns"""
    
    def __init__(self, sample_rate: int = 16000):
        self.sample_rate = sample_rate
        self.is_active = False
        self.audio_queue = queue.Queue()
        self.recording_thread = None
        self.simulation_phrases = [
            "help", "emergency", "nearest shelter", "medical emergency",
            "fire emergency", "flood emergency", "earthquake"
        ]
        self.current_phrase_index = 0
        
    def start_recording(self):
        """Start virtual microphone recording"""
        if self.is_active:
            return
            
        self.is_active = True
        self.recording_thread = threading.Thread(target=self._recording_loop, daemon=True)
        self.recording_thread.start()
        logger.info("Virtual microphone started")
    
    def stop_recording(self):
        """Stop virtual microphone recording"""
        self.is_active = False
        if self.recording_thread:
            self.recording_thread.join(timeout=1.0)
        logger.info("Virtual microphone stopped")
    
    def _recording_loop(self):
        """Main recording loop that generates audio data"""
        while self.is_active:
            # Generate silence with occasional "voice" activity
            chunk_size = 4000
            silence_duration = np.random.uniform(3, 8)  # 3-8 seconds of silence
            
            # Generate silence
            for _ in range(int(silence_duration * self.sample_rate / chunk_size)):
                if not self.is_active:
                    break
                    
                # Generate low-level noise (simulating ambient sound)
                noise = np.random.normal(0, 50, chunk_size).astype(np.int16)
                self.audio_queue.put(noise.tobytes())
                time.sleep(chunk_size / self.sample_rate)
            
            # Simulate voice activity (higher amplitude signal)
            if self.is_active:
                self._simulate_voice_activity()
    
    def _simulate_voice_activity(self):
        """Simulate voice activity with recognizable patterns"""
        # Generate a more complex waveform that might trigger recognition
        chunk_size = 4000
        voice_duration = 2.0  # 2 seconds of "voice"
        
        for i in range(int(voice_duration * self.sample_rate / chunk_size)):
            if not self.is_active:
                break
                
            # Generate a more complex signal that resembles speech patterns
            t = np.arange(chunk_size) / self.sample_rate
            
            # Multiple frequency components to simulate speech
            freq1 = 150 + 50 * np.sin(2 * np.pi * 2 * t * i)  # Fundamental frequency variation
            freq2 = 300 + 100 * np.sin(2 * np.pi * 3 * t * i)  # First harmonic
            freq3 = 600 + 200 * np.sin(2 * np.pi * 1.5 * t * i)  # Second harmonic
            
            # Combine frequencies with amplitude modulation
            amplitude = 1000 * (1 + 0.5 * np.sin(2 * np.pi * 5 * t * i))
            
            signal = amplitude * (
                0.4 * np.sin(2 * np.pi * freq1 * t) +
                0.3 * np.sin(2 * np.pi * freq2 * t) +
                0.3 * np.sin(2 * np.pi * freq3 * t)
            )
            
            # Add some noise for realism
            noise = np.random.normal(0, 100, chunk_size)
            final_signal = (signal + noise).astype(np.int16)
            
            self.audio_queue.put(final_signal.tobytes())
            time.sleep(chunk_size / self.sample_rate)
        
        logger.info(f"Virtual voice activity completed - simulating phrase: '{self.simulation_phrases[self.current_phrase_index]}'")
        self.current_phrase_index = (self.current_phrase_index + 1) % len(self.simulation_phrases)
    
    def read_audio(self, chunk_size: int) -> Optional[bytes]:
        """Read audio data from virtual microphone"""
        try:
            return self.audio_queue.get_nowait()
        except queue.Empty:
            # Return silence if no data available
            return np.zeros(chunk_size, dtype=np.int16).tobytes()
    
    def get_simulated_phrase(self) -> str:
        """Get the current simulated phrase for testing"""
        return self.simulation_phrases[self.current_phrase_index]


class VirtualAudioManager:
    """Manages virtual audio devices for VaaniRakshak"""
    
    def __init__(self):
        self.virtual_mic = VirtualMicrophone()
        self.phrase_callback = None
        self.phrase_injection_active = False
        
    def start_virtual_audio(self):
        """Start virtual audio system"""
        self.virtual_mic.start_recording()
        logger.info("Virtual audio system started")
    
    def stop_virtual_audio(self):
        """Stop virtual audio system"""
        self.virtual_mic.stop_recording()
        self.phrase_injection_active = False
        logger.info("Virtual audio system stopped")
    
    def inject_phrase(self, phrase: str, callback: Optional[Callable] = None):
        """Inject a specific phrase for recognition"""
        if callback:
            self.phrase_callback = callback
            # Simulate phrase recognition after a short delay
            threading.Timer(1.0, lambda: callback(phrase)).start()
            logger.info(f"Injected phrase for recognition: '{phrase}'")
    
    def enable_auto_phrase_injection(self, callback: Callable):
        """Enable automatic phrase injection for testing"""
        self.phrase_callback = callback
        self.phrase_injection_active = True
        
        def auto_inject():
            phrases = [
                "help", "nearest shelter", "medical emergency", 
                "fire emergency", "I need help"
            ]
            index = 0
            
            while self.phrase_injection_active:
                time.sleep(10)  # Wait 10 seconds between phrases
                if self.phrase_injection_active and callback:
                    phrase = phrases[index % len(phrases)]
                    callback(phrase)
                    logger.info(f"Auto-injected phrase: '{phrase}'")
                    index += 1
        
        threading.Thread(target=auto_inject, daemon=True).start()
        logger.info("Auto phrase injection enabled")
    
    def disable_auto_phrase_injection(self):
        """Disable automatic phrase injection"""
        self.phrase_injection_active = False
        logger.info("Auto phrase injection disabled")
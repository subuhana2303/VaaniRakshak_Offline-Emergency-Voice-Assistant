#!/usr/bin/env python3
"""
VaaniRakshak - Offline Voice Assistant for Disaster Emergency Situations
Main entry point for the application
"""

import sys
import os
import logging
import threading
import tkinter as tk
from tkinter import messagebox

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from voice_assistant import VoiceAssistant
from gui_interface import EmergencyGUI
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('vaanirakshak.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class VaaniRakshakApp:
    """Main application class for VaaniRakshak"""
    
    def __init__(self):
        self.voice_assistant = None
        self.gui = None
        self.running = False
        
    def initialize_components(self):
        """Initialize all application components"""
        try:
            # Initialize voice assistant
            self.voice_assistant = VoiceAssistant()
            
            # Initialize GUI
            self.gui = EmergencyGUI(self.voice_assistant)
            
            # Connect GUI callbacks
            self.gui.set_start_callback(self.start_voice_assistant)
            self.gui.set_stop_callback(self.stop_voice_assistant)
            
            logger.info("All components initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize components: {e}")
            messagebox.showerror("Initialization Error", 
                               f"Failed to initialize VaaniRakshak: {e}")
            return False
    
    def start_voice_assistant(self):
        """Start the voice assistant in a separate thread"""
        if not self.running:
            self.running = True
            voice_thread = threading.Thread(target=self._run_voice_assistant, daemon=True)
            voice_thread.start()
            logger.info("Voice assistant started")
    
    def stop_voice_assistant(self):
        """Stop the voice assistant"""
        self.running = False
        if self.voice_assistant:
            self.voice_assistant.stop_listening()
        logger.info("Voice assistant stopped")
    
    def _run_voice_assistant(self):
        """Run voice assistant in background thread"""
        try:
            if self.voice_assistant:
                self.voice_assistant.start_listening(
                    status_callback=self.gui.update_status,
                    response_callback=self.gui.add_response
                )
        except Exception as e:
            logger.error(f"Voice assistant error: {e}")
            self.gui.update_status(f"Error: {e}", "error")
    
    def run(self):
        """Run the main application"""
        try:
            if not self.initialize_components():
                return
            
            # Start GUI main loop
            self.gui.run()
            
        except KeyboardInterrupt:
            logger.info("Application interrupted by user")
        except Exception as e:
            logger.error(f"Application error: {e}")
            messagebox.showerror("Application Error", f"An error occurred: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        self.stop_voice_assistant()
        logger.info("Application cleanup completed")

def check_dependencies():
    """Check if all required dependencies are available"""
    missing_deps = []
    
    try:
        import vosk
    except ImportError:
        missing_deps.append("vosk")
    
    try:
        import pyttsx3
    except ImportError:
        missing_deps.append("pyttsx3")
    
    try:
        import pyaudio
    except ImportError:
        missing_deps.append("pyaudio")
    
    if missing_deps:
        print(f"Missing dependencies: {', '.join(missing_deps)}")
        print("Please install them using pip:")
        for dep in missing_deps:
            print(f"pip install {dep}")
        return False
    
    return True

def main():
    """Main function"""
    print("=" * 50)
    print("VaaniRakshak - Emergency Voice Assistant")
    print("Offline Voice Assistant for Disaster Situations")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Create and run application
    app = VaaniRakshakApp()
    app.run()

if __name__ == "__main__":
    main()

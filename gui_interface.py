"""
GUI Interface for VaaniRakshak
Provides accessible graphical interface for emergency voice assistant
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import logging
from datetime import datetime
from typing import Callable, Optional

from config import Config

logger = logging.getLogger(__name__)

class EmergencyGUI:
    """Main GUI interface for VaaniRakshak"""
    
    def __init__(self, voice_assistant):
        self.voice_assistant = voice_assistant
        self.root = None
        self.start_callback = None
        self.stop_callback = None
        
        # GUI elements
        self.status_label = None
        self.status_indicator = None
        self.conversation_area = None
        self.manual_input = None
        self.control_buttons = {}
        
        self._create_gui()
    
    def _create_gui(self):
        """Create the main GUI interface"""
        self.root = tk.Tk()
        self.root.title("VaaniRakshak - Emergency Voice Assistant")
        self.root.geometry("800x700")
        self.root.configure(bg='#f0f0f0')
        
        # Configure styles
        self._configure_styles()
        
        # Create GUI layout
        self._create_header()
        self._create_status_section()
        self._create_conversation_section()
        self._create_manual_input_section()
        self._create_control_section()
        self._create_info_section()
        
        # Configure window closing
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        logger.info("GUI interface created")
    
    def _configure_styles(self):
        """Configure GUI styles"""
        style = ttk.Style()
        
        # Configure emergency color scheme
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#d32f2f')
        style.configure('Status.TLabel', font=('Arial', 12), foreground='#333333')
        style.configure('Emergency.TButton', font=('Arial', 12, 'bold'))
        style.configure('Control.TButton', font=('Arial', 10))
    
    def _create_header(self):
        """Create header section"""
        header_frame = tk.Frame(self.root, bg='#d32f2f', height=80)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="🛡️ VaaniRakshak",
            font=('Arial', 20, 'bold'),
            fg='white',
            bg='#d32f2f'
        )
        title_label.pack(pady=15)
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Offline Emergency Voice Assistant",
            font=('Arial', 12),
            fg='white',
            bg='#d32f2f'
        )
        subtitle_label.pack()
    
    def _create_status_section(self):
        """Create status display section"""
        status_frame = tk.Frame(self.root, bg='#f0f0f0', pady=10)
        status_frame.pack(fill='x', padx=20)
        
        # Status indicator and text
        indicator_frame = tk.Frame(status_frame, bg='#f0f0f0')
        indicator_frame.pack()
        
        # Status indicator (colored circle)
        self.status_indicator = tk.Label(
            indicator_frame,
            text="●",
            font=('Arial', 16),
            fg='#ffa726',  # Orange - ready
            bg='#f0f0f0'
        )
        self.status_indicator.pack(side='left', padx=(0, 10))
        
        # Status text
        self.status_label = tk.Label(
            indicator_frame,
            text="Ready - Click 'Start Listening' to begin",
            font=('Arial', 12),
            fg='#333333',
            bg='#f0f0f0'
        )
        self.status_label.pack(side='left')
    
    def _create_conversation_section(self):
        """Create conversation display section"""
        conv_frame = tk.Frame(self.root, bg='#f0f0f0')
        conv_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Conversation label
        conv_label = tk.Label(
            conv_frame,
            text="Emergency Conversation",
            font=('Arial', 12, 'bold'),
            fg='#333333',
            bg='#f0f0f0'
        )
        conv_label.pack(anchor='w', pady=(0, 5))
        
        # Conversation text area
        self.conversation_area = scrolledtext.ScrolledText(
            conv_frame,
            height=15,
            font=('Arial', 10),
            wrap=tk.WORD,
            bg='white',
            fg='#333333',
            state='disabled'
        )
        self.conversation_area.pack(fill='both', expand=True)
        
        # Configure text tags for different message types
        self.conversation_area.tag_configure('user', foreground='#1976d2', font=('Arial', 10, 'bold'))
        self.conversation_area.tag_configure('assistant', foreground='#d32f2f', font=('Arial', 10, 'bold'))
        self.conversation_area.tag_configure('timestamp', foreground='#666666', font=('Arial', 8))
    
    def _create_manual_input_section(self):
        """Create manual text input section"""
        input_frame = tk.Frame(self.root, bg='#f0f0f0')
        input_frame.pack(fill='x', padx=20, pady=10)
        
        # Input label
        input_label = tk.Label(
            input_frame,
            text="Manual Emergency Input (if voice is unavailable):",
            font=('Arial', 10),
            fg='#333333',
            bg='#f0f0f0'
        )
        input_label.pack(anchor='w', pady=(0, 5))
        
        # Input field and button frame
        input_controls = tk.Frame(input_frame, bg='#f0f0f0')
        input_controls.pack(fill='x')
        
        # Text input
        self.manual_input = tk.Entry(
            input_controls,
            font=('Arial', 12),
            fg='#333333'
        )
        self.manual_input.pack(side='left', fill='x', expand=True, padx=(0, 10))
        self.manual_input.bind('<Return>', self._process_manual_input)
        
        # Send button
        send_button = ttk.Button(
            input_controls,
            text="Send",
            command=self._process_manual_input,
            style='Control.TButton'
        )
        send_button.pack(side='right')
    
    def _create_control_section(self):
        """Create control buttons section"""
        control_frame = tk.Frame(self.root, bg='#f0f0f0')
        control_frame.pack(fill='x', padx=20, pady=10)
        
        # Buttons frame
        buttons_frame = tk.Frame(control_frame, bg='#f0f0f0')
        buttons_frame.pack()
        
        # Start button
        self.control_buttons['start'] = ttk.Button(
            buttons_frame,
            text="🎤 Start Listening",
            command=self._start_listening,
            style='Emergency.TButton'
        )
        self.control_buttons['start'].pack(side='left', padx=10)
        
        # Stop button
        self.control_buttons['stop'] = ttk.Button(
            buttons_frame,
            text="⏹️ Stop Listening",
            command=self._stop_listening,
            style='Emergency.TButton'
        )
        self.control_buttons['stop'].pack(side='left', padx=10)
        
        # Clear button
        self.control_buttons['clear'] = ttk.Button(
            buttons_frame,
            text="🗑️ Clear",
            command=self._clear_conversation,
            style='Control.TButton'
        )
        self.control_buttons['clear'].pack(side='left', padx=10)
        
        # Status button
        self.control_buttons['status'] = ttk.Button(
            buttons_frame,
            text="ℹ️ Status",
            command=self._show_status,
            style='Control.TButton'
        )
        self.control_buttons['status'].pack(side='left', padx=10)
    
    def _create_info_section(self):
        """Create information section"""
        info_frame = tk.Frame(self.root, bg='#f0f0f0')
        info_frame.pack(fill='x', padx=20, pady=10)
        
        # Emergency phrases info
        info_text = (
            "Emergency Phrases: 'I need help', 'nearest shelter', 'medical emergency', "
            "'fire emergency', 'flood emergency', 'earthquake' | "
            "Emergency Number: 108"
        )
        
        info_label = tk.Label(
            info_frame,
            text=info_text,
            font=('Arial', 9),
            fg='#666666',
            bg='#f0f0f0',
            wraplength=750,
            justify='center'
        )
        info_label.pack()
    
    def _start_listening(self):
        """Start voice recognition"""
        if self.start_callback:
            self.start_callback()
        
        self.control_buttons['start'].configure(state='disabled')
        self.control_buttons['stop'].configure(state='normal')
    
    def _stop_listening(self):
        """Stop voice recognition"""
        if self.stop_callback:
            self.stop_callback()
        
        self.control_buttons['start'].configure(state='normal')
        self.control_buttons['stop'].configure(state='disabled')
    
    def _process_manual_input(self, event=None):
        """Process manual text input"""
        text = self.manual_input.get().strip()
        if not text:
            return
        
        # Clear input field
        self.manual_input.delete(0, tk.END)
        
        # Process with voice assistant
        try:
            response = self.voice_assistant.process_manual_input(text)
            self.add_response(f"You: {text}", f"VaaniRakshak: {response}")
        except Exception as e:
            logger.error(f"Manual input processing error: {e}")
            self.add_response(f"You: {text}", f"VaaniRakshak: Error processing request")
    
    def _clear_conversation(self):
        """Clear conversation area"""
        self.conversation_area.configure(state='normal')
        self.conversation_area.delete(1.0, tk.END)
        self.conversation_area.configure(state='disabled')
    
    def _show_status(self):
        """Show system status"""
        try:
            status = self.voice_assistant.get_status()
            status_text = f"""VaaniRakshak System Status:
            
Initialized: {status.get('initialized', False)}
Listening: {status.get('listening', False)}
Speech Processor: {status.get('speech_processor_ready', False)}
Emergency Handler: {status.get('emergency_handler_ready', False)}

Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            messagebox.showinfo("System Status", status_text)
        except Exception as e:
            messagebox.showerror("Status Error", f"Could not retrieve status: {e}")
    
    def _on_closing(self):
        """Handle window closing"""
        if self.stop_callback:
            self.stop_callback()
        self.root.destroy()
    
    def update_status(self, message: str, status_type: str = "info"):
        """Update status display"""
        def _update():
            self.status_label.configure(text=message)
            
            # Update status indicator color
            if status_type == "listening":
                self.status_indicator.configure(fg='#4caf50')  # Green
            elif status_type == "error":
                self.status_indicator.configure(fg='#f44336')  # Red
            elif status_type == "stopped":
                self.status_indicator.configure(fg='#ffa726')  # Orange
            else:
                self.status_indicator.configure(fg='#2196f3')  # Blue
        
        # Ensure GUI update happens in main thread
        self.root.after(0, _update)
    
    def add_response(self, user_message: str, assistant_message: str):
        """Add conversation to display"""
        def _add():
            self.conversation_area.configure(state='normal')
            
            # Add timestamp
            timestamp = datetime.now().strftime('%H:%M:%S')
            self.conversation_area.insert(tk.END, f"[{timestamp}] ", 'timestamp')
            
            # Add user message
            self.conversation_area.insert(tk.END, f"{user_message}\n", 'user')
            
            # Add assistant message
            self.conversation_area.insert(tk.END, f"{assistant_message}\n\n", 'assistant')
            
            # Scroll to bottom
            self.conversation_area.see(tk.END)
            self.conversation_area.configure(state='disabled')
        
        # Ensure GUI update happens in main thread
        self.root.after(0, _add)
    
    def set_start_callback(self, callback: Callable):
        """Set callback for start button"""
        self.start_callback = callback
    
    def set_stop_callback(self, callback: Callable):
        """Set callback for stop button"""
        self.stop_callback = callback
    
    def run(self):
        """Start GUI main loop"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            logger.info("GUI interrupted by user")
        except Exception as e:
            logger.error(f"GUI error: {e}")
            messagebox.showerror("GUI Error", f"An error occurred: {e}")

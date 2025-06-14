# 🛡️ VaaniRakshak: Offline Emergency Voice Assistant

**VaaniRakshak** is an intelligent, offline voice assistant tailored for disaster and emergency response scenarios. Designed to operate **without internet connectivity**, it provides real-time assistance using voice commands, helping users locate shelters, access emergency services, and receive critical information — even in infrastructure-compromised environments.

---

## 📸 Output Preview

### 🖥️ GUI Interface

<img src="assets/vaani_gui_preview.png" alt="VaaniRakshak GUI Screenshot" width="600"/>

- 🔴 Emergency-themed interface
- 🎙️ Start/Stop voice control
- ✍️ Manual text input
- 🧭 Real-time updates and response messages

---

## 🎬 Demo Video

https://user-images.githubusercontent.com/your-username/your-repo/assets/demo_vaani_voice_assistant.mp4

> ✅ *Watch the assistant recognize phrases like “I need help”, “medical emergency”, and reply with shelter info, alerts, and voice feedback.*

---

## 📌 Features

- 🎙️ **Offline Speech Recognition** using [Vosk](https://alphacephei.com/vosk/)
- 🗣️ **Text-to-Speech Synthesis** with `pyttsx3`
- 🖥️ **User-Friendly GUI** powered by Tkinter
- 📡 **Emergency Response Engine** with shelter lookup and SMS alert simulation
- 🌍 **Location-aware guidance** (mocked for offline support)
- 🔧 Fully modular and configurable architecture

---

## 🧠 Use Case

> “In disaster scenarios where internet access is disrupted, **VaaniRakshak** enables users to interact with emergency services and systems **hands-free, offline, and in real-time** — just by speaking.”

---

## 🏗️ Architecture Overview

```
+---------------------+
|   GUI Interface     |
+----------+----------+
           ↓
+----------v----------+
|   Voice Assistant   |  <-- Orchestrator
+----------+----------+
           ↓
+----------v----------+
|  Speech Processor   |  <-- STT + TTS
+----------+----------+
           ↓
+----------v----------+
| Emergency Handler   |  <-- Logic + Lookup
+----------+----------+
           ↓
+----------v----------+
| Configuration Layer |
+---------------------+
```

---

## 💻 Technology Stack

| Layer             | Tool/Library                  |
|------------------|-------------------------------|
| Programming Lang | Python 3.11                   |
| Speech Recognition | Vosk (offline)              |
| Text-to-Speech   | pyttsx3                       |
| Audio Input/Output| PyAudio                      |
| GUI              | Tkinter (standard Python GUI) |
| Data Storage     | JSON                          |

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/VaaniRakshak.git
cd VaaniRakshak
```

### 2. Install Dependencies

```bash
pip install vosk pyttsx3 pyaudio
```

> 💡 If `pyaudio` installation fails:
```bash
pip install pipwin
pipwin install pyaudio
```

---

### 3. Download Vosk Model

Download [`vosk-model-small-en-us-0.15`](https://alphacephei.com/vosk/models) and extract it here:

```
VaaniRakshak/
└── models/
    └── vosk-model-small-en-us-0.15/
        ├── am/
        ├── conf/
        ├── model.conf
        └── ...
```

---

## ▶️ Run the Application

```bash
python main.py
```

---

## 🧪 Sample Voice Commands

- `"I need help"`
- `"Nearest shelter"`
- `"Medical emergency"`
- `"Fire alert"`
- `"Exit"`

---

## 📦 Deployment

### 📁 Build an Executable (.exe) – Windows

Install [PyInstaller](https://pyinstaller.org/):

```bash
pip install pyinstaller
```

Then build:

```bash
pyinstaller --noconfirm --onefile --windowed main.py
```

Place `models/` and `data/` folders alongside the `.exe`.

---

## 🧾 License

This project is licensed under the [MIT License](LICENSE).

---

## 🤝 Contributing

Pull requests are welcome! If you'd like to contribute improvements, localization, or accessibility features, please open an issue.

---

## 📅 Changelog

- **2025-06-14** – Initial release with full offline assistant functionality

---

## 👤 Author

**Subuhana Basheer**  
*Developer | Tech for Social Good | Voice AI Enthusiast*

---

> “VaaniRakshak speaks for you — when your voice is the only tool you have.”


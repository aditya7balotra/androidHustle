# androidHustle

**Automate Android device interaction and data extraction using ADB (Android Debug Bridge)**

A Python package that simplifies interaction with Android devices, enabling you to programmatically extract messages, contacts, media files, and more from connected Android devices.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#-features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [CLI Usage](#cli-usage)
  - [Programmatic Usage](#programmatic-usage)
- [Project Structure](#project-structure)
- [Module Documentation](#module-documentation)
  - [Connection Management](#connection-management)
  - [Data Loading Modules](#data-loading-modules)
  - [CLI Commands](#cli-commands)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

**androidHustle** is a comprehensive automation toolkit for Android devices. It leverages ADB to establish secure connections with Android devices and provides an intuitive interface to:

- Extract call logs and SMS messages
- Export contacts and device metadata
- Download media files (images, videos, audio)
- Extract data from messaging apps (WhatsApp, Telegram)
- Get insights into device information

Whether you're building a automating device backup, androidHustle handles the complexity of ADB communication and data extraction.

---

## ✨ Features

| Feature | Supported |
|---------|-----------|
| **Call Logs** | ✅ Extract call history with timestamps and duration |
| **SMS Logs** | ✅ Extract SMS messages with sender/receiver info |
| **Contacts** | ✅ Export device contacts with phone numbers |
| **Device Media** | ✅ Download photos, videos, and audio files |
| **WhatsApp Data** | ✅ Extract images, videos, audio, documents, and notes |
| **Telegram Data** | ✅ Extract cache, media, documents, and files |
| **Device Metadata** | ✅ Get device info, build properties, system details |
| **Multi-Device Support** | ✅ Connect to multiple devices by serial number |
| **Progress Tracking** | ✅ Real-time progress bars for large data transfers |
| **Flexible Output** | ✅ JSON and raw data formats |

---

## Prerequisites

Before using androidHustle, ensure you have:

1. **Python 3.12 or higher** - [Download Python](https://www.python.org/downloads/)
2. **ADB (Android Debug Bridge)** installed
   - **Windows**: Download from [Android SDK Platform Tools](https://developer.android.com/tools/releases/platform-tools)
   - **Linux**: `sudo apt-get install android-tools-adb`
   - **macOS**: `brew install android-platform-tools`
3. **Android device** with USB debugging enabled

### Enable USB Debugging on Your Android Device

1. Go to **Settings** → **About Phone**
2. Tap **Build Number** 7 times to enable Developer Options
3. Go back and open **Developer Options**
4. Enable **USB Debugging**
5. Connect device to computer with USB cable
6. Accept the authorization prompt on your device

---

## Installation

### Option 1: Install from PyPI (Once Published | not published yet)

```bash
pip install androidHustle
```

### Option 2: Install from Source

```bash
git clone https://github.com/aditya7balotra/androidHustle.git
cd androidHustle
pip install -e .
```

### Verify Installation

```bash
# Check if the CLI is available
ahustle --list-devices

# Check installed version
python -c "import androidHustle; print(androidHustle.__version__)"
```

---

## Quick Start

### 1. Connect to Your Device

```python
from androidHustle.connect import Connection

# Initialize connection
conn = Connection(fname="my_extraction")

# Get all available devices
devices = conn.get_avl()  # Returns list of device serial numbers
print(devices)

# Connect to the first device
conn.connect(devices[0])
```

### 2. Extract Data (Example: Call Logs)

```python
from androidHustle.load import Call

# Initialize Call data loader
call_extractor = Call(conn)

# Extract call logs
call_extractor.get_call_logs()
# Data saved to: my_extraction/call_logs/
```

### 3. Access Your Data

Extracted files are organized by data type in the extraction folder:
```
my_extraction/
├── call_logs/
├── sms_logs/
├── contacts/
├── device_media/
├── whatsapp/
├── telegram/
└── metadata/
```

---

## Usage

### CLI Usage

The command-line interface makes it easy to extract data without writing code.

#### List Connected Devices

```bash
ahustle --list-devices
ahustle -ldevs
```

#### Extract Call Logs

```bash
# Extract from device at index 0 (default)
ahustle --calllog

# Extract from specific device
ahustle --calllog --index-dev 1
```

#### Extract SMS Messages

```bash
ahustle --msglog
ahustle -mlog --index-dev 0
```

#### Extract Contacts

```bash
ahustle --contact
ahustle -cont
```

#### Extract WhatsApp Data

```bash
# Extract WhatsApp images and videos
ahustle --whatsapp img vid

# Available options: img, aud, docs, vnotes, vidnotes, vid
ahustle -wha img aud docs --index-dev 1
```

#### Extract Telegram Data

```bash
# Extract Telegram photos and documents
ahustle --telegram img docs

# Available options: cache, aud, vid, file, docs, img
ahustle -tel cache aud vid --index-dev 0
```

#### Extract Device Media

```bash
# Extract device photos, videos, and audio
ahustle --device img vid aud

# Available options: vid, aud, file, img
ahustle -dev img file
```

#### Extract Contacts

```bash
ahustle --metadata
ahustle -met
```

#### Combined Usage

```bash
# You can extract multiple data types in one command
ahustle --calllog --contact --whatsapp img vid --index-dev 0
```

---

### Programmatic Usage

Use androidHustle in your Python code for fine-grained control.

#### Basic Template

```python
from androidHustle.connect import Connection
from androidHustle.load import (
    Call,
    Sms,
    Contacts,
    Metadata,
    DeviceMedia,
    WhatsApp,
    Telegram
)

# 1. Initialize connection
conn = Connection(fname="extraction_folder")

# 2. Get available devices
devices = conn.get_avl()
print(f"Available devices: {devices}")

# 3. Connect to a device
conn.connect(devices[0])

# 4. Create data loaders and extract data
call = Call(conn)
call.get_call_logs()

sms = Sms(conn)
sms.get_sms_logs()

contacts = Contacts(conn)
contacts.get_contacts()
```

---

## Project Structure

```
androidHustle/
├── src/androidHustle/
│   ├── __init__.py              # Package initialization and version
│   ├── __main__.py              # Entry point for module execution
│   ├── cli.py                   # Command-line interface
│   ├── utils.py                 # Utility functions (parsing, validation)
│   ├── version.py               # Version information
│   │
│   ├── configs/                 # Configuration management
│   │   └── _android.py          # Android-specific configurations
│   │
│   ├── connect/                 # ADB connection handling
│   │   └── connect.py           # Connection class
│   │
│   └── load/                    # Data extraction modules
│       ├── __init__.py
│       ├── call_logs.py         # Call log extraction
│       ├── sms_logs.py          # SMS extraction
│       ├── contacts.py          # Contact extraction
│       ├── metadata.py          # Device metadata extraction
│       ├── device_media.py      # Device media files extraction
│       ├── whatsapp.py          # WhatsApp data extraction
│       └── telegram.py          # Telegram data extraction
│
├── example/
│   └── basic.py                 # Basic usage example
│
├── requirements.txt             # Python dependencies
├── setup.py                     # Package setup configuration
├── Makefile                     # Build automation
└── README.md                    # This file
```

---

## Module Documentation

### Connection Management

**Module:** [src/androidHustle/connect/](src/androidHustle/connect/)

The `Connection` class manages ADB connections to Android devices.

```python
from androidHustle.connect import Connection

# Initialize connection
conn = Connection(
    host="localhost",    # ADB host (default: localhost)
    port=5037,          # ADB port (default: 5037)
    fname="my_extraction" # Output folder name
)

# List available devices
devices = conn.get_avl()  # Returns: ["device_serial_1", "device_serial_2"]

# Connect to a specific device
device = conn.connect("device_serial")

# Connected device object is stored in conn.device
print(conn.device)
```

**Key Methods:**
- `get_avl()` - Get list of available device serial numbers
- `connect(serial)` - Connect to device by serial number

---

### Data Loading Modules

**Location:** [src/androidHustle/load/](src/androidHustle/load/)

Each module extracts a specific type of data. All modules inherit from `Tools` base class and follow the same pattern.

#### Call Logs - [call_logs.py](src/androidHustle/load/call_logs.py)

Extract device call history.

```python
from androidHustle.load import Call

call = Call(conn)
call.get_call_logs()

# Files created:
# - call_logs/raw_call_logs.txt
# - call_logs/call_logs.json
```

**Extracted Data:** Call timestamp, duration, caller/callee info

---

#### SMS Logs - [sms_logs.py](src/androidHustle/load/sms_logs.py)

Extract SMS message history.

```python
from androidHustle.load import Sms

sms = Sms(conn)
sms.get_sms_logs()

# Files created:
# - sms_logs/raw_sms_logs.txt
# - sms_logs/sms_logs.json
```

**Extracted Data:** Message content, sender, timestamp, read status

---

#### Contacts - [contacts.py](src/androidHustle/load/contacts.py)

Extract saved device contacts.

```python
from androidHustle.load import Contacts

contacts = Contacts(conn)
contacts.get_contacts()

# Files created:
# - contacts/raw_contacts.txt
# - contacts/saved_contacts.json
```

**Extracted Data:** Contact name, phone numbers, email addresses

---

#### Device Media - [device_media.py](src/androidHustle/load/device_media.py)

Extract media files from device storage.

```python
from androidHustle.load import DeviceMedia

media = DeviceMedia(conn)
media.get_device_data(["img", "vid", "aud"])

# Options: "img" (images), "vid" (videos), "aud" (audio), "file" (documents)
```

**Extracted Data:** Photos, videos, audio files from device storage

---

#### Device Metadata - [metadata.py](src/androidHustle/load/metadata.py)

Extract device information and system properties.

```python
from androidHustle.load import Metadata

metadata = Metadata(conn)
metadata.get_metadata()

# Files created:
# - metadata/metadata.json
```

**Extracted Data:** Device name, model, Android version, IMEI, etc.

---

#### WhatsApp - [whatsapp.py](src/androidHustle/load/whatsapp.py)

Extract WhatsApp data if installed on device.

```python
from androidHustle.load import WhatsApp

whatsapp = WhatsApp(conn)
whatsapp.get_data(["img", "vid", "aud", "docs"])

# Available options:
# - "img"      : WhatsApp images
# - "vid"      : WhatsApp videos
# - "aud"      : WhatsApp audio messages
# - "docs"     : WhatsApp documents
# - "vnotes"   : WhatsApp voice notes
# - "vidnotes" : WhatsApp video notes
```

**Extracted Data:** WhatsApp photos, videos, audio messages, documents

---

#### Telegram - [telegram.py](src/androidHustle/load/telegram.py)

Extract Telegram data if installed on device.

```python
from androidHustle.load import Telegram

telegram = Telegram(conn)
telegram.get_data(["img", "vid", "docs", "cache"])

# Available options:
# - "img"   : Telegram photos
# - "vid"   : Telegram videos
# - "aud"   : Telegram audio files
# - "docs"  : Telegram documents
# - "file"  : Telegram files
# - "cache" : Telegram cache
```

**Extracted Data:** Telegram media, documents, and cached files

---

### CLI Commands

**Module:** [src/androidHustle/cli.py](src/androidHustle/cli.py)

The CLI provides command-line access to all extraction features.

**Entry Point:** `ahustle`

**Global Options:**
- `--index-dev`, `-ind` - Device index to target (default: 0)
- `--list-devices`, `-ldevs` - List all connected devices

**Data Extraction Commands:**

| Command | Aliases | Type | Output |
|---------|---------|------|--------|
| `--calllog` | `-clog` | Boolean | Call logs |
| `--msglog` | `-mlog` | Boolean | SMS messages |
| `--contact` | `-cont` | Boolean | Contacts |
| `--metadata` | `-met` | Boolean | Device info |
| `--device` | `-dev` | Multi-choice | Device media (img, vid, aud, file) |
| `--whatsapp` | `-wha` | Multi-choice | WhatsApp (img, aud, docs, vnotes, vidnotes, vid) |
| `--telegram` | `-tel` | Multi-choice | Telegram (cache, aud, vid, file, docs, img) |

---

## Examples

### Example 1: Extract Everything from Device

```python
from androidHustle.connect import Connection
from androidHustle.load import (
    Call, Sms, Contacts, Metadata, DeviceMedia, WhatsApp
)

# Setup
conn = Connection(fname="device_backup")
conn.connect(conn.get_avl()[0])

# Extract all data
Call(conn).get_call_logs()
Sms(conn).get_sms_logs()
Contacts(conn).get_contacts()
Metadata(conn).get_metadata()
DeviceMedia(conn).get_device_data(["img", "vid"])
WhatsApp(conn).get_data(["img", "vid", "aud"])

print("Extraction complete! Check device_backup/ folder")
```

### Example 2: Selective WhatsApp Extraction

```python
from androidHustle.connect import Connection
from androidHustle.load import WhatsApp

conn = Connection(fname="whatsapp_backup")
conn.connect(conn.get_avl()[0])

# Extract only WhatsApp images and documents
whatsapp = WhatsApp(conn)
whatsapp.get_data(["img", "docs"])
```

### Example 3: Using CLI for Quick Extraction

```bash
# List devices
ahustle --list-devices

# Extract call logs and contacts
ahustle --calllog --contact

# Extract WhatsApp media from device index 1
ahustle --whatsapp img vid --index-dev 1

# Extract Telegram with all options
ahustle --telegram img vid docs aud cache
```

### Example 4: Multi-Device Extraction

```python
from androidHustle.connect import Connection
from androidHustle.load import Call, Sms

conn = Connection()
devices = conn.get_avl()

for idx, serial in enumerate(devices):
    conn.connect(serial)
    print(f"Extracting from device {idx}: {serial}")
    
    Call(conn).get_call_logs()
    Sms(conn).get_sms_logs()
    
    print(f"Device {idx} extraction complete!\n")
```

---

## Troubleshooting

### Device Not Found

```bash
# Verify ADB is installed and device is connected
adb devices

# If not listed, ensure:
# 1. USB Debugging is enabled on device
# 2. Device is connected with USB cable
# 3. You've accepted the authorization prompt on device
adb kill-server
adb start-server
```

### Permission Denied

Ensure your user has permission to access USB devices:

```bash
# Linux/macOS
sudo chmod 666 /dev/bus/usb/*/*
```

### ADB Connection Failed

Check if ADB server is running:

```bash
# Restart ADB
adb kill-server
adb start-server
adb devices
```

---

## Contributing

Contributions are welcome! Please feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Author

**Aditya Blotra**
- Email: mr.balotra4@gmail.com
- GitHub: [@aditya7balotra](https://github.com/aditya7balotra)

---

## Acknowledgments

- [pure-python-adb](https://github.com/Swind/pure-python-adb) - Pure Python ADB client
- [tqdm](https://github.com/tqdm/tqdm) - Progress bars for Python

---

**Last Updated:** February 2026
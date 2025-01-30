# jubilant-garbanzo

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Examples](#examples)
- [Contributing](#contributing)
- [Testing](#testing)
- [License](#license)
- [Contact](#contact)

## Overview

a Python program that monitors a folder for new PDF files and prints them using configuration variables from a file:

**config.ini**
```ini
[DEFAULT]
monitoring_path = C:\somepathtofolder
printer_name = Printer Name
```

**Key Windows-specific changes:**
1. Uses `win32api.ShellExecute` for native Windows printing
2. Implements real-time monitoring with `watchdog` instead of polling
3. Uses Windows-style path handling
4. Verifies printer names against Windows installed printers
5. Adds proper file closure handling
6. Includes 1-second delay after file detection to ensure write completion

**Requirements:**
```bash
pip install pywin32 watchdog
```

**Features:**
1. Real-time file monitoring (no 30-second delay)
2. Automatic directory creation
3. Native Windows printing dialog handling
4. Proper error handling for Windows permissions
5. Case-insensitive PDF detection
6. Clean exit with Ctrl+C

**Notes:**
1. The printer name must match exactly with a installed printer
2. Requires admin privileges if using network printers
3. Uses Windows file locking mechanisms to ensure complete writes
4. The "printed" directory will be created automatically
5. Handles spaces in file paths and directory names

**To find your printer name:**
```python
import win32print
print(win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL))
```

This version provides more reliable monitoring on Windows and integrates better with the Windows printing subsystem while maintaining the requested file-moving functionality.
# Liquid Glass Clock Widget

A sleek, transparent "Liquid Glass" style clock widget for Windows 11.

![Liquid Glass Clock](https://github.com/inchinet/liquid-glass-clock/blob/master/LiquidClock.jpg)

## Features

- **Liquid Glass Aesthetic**: Transparent, high-quality rendering that looks great on any wallpaper.
- **Draggable**: Move the widget anywhere on your desktop.
- **Persistent Position**: Remembers where you left it on your next startup.
- **Date & Lunar Date**: Displays current date, day of week, and accurate Chinese Lunar date.
- **24 Solar Terms (廿四節氣)**: Dynamically calculates and displays the current solar term using astronomical calculations. Works for any year (past, present, or future) with dates accurate to Hong Kong timezone. No hardcoded dates - all calculations based on the sun's ecliptic longitude.
- **Taskbar Integration**: Minimizes to taskbar for easy access.

## Requirements

- Windows 10/11
- Python 3.x (if running from source)

## Usage

### Running from Executable
1. Download the latest release (`LiquidGlassClock.exe`).
2. Run the executable.
3. Drag to position.
4. Click `_` to minimize to taskbar.
5. Click `X` to close completely.

### Running from Source

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/liquid-glass-clock.git
   cd liquid-glass-clock
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## Configuration

The widget creates a `config.ini` file upon first run/close to store your settings.
```ini
[Settings]
WindowX=1500
WindowY=50
Active=1
```

## Building

To build the executable yourself using PyInstaller:

```bash
build_exe.bat
```
The output file will be in the `dist/` folder.

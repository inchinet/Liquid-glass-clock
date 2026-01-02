import sys
import os
import ctypes
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from clock_ui import ClockWidget

def main():
    # Set AppUserModelID to ensure taskbar icon works correctly
    # Set AppUserModelID to ensure taskbar icon works correctly
    myappid = 'inchinet.liquidglassclock.widget.1.0' 
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass

    # Setup basic logging
    log_file = os.path.join(os.path.dirname(sys.executable), 'debug.log') if getattr(sys, 'frozen', False) else 'debug.log'
    with open(log_file, 'w') as f:
        f.write(f"Starting application...\n")
        f.write(f"Frozen: {getattr(sys, 'frozen', False)}\n")

    app = QApplication(sys.argv)

    # Set Application Icon (Important for Taskbar)
    if getattr(sys, 'frozen', False):
        resource_path = sys._MEIPASS
    else:
        resource_path = os.path.dirname(os.path.abspath(__file__))
    
    with open(log_file, 'a') as f:
        f.write(f"Resource Path: {resource_path}\n")

    icon_path = os.path.join(resource_path, 'clock.ico')
    
    with open(log_file, 'a') as f:
        f.write(f"Icon Path: {icon_path}\n")
        f.write(f"Icon Exists: {os.path.exists(icon_path)}\n")

    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
        with open(log_file, 'a') as f:
            f.write(f"Parameters setWindowIcon called.\n")

    clock = ClockWidget()
    clock.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

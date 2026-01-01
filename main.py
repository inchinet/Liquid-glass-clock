
import sys
from PyQt6.QtWidgets import QApplication
from clock_ui import ClockWidget

def main():
    app = QApplication(sys.argv)
    clock = ClockWidget()
    clock.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

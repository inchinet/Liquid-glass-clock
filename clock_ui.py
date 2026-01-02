
import sys
import os
import datetime
import configparser
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import Qt, QTimer, QPoint, QRect, QTime, QDate
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPolygon, QIcon, QAction, QRadialGradient
from lunarcalendar import Converter, Solar



if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app 
    # path into variable _MEIPASS.
    # Config should be external (next to exe), Assets internal (in temp bundle dir)
    application_path = os.path.dirname(sys.executable)
    resource_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))
    resource_path = application_path

CONFIG_FILE = os.path.join(application_path, 'config.ini')


class ClockWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.config = configparser.ConfigParser()
        self.initUI() # Init UI first to get geometry for default position calculation if needed
        self.read_config()
        self.dragging = False
        self.offset = QPoint()

        # Timer for updating the clock
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(100) # Update every 100ms for smooth second hand

    def read_config(self):
        self.config.read(CONFIG_FILE)
        if 'Settings' not in self.config:
            self.config['Settings'] = {}
        
        settings = self.config['Settings']
        
        # Default Position Logic
        if 'WindowX' in settings and 'WindowY' in settings:
            x = int(settings['WindowX'])
            y = int(settings['WindowY'])
            
            # Validate if the position is on any connected screen
            is_visible = False
            widget_rect = QRect(x, y, 200, 200) # Assuming 200x200 size
            
            for screen in QApplication.screens():
                # Check if the center of the widget is on the screen to ensure visibility
                # Or at least a significant portion. Let's use center.
                if screen.geometry().contains(QRect(x, y, 200, 200).center()):
                    is_visible = True
                    break
            
            if not is_visible:
                # Reset to default if off-screen
                screen_geometry = QApplication.primaryScreen().geometry()
                x = screen_geometry.width() - 200 - 50
                y = 50
        else:
            # Default to Top-Right
            screen_geometry = QApplication.primaryScreen().geometry()
            x = screen_geometry.width() - self.width() - 50
            y = 50
            
        self.move(x, y)
        
        # Ensure it's active if specified
        self.active = int(settings.get('Active', 1))

    def save_config(self):
        if 'Settings' not in self.config:
            self.config['Settings'] = {}
        
        self.config['Settings']['WindowX'] = str(self.x())
        self.config['Settings']['WindowY'] = str(self.y())
        self.config['Settings']['Active'] = str(self.active)
        
        with open(CONFIG_FILE, 'w') as configfile:
            self.config.write(configfile)

    def initUI(self):
        # Frameless window that stays on top
        # We DO NOT use Qt.WindowType.Tool because we want it to show in the taskbar for minimizing
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(200, 200) # Updated size as requested
        self.setWindowTitle('Liquid Clock')

        # Set Window Icon
        icon_path = os.path.join(resource_path, 'clock.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Scale everything from the original 300x300 design to current size
        scale = min(self.width(), self.height()) / 300.0
        painter.scale(scale, scale)

        # Draw "Liquid Glass" Background
        painter.setPen(Qt.PenStyle.NoPen)
        
        # Gradient for liquid effect
        # Center of gradient slightly offset to top-left to simulate light source
        gradient = QRadialGradient(100, 100, 200) 
        gradient.setColorAt(0, QColor(255, 255, 255, 180))   # Highlight
        gradient.setColorAt(0.5, QColor(255, 255, 255, 40))  # Main body transparent
        gradient.setColorAt(1, QColor(255, 255, 255, 100))   # Edge slightly clearer
        
        painter.setBrush(QBrush(gradient))
        painter.drawEllipse(10, 10, 280, 280)
        
        # Glass Rim effect - Outer
        pen = QPen(QColor(255, 255, 255, 200), 2)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(10, 10, 280, 280)

        # Inner subtle rim to give depth
        pen = QPen(QColor(255, 255, 255, 50), 4)
        painter.setPen(pen)
        painter.drawEllipse(15, 15, 270, 270)

        # Draw Clock Face logic here
        self.draw_clock(painter)
        
        # Draw Buttons
        self.draw_buttons(painter)

    def draw_clock(self, painter):
        # Center
        center = QPoint(150, 150)

        # Draw 12 hour ticks
        painter.save()
        painter.translate(center)
        painter.setPen(QPen(QColor(255, 255, 255, 180), 2))
        for i in range(12):
            painter.rotate(30)
            painter.drawLine(0, -135, 0, -125) # Close to the edge (radius 140 approx)
        painter.restore()
        
        # Date & Lunar Date Box
        painter.setPen(Qt.PenStyle.NoPen)
        
        # Box Gradient
        box_gradient = QRadialGradient(center.x(), center.y() + 70, 80)
        box_gradient.setColorAt(0, QColor(0, 0, 0, 80))
        box_gradient.setColorAt(1, QColor(0, 0, 0, 40))
        painter.setBrush(QBrush(box_gradient))
        
        rect_width = 200
        rect_height = 85
        # Draw rounded rect bg
        # Shift up slightly to fit 3 lines (Date, Time, Lunar)
        # Center Y is 150. Hands extend down to ~170 (second hand 20px). 
        # Start box at 180 to be safe.
        box_top_y = center.y() + 5
        painter.drawRoundedRect(center.x() - rect_width//2, box_top_y, rect_width, rect_height, 15, 15)

        # Text
        # Light Purple/Blue for better visibility.
        # R=200, G=225, B=255 gives a nice light blue/purple tint.
        text_color = QColor(200, 225, 255)
        painter.setPen(text_color)
        current_time = datetime.datetime.now()
        
        # Date YYYY/MM/DD Weekday
        date_str = current_time.strftime("%Y/%m/%d %a")
        painter.setFont(QFont('Segoe UI', 11, QFont.Weight.Bold))
        painter.drawText(QRect(center.x() - rect_width//2, box_top_y + 5, rect_width, 25), Qt.AlignmentFlag.AlignCenter, date_str)

        # Time AM/PM
        time_str = current_time.strftime("%I:%M:%S %p")
        painter.setFont(QFont('Segoe UI', 12, QFont.Weight.Bold))
        painter.drawText(QRect(center.x() - rect_width//2, box_top_y + 30, rect_width, 25), Qt.AlignmentFlag.AlignCenter, time_str)

        # Lunar Date
        solar = Solar(current_time.year, current_time.month, current_time.day)
        lunar = Converter.Solar2Lunar(solar)
        lunar_str = self.get_lunar_string(lunar)
        painter.setFont(QFont('Segoe UI', 10, QFont.Weight.Bold))
        painter.drawText(QRect(center.x() - rect_width//2, box_top_y + 55, rect_width, 25), Qt.AlignmentFlag.AlignCenter, lunar_str)

        # Hands
        painter.save()
        painter.translate(center)
        
        time = QTime.currentTime()
        
        # Hour Hand
        painter.save()
        painter.rotate(30.0 * ((time.hour() + time.minute() / 60.0)))
        # Darker pen for better contrast on white background
        painter.setPen(QPen(QColor(50, 50, 50, 200), 2)) 
        painter.setBrush(QColor(240, 240, 240, 255))
        # Slightly wider and nicer shape
        painter.drawConvexPolygon(QPolygon([QPoint(-4, 0), QPoint(-2, -60), QPoint(0, -65), QPoint(2, -60), QPoint(4, 0)]))
        painter.restore()

        # Minute Hand
        painter.save()
        painter.rotate(6.0 * (time.minute() + time.second() / 60.0))
        # Darker pen for better contrast
        painter.setPen(QPen(QColor(50, 50, 50, 200), 2))
        painter.setBrush(QColor(240, 240, 240, 255))
        painter.drawConvexPolygon(QPolygon([QPoint(-3, 0), QPoint(-1, -90), QPoint(0, -95), QPoint(1, -90), QPoint(3, 0)]))
        painter.restore()

        # Second Hand
        painter.save()
        painter.rotate(6.0 * time.second())
        # Dark pen for outline, red fill for visibility
        painter.setPen(QPen(QColor(50, 50, 50, 200), 1))
        painter.setBrush(QColor(200, 50, 50, 255)) # Red second hand
        painter.drawConvexPolygon(QPolygon([QPoint(-1, 20), QPoint(-1, -100), QPoint(1, -100), QPoint(1, 20)]))
        painter.restore()
        
        # Center Cap
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawEllipse(QPoint(0,0), 4, 4)
        
        painter.restore()

    def get_lunar_string(self, lunar):
        # lunar is an object with year, month, day.
        # We need Chinese mapping.
        CHINESE_MONTHS = ["", "正月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"]
        CHINESE_DAYS = ["", "初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
                        "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
                        "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"]
        month_str = CHINESE_MONTHS[lunar.month] if 1 <= lunar.month <= 12 else str(lunar.month)
        day_str = CHINESE_DAYS[lunar.day] if 1 <= lunar.day <= 30 else str(lunar.day)
        return f"{month_str}{day_str}"

    def draw_buttons(self, painter):
        # Clean, modern buttons
        # Floating near top right of circle
        
        # We need to set rects for hit testing
        # Let's put them on the rim area approx
        
        # Minimize (underscore) - Top Left
        self.min_btn_rect = QRect(10, 10, 24, 24)
        
        # Close (X) - Top Right
        # Widget width is 300 in "design space" (because of scaling), or we should use relative positions?
        # The painter is scaled by `scale = min(self.width(), self.height()) / 300.0`
        # So we should define coordinates in the 300x300 design space.
        self.close_btn_rect = QRect(266, 10, 24, 24)
        
        # Draw backgrounds (grey background as requested)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(100, 100, 100, 200)) # Grey background
        painter.drawEllipse(self.min_btn_rect)
        painter.drawEllipse(self.close_btn_rect)
        
        # Draw Symbols
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        
        # Minimize (underscore)
        painter.drawText(self.min_btn_rect, Qt.AlignmentFlag.AlignCenter, "_")
        
        # Close (X)
        painter.setFont(QFont('Arial', 10, QFont.Weight.Bold))
        painter.drawText(self.close_btn_rect, Qt.AlignmentFlag.AlignCenter, "X")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            
            # Hit testing logic considering scale
            scale = min(self.width(), self.height()) / 300.0
            pos_x = event.position().x() / scale
            pos_y = event.position().y() / scale
            mapped_pos = QPoint(int(pos_x), int(pos_y))
            
            if self.min_btn_rect.contains(mapped_pos):
                self.showMinimized()
            elif self.close_btn_rect.contains(mapped_pos):
                self.save_config()
                QApplication.quit()
            else:
                self.dragging = True
                self.offset = event.globalPosition().toPoint() - self.pos()


    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPosition().toPoint() - self.offset)

    def mouseReleaseEvent(self, event):
        if self.dragging:
            self.dragging = False
            self.save_config()

    def closeEvent(self, event):
        self.save_config()
        event.accept()

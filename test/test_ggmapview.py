import os
os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--no-sandbox'

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt, QRect, QUrl
import sys


class MapOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.start_point = None
        self.end_point = None
        self.shapes = []  # Store drawn shapes
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)  # Allow interaction
        self.setAttribute(Qt.WA_StyledBackground, True)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_point = event.pos()
            self.end_point = None
            self.update()

    def mouseMoveEvent(self, event):
        if self.start_point:
            self.end_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.start_point:
            self.shapes.append((self.start_point, self.end_point))
            self.start_point = None
            self.end_point = None
            self.update()

    def paintEvent(self, event):
        if not self.start_point and not self.shapes:
            return

        painter = QPainter(self)
        pen = QPen(Qt.red, 2, Qt.SolidLine)
        painter.setPen(pen)

        # Draw existing shapes
        for shape in self.shapes:
            painter.drawRect(QRect(shape[0], shape[1]))

        # Draw current shape
        if self.start_point and self.end_point:
            painter.drawRect(QRect(self.start_point, self.end_point))


class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Map Viewer with Drawing")
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # QWebEngineView for displaying the map
        self.webview = QWebEngineView()

        # Replace with Bing Maps URL and your API key
        bing_api_key = "AkCDUXwYzM3w36XYcNeT0kNOFhpTiQuwluXkQlFBs1WhFbknP2_2iDBXeL_WzXCc"  # Replace with your actual API key
        map_url = f"https://www.bing.com/maps/embed?h=600&w=800&cp=47.6205~-122.3493&lvl=14&typ=d&sty=r&src=SHELL&FORM=MBEDV8&key={bing_api_key}"
        self.webview.setUrl(QUrl(map_url))

        # Map overlay for drawing
        self.overlay = MapOverlay(self)
        self.overlay.setGeometry(0, 0, 800, 600)
        self.overlay.setStyleSheet("background: transparent;")

        # Add map widget to layout
        layout.addWidget(self.webview)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.overlay.setGeometry(self.webview.geometry())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapWindow()
    window.show()
    sys.exit(app.exec_())

import os
os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--no-sandbox'

import sys
import folium
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget


class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Map Viewer")

        # Create the map
        self.map = folium.Map(location=[36.241332, 127.657246], 
                              zoom_start=15, 
                              tiles='OpenStreetMap')

        # Create a Qt WebEngineView to display the map
        self.web_view = QWebEngineView()
        self.web_view.setHtml(self.map._repr_html_())

        # Create a layout to hold the web view
        self.widget_layout = QVBoxLayout()
        self.widget_layout.addWidget(self.web_view)

        # Create a central widget and set its layout
        self.widget = QWidget()
        self.widget.setLayout(self.widget_layout)

        # Set the widget as the central widget of the main window
        self.setCentralWidget(self.widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MapWindow()
    window.show()
    sys.exit(app.exec_())

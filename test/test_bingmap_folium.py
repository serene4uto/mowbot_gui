import os
os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--no-sandbox'

import sys
import folium
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget


class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Map Viewer - Bing Maps")

        # Your Bing Maps API key
        BING_API_KEY = "AkCDUXwYzM3w36XYcNeT0kNOFhpTiQuwluXkQlFBs1WhFbknP2_2iDBXeL_WzXCc"

        # Create the map
        self.map = folium.Map(location=[36.111165, 128.38427166], zoom_start=15)

        # Add Bing Maps tile layer
        bing_tile_layer = folium.TileLayer(
            tiles=f"https://t.ssl.ak.dynamic.tiles.virtualearth.net/comp/ch/{{z}}/{{x}}/{{y}}?mkt=en-US&it=A&key={BING_API_KEY}",
            attr="Bing Maps",
            name="Bing Aerial",
            overlay=True,
            control=True,
        )
        bing_tile_layer.add_to(self.map)

        # Add layer control to switch layers
        folium.LayerControl().add_to(self.map)

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
    # Set QtWebEngine environment flags
    os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--no-sandbox'

    app = QApplication(sys.argv)
    window = MapWindow()
    window.show()
    sys.exit(app.exec_())

from PyQt5.QtWebEngineWidgets import QWebEngineView

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
)

import folium
import io


class MapView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set up layout for the custom widget
        layout = QVBoxLayout(self)

        # Create a QWebEngineView to display the folium map
        self.webview = QWebEngineView(self)

        # Initialize map attributes
        self.default_location = [27.9585376, 170.0278471]
        self.zoom_start = 13
        self.map = folium.Map(location=self.default_location, zoom_start=self.zoom_start)
        self.markers = []

        # folium.TileLayer('openstreetmap').add_to(self.map)
        # folium.LayerControl().add_to(self.map)

        # Load the initial map
        self._reload_map()

        # Add the webview to the layout
        layout.addWidget(self.webview)

    def _reload_map(self):
        """Helper function to reload the map into the QWebEngineView."""
        data = io.BytesIO()
        self.map.save(data, close_file=False)
        self.webview.setHtml(data.getvalue().decode('utf-8'))

    def update_map_location(self, latitude, longitude, zoom=None):
        """
        Update the map center location and optionally the zoom level.
        """
        # Update the map location and zoom
        self.default_location = [latitude, longitude]
        self.map = folium.Map(location=self.default_location, zoom_start=zoom or self.zoom_start)
        self.markers.clear()  # Clear any existing markers
        self._reload_map()

    def add_marker(self, latitude, longitude, popup_text=None):
        """
        Add a marker to the map at the given latitude and longitude.
        """
        marker = folium.Marker(location=[latitude, longitude], popup=popup_text or "")
        self.markers.append(marker)
        marker.add_to(self.map)
        self._reload_map()

    def remove_markers(self):
        """
        Remove all markers from the map.
        """
        # Recreate the map with the same center and zoom, but without markers
        self.map = folium.Map(location=self.default_location, zoom_start=self.zoom_start)
        self.markers.clear()
        self._reload_map()

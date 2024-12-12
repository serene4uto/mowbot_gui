from PyQt5 import (
    QtWidgets,
    QtWebEngineWidgets,
)

import folium
import io


class MapView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Set up layout for the custom widget
        layout = QtWidgets.QVBoxLayout(self)
        
        # Create a QWebEngineView to display the folium map
        self.webview = QtWebEngineWidgets.QWebEngineView(self)

        # Create a folium map instance
        # You can customize the initial location, tiles, and zoom level as needed.
        m = folium.Map(
            location=[45.5236, -122.6750],
            zoom_start=13,
            tiles='OpenStreetMap'
        )

        # Save the map to an in-memory HTML buffer
        data = io.BytesIO()
        m.save(data, close_file=False)
        
        # Load the HTML content into the QWebEngineView
        self.webview.setHtml(data.getvalue().decode('utf-8'))
        
        # Add the webview to the layout
        layout.addWidget(self.webview)
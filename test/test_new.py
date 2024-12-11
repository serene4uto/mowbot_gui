import os
os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--no-sandbox --disable-gpu'

import sys
import math
import requests
import folium
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

# Function to calculate the quadkey for a specific tile
def tile_to_quadkey(tile_x, tile_y, zoom):
    quadkey = []
    for i in range(zoom, 0, -1):
        digit = 0
        mask = 1 << (i - 1)
        if (tile_x & mask) != 0:
            digit += 1
        if (tile_y & mask) != 0:
            digit += 2
        quadkey.append(str(digit))
    return ''.join(quadkey)

# Function to fetch Bing Maps tile metadata
def fetch_bing_metadata(api_key, imagery="Aerial"):
    metadata_url = f"http://dev.virtualearth.net/REST/V1/Imagery/Metadata/{imagery}?output=json&include=ImageryProviders&key={api_key}"
    response = requests.get(metadata_url)
    response.raise_for_status()
    metadata = response.json()
    return metadata

# Main PyQt Application
class MapWindow(QMainWindow):
    def __init__(self, bing_metadata):
        super().__init__()
        self.setWindowTitle("Bing Maps with Folium and PyQt")
        self.resize(800, 600)

        # Extract tile URL template and subdomain
        tile_url_template = bing_metadata['resourceSets'][0]['resources'][0]['imageUrl']
        subdomains = bing_metadata['resourceSets'][0]['resources'][0]['imageUrlSubdomains']

        # Replace {subdomain} with the first subdomain
        subdomain = subdomains[0]
        tile_url_template = tile_url_template.replace("{subdomain}", subdomain)

        # Replace {quadkey} with a specific quadkey for New York City (example coordinates)
        zoom_level = 10
        lat, lon = 40.7128, -74.0060  # New York City coordinates
        tile_x = int((lon + 180) / 360 * (2 ** zoom_level))
        sin_lat = math.sin(math.radians(lat))
        tile_y = int((1 - math.log((1 + sin_lat) / (1 - sin_lat)) / (4 * math.pi)) * (2 ** (zoom_level - 1)))
        quadkey = tile_to_quadkey(tile_x, tile_y, zoom_level)

        # Final tile URL
        tile_url = tile_url_template.replace("{quadkey}", quadkey)
        print("Generated Tile URL:", tile_url)  # Debug: Log the generated tile URL

        # Create a map using Folium
        self.map = folium.Map(location=[lat, lon], zoom_start=zoom_level)
        folium.TileLayer(
            tiles=tile_url,
            attr="© Microsoft Bing Maps",
            name="Bing Satellite",
            min_zoom=1,
            max_zoom=19
        ).add_to(self.map)

        # Add CSS fix for map container
        self.map.get_root().header.add_child(folium.Element("""
            <style>
                .folium-map {
                    width: 100%;
                    height: 100%;
                    position: absolute;
                }
            </style>
        """))

        # Add delay for initialization
        self.map.get_root().script.add_child(folium.Element("""
            setTimeout(() => {
                var map = document.getElementsByClassName('folium-map')[0];
                if (map) {
                    map.style.width = '100%';
                    map.style.height = '100%';
                }
            }, 1000);
        """))

        # Save the map as an HTML file
        map_html = os.path.abspath("map.html")  # Use absolute path
        self.map.save(map_html)

        # Display the map in a QWebEngineView
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl.fromLocalFile(map_html))  # Convert file path to QUrl

        # Set the layout
        container = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        container.setLayout(layout)
        self.setCentralWidget(container)

if __name__ == "__main__":
    # Replace with your Bing Maps API key
    BING_API_KEY = "AkCDUXwYzM3w36XYcNeT0kNOFhpTiQuwluXkQlFBs1WhFbknP2_2iDBXeL_WzXCc"

    # Fetch Bing Maps metadata
    bing_metadata = fetch_bing_metadata(BING_API_KEY, imagery="Aerial")

    # Launch the PyQt Application
    app = QApplication(sys.argv)
    window = MapWindow(bing_metadata)
    window.show()
    sys.exit(app.exec_())

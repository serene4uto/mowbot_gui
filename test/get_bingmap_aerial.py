import os
os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--no-sandbox --disable-gpu'

import requests
import math
from PIL import Image
from io import BytesIO
import folium
import branca
from branca.utilities import image_to_url
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView

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

# Function to download a Bing Maps tile
def fetch_bing_tile(api_key, zoom, lat, lon, imagery="Aerial"):
    sin_lat = math.sin(math.radians(lat))
    pixel_x = int((lon + 180) / 360 * 256 * (2 ** zoom))
    pixel_y = int((0.5 - math.log((1 + sin_lat) / (1 - sin_lat)) / (4 * math.pi)) * 256 * (2 ** zoom))
    tile_x = pixel_x // 256
    tile_y = pixel_y // 256

    quadkey = tile_to_quadkey(tile_x, tile_y, zoom)

    metadata_url = f"http://dev.virtualearth.net/REST/V1/Imagery/Metadata/{imagery}?output=json&include=ImageryProviders&key={api_key}"
    response = requests.get(metadata_url)
    response.raise_for_status()
    metadata = response.json()

    tile_url_template = metadata['resourceSets'][0]['resources'][0]['imageUrl']
    subdomains = metadata['resourceSets'][0]['resources'][0]['imageUrlSubdomains']
    tile_url = tile_url_template.replace("{subdomain}", subdomains[0]).replace("{quadkey}", quadkey)

    tile_response = requests.get(tile_url)
    tile_response.raise_for_status()
    tile_image = Image.open(BytesIO(tile_response.content))

    return tile_image

# PyQt Widget to Display Folium Map
class MapViewer(QWidget):
    def __init__(self, map_html):
        super().__init__()
        self.setWindowTitle("Map Viewer")
        self.init_ui(map_html)

    def init_ui(self, map_html):
        # Create a QWebEngineView
        web_view = QWebEngineView()
        web_view.setHtml(map_html)

        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(web_view)
        self.setLayout(layout)

if __name__ == "__main__":
    import sys

    BING_API_KEY = "AkCDUXwYzM3w36XYcNeT0kNOFhpTiQuwluXkQlFBs1WhFbknP2_2iDBXeL_WzXCc"
    ZOOM_LEVEL = 10
    LATITUDE = 40.7128
    LONGITUDE = -74.0060

    # Fetch the Bing Maps tile
    tile_image = fetch_bing_tile(BING_API_KEY, ZOOM_LEVEL, LATITUDE, LONGITUDE, imagery="Aerial")

    # Convert the image to a data URL using branca
    img_buffer = BytesIO()
    tile_image.save(img_buffer, format="PNG")
    img_buffer.seek(0)
    tile_url = image_to_url(img_buffer)
    
    green_tile = branca.utilities.image_to_url([[0, 255], [0, 255]])
    # white_tile = branca.utilities.image_to_url([[1, 1], [1, 1]])
    
    # save url to file
    with open("green_tile.html", "w") as f:
        f.write(green_tile)

    # Create a Folium Map
    m = folium.Map(location=[LATITUDE, LONGITUDE], zoom_start=ZOOM_LEVEL, tiles=green_tile, attr=" tile")
    # folium.raster_layers.ImageOverlay(tile_url, bounds=[[LATITUDE - 0.05, LONGITUDE - 0.05], [LATITUDE + 0.05, LONGITUDE + 0.05]]).add_to(m)

    # Launch the PyQt application
    app = QApplication(sys.argv)
    map_viewer = MapViewer(m._repr_html_())
    map_viewer.show()
    sys.exit(app.exec_())

import requests
import math
from PIL import Image
from io import BytesIO

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
    # Convert lat/lon to tile x, y
    sin_lat = math.sin(math.radians(lat))
    pixel_x = int((lon + 180) / 360 * 256 * (2 ** zoom))
    pixel_y = int((0.5 - math.log((1 + sin_lat) / (1 - sin_lat)) / (4 * math.pi)) * 256 * (2 ** zoom))
    tile_x = pixel_x // 256
    tile_y = pixel_y // 256

    # Calculate the quadkey
    quadkey = tile_to_quadkey(tile_x, tile_y, zoom)

    # Fetch tile metadata from Bing Maps Imagery REST API
    metadata_url = f"http://dev.virtualearth.net/REST/V1/Imagery/Metadata/{imagery}?output=json&include=ImageryProviders&key={api_key}"
    response = requests.get(metadata_url)
    response.raise_for_status()
    metadata = response.json()

    # Extract the tile URL template
    tile_url_template = metadata['resourceSets'][0]['resources'][0]['imageUrl']
    subdomains = metadata['resourceSets'][0]['resources'][0]['imageUrlSubdomains']

    # Construct the tile URL
    tile_url = tile_url_template.replace("{subdomain}", subdomains[0]).replace("{quadkey}", quadkey)

    # Fetch the tile image
    tile_response = requests.get(tile_url)
    tile_response.raise_for_status()
    tile_image = Image.open(BytesIO(tile_response.content))

    return tile_image

# Example usage
if __name__ == "__main__":
    BING_API_KEY = "AkCDUXwYzM3w36XYcNeT0kNOFhpTiQuwluXkQlFBs1WhFbknP2_2iDBXeL_WzXCc"
    ZOOM_LEVEL = 10
    LATITUDE = 40.7128  # New York City latitude
    LONGITUDE = -74.0060  # New York City longitude

    # Fetch and display the Bing Maps satellite (aerial) tile
    tile = fetch_bing_tile(BING_API_KEY, ZOOM_LEVEL, LATITUDE, LONGITUDE, imagery="Aerial")
    tile.show()

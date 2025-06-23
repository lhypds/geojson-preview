import geopandas as gpd
import matplotlib.pyplot as plt
import os
import sys

# Path to your GeoJSON file
geojson_path = "sample.geojson"

# Check if the file exists
if not os.path.exists(geojson_path):
    print(f"Error: GeoJSON file '{geojson_path}' not found.")
    sys.exit(1)

# Read GeoJSON
gdf = gpd.read_file(geojson_path)

# Plot and save as image
fig, ax = plt.subplots(figsize=(8, 8))  # you can adjust the image size
gdf.plot(ax=ax, color="blue", edgecolor="black")  # you can customize colors

plt.axis("off")  # optional: turn off axis
plt.savefig("preview.png", bbox_inches="tight", pad_inches=0, dpi=300)
plt.close()

print("Image saved as preview.png")
try:
    os.startfile("preview.png")
except Exception as e:
    print(f"Could not open image automatically: {e}")

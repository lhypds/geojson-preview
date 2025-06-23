import geopandas as gpd
import matplotlib.pyplot as plt

# Path to your GeoJSON file
geojson_path = "sample.geojson"

# Read GeoJSON
gdf = gpd.read_file(geojson_path)

# Plot and save as image
fig, ax = plt.subplots(figsize=(8, 8)) # you can adjust the image size
gdf.plot(ax=ax, color='blue', edgecolor='black') # you can customize colors

plt.axis('off')  # optional: turn off axis
plt.savefig("geojson_preview.png", bbox_inches='tight', pad_inches=0, dpi=300)
plt.close()

print("Image saved as geojson_preview.png")
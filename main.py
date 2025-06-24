import os
import sys
import geopandas as gpd
import matplotlib.pyplot as plt
import argparse


# New function to generate a preview image from a GeoJSON file
def preview_geojson(input_path, output_path):
    # Check if the file exists
    if not os.path.exists(input_path):
        print(f"Error: GeoJSON file '{input_path}' not found.")
        sys.exit(1)

    # Read the GeoJSON file
    gdf = gpd.read_file(input_path)
    # Plot and save as image
    fig, ax = plt.subplots(figsize=(8, 8))
    gdf.plot(ax=ax, color="lightgray", edgecolor="gray")
    plt.axis("off")
    plt.savefig(output_path, bbox_inches="tight", pad_inches=0, dpi=300)
    plt.close()
    print(f"Image saved as {output_path}")
    try:
        os.startfile(output_path)
    except Exception as e:
        print(f"Could not open image automatically: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate preview PNG from a GeoJSON file"
    )
    parser.add_argument(
        "-i",
        "--input",
        dest="input_path",
        default="sample.geojson",
        help="Path to the input GeoJSON file",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output_path",
        default="preview.png",
        help="Path for the output PNG file",
    )
    args = parser.parse_args()

    # Process GeoJSON
    print(f"Input GeoJSON file: {args.input_path}")
    print(f"Output PNG file: {args.output_path}")
    preview_geojson(args.input_path, args.output_path)


if __name__ == "__main__":
    main()

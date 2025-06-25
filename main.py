import os
import sys
import geopandas as gpd
import matplotlib.pyplot as plt
import argparse
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()
DEFAULT_OUTPUT_FORMAT = os.getenv("DEFAULT_OUTPUT_FORMAT", "png").lower()


# New function to generate a preview image from a GeoJSON file
def preview_geojson(input_path, format="png"):
    output_path = os.path.splitext(input_path)[0] + f".{format}"

    # Check if the file exists
    if not os.path.exists(input_path):
        print(f"Error: GeoJSON file '{input_path}' not found.")
        sys.exit(1)

    # Read the GeoJSON file
    gdf = gpd.read_file(input_path)
    # Plot and save as image
    fig, ax = plt.subplots(figsize=(8, 8))

    # Plot each feature individually to apply per-feature styling
    for _, row in gdf.iterrows():
        edgecolor = "black" if row.get("種類") == "図郭" else "gray"
        linewidth = 2 if row.get("種類") == "図郭" else 1
        gpd.GeoSeries([row.geometry]).plot(
            ax=ax,
            facecolor="lightgray",
            edgecolor=edgecolor,
            linewidth=linewidth,
            alpha=0.5,
        )

    plt.axis("off")
    plt.savefig(output_path, format=format, bbox_inches="tight", pad_inches=0, dpi=300)
    plt.close()
    print(f"Saved as {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate preview image from a GeoJSON file"
    )
    parser.add_argument(
        "-f",
        "--format",
        dest="output_format",
        default=DEFAULT_OUTPUT_FORMAT,
        help="Output image format (e.g., png, jpg)",
    )
    parser.add_argument(
        "-i",
        "--input",
        dest="input_path",
        default="sample.geojson",
        help="Path to the input GeoJSON file",
    )
    args = parser.parse_args()

    # Process GeoJSON
    print(f"Input GeoJSON file: {args.input_path}")
    print(f"Output format: {args.output_format}")
    preview_geojson(args.input_path, format=args.output_format)


if __name__ == "__main__":
    main()

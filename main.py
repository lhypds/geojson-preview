import os
import sys
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import argparse
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()
DEFAULT_OUTPUT_FORMAT = os.getenv("DEFAULT_OUTPUT_FORMAT", "png").lower()


# Set Japanese font to avoid mojibake (uses Windows Meiryo)
font_path = r"C:\Windows\Fonts\meiryo.ttc"
jp_font = fm.FontProperties(fname=font_path)
plt.rcParams["font.family"] = jp_font.get_name()


# New function to generate a preview image from a GeoJSON file
def preview_geojson(input_path, format="png"):
    output_path = os.path.splitext(input_path)[0] + f".{format}"

    # Check if the file exists
    if not os.path.exists(input_path):
        print(f"Error: GeoJSON file '{input_path}' not found.")
        sys.exit(1)

    # Read the GeoJSON file
    gdf = gpd.read_file(input_path, encoding="utf-8")

    # Identify the "図郭" polygon
    contour_polygon = gdf[gdf["種類"] == "図郭"].geometry.union_all()

    # Plot and save as image
    fig, ax = plt.subplots(figsize=(8, 8))

    # Plot each feature individually to apply per-feature styling
    for _, row in gdf.iterrows():
        is_contour = row.get("種類") == "図郭"
        edgecolor = (
            "red"
            if row.geometry.type == "Point"
            else (
                "cornflowerblue"
                if row.geometry.type in ["LineString", "MultiLineString"]
                else ("black" if is_contour else "gray")
            )
        )
        linewidth = (
            2
            if is_contour
            else (
                1 if row.geometry.type not in ["LineString", "MultiLineString"] else 1.5
            )
        )
        facecolor = (
            "none"
            if row.geometry.type == "LineString"
            else ("none" if is_contour else "lightgray")
        )
        alpha = 1 if is_contour else 0.5

        geometry_to_plot = row.geometry
        if not is_contour and contour_polygon:
            # Clip the geometry to the "図郭" polygon
            geometry_to_plot = row.geometry.intersection(contour_polygon)

        if not is_contour:
            land_number = row.get("地番")
            if land_number and not geometry_to_plot.is_empty:
                # Draw land number text on the center of the clipped polygon
                centroid = geometry_to_plot.centroid
                ax.text(
                    centroid.x,
                    centroid.y,
                    str(land_number),
                    fontsize=6,
                    ha="center",
                    va="center",
                    color="black",
                )

        if not geometry_to_plot.is_empty:
            gpd.GeoSeries([geometry_to_plot]).plot(
                ax=ax,
                facecolor=facecolor,
                edgecolor=edgecolor,
                linewidth=linewidth,
                alpha=alpha,
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

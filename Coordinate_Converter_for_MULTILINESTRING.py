#-------------------------------------------------------------------------------
# Name:        module5
# Purpose:
#
# Author:      MohammadalizadehkorM
#
# Created:     29/03/2024
# Copyright:   (c) MohammadalizadehkorM 2024
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import csv
import shapefile
import pyproj

# Set the input CSV file
input_csv = r"C:\Users\MohammadalizadehkorM\Downloads\TRANSPORTATION_urban_trails_network_20240329.csv"

# Set the name for the output shapefile (without extension)
output_shapefile = r"C:\Users\MohammadalizadehkorM\Downloads\New folder\output_shapefile"

# Function to parse MULTILINESTRING string into individual coordinate pairs
def parse_multilinestring(multilinestring_str):
    # Remove "MULTILINESTRING ((" from the beginning and "))" from the end
    multilinestring_str = multilinestring_str.replace("MULTILINESTRING ((", "").replace("))", "")
    # Split the string by ", " to get individual coordinate pairs
    coordinate_pairs = multilinestring_str.split(", ")
    # Remove any leading or trailing characters like parentheses from the coordinate pairs
    coordinate_pairs = [coord.strip("()") for coord in coordinate_pairs]
    # Split each coordinate pair into longitude and latitude
    coordinates = [[float(coord.split()[0]), float(coord.split()[1])] for coord in coordinate_pairs]
    return coordinates

try:
    # Create a new shapefile writer
    with shapefile.Writer(output_shapefile, shapeType=shapefile.POLYLINE) as shp_writer:
        # Create fields in the shapefile for other attributes
        with open(input_csv, 'r', newline='') as csvfile:
            csvreader = csv.DictReader(csvfile)
            # Create fields in the shapefile based on the CSV header
            for field in csvreader.fieldnames:
                shp_writer.field(field, "C")  # Assuming all fields are of string type

            # Iterate through each row in the input CSV file
            for row in csvreader:
                # Get the MULTILINESTRING data from the "the_geom" column
                multilinestring_str = row['the_geom']
                # Parse the MULTILINESTRING string into individual coordinate pairs
                coordinates = parse_multilinestring(multilinestring_str)

                # Project coordinates to EPSG:2277 (NAD83 / California Zone 3)
                transformer = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:2277", always_xy=True)
                projected_coordinates = [transformer.transform(lon, lat) for lon, lat in coordinates]

                # Add the polyline shape to the shapefile
                shp_writer.line([projected_coordinates])
                # Add attributes to the shapefile for each polyline
                shp_writer.record(**row)

    print("Shapefile creation completed successfully.")

except Exception as e:
    print(e)

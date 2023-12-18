# note: gsi area shapefile and airports data csv file should be with us to run this code

import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import numpy as np
from matplotlib_scalebar.scalebar import ScaleBar
import math
import warnings
warnings.filterwarnings("ignore")
plt.style.use("bmh")
# Load and convert Block-13 GeoDataFrame to the target CRS
shapefile = input("Type your shapefile name with extenstion(.shp) : ")
gdf = gpd.read_file(shapefile)
target_crs = "EPSG:4326"
gdf = gdf.to_crs(target_crs)

# Plot Block-13 GeoDataFrame
fig, ax = plt.subplots(figsize=(8, 8))
gdf.plot(edgecolor="black", color="None", ax=ax)
gdf.geometry.bounds
title = input("Enter your block/area title name:" )  
plt.ylim([int(gdf.geometry.bounds["miny"]),math.ceil(float(gdf.geometry.bounds["maxy"]))])    
plt.xlim([int(gdf.geometry.bounds["minx"]),math.ceil(float(gdf.geometry.bounds["maxx"]))])
plt.title(title, color="black", size=15)

# Read places GeoDataFrame from CSV and create Point geometries
airports = input("Enter your airport csv file with extension(.csv): ")
gdf_airports = gpd.read_file(airports)
geometry_airports = [Point(xy) for xy in zip(gdf_airports["Longitude"], gdf_airports["Latitude"])]
gdf_airports["geometry"] = geometry_airports


# Plot places GeoDataFrame
gdf_airports.plot(ax=ax, color="red", markersize=50)

# Annotate each point with its name
for idx, row in gdf_airports.iterrows():
    ax.annotate(row["Name"], xy=(row["geometry"].x, row["geometry"].y), xytext=(-21, -12),
                textcoords="offset points", color="black", size=8, ha="center")

# Set y-axis ticks interval to 0.50
r1 = np.arange((int(gdf.geometry.bounds["miny"])),(math.ceil(float(gdf.geometry.bounds["maxy"]))+0.5),0.5)
plt.yticks(r1)

# Adjust x-axis ticks
r2 = np.arange((int(gdf.geometry.bounds["minx"])),(math.ceil(float(gdf.geometry.bounds["maxx"]))+0.5),0.5)
#r = np.arange(70.00, 75.01, 0.50)  # Ensure the range matches the x-axis limits
plt.xticks(r2)

# Add scale bar at the bottom center of the map
scalebar = ScaleBar(1, location='lower right', units='km', length_fraction=0.15, scale_loc='bottom')
ax.add_artist(scalebar)

#add North arrow to the upper right side of the map
ax.text(0.98, 0.97, '↑', transform=ax.transAxes, fontsize=20, ha='center', va='center', color='black', rotation=0)
saving_file_name = input("Enter the Name of your saving file: ")
plt.savefig(saving_file_name+".png", dpi=300)
plt.show()

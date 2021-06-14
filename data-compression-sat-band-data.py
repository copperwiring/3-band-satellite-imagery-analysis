'''
In the script we will compress a data (TIF) file Read sample data (TIF) file.
Raster datasets use **compression** to reduce filesize. There are a number of compression methods, all of which fall into two categories: lossy and lossless. 
1. Lossless compression methods retain the original values in each pixel of the raster, while 
2. Lossy methods result in some values being removed. 
Because of this, lossy compression is generally not well-suited for analytic purposes, but can be very useful for reducing storage size of visual imagery.

The data we use are from PlanetLabs (details below) and are available as GeoTIFFs using lossless LZW compression. 
By creating a lossy-compressed copy of a visual asset, we can significantly reduce the dataset's filesize. In this example, we will create a copy using the "JPEG" lossy compression method

Images Used:
The images which is provided here are from Planet Labs and are at 3m resolution i.e. each pixel represents 3m on the surface of the earth.
These images will have band assets a.)Red b.)Green c.) Blue and d.)Near-Infrared.

Source file used in the code can be downloaded from the link below:
Link: https://drive.google.com/drive/folders/1zbZVT07RjATmcmBEMEWsEWqLhxDvX_3E?usp=sharing

Note: To open and visualize .TIF files, you can use QGIS and open it as a raster.

'''
import rasterio
import os
from humanize import naturalsize as sz

# Loading a 3 Band dataset
# Extracting metadata information from a satellite image
# User rasterio to open a 3-band (red, green, blue) visual asset

satdat = rasterio.open("20160831_180302_0e26_3B_Visual.tif")

# Minimum bounding box in projected units
print("Bounding Box: ", satdat.bounds)

# Get dimensions, in map units (using the example GeoTIFF, that's meters)
# To understand more about map units, see link below: 
# Link: http://www.geo.hunter.cuny.edu/~jochen/gtech201/lectures/lec6concepts/08%20-%20Understanding%20map%20units%20and%20display%20units.html 
width_in_projected_units = satdat.bounds.right - satdat.bounds.left
height_in_projected_units = satdat.bounds.top - satdat.bounds.bottom
print("Image Width: {}, Height: {}".format(width_in_projected_units, height_in_projected_units))

# Number of rows and columns.
print("Image Rows: {}, Columns: {}".format(satdat.height, satdat.width))

# This dataset's projection uses meters as distance units.  What are the dimensions of a single pixel in meters?
xres = (satdat.bounds.right - satdat.bounds.left) / satdat.width
yres = (satdat.bounds.top - satdat.bounds.bottom) / satdat.height

print(xres, yres)
print("Are the pixels square: {}".format(xres == yres))

# Get coordinate reference system
# we can find CRS info also from https://www.spatialreference.org/
print("Coordinate Reference System" , satdat.crs)

# Convert pixel coordinates to world coordinates
# Note rasterio can do this since it knows the CRS cooridnate and hence will use that information 
# to convert from pixel cooridnate to world coordinates
# Upper left pixel
row_min = 0
col_min = 0

# Lower right pixel.  Rows and columns are zero indexing.
row_max = satdat.height - 1
col_max = satdat.width - 1

# Transform coordinates with the dataset's affine transformation.
topleft = satdat.transform * (row_min, col_min)
botright = satdat.transform * (row_max, col_max)

# Note the results will be in metre coordinates (UTM)
print("In UTM, Top left corner coordinates: {}".format(topleft))
print("In UTM, Bottom right corner coordinates: {}".format(botright))

# All of the metadata required to create an image of the same dimensions, datatype, format, etc. 
# is stored in the dataset's profile:
print("Metadata of the Satellite data: ",satdat.profile)

# File Compression
# Returns size in bytes
size = os.path.getsize("20160831_180302_0e26_3B_Visual.tif")

# output a human-friendly size
print("Human readable size: before compression: ", sz(size))

# Copying a dataset
#----------------------------------------------------------------------------
# Read all bands from source dataset into a single 3-dimensional ndarray
data = satdat.read()

# Write new file using profile metadata from original dataset and specifying JPEG compression
profile = satdat.profile
profile['compress'] = 'JPEG'

with rasterio.open('compressed.tif', 'w', **profile) as dst:
    dst.write(data)

# Lossy compression results
new_size = os.path.getsize("compressed.tif")
print("Human readable size: after compression:  ", sz(new_size))

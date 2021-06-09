# Read sample data (TIF) file 

# The images which is provided here are from Planet Labs and are at 3m resolution i.e. each pixel represents 3m onthe surface of the earth.
# Here we will have band assets a.)Red b.)Green c.) Blue and d.)Near-Infrared

# Reading satellite data with rasterio
# Loading a 4 Band dataset

import rasterio


# Loading a 3 Band dataset
# Extracting metadata information from a satellite image
# User rasterio to open a 3-band (red, green, blue) visual asset

satdat = rasterio.open("20160831_180302_0e26_3B_Visual.tif")

# Minimum bounding box in projected units

print(satdat.bounds)

# Get dimensions, in map units (using the example GeoTIFF, that's meters)

width_in_projected_units = satdat.bounds.right - satdat.bounds.left
height_in_projected_units = satdat.bounds.top - satdat.bounds.bottom

print("Width: {}, Height: {}".format(width_in_projected_units, height_in_projected_units))

# Number of rows and columns.

print("Rows: {}, Columns: {}".format(satdat.height, satdat.width))

# This dataset's projection uses meters as distance units.  What are the dimensions of a single pixel in meters?

xres = (satdat.bounds.right - satdat.bounds.left) / satdat.width
yres = (satdat.bounds.top - satdat.bounds.bottom) / satdat.height

print(xres, yres)
print("Are the pixels square: {}".format(xres == yres))

# Get coordinate reference system
# we can find CRS info also from https://www.spatialreference.org/

satdat.crs

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

# Noe the results will be in metre coordinates (UTM)
print("Top left corner coordinates: {}".format(topleft))
print("Bottom right corner coordinates: {}".format(botright))

# All of the metadata required to create an image of the same dimensions, datatype, format, etc. 
# is stored in the dataset's profile:

print(satdat.profile)

# File Compression
# Raster datasets use **compression** to reduce filesize. There are a number of compression methods, all of which fall into two categories: lossy and lossless. _Lossless_ compression methods retain the original values in each pixel of the raster, while _lossy_ methods result in some values being removed. Because of this, lossy compression is generally not well-suited for analytic purposes, but can be very useful for reducing storage size of visual imagery.
# All Planet data products are available as GeoTIFFs using lossless LZW compression. 
# # By creating a lossy-compressed copy of a visual asset, we can significantly reduce the dataset's filesize. In this example, we will create a copy using the "JPEG" lossy compression method

import os
from humanize import naturalsize as sz

# returns size in bytes
size = os.path.getsize("20160831_180302_0e26_3B_Visual.tif")

# output a human-friendly size
print(sz(size))

# Copying a dataset

# read all bands from source dataset into a single 3-dimensional ndarray
data = satdat.read()

# write new file using profile metadata from original dataset
# and specifying JPEG compression

profile = satdat.profile
profile['compress'] = 'JPEG'

with rasterio.open('compressed.tif', 'w', **profile) as dst:
    dst.write(data)

# Lossy compression results

new_size = os.path.getsize("compressed.tif")
print(sz(new_size))

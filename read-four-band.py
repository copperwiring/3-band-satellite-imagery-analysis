'''
This script helps in unerstanding the basic structure of satellite image. 
It reads a 4 band data and describes various properties of the band:
1. Number of bands
2. Datatype of the file
3. Datatype of each band
4. Width ad Height of the satellite data/image

Source file used in the code can be downloaded from the link below:
Link: https://drive.google.com/drive/folders/1zbZVT07RjATmcmBEMEWsEWqLhxDvX_3E?usp=sharing
'''

import rasterio

# This cell explores a single 4 band (blue, green, red, NIR)
image_file = "20190321_174348_0f1a_3B_AnalyticMS.tif"

satdat = rasterio.open(image_file)

# satdat is now a open dataset object
print("Satellite Data data type: ", satdat)

# let's look at some basic information about this geoTIFF:
# 1. Dataset name
print("Satellite dataset name: ", satdat.name)

# 2. Number of bands in this dataset
print("Numbers of bands in satellite", satdat.count)

# Parsing bands:
# Sequence of band indexes.These are one indexing, not zero indexing like Numpy arrays.
print("Sequence of bands in satellites", satdat.indexes)

blue, green, red, nir = satdat.read()

# Or read the entire dataset into a single 3D array:
#    data = satdat.read()
# each band is stored as a numpy array, and its values are a numpy data type
print("Datatype of each band of satellite data: ", blue.dtype)

# using the blue band as an example, examine the width & height of the image (in pixels)

w = blue.shape[0]
h = blue.shape[1]

print("For the image, in pixels, width: {w}, height: {h}".format(w=w, h=h))
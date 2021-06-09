import rasterio

# This cell explores a single 4 band (blue, green, red, NIR)
image_file = "20190321_174348_0f1a_3B_AnalyticMS.tif"

satdat = rasterio.open(image_file)

# satdat is now a open dataset object
print(satdat)

# let's look at some basic information about this geoTIFF:
# dataset name
print(satdat.name)

# number of bands in this dataset
print(satdat.count)

# Parsing bands

# Squence of band indexes.These are one indexing, not zero indexing like Numpy arrays.
print(satdat.indexes)

blue, green, red, nir = satdat.read()

# Or read the entire dataset into a single 3D array:
#    data = satdat.read()

# each band is stored as a numpy array, and its values are a numpy data type
print(blue.dtype)

# using the blue band as an example, examine the width & height of the image (in pixels)

w = blue.shape[0]
h = blue.shape[1]

print("width: {w}, height: {h}".format(w=w, h=h))
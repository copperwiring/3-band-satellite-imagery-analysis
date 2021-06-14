'''
In this script we're going to clip a fullsized PlanetScope dataset to an area of interest (AOI) polygon. 
Because this AOI is a vector dataset (versus raster), we'll use Rasterio's sister-library, Fiona, to read the geoJSON dataset.
Read more about Fiona here: https://fiona.readthedocs.io/en/latest/manual.html 

Hence, we will do the following steps:
1. Read the image file/raster.
2. Use a mask to cut raster along boundary and use fiona to open our AOI GeoJSON.
   Note, we be using GeoJSON which is for vector data because it has boundaries of polygon in it. Fiona is counterpart of raster but in vector data.
3. Clip our original raster to the boundary defined by the AOI, we'll use rasterio's mask function. 
   This will create a copy of our original dataset, with all pixels outside of the input AOI shape set to no data value/null value.
4. Update the meta data from our original raster dataset. Hence, we can write a new geoTIFF containing the new, clipped raster data using the metadata from our original mosaic.
5. Write the new data into a new GeoTIFF file.
6. Reproject the new rasterio. Here we will project into EPSG 4326. In order to translate pixel coordinates in a raster dataset into coordinates that use a spatial reference system, an affine transformation must be applied to the dataset. This transform is a matrix used to translate rows and columns of pixels into (x,y) spatial coordinate pairs. Every spatially referenced raster dataset has an affine transform that describes its pixel-to-map-coordinate transformation. This can be calculated directly using `calculate_default_transform` fucntion.
7. Use the transformation to update the meta data which can finally be used to generate a new GeoTIFF file

'''

import rasterio
from rasterio.mask import mask
from matplotlib import pyplot as plt
from rasterio.warp import calculate_default_transform, reproject
import fiona

# Read TIFF file
image_file = "20190321_174348_0f1a_3B_AnalyticMS.tif"

# Use Rasterio to open the image.
satdat = rasterio.open(image_file)

# use fiona to open our AOI GeoJSON
with fiona.open('aoi.geojson') as f:
    aoi = [feature["geometry"] for feature in f]    
    
    
# -----------------------------------------------------------------------------------
# Clip the raster

# Apply mask with crop=True to crop the resulting raster to the AOI's bounding box
with rasterio.open(image_file) as img:
    clipped, transform = mask(img, aoi, crop=True)
    
print("Size of the new clipped image: ", clipped.shape)

# Use the metadata from our original mosaic
meta = img.meta.copy()

# Update metadata with new, clipped mosaic's boundaries
meta.update({"transform": transform,
    "height":clipped.shape[1],
    "width":clipped.shape[2]})

# Write the clipped-and-cropped dataset to a new GeoTIFF
with rasterio.open('clipped.tif', 'w', **meta) as dst:
    dst.write(clipped)

clipped_img = rasterio.open("clipped.tif")

#---------------------------------------------------------------------------------------
# Reprojecting with rasterio

# Now let's reproject our clipped dataset: for this example, we'll reproject into EPSG 4326
from rasterio.warp import calculate_default_transform, reproject

# Define our target CRS - rasterio will accept any CRS that can be defined using WKT
target_crs = 'EPSG:4326'

# In order to reproject a raster dataset from one coordinate reference system to another, rasterio uses the transform of the dataset: this can be calculated automatically using rasterio's calculate_default_transform method:
# Calculate a transform and new dimensions using our dataset's current CRS and dimensions
transform, width, height = calculate_default_transform(clipped_img.crs, 
                                                      target_crs, 
                                                       clipped_img.width, 
                                                       clipped_img.height, 
                                                       *clipped_img.bounds)


# Using a copy of the metadata from the clipped raster dataset and the transform we defined above, 
# we can write a new geoTIFF containing the reprojected and clipped raster data:
# Copy the metadata from the clipped dataset
metadata = clipped_img.meta.copy()

# Change the CRS, transform, and dimensions in metadata to match our desired output dataset
metadata.update({'crs':target_crs, 
                'transform':transform,
                'width':width,
                'height':height})


# Apply the transform & metadata to perform the reprojection
# Here we're saving the output to a new 'clipped_4326.tif' file
with rasterio.open('clipped_4326.tif', 'w', **metadata) as reprojected:
    for band in range(1, clipped_img.count + 1):
        reproject(
            source=rasterio.band(clipped_img, band),
            destination=rasterio.band(reprojected, band),
            src_transform=clipped_img.transform,
            src_crs=clipped_img.crs,
            dst_transform=transform,
            dst_crs=target_crs
        )

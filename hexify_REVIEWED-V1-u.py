#Import Modules
from __future__ import print_function
import os, sys, datetime, math, arcpy
from mod_messages import *
from mod_geo import add_data_to_map
from arcMsg import display



tool_info  = '''
==============================================================================================
Classification: UNCLASSIFIED
Name: Hexify (Hexagon Fishnet)
Script: hexify.py
Author: ###COMMENT REMOVED
Date: August 2015
Updated: N/A
Version: 1.0 (previous versions developed for ###COMMENT REMOVED)

Description:
Hex the World! Take an input featureclass or layer and generate a featureclass containing hexagonal polygons. Statistics about the input featureclass are then calculated for each hexagon and included in the hexagon featureclass.

INPUTS:
- Input Feature Class:  This is the input featureclass (or featurelayer)containing the features (or features selected) which are to be analyzed.
- Group by:  The analysis will be repeated for each value found within the Group_by field. Note that the number of unique values which the data can be grouped into is limited to 12 to prevent excessive computation time.
- Hexagon Area:  The area of the hexagons in square kilometers(1 km2 = 100 ha, 1 km2 = 1 000 000 m2). If this value is not provided the width and then height parameters will be checked. If none of these parameters is
                 provided the hexagon size will be automatically determined such that the extent of the input featureclass or featurelayer will be covered by approximately 1000 hexagons.
- Hexagon Width:  The width of the hexagons in kilometers. This value will only be used if the hexagon area is not provided. If this value is not provided the height parameters will be checked. If none of these
                  parameters is provided the hexagon size will be automatically determined such that the extent of the input featureclass or featurelayer will be covered by approximately 1000 hexagons.
- Hexagon Height:  The height of the hexagons in kilometers. This value will only be used if the hexagon area and hexagon width are not provided. If this value is also not provided the hexagon size will be automatically
                   determined such that the extent of the input featureclass or featurelayer will be covered by approximately 1000 hexagons.

                
OUTPUTS:
- Output Feature class:  This will be the resulting featureclass that contains hexagon polygons. The results of the analysis will be attributes of the hexagon polygons.
  
Notes:
- Original code adapted for inclusion in the AAT-C OPIR Toolbox v1.6
- This tool replaces the OPIR Hex Detections tool which basically did the same thing.  This tool is streamlined for large data inputs and outputs and offers more users parameters.

Updates:
- N/A

==============================================================================================
'''

# hexify.py
# Version: 1.3
# Author: ###COMMENT REMOVED
# Section: ###COMMENT REMOVED
#          ###COMMENT REMOVED
# Create date: July 2015
# Purpose: Take an input featureclass or layer and generate an in memory
#          featureclass containing hexagonal polygons. Statistics about the
#          input featureclass are then calculated for each hexagon and
#          included in the hexagon featureclass.
# Python version: 2.7.2
# Classification: UNCLASSIFIED
# Maintained: Yes - ###COMMMENT REMOVED
# Requires: arcpy     (ArcMap library)
#           arcMsg.py (custom python functions)
# Notes:
# Note the functions within this can be imported to other standalone Python
# scripts and used. The mainline is designed to be used as an ArcMap tool.

# Version 1.3 08-07-2015
# Bug identified in generate_hex_bin_fc when the describe object doesn't
# have a FIDSet attribute. This occurs when not operating on a FeatureLayer
# therefore there can't be any selection.

# Version 1.2 03-07-2015
# - Removed nestered cursors when performing stats per hexagon to improve
#   performance, hexagon geometry objects are now read into memory

# Version 1.1 02-07-2015
# - The extent of the features in the input featureclass is now only
#   checked when there is a selection on the input featureclass
# - The input features are no longer read into memory when performing
#   stats per hexagon, this is now done using nestered cursors
# - Included a check to make sure that when performing the stats per
#   hexagon that the geometry object returned is not None (this can occur
# if the geometry is build poorly

# Version 1.0 - Initial Release

def generate_hex_bins_fc(input_fc, clip_type = 'INTERSECT',
                         hex_area_km2 = None, hex_width_km = None,
                         hex_height_km = None, smart_limit = True):
    # Returns a feature class (in the same projection) containing hexagons of
    # the desired area to cover the extent of input_fc. Note that a reference
    # point is used to ensure hexagons fall at the same location (if they are
    # the same size) regardless of the extent of the dataset.
    #
    # input_fc       - Controls the extent of the ouput hexagon featureclass
    #
    # clip_type      - NONE:      The hexagon featureclass will not be clipped
    #                             and will cover the extent of the input
    #                             features
    #                  INTERSECT: The hexagon featureclass will be clipped such
    #                             that only hexagons which intersect an input
    #                             feature will be present (Default).
    #                  MIN_BBOX:  A minimum bounding geometry will be used to
    #                             bound the hexagons. NOTE: This requires an
    #                             Advanced Desktop License.
    #
    # hex_area_km2   - The area of the hexagons in square kilometers
    #                  (1 km2 = 100 ha, 1 km2 = 1 000 000 m2)
    # hex_width_km   - The width of the hexagons in kilometers
    # hex_height_km  - The height of the hexagons in kilometers
    #
    # NB: Only one of these three variables needs to be specified. These are
    # listed in preference order, subsequent ones will be ignored. If all three
    # are None (default), the area of the hexagons will be determined such that
    # approximately 1000 hexagons will cover the extent of the input
    # featureclass. In addition, due to variations between projection, the area
    # is usually most accurate parameter to specify.
    #
    # smart_limit    - If True (default) it will prevent the creation of more
    #                  than 100 000 hexagons by increasing the hexagon size.
    #                  False will allow the user to override this check and
    #                  create hexagons of the desired size, acknowledging that
    #                  there may be excessive processing time.
    #
    # Requires: arcpy
    # ###COMMENT REMOVED
    # Version 2.2 - July 2015
    
    # Display a subtitle message
    print('Generating Hexagon Featureclass')
    
    # Validate the input featureclass
    if not arcpy.Exists(input_fc):
        # Display an error and terminate the execution
        print('Input featureclass doesn\'t exist\n{}'.format(input_fc))
    
    # Validate the input clip type
    clip_type = clip_type.upper()
    if clip_type not in ('NONE', 'INTERSECT', 'MIN_BBOX'):
        clip_type = 'INTERSECT'
    
    # Check if an advanced license is required
    if clip_type == 'MIN_BBOX':
        # Make sure that an advanced license has been set
        if arcpy.ProductInfo() != u'ArcInfo':
            # License not available, perform intersect
            print('Advanced license not set, \
                     performing INTERSECT not MIN_BBOX')
            clip_type = 'INTERSECT'
    
    # Allow the function to overwrite existing in memory featureclasses
    init_arcpy_overwrite = arcpy.env.overwriteOutput
    arcpy.env.overwriteOutput = True
    
    # Define a function for the determining the corners of a hexagon using the
    # centre point and the side length
    def hex_corners(centre, sl, hsl, hh):
        # From the centre point and the side length of the hexagon, return the
        # corner points. Corners start from the bottom left and go clockwise
        x,y = centre
        corners =  ((x - hsl, y - hh),
                    (x - sl , y     ),
                    (x - hsl, y + hh),
                    (x + hsl, y + hh),
                    (x + sl , y     ),
                    (x + hsl, y - hh))
        return corners
    
    # reference point so hexagons occur at the same location (for each size)
    ref_point = (0,0)
    # Determine the threshold for 'too many hexagons' if smart_limit is True
    hex_count_ideal = 1000      # Approximations due to the overlap of the 
    hex_count_limit = 100000    # hexagons over the edge of the extent
    
    # Generate the hexagon bin featureclass using a World Mercator projection
    mercator = arcpy.SpatialReference(3395)
    wgs_84 = arcpy.SpatialReference(4326)
    # 3395 WGS_1984_World_Mercator
    # 54030 World Robinson
    # 54034 World_Cylindrical_Equal_Area
    # 32662 WGS_1984_Plate_Carree
    # UTM projections would be a better solution, but much too complicated!
    
    # Determine the extent of the input featureclass and its projection
    desc = arcpy.Describe(input_fc)
    in_sr = desc.spatialreference
    if in_sr.name == u'Unknown':
        print('The Input featureclass doesn\'t have a spatial reference')
    
    # Determine the extent polygon
    # NB: The extent object of desc can by used to describe the extent of the
    # whole featureclass or featurelayer. However, if there is a selection of
    # a featurelayer, it will not reflect the extent of the selection.
    
    # Try and see if desc has FIDSet, if so there could be a selection
    try:
        fidset = desc.FIDSet
    except:
        # desc doesn't have FIDSet, therefore there can't be a selection
        fidset = u''
    
    # Test to see if fidset is an empty (unicode) string
    if fidset == u'':
        # Then there is no selection, use the describe object
        print('Determining the extent of the featureclass')
        extent = desc.extent
        extent_poly = arcpy.Polygon(arcpy.Array([extent.lowerLeft,
                                                 extent.upperLeft,
                                                 extent.upperRight,
                                                 extent.lowerRight,
                                                 extent.lowerLeft]),
                                    extent.spatialReference)
    else:
        # Some of the features have been selected, determine the extent using
        # a cursor object on the input featureclass or featurelayer
        print('Determining the extent of the selected features')
        with arcpy.da.SearchCursor(input_fc, ['SHAPE@']) as cur:
            
            # Initialise the bounds with the first feature's bounds
            try:
                # Use the cursor to access the first feature
                feature_extent = cur.next()[0].extent
                # Initialise the bounds
                xmin = feature_extent.XMin
                xmax = feature_extent.XMax
                ymin = feature_extent.YMin
                ymax = feature_extent.YMax
            
            except:
                # There are no features display error and terminate
                print('Input featureclass contains no features')
            
            # Iterate through each feature
            for row in cur:
                
                # Determine if the extent of the feature is outside the
                # current extent bounds
                feature_extent = row[0].extent
                if feature_extent.XMin < xmin: xmin = feature_extent.XMin
                if feature_extent.XMax > xmax: xmax = feature_extent.XMax
                if feature_extent.YMin < ymin: ymin = feature_extent.YMin
                if feature_extent.YMax > ymax: ymax = feature_extent.YMax
                
        # Construct a polygon of the extent (with a spatial reference)
        extent_poly = arcpy.Polygon(arcpy.Array([arcpy.Point(xmin, ymin),
                                                 arcpy.Point(xmax, ymin),
                                                 arcpy.Point(xmax, ymax),
                                                 arcpy.Point(xmin, ymax),
                                                 arcpy.Point(xmin, ymin)]),
                                    feature_extent.spatialReference)
    
    # Validate the extent
    extent_poly_wgs84 = extent_poly.projectAs(wgs_84)
    # Ckeck that nothing strange is going on with the extent
    if extent_poly_wgs84.pointCount != 5    or \
       extent_poly_wgs84.extent.XMin < -180 or \
       extent_poly_wgs84.extent.XMax >  180 or \
       extent_poly_wgs84.extent.YMin <  -90 or \
       extent_poly_wgs84.extent.YMax >   90:

       # Then there is something odd about the extent of the featureclass
        print('The input Featureclass has a bad projection or extents')
    
    # Reproject the extent polygon to Mercator
    extent_wm = extent_poly.projectAs(mercator)
    # Determine the extent area in hectares
    extent_area = extent_wm.area
    
    # Determine the hexagons' side length (in m) and area (in m^2)
    # Make sure the values passed in are resonable
    try:
        # Check if the user entered a numeric area
        hex_area = float(hex_area_km2) * 1000000
        # Calculate the side length parameter
        side_length = (0.3849001794597505 * hex_area) ** 0.5
        # Check the value, if it's bad trigger the except
        if side_length <= 0: raise IOError
        
    except:
        # hex_area_km2 is None or bad user input
        
        try:
            # Check if the user entered a numeric width
            width = float(hex_width_km) * 1000
            # Calculate the three paramters
            side_length = width / 2.0
            # Check the value, if it's bad trigger the except
            if side_length <= 0: raise IOError
        
        except:
            # hex_width_km is None or bad user input
            
            try:
                # Check if the user entered a numeric height
                height = float(hex_height_km) * 1000
                # Calculate the three parameters
                side_length = 0.5773502691896258 * height
                # Check the value, if it's bad trigger the except
                if side_length <= 0: raise IOError
            
            except:
                # No valid size input or all None
                hex_area = extent_area // hex_count_ideal
                side_length = (0.3849001794597505 * hex_area) ** 0.5
                # Turn off the smart limit
                smart_limit = False
    
    # Determine the hexagon area from the side length
    hex_area = 2.598076211353316 * side_length ** 2
    
    # Check that the user hasn't specified something very time consuming
    # without knowing it
    if smart_limit:
        # Check the number of hexagons to be generated
        
        if extent_area / hex_area > hex_count_limit:
            # There are too many hexagons, limit it
            print('Number of hexagons too large, overriding user input')
            hex_area = extent_area // hex_count_limit
            side_length = (0.3849001794597505 * hex_area) ** 0.5
    
    # Determine the parameters of the hexagons from the side length
    height = 1.7320508075688772 * side_length
    width = 2.0 * side_length
    # Determine additional parameters to speed up processing
    side_length_half = side_length / 2.0
    height_half = height / 2.0
    hori_cc_double = width + side_length
    hori_cc = hori_cc_double / 2.0 # Horizontal centre to centre distance
    # Determine the hexagon area in km2 (rounded)
    hex_area_actual_km2 = int(hex_area) // 1000000
    
    # Determine the difference between the reference point and the extent
    print('Determining location of bottom left hexagon')
    dx = extent_wm.extent.XMin - ref_point[0]
    # Determine the number of horizontal hexagons to move
    # Note: // rounds to -ve infinity which is very much desired!
    x_steps = dx // hori_cc
    
    # Translate the starting point horizontally
    start_x = ref_point[0] + x_steps * hori_cc
    
    # Check if the horizontal starting point can be shifted inside the extent
    if start_x + side_length < extent_wm.extent.XMin:
        # Put the centre point inside the extent
        start_x += hori_cc
        # Take one more or one less step (not actually important which)
        x_steps += 1 * cmp(dx)
    
    # Make start_y the same as the Y value of the reference point
    start_y = ref_point[1]
    
    # Check if the horizontal translation has affected the vertical position.
    # If the number of x steps is odd, shift the vertical position up by half
    # a hexagon
    if not x_steps % 2:
        # An ODD number of vertical steps were taken
        # Alter the start_y away from the reference point
        start_y += height_half
    
    # Determine the difference between the reference point and the extent
    dy = extent_wm.extent.YMin - start_y
    
    # Translate the starting point vertically
    # Note: // rounds to -ve infinity which is very much desired!
    start_y += (dy // height) * height
    
    # Generate the hex bins and write them into hex_fc_full
    centre_pt = [start_x, start_y]
    
    # Set the starting hexagon to be a left row
    row_left = True
    
    # Check to see if the first left row can be skipped
    if start_y + height_half < extent_wm.extent.YMin:
        # Adjust to the first right row
        centre_pt[0] += hori_cc
        centre_pt[1] += height_half
        row_left = False
    
    # Determine the vertical and horizontal limits to make sure the extent is
    # covered. Note: The vertical limit is determined for a 'down' hexagon
    lim_y = extent_wm.extent.YMax + height_half
    lim_x = extent_wm.extent.XMax + side_length
    
    # Create an in_memory featureclass to contain the hexagon features
    print('Generating empty virtual featureclass')
    hex_fc_full_name = 'hex_{}km2_full'.format(hex_area_actual_km2)
    hex_fc_full = arcpy.CreateFeatureclass_management('in_memory',
                                                       hex_fc_full_name,
                                                       'POLYGON',
                                                       '', '', '',
                                                       in_sr).getOutput(0)
    
    # Open an insert cursor to populate the featureclass
    print('Generating hexagons')
    with arcpy.da.InsertCursor(hex_fc_full,['SHAPE@']) as cur:
        
        # Create a 'row' of hexagons
        while centre_pt[1] <= lim_y:
            
            # Create a row of polygons for each horizontal step necessary
            while centre_pt[0] < lim_x:
                
                # Determine the corners of this hexagon
                boundary_pts = hex_corners(centre_pt, side_length,
                                           side_length_half, height_half)
                hex_boundary = [arcpy.Point(*pt) for pt in boundary_pts]
                # Append the first point to close the polygon
                hex_boundary.append(hex_boundary[0])
                
                # Create the hexagon polygon (in mercator)
                hex_poly = arcpy.Polygon(arcpy.Array(hex_boundary), mercator)
                
                # Insert it into the featureclass with the desired projection
                cur.insertRow([hex_poly.projectAs(in_sr)])
                
                # Move across to the next hexagon
                centre_pt[0] += hori_cc_double
            
            # The 'row' has been complete, prepare the next row
            row_left = not row_left
            # Reset the horizontal position
            if row_left:
                # Set up for a left row
                centre_pt[0] = start_x
            else:
                # Set up for a right row
                centre_pt[0] = start_x + hori_cc
            # Move up to the next row
            centre_pt[1] += height_half
    
    # Set the full hexagon featureclass as the output
    output_fc = hex_fc_full
    
    # If the user desires it, remove unnecessary hexagons
    if clip_type != 'NONE':
        # Remove (clip) unnecessary hexagons
        print('Clipping hexagons to features')
        
        # Create some feature layers to intersect
        arcpy.MakeFeatureLayer_management(input_fc, 'input_lyr')
        arcpy.MakeFeatureLayer_management(hex_fc_full, 'hex_lyr')
        
        if clip_type == 'INTERSECT':
        
            # Intersect the layers and select the hexagons which intersect the
            # features in input_fc
            arcpy.SelectLayerByLocation_management('hex_lyr',
                                                   'intersect',
                                                   'input_lyr')
        
        elif clip_type == 'MIN_BBOX':
            
            # Generate a minimum bounding box feature to for the selection
            min_bbox_fc = 'in_memory\\min_bbox'
            arcpy.MinimumBoundingGeometry_management('input_lyr',
                                                     min_bbox_fc,
                                                     'CONVEX_HULL',
                                                     'ALL')
            
            # Make it a featurelayer
            arcpy.MakeFeatureLayer_management(min_bbox_fc, 'min_bbox_lyr')
            
            # Select the hexagons which intersect this layer
            arcpy.SelectLayerByLocation_management('hex_lyr',
                                                   'intersect',
                                                   'min_bbox_lyr')
            
            # Delete min_bbox_fc and min_bbox_lyr
            arcpy.Delete_management(min_bbox_fc)
            arcpy.Delete_management('min_bbox_lyr')
        
        # Delete the input_lyr from memory
        arcpy.Delete_management('input_lyr')
        
        # Copy the selected features into a new in_memory featureclass
        hex_fc_clip = 'in_memory\\hex_{}km2_clip'.format(hex_area_actual_km2)
        arcpy.CopyFeatures_management('hex_lyr', hex_fc_clip)
        
        # Remove hex_lyr from memory
        arcpy.Delete_management('hex_lyr')
        
        # Remove the full hexagon featureclass from memory
        arcpy.Delete_management(hex_fc_full)
        
        # Change output_fc to the clipped featureclass and remove the full one
        output_fc = hex_fc_clip
    
    # Reset the overwrite status back to what it was
    arcpy.env.overwriteOutput = init_arcpy_overwrite
    
    return output_fc

def features_per_hexagons(input_fc, hexagon_fc, field_base = ''):
    # This will count how many features intersect each hexagon. The results are
    # returned within a tuple containing 3 items.
    #   1. A field name
    #   2. A field type
    #   3. A dictionary with the key being the object ID of the feature in
    #      hexagon_fc and the value being the count for this feature.
    # Any features which fall on or across the boundary between hexagons will
    # be considered to fall in both hexagons.
    #
    # input_fc       - The input featureclass which is the hexagons are
    #                  overlayed. Can be points, lines or polygons
    #
    # hexagon_fc     - The hexagon featureclass which is used to group the
    #                  points into spatial areas.
    # Note that hexagon_fc must be a polygon featureclass, but the analysis
    # will work with any shape polygons
    #
    # field_base     - This is the base name of the field the results will be
    #                  stored in. If field_base is an empty string the default
    #                  (Features_per_Hexagon) will be used. Otherwise '_fph'
    #                  will be appended to field_base.
    #
    # Requires: arcpy
    # Jason Roberts (robeja@au.qa.ic.gov)
    # Version 1.0 - May 2015
    
    # Perform a spatial join to determine how many features per hexagon
    # Note the field mapping is a placeholder to prevent all the fields from
    # being copied across (as a truly blank mapping will do).
    join_fc = arcpy.SpatialJoin_analysis(hexagon_fc,
                                         input_fc,
                                         'in_memory\\hex_join',
                                         'JOIN_ONE_TO_ONE',
                                         'KEEP_COMMON',
                                         'a "a" true true false 0 Short',
                                         'INTERSECT', '#', '#'
                                         ).getOutput(0)
    
    # Create a dictionary to capture the data
    data = dict()
    
    # Read the results back from the spatial join featureclass
    with arcpy.da.SearchCursor(join_fc, ['TARGET_FID', 'Join_Count']) as cur:
        # The TARGET_ID field will contain the ID field of hexagon
        # The Join_Count field will contain the number of features
        for row in cur:
            data[row[0]] = row[1]
    
    # Now delete the spatial join featureclass
    arcpy.Delete_management(join_fc)
    
    # Determine the name of the field the data will be written to
    if field_base == '':
        # Run with the default
        fld = 'Features_per_Hexagon'
    else:
        # Use the provided field name and append '_fph'
        # fph - Features Per Hexagon
        fld = '{}_fph'.format(make_name_valid(field_base))
    
    # Create a results tuple to return
    return (fld, 'LONG', data)

def lines_stats_per_hexagons(input_line_fc, hexagon_fc, field_base = ''):
    # This function determines a number of properties per polygon feature in
    # hexagon_fc. The results are returned within a tuple, each type of
    # analysis is an entry in the tuple. Each entry a tuple containing 3 items.
    #   1. A field name
    #   2. A field type
    #   3. A dictionary with the key being the object ID of the feature in
    #      hexagon_fc and the value being the count for this feature.
    # Any features which fall on or across the boundary between hexagons will
    # be considered to fall in both hexagons. There are three types of analysis
    # currently performed as follows.
    #   1. How many lines intersect with the hexagon.
    #   2. The sum of the length of each line within the hexagon.
    #   3. The sum of the percentage length of each line within the hexagon.
    #
    # input_line_fc  - The line featureclass which the hexagons are
    #                  overlayed.
    #
    # hexagon_fc     - The hexagon featureclass which is used to group
    #                  the points into spatial areas.
    # Note that hexagon_fc must be a polygon featureclass, but the analysis
    # will work with any shape polygons (even overlapping polygons)
    #
    # field_base     - This is the base name of the field the results will
    #                  be stored in. If field_base is an empty string the
    #                  default (Features_per_Hexagon) will be used.
    #                  Otherwise '_fph' will be appended to field_base.
    #
    # Requires: arcpy
    # Jason Roberts (robeja@au.qa.ic.gov)
    # Version 1.2 - July 2015
    
    # Generate the hexagon bin featureclass using a World Mercator projection
    mercator = arcpy.SpatialReference(3395)
    
    # Create some feature layers to intersect
    arcpy.MakeFeatureLayer_management(input_line_fc, 'input_line_lyr')
    arcpy.MakeFeatureLayer_management(hexagon_fc, 'hex_lyr')
    
    # Intersect the layers and select the hexagons which intersect the features
    # in input_line_lyr so only these hexagons are processed
    arcpy.SelectLayerByLocation_management('hex_lyr', 'intersect', 'input_line_lyr')
    
    # Delete input_line_lyr
    arcpy.Delete_management('input_line_lyr')
    
    # Fetch all the hexagon geometries
    hex_geoms = geometry_dictionary('hex_lyr')
    
    # Delete hexagon layer
    arcpy.Delete_management('hex_lyr')
    
    # Create data dictionaries to populate
    data1 = dict()
    data2 = dict()
    data3 = dict()
    
    # Iterate through each of the hexagons in memory
    for hexagon_id in hex_geoms:
        
        # Initialise the data dictionary for each hexagon
        data1[hexagon_id] = 0
        data2[hexagon_id] = 0
        data3[hexagon_id] = 0
    
    # Create a cursor to access the polygon features
    with arcpy.da.SearchCursor(input_line_fc, ['SHAPE@']) as cur:
        
        # Iterate through each of the selected polygons
        for row in cur:
            
            # Fetch the polygon geometry object
            line = row[0]
            
            # Make sure that the polygon has geometry
            if line is not None:
                
                # Iterate through each of the hexagons in memory
                for hexagon_id, hexagon in hex_geoms.items():
                
                    # Determine if the two are disjointed
                    if not hexagon.disjoint(line):
                        
                        # The two geometries intersect, increment the count
                        data1[hexagon_id] += 1
                        
                        # Create a line for the intersection between the two
                        inter_line = hexagon.intersect(line)
                        
                        # Add the length of the intersection line
                        data2[hexagon_id] += inter_line.projectAs(mercator).length
                        # Determine the length of the intersection length line as a
                        # ratio of the total length of the line
                        data3[hexagon_id] += inter_line.length / line.length
    
    # Determine the name of the field the data will be written to
    if field_base == '':
        # Run with the default
        fld1 = 'Lines_per_Hexagon'
        fld2 = 'Line_length_m'
        fld3 = 'Statistical_length'
    else:
        # Use the provided field name and append the following
        # lph  - Lines Per Hexagon
        fld1 = '{}_lph'.format(make_name_valid(field_base))
        # ll_m - Line Length (m)
        fld2 = '{}_ll_m'.format(make_name_valid(field_base))
        # sl   - Statistical Length
        fld3 = '{}_sl'.format(make_name_valid(field_base))
    
    # Create a tuple of the results
    results = ((fld1, 'LONG' , data1),  # Number of Lines
               (fld2, 'FLOAT', data2),  # Total Length
               (fld3, 'FLOAT', data3))  # Percentage Length
    
    return results

def polys_stats_per_hexagons(input_poly_fc, hexagon_fc, field_base = ''):
    # This function determines a number of properties per polygon feature in
    # hexagon_fc. The results are returned within a tuple, each type of
    # analysis is an entry in the tuple. Each entry a tuple containing 3 items.
    #   1. A field name
    #   2. A field type
    #   3. A dictionary with the key being the object ID of the feature in
    #      hexagon_fc and the value being the count for this feature.
    # Any features which fall on or across the boundary between hexagons will
    # be considered to fall in both hexagons. There are three types of analysis
    # currently performed as follows.
    #   1. How many polygons intersect with the hexagon.
    #   2. The sum of the area of each polygon within the hexagon.
    #   3. The sum of the percentage area of each polygon within the hexagon.
    #
    # input_poly_fc  - The input polygon featureclass
    #
    # hexagon_fc     - The hexagon featureclass which is used to group the
    #                  points into spatial areas.
    # Note that hexagon_fc must be a polygon featureclass, but the analysis
    # will work with any shape polygons (even overlapping polygons)
    #
    # field_base     - This is the base name of the field the results will be
    #                  stored in. If field_base is an empty string the default
    #                  (Features_per_Hexagon) will be used. Otherwise '_fph'
    #                  will be appended to field_base.
    #
    # Requires: arcpy
    # Jason Roberts (robeja@au.qa.ic.gov)
    # Version 1.2 - July 2015
    
    # Generate the hexagon bin featureclass using a World Mercator projection
    mercator = arcpy.SpatialReference(3395)
    
    # Create some feature layers to intersect
    arcpy.MakeFeatureLayer_management(input_poly_fc, 'input_poly_lyr')
    arcpy.MakeFeatureLayer_management(hexagon_fc, 'hex_lyr')
    
    # Intersect the layers and select the hexagons which intersect the features
    # in input_poly_lyr so only these hexagons are processed
    arcpy.SelectLayerByLocation_management('hex_lyr', 'intersect', 'input_poly_lyr')
    
    # Delete input_poly_lyr
    arcpy.Delete_management('input_poly_lyr')
    
    # Fetch all the hexagon geometries
    hex_geoms = geometry_dictionary('hex_lyr')
    
    # Delete hexagon layer
    arcpy.Delete_management('hex_lyr')
    
    # Create data dictionaries to populate
    data1 = dict()
    data2 = dict()
    data3 = dict()
    
    # Iterate through each of the hexagons in memory
    for hexagon_id in hex_geoms:
        
        # Initialise the data dictionary for each hexagon
        data1[hexagon_id] = 0
        data2[hexagon_id] = 0
        data3[hexagon_id] = 0
    
    # Create a cursor to access the polygon features
    with arcpy.da.SearchCursor(input_poly_fc, ['SHAPE@']) as cur:
        
        # Iterate through each of the selected polygons
        for row in cur:
            
            # Fetch the polygon geometry object
            poly = row[0]
            
            # Make sure that the polygon has geometry
            if poly is not None:
                
                # Iterate through each of the hexagons in memory
                for hexagon_id, hexagon in hex_geoms.items():
                    
                    # Determine if the two are disjointed
                    if not hexagon.disjoint(poly):
                        
                        # The two geometries intersect, increment the count
                        data1[hexagon_id] += 1
                        
                        # Create an polygon for the intersection between the two
                        inter_poly = hexagon.intersect(poly)
                        
                        # Add the area of the intersection polygon
                        data2[hexagon_id] += inter_poly.projectAs(mercator).area
                        # Determine the area of the intersection area polygon
                        # as a ratio of the total area of the polygon
                        data3[hexagon_id] += inter_poly.area / poly.area
    
    # Determine the name of the field the data will be written to
    if field_base == '':
        # Run with the default
        fld1 = 'Polys_per_Hexagon'
        fld2 = 'Poly_area_m'
        fld3 = 'Statistical_area'
    else:
        # Use the provided field name and append the following
        # pph  - Polygons Per Hexagon
        fld1 = '{}_pph'.format(make_name_valid(field_base))
        # pa_m - Polygon Area (m)
        fld2 = '{}_pa_m'.format(make_name_valid(field_base))
        # sa   - Statistical Area
        fld3 = '{}_sa'.format(make_name_valid(field_base))
    
    # Create the results tuple
    results = ((fld1, 'LONG' , data1),  # Number of Polygons
               (fld2, 'FLOAT', data2),  # Total Area
               (fld3, 'FLOAT', data3))  # Percentage Area
    
    # Return the results
    return results

def hexagon_analysis(input_fc, hexagon_fc, statistical_analysis = True):
    # Perform the spatial analysis of the input featureclass with the hexagon
    # featureclass. Note that this will perform the analysis of an input
    # featureclass or featurelayer.
    #
    # input_fc             - The input featureclass
    #
    # hexagon_fc           - The hexagon featureclass which is used to group the
    #                        points into spatial areas.
    # Note that hexagon_fc must be a polygon featureclass, but the analysis
    # will work with any shape polygons (even overlapping polygons)
    #
    # statistical_analysis - This determines the type of analysis which will been
    #                        be performed for lines and polygons. This has no
    #                        effect for points.
    #
    # Requires: arcpy
    # Jason Roberts (robeja@au.qa.ic.gov)
    # Version 1.0 - May 2015
    
    print('Performing The Analysis')
    
    # Perform the analysis according to the input featureclass type
    desc = arcpy.Describe(input_fc)
    
    if not statistical_analysis or \
       desc.shapeType == u'Point' or \
       desc.shapeType == u'Multipoint':
        # Simply count the number of features which intersect each hexagon
        # Note that Multipoint featureclasses aren't exploded, a multipoint
        # is just treated the same as a point
        print('Determining the number of features per hexagon')
        results = (features_per_hexagons(input_fc, hexagon_fc), )
    
    else:
        # Perform the more complicated statistical analysis
        
        if desc.shapeType == u'Polyline':
            # Perform the analysis to determine spatial statistics
            print('Determining relationships between lines and hexgons')
            results = lines_stats_per_hexagons(input_fc, hexagon_fc)
        
        elif desc.shapeType == u'Polygon':
            # Perform the analysis to determine spatial statistics
            print('Determining relationships between polygons and hexgons')
            results = polys_stats_per_hexagons(input_fc, hexagon_fc)
    
    # Return results
    return results

def grouped_hexagon_analysis(input_fc, hexagon_fc,
                             statistical_analysis = True,
                             group_by_field = ''):
    # Perform the spatial analysis of the input featureclass with the hexagon
    # featureclass grouping the analysis by the values within the
    # group_by_field. Note that this will perform the analysis of an input
    # featureclass or featurelayer.
    #
    # input_fc             - The input featureclass
    #
    # hexagon_fc           - The hexagon featureclass which is used to group the
    #                        points into spatial areas.
    # Note that hexagon_fc must be a polygon featureclass, but the analysis
    # will work with any shape polygons (even overlapping polygons)
    #
    # statistical_analysis - This determines the type of analysis which will been
    #                        be performed for lines and polygons. This has no
    #                        effect for points.
    #
    # group_by_field       - The analysis will be repeated for each value found
    #                        within this field. If this field is not found within
    #                       the input featureclass an error will be raised.
    #
    # Requires: arcpy
    # Jason Roberts (robeja@au.qa.ic.gov)
    # Version 1.0 - May 2015
    
    # This is the maximium number of unique values which will be permitted
    # in the group_by field to prevent excessive processing time.
    group_by_limit = 12
    
    # Initialise results
    results = []
    
    # Perform the analysis according to the input featureclass type
    desc = arcpy.Describe(input_fc)
    
    # Make sure that the group by field exists (since we already need the
    # decribe object anyway)
    if group_by_field not in [field.name for field in desc.fields]:
        # The field to group the analysis by doesn't exist, error
        print('The group by field doesn\'t exist in the input featureclass')
    
    # Create the necessary queries
    print('Grouping using the {} field'.format(group_by_field))
    queries = build_group_by_queries(input_fc, group_by_field)
    
    # Make sure that there aren't an excessive number of groups
    query_count = len(queries)
    if query_count > group_by_limit:
        # There are too many groups
        print('Too many values ({}) in {} to use as a Group By field'\
                .format(query_count, group_by_field),3)
    
    # Indicate to the user how many groups have been identified
    print('There are {} groups to process'.format(query_count))
    
    # Create a feature layer to make sure that when the selections are
    # performed using the queries only the desired data is processed
    arcpy.MakeFeatureLayer_management(input_fc, 'input_lyr')
    
    # Determine the type of analysis to carry output
    if not statistical_analysis or \
       desc.shapeType == u'Point' or \
       desc.shapeType == u'Multipoint':
        # Simply count the number of features which intersect each hexagon
        # Note that Multipoint featureclasses aren't exploded, a multipoint is
        # just treated the same as a point
        
        # Create the field to store the total results
        results.append(('Features_per_Hexagon', 'LONG', {}))
        
        # Process each query and perform the analysis
        for query, field_base in queries:
            
            # Select the features of interest using the query
            arcpy.SelectLayerByAttribute_management('input_lyr',
                                                    'NEW_SELECTION',
                                                    query)
            
            # Perform the analysis on the selected data
            print('Determining the number of features per hexagon where: {}'\
                    .format(query), 1, False)
            group_results = features_per_hexagons('input_lyr',
                                                  hexagon_fc,
                                                  field_base)
            # Add the results for this group into results
            results.append(group_results)
            
        # Construct the total result from the group analysis
        total_data = results[0][2]
        
        # Iterate through each group
        for result in results[1:]:
            
            # Pull the result dictionary
            group_dic = result[2]
            
            # Process each hexagon and add it to the total
            for hex in group_dic:
                
                # Check if this hexagon already exists in total_data
                if hex in total_data:
                    # Add the count from this group
                    total_data[hex] += group_dic[hex]
                else:
                    # Initialise this hexagon
                    total_data[hex] = group_dic[hex]
    
    else:
        # Perform the more complicated statistical analysis
        
        # Create a grouped_results list to store results nestered by group
        grouped_results = []
        
        if desc.shapeType == u'Polyline':
            
            # Create the field to store the total results
            grouped_results.append((('Lines_per_Hexagon', 'LONG', {}),
                                    ('Line_length_m', 'FLOAT', {}),
                                    ('Statistical_length', 'FLOAT', {})))
            
            for query, field_base in queries:
                
                # Select the features of interest using the query
                arcpy.SelectLayerByAttribute_management('input_lyr',
                                                        'NEW_SELECTION',
                                                        query)
            
                # Perform the analysis to determine spatial statistics
                msg = 'Determining relationships between lines and hexgons'
                msg += ' where: {}'.format(query)
                print(msg, 1, False)
                group_results = lines_stats_per_hexagons('input_lyr',
                                                         hexagon_fc,
                                                         field_base)
                
                # Add the results for this group into results
                grouped_results.append(group_results)
        
        elif desc.shapeType == u'Polygon':
            
            # Create the field to store the total results
            grouped_results.append((('Polys_per_Hexagon', 'LONG', {}),
                                    ('Poly_area_m', 'FLOAT', {}),
                                    ('Statistical_area', 'FLOAT', {})))
            
            for query, field_base in queries:
                
                # Select the features of interest using the query
                arcpy.SelectLayerByAttribute_management('input_lyr',
                                                        'NEW_SELECTION',
                                                        query)
                
                # Perform the analysis to determine spatial statistics
                msg = 'Determining relationships between polygons and hexgons'
                msg += ' where: {}'.format(query)
                print(msg, 1, False)
                group_results = polys_stats_per_hexagons('input_lyr',
                                                         hexagon_fc,
                                                         field_base)
                
                # Add the results for this group into results
                grouped_results.append(group_results)
        
        # Construct the total result from the group analysis for BOTH lines
        # and polygons. Note if you've added another type of result in the
        # statistical analysis this will be automatically calculated if you've
        # added it to results before the loop.
        # This is what the check below is for... :)
        if len(grouped_results[0]) != len(grouped_results[1]):
            print('You made an ERROR in the code when you modified it')
        
        # Fetch the data dictionaries for each group
        data_dics = [group_results[2] for group_results in grouped_results[0]]
        
        # Iterate through each group
        for group_results in grouped_results[1:]:
            
            # Pull the result for the fields
            group_dics = [group_result[2] for group_result in group_results]
            
            # Iterate through each of the analysis types
            for i in range(len(group_results)):
                # Fetch the necessary dictionaries
                data_dic = data_dics[i]
                group_dic = group_dics[i]
                
                # Process each hexagon and add it to the total
                for hex in group_dic:
                    if hex in data_dic:
                        # Add the count from this group
                        data_dic[hex] += group_dic[hex]
                    else:
                        # Initialise this hexagon
                        data_dic[hex] = group_dic[hex]
        
        # Unpack grouped_results into a flat, ungrouped structure in results
        for group_results in grouped_results:
            # For each group, append each results field to results
            for group_result in group_results:
                # Append this to results
                results.append(group_result)
    
    # Return the results
    return results

def geometry_dictionary(input_fc):
    # Fetch all the geometry objects of a featureclass
    # Return a dictionary where key is ID and value is geometry
    
    # Determine the ObjectID field of the input featureclass
    desc = arcpy.Describe(input_fc)
    feat_id_field = desc.OIDFieldName
    
    # Fetch all the feature geometries
    geoms = {}
    
    # Iterate through each feature using a search cursor
    with arcpy.da.SearchCursor(input_fc, [feat_id_field, 'SHAPE@']) as cur:
        
        # Iterate through each of the features
        for row in cur:
            
            # Fetch the hexagon ID and geometry object
            geoms[row[0]] = row[1]
    
    return geoms

def make_name_valid(input_name, char_limit = None):
    # Take an input name, remove all the illegal characters and output a name
    # containing no illegal characters.
    
    # Include the numbers 0-9
    valid_chrs = [chr(i) for i in range(48, 58)]
    # Include the characters A-Z
    valid_chrs.extend([chr(i) for i in range(65,91)])
    # Include the characters a-z
    valid_chrs.extend([chr(i) for i in range(97,123)])
    # Include the underscore character
    valid_chrs.append('_')
    
    # Remove all the invalid characters
    output_name = ''.join(c for c in input_name if c in valid_chrs)
    
    # Make sure that is doesn't start with a number
    if ord(output_name[0]) in range(48,58):
        # Stick an 'a' in front of the first character
        output_name = 'a' + output_name
    
    # Check if the user specified a limit to the length of output_name
    if isinstance(char_limit, int) and char_limit > 6:
        # Reduce the length of the output_name to the desired length
        output_name = output_name[0:char_limit]
    
    return output_name

def build_group_by_queries(input_fc, group_by_field):
    # For each value within the group_by_field in the input featureclass or
    # featurelayer, construct a queries such that only records with these
    # Hexagon Parameters
    # values can be selected. Note it is not checked if the group_by_field
    # exists within input_fc.
    #
    # input_fc             - The input featureclass
    #
    # group_by_field       - The analysis will be repeated for each value found
    #                        within this field. If this field is not found within
    #                        the input featureclass the function will fail.
    #
    # Requires: arcpy
    # Jason Roberts (robeja@au.qa.ic.gov)
    # Version 1.0 - May 2015
    
    print('Determining the number of groups')
    
    # Determine the values in the field to group the data by
    values = set()
    
    # Create a cursor to read the available values
    with arcpy.da.SearchCursor(input_fc, [group_by_field]) as cur:
        
        # Iterate through each feature
        for row in cur:
            # Fetch the value and add it to the set (if necessary)
            values.add(row[0])
    
    # Construct the queries
    queries = []
    
    # Check for NULL values (None)
    if None in values:
        # This is a special case which requires IS
        query = '"{}" IS NULL'.format(group_by_field)
        # Define a name for the field
        field_base = '{}_isNULL'.format(group_by_field)
        # Append it to the list of queries
        queries.append([query, field_base])
        # Remove None from the list of values
        values.remove(None)
    
    # Process the rest of the values    
    for value in values:
        # Check the data type of value
        
        if isinstance(value, str) or isinstance(value, unicode):
            # Build the query for a string
            # The value needs to be within single quotes
            query = '"{}" = \'{}\''.format(group_by_field, value)
        else:
            # Assume that it's numeric (no quotes needed
            query = '"{}" = {}'.format(group_by_field, value)
        
        # Define a name for the field
        field_base = '{}_{}'.format(group_by_field, value)
        # Append it to the list of queries
        queries.append([query, field_base])
    
    return queries

def insert_results(results, output_fc):
    # Insert the results found within the results list (or tuple) into 
    # output_fc. Each item in results is inserted into its own field.
    #
    # output_fc - The output featureclass to which results are added
    #
    # results  - The results to insert into output_fc. Each item in results
    #            must contain the following 3 items.
    #               1. A field name
    #               2. A field type
    #               3. A dictionary with the key being the object ID of the
    #                  feature in hexagon_fc and the value being the count for
    #                  this feature.
    #
    # Requires: arcpy
    # Jason Roberts (robeja@au.qa.ic.gov)
    # Version 1.0 - May 2015
    
    print('Inserting the results into the Featureclass')
    
    # Iterate through each field and add each to the output featureclass
    print('Adding the required fields')
    
    # Determine the ObjectID field of the hexagon featureclass
    desc = arcpy.Describe(output_fc)
    hex_id_field = desc.OIDFieldName
    
    # Initialise a list of fieldnames to update
    fieldnames = [hex_id_field]
    
    # Iterate through each of the results fields
    for field in results:
        # Add the field into the output featureclass
        arcpy.AddField_management(output_fc, field[0], field[1])
        # Construct a list of names
        fieldnames.append(field[0])
    
    # Insert the results into output_fc
    print('Inserting the results')
    with arcpy.da.UpdateCursor(output_fc, fieldnames) as cur:
        
        # Iterate through each row
        for row in cur:
            
            # Determine the hexagon ID
            hex_id = row[0]
            
            # Determine the values for this hexagon
            values = []
            # Iterate through each of the fields
            for field in results:
                
                # Extract the data dictionary
                data = field[2]
                
                # Fetch the value, or use a zero
                if hex_id in data:
                    values.append(data[hex_id])
                else:
                    values.append(0)
            
            # Insert the results from the data
            row[1:] = values
            
            # Update the row
            cur.updateRow(row)
    
    # Don't return anything, output_fc is modified in place
    return None

def hexify(input_fc, clip_type = 'INTERSECT',
           hex_area_km2 = None, hex_width_km = None,
           hex_height_km = None, group_by_field = '',
           statistical_analysis = True, smart_limit = True):
    # This is the highest level function.  This function will generate the
    # hexagon featureclass, perform the analysis (grouped or ungrouped) and
    # then insert the results into the hexagon featureclass.
    #
    # input_fc       - This is the input featureclass (or featurelayer)
    #                  containing the features (or features selected) which are
    #                  to be analysed.
    #
    # For the generation of the hexagons
    # clip_type      - NONE:      The hexagon featureclass will not be clipped
    #                             and will cover the extent of the input
    #                             features
    #                  INTERSECT: The hexagon featureclass will be clipped such
    #                             that only hexagons which intersect an input
    #                             feature will be present (Default).
    #                  MIN_BBOX:  A minimum bounding geometry will be used to
    #                             bound the hexagons. NOTE: This requires an
    #                             Advanced Desktop License.
    #
    # hex_area_km2   - The area of the hexagons in square kilometers
    #                  (1 km2 = 100 ha, 1 km2 = 1 000 000 m2)
    # hex_width_km   - The width of the hexagons in kilometers
    # hex_height_km  - The height of the hexagons in kilometers
    # NB: Only one of these three variables needs to be specified. These are
    # listed in preference order, subsequent ones will be ignored. If all three
    # are None (default), the area of the hexagons will be determined such that
    # approximately 1000 hexagons will cover the extent of the input featureclass. In addition, due to variations between projection, the
    # area is usually most accurate parameter to specify.
    #
    # smart_limit    - If True (default) it will prevent the creation of more
    #                  than 100 000 hexagons by increasing the hexagon size.
    #                  False will allow the user to override this check and
    #                  create hexagons of the desired size, acknowledging that
    #                  there may be excessive processing time.
    #
    # For the analysis
    # statistical_analysis - This determines the type of analysis which will been
    #                        be performed for lines and polygons. This has no
    #                        effect for points.
    #
    # group_by_field       - The analysis will be repeated for each value found
    #                        within this field. If this field is not found within
    #                       the input featureclass an error will be raised.
    #
    # Jason Roberts (robeja@au.qa.ic.gov)
    # Version 1.0 - May 2015
    
    # Generate the hexagon featureclass
    hexagon_fc = generate_hex_bins_fc(input_fc, clip_type,
                                      hex_area_km2, hex_width_km,
                                      hex_height_km, smart_limit)
    
    # Check if grouped analysis is required
    if group_by_field == '':
        
        # Perform the simple, ungrouped analysis
        results = hexagon_analysis(input_fc, hexagon_fc, statistical_analysis)
    
    else:
        
        # Performing the grouped analysis
        results = grouped_hexagon_analysis(input_fc, hexagon_fc,
                                           statistical_analysis,
                                           group_by_field)
    
    # Insert the results back into the hexagon featureclass
    insert_results(results, hexagon_fc)
    
    # Return the (in memory) hexagon featureclass
    return hexagon_fc

# Main Line
# This is for execution as an ArcMap tool
if __name__ == '__main__':

    msg("", 99)
    msg(tool_info, 0)
  
    # Get input parameters
    input_fc = arcpy.GetParameter(0)
    output_fc = arcpy.GetParameterAsText(1)
    clip_type = arcpy.GetParameter(2)
    
    # Advanced Parameters
    group_by_field = arcpy.GetParameterAsText(3)
    statistical_analysis = arcpy.GetParameter(4)
    smart_limit = arcpy.GetParameter(5)
    
    # Hexagon Parameters
    hex_area_km2 = arcpy.GetParameter(6)
    hex_width_km = arcpy.GetParameter(7)
    hex_height_km = arcpy.GetParameter(8)
    
    # Perform the Hexification
    print('Performing Hexagon Analysis')
    hexagon_fc = hexify(input_fc,
                        clip_type,
                        hex_area_km2,
                        hex_width_km,
                        hex_height_km,
                        group_by_field,
                        statistical_analysis,
                        smart_limit)
    
    # Copy the in_memory hexagon output to the users desired location
    print('Hexagon Analysis Complete')
    print('Saving results from memory to disk')
    arcpy.CopyFeatures_management(hexagon_fc, output_fc)
    
    print('Hexification complete')
    display_data = [(output_fc, "hexify.lyr")]
    add_data_to_map(display_data)

    del arcpy
    

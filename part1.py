import arcpy
import csv
arcpy.env.overwriteOutput = True

# Set workspace and input data variables
presence_inFile_csv = arcpy.GetParameterAsText(0)
presence_inFile_shp = arcpy.GetParameterAsText(1)
speciesName = arcpy.GetParameterAsText(2)
output_workspace = arcpy.GetParameterAsText(3)
coordSys = arcpy.GetParameterAsText(4)

# Check file type of presence points inputted by user
if presence_inFile_csv.lower().endswith('.csv'):

    # Coordinate system of input presence points is assumed to be WGS 1984 (WKID #4326)
    wgs1984 = arcpy.SpatialReference(4326)

    # Create point shapefile and add lat/lon fields
    pointFC_latlon = speciesName + "_presence_latlon.shp"
    arcpy.CreateFeatureclass_management(output_workspace,pointFC_latlon,"POINT","","","",wgs1984)


    gpsTrack = open(presence_inFile_csv, "r")
    headerLine = gpsTrack.readline()
    valueList = headerLine.strip().split(",")

    # Create lists of possible coordinate field names for lat and lon
    latCSV_options = ["latitude", "lat", "Lat", "Latitude", "LAT", "LATITUDE", "y", "Y"]
    lonCSV_options = ["longitude", "lon", "Lon", "Longitude", "LON", "LONGITUDE", "x", "X"]

    # Check if csv contains one of the acceptable field names located in lists
    for item in valueList:
        if item in latCSV_options:
            latValueIndex = valueList.index(item)
            print "Lat field found..."
        elif item in lonCSV_options:
            lonValueIndex = valueList.index(item)
            print "Lon field found..."
        else:
            print "Coordinate fields not found in CSV. Please edit field name(s)\
             to match one of the CSV field name options."

    # Read each line in csv file and create point feature in new feature class
    with arcpy.da.InsertCursor(pointFC_latlon, ['SHAPE@']) as cursor:
        for point in gpsTrack.readlines():

           segmentedPoint = point.split(",")
           # Get the lat/lon values of the current reading
           latValue = segmentedPoint[latValueIndex]
           lonValue = segmentedPoint[lonValueIndex]
           vertex = arcpy.CreateObject("Point")
           vertex.X = lonValue
           vertex.Y = latValue
           feature = arcpy.PointGeometry(vertex)
           cursor.insertRow(feature)

    # Add fields with lat and lon coordinates for easy reference
    arcpy.AddGeometryAttributes_management(pointFC_latlon, "POINT_X_Y_Z_M")

    # Project the presence points from WGS 1984 to the user's desired PCS 
    pointFC_proj = pointFC_latlon[:-10] + "proj.shp"
    arcpy.Project_management(pointFC_latlon, pointFC_proj, coordSys)

    # Add the Presence, Pnum and Pnum1 fields
    arcpy.AddField_management(pointFC_proj, "Presence", "TEXT", "", "",2)
    arcpy.AddField_management(pointFC_proj, "Pnum", "SHORT")
    arcpy.AddField_management(pointFC_proj, "Pnum1", "SHORT")

    # Add identical values to the Presence, Pnum and Pnum1 fields
    arcpy.CalculateField_management(pointFC_proj, "Presence", '"P"')
    arcpy.CalculateField_management(pointFC_proj, "Pnum", 1)
    arcpy.CalculateField_management(pointFC_proj, "Pnum1", 1)


elif presence_inFile_shp.lower().endswith('.shp'):
    # Project the presence points from native CS to the user's desired PCS
    pointFC_proj = presence_inFile_shp[:-4] + "_proj.shp"
    arcpy.Project_management(presence_inFile_shp, pointFC_proj, coordSys)

    # Add the Presence, Pnum and Pnum1 fields
    arcpy.AddField_management(pointFC_proj, "Presence", "TEXT", "", "",2)
    arcpy.AddField_management(pointFC_proj, "Pnum", "SHORT")
    arcpy.AddField_management(pointFC_proj, "Pnum1", "SHORT")

    # Add identical values to the Presence, Pnum and Pnum1 fields
    arcpy.CalculateField_management(pointFC_proj, "Presence", '"P"')
    arcpy.CalculateField_management(pointFC_proj, "Pnum", 1)
    arcpy.CalculateField_management(pointFC_proj, "Pnum1", 1)

else:
    print "Incorrect file type! The input presence points file must be *.csv or *.shp feature class."

"""
    Author: Carson Hauck, Marc Healy and Michelle Lam
    Date: April 15, 2018
    Note: 
"""

import arcpy


class Toolbox(object):
    # Define the toolbox (the name of the toolbox is the name of the .pyt file)
    def __init__(self):
        self.label = "Habitat Modeling"
        self.alias = "habitat"

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    # Define the tool (tool name is the name of the class)
    def __init__(self):
        self.label = "Tool"
        self.description = ""
        self.canRunInBackground = False

    # Define parameter definitions
    def getParameterInfo(self):
        presenceInFileCSV=arcpy.Parameter(
            displayName="Input Presence Points CSV",
            name="ppCSV",
            datatype="DETable",
            parameterType="Optional",
            direction="Input")

        presenceInFileFL=arcpy.Parameter(
            displayName="Input Presence Points Feature Layer",
            name="ppFL",
            datatype="GPFeatureLayer",
            parameterType="Optional",
            direction="Input")

        speciesName=arcpy.Parameter(
            displayName="Species Name",
            name="speciesName",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        outputWorkspace=arcpy.Parameter(
            displayName="Output Workspace",
            name="outputWorkspace",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")

        coordSys=arcpy.Parameter(
            displayName="Output Coordinate System",
            name="coordSys",
            datatype="GPSpatialReference",
            parameterType="Required",
            direction="Input")

        parameters = [presenceInFileCSV, presenceInFileFL, speciesName, outputWorkspace, coordSys]
        return parameters

    # Set whether tool is licensed to execute
    def isLicensed(self):
        return True

    """Modify the values and properties of parameters before internal
       validation is performed.  This method is called whenever a parameter
       has been changed."""
    def updateParameters(self, parameters):
        return

    """Modify the messages created by internal validation for each tool
       parameter. This method is called after internal validation."""
    def updateMessages(self, parameters):
        return

    # The source code of the tool 
    def execute(self, parameters, messages):
        
        # Get parameters from user
        presenceInFileCSV = parameters[0].valueAsText
        presenceInFileFL = parameters[1].valueAsText
        speciesName = parameters[2].valueAsText
        outputWorkspace = parameters[3].valueAsText
        coordSys = parameters[4].valueAsText

        arcpy.env.overwriteOutput = True

        # Return file extension
        def checkFileExt(file): 
            desc = arcpy.Describe(file)
            return desc 


        # Check if in GBD 
        def checkGDB(): 
            if outputWorkspace.endswith('.gdb'):
                return ""
            else: 
                return ".shp"
        
        # Initialize shape file or feature class
        def initialize():
            ext = checkGDB()        # check whether we need .shp

            if presenceInFileCSV != "":
                # Coordinate system of input presence points is assumed to be WGS 1984 (WKID #4326)
                wgs1984 = arcpy.SpatialReference(4326)

                # Create point shapefile and add lat/lon fields
                pointFC_latlon = speciesName + "_presence_latlon" + ext
                arcpy.CreateFeatureclass_management(outputWorkspace, pointFC_latlon, "POINT","","","",wgs1984, "", "", "", "")
                messages.addMessage("\n" + "Yay, you're doing great!")

                gpsTrack = open(presenceInFileCSV, "r")
                headerLine = gpsTrack.readline()
                valueList = headerLine.strip().split(",")

                # Create lists of possible coordinate field names for lat and lon
                latCSV_options = ["latitude", "lat", "Lat", "Latitude", "LAT", "LATITUDE", "y", "Y"]
                lonCSV_options = ["longitude", "lon", "Lon", "long", "Long", "LONG", "Longitude", "LON", "LONGITUDE", "x", "X"]

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
                
                createPP(pointFC_latlon)
                return                

            elif presenceInFileFL != "":
                #createPP()
                return 

            else: 
                print ("Incorrect file type! The input presence points file must be\
                        *.csv or *.shp feature class.")


        # create presence points
        def createPP(pointFC_latlon):
            ext = checkGDB()
            arcpy.AddGeometryAttributes_management(pointFC_latlon, "POINT_X_Y_Z_M")

            # Project the presence points from WGS 1984 to the user's desired PCS
            pointFC_proj = pointFC_latlon + "proj" + ext
            arcpy.Project_management(pointFC_latlon, pointFC_proj, coordSys)

            # Add the Presence, Pnum and Pnum1 fields
            arcpy.AddField_management(pointFC_proj, "Presence", "TEXT", "", "",2)
            arcpy.AddField_management(pointFC_proj, "Pnum", "SHORT")
            arcpy.AddField_management(pointFC_proj, "Pnum1", "SHORT")

            # Add identical values to the Presence, Pnum and Pnum1 fields
            arcpy.CalculateField_management(pointFC_proj, "Presence", '"P"')
            arcpy.CalculateField_management(pointFC_proj, "Pnum", 1)
            arcpy.CalculateField_management(pointFC_proj, "Pnum1", 1)


        initialize()
        return




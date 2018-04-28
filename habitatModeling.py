"""
    Author: Carson Hauck, Marc Healy, and Michelle Lam
    Date: 30 April 2018
"""

import arcpy
import csv

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
        self.label = "Create Species Absence Points"
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
            parameterType="Optional",
            direction="Input")

        eraseFeatures=arcpy.Parameter(
            displayName="Constraining Polygon",
            name="constrainPoly",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")

        distVal = arcpy.Parameter(
            displayName="Buffer Distance",
            name="buffDist",
            datatype="GPLinearUnit",
            parameterType="Optional",
            direction="Input")

        numField=arcpy.Parameter(
            displayName="Number of Random Points",
            name="numOfRandPoints",
            datatype="GPLong",
            parameterType="Required",
            direction="Input")

        minAllowedDist=arcpy.Parameter(
            displayName="Minimum Allowed Distance Between Points",
            name="minAllowedDistBtwP",
            datatype="GPLinearUnit",
            parameterType="Optional",
            direction="Input")

        parameters = [presenceInFileCSV, presenceInFileFL, speciesName, outputWorkspace, coordSys, eraseFeatures, distVal, numField, minAllowedDist]
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
        eraseFeatures = parameters[5].valueAsText
        distVal = parameters[6].valueAsText
        numField = parameters[7].valueAsText
        minAllowedDist = parameters[8].valueAsText

        OW = str(outputWorkspace + "\\")

        arcpy.env.overwriteOutput = True

        # Adding Workspace Path
        def WS():
            if presenceInFileCSV != None and presenceInFileCSV.endswith(".csv"):
                temp = str(outputWorkspace + "\\")
                return temp
            else:
                temp = ""
                return temp

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

            if presenceInFileCSV != None and presenceInFileCSV.endswith(".csv"):

                # Coordinate system of input presence points is assumed to be WGS 1984 (WKID #4326)
                wgs1984 = arcpy.SpatialReference(4326)

                # Create point shapefile and add lat/lon fields
                pointFC_latlon = speciesName + "_Presence_latlon" + ext
                arcpy.CreateFeatureclass_management(outputWorkspace, pointFC_latlon, "POINT","","","",wgs1984, "", "", "", "")

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
                        messages.addMessage("Latitude field found...")
                    elif item in lonCSV_options:
                        lonValueIndex = valueList.index(item)
                        messages.addMessage("Longitude field found...")
                    else:
                        messages.addMessage("Coordinate fields not found in CSV. Please edit field name(s)\
                                to match one of the CSV field name options.")

                # Read each line in csv file and create point feature in new feature class
                with arcpy.da.InsertCursor(OW + pointFC_latlon, ['SHAPE@']) as cursor:
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

                messages.addMessage("Created Point Feature...")
                createPP(pointFC_latlon)
                return                

            elif presenceInFileFL != "":
                pointFC_latlon = presenceInFileFL
                createPP(pointFC_latlon)
                return 

            else: 
                messages.addMessage("Incorrect file type! The input presence points file must be\
                        *.csv or *.shp feature class.")


        # create presence points
        def createPP(pointFC_latlon):

            temp = WS()
            ext = checkGDB()
            pointFC_proj = ""

            if coordSys != None:
                # Project the presence points from WGS 1984 to the user's desired PCS
                pointFC_proj = OW + speciesName + "_Presence_proj" + ext
                arcpy.Project_management(temp + pointFC_latlon, pointFC_proj, coordSys, "", "", "", "", "")

            elif coordSys == None and presenceInFileFL != None:
                pointFC_proj = presenceInFileFL

            else:
                pointFC_proj = OW + speciesName + "_Presence_latlon" + ext

            # Add the Presence, Pnum and Pnum1 fields
            arcpy.AddField_management(pointFC_proj, "Presence", "TEXT", "", "",2)
            arcpy.AddField_management(pointFC_proj, "Pnum", "SHORT")
            arcpy.AddField_management(pointFC_proj, "Pnum1", "SHORT")

            # Add identical values to the Presence, Pnum and Pnum1 fields
            arcpy.CalculateField_management(pointFC_proj, "Presence", '"P"')
            arcpy.CalculateField_management(pointFC_proj, "Pnum", 1)
            arcpy.CalculateField_management(pointFC_proj, "Pnum1", 1)

            messages.addMessage("Finished Adding Attribute Fields...")

            buffer(pointFC_proj)


        # Process: Buffer
        def buffer(pointFC_proj):

            ext = checkGDB()
            buffDist = ""

            if distVal != None:
                messages.addMessage("Buffering...")
                buffDist = OW + speciesName + "_Buffer_Zones" + ext
                arcpy.Buffer_analysis(pointFC_proj, buffDist, distVal, "FULL", "ROUND", "ALL", "", "PLANAR")

                messages.addMessage("Finished Buffering...")

                erase(buffDist)

            else:
                randomPointGen(eraseFeatures)



        # Process: Erase
        def erase(buffDist):
            messages.addMessage("Erasing Buffer Zones from Constraining Polygon...")
            ext = checkGDB()
            exBuffZone = OW + speciesName + "_Buffered_Point_Constraint" + ext

            arcpy.Erase_analysis(eraseFeatures, buffDist, exBuffZone, "")

            messages.addMessage("Finished Erase...")

            randomPointGen(exBuffZone)


        # Create random points
        def randomPointGen(constrainPoly):
            ext = checkGDB()

            minDist = ""
            if minAllowedDist != None:
                minDist = minAllowedDist

            else:
                minDist = ""

            outName = speciesName + "_RandomAbsence" + ext
            arcpy.CreateRandomPoints_management(OW, outName, constrainPoly, "", numField, minDist)

            messages.addMessage("Finished Generating Random Points...")

            addTextField(outName)

            messages.addMessage("Finished Adding Attribute Fields...")

            merge()

            messages.addMessage("Finished Merge.")


        # Add text fields
        def addTextField(outName):
            ext = checkGDB()

            # Create fields
            presence = "Presence"
            pnum = "Pnum"
            pnum1 = "Pnum1"
            arcpy.AddField_management(OW + outName, presence, "TEXT")  # add text field
            arcpy.AddField_management(OW + outName, pnum, "SHORT") # add short field
            arcpy.AddField_management(OW + outName, pnum1, "SHORT") # add short field

            # Fill in given value for every record
            arcpy.CalculateField_management(OW + outName, presence, '"A"')
            arcpy.CalculateField_management(OW + outName, pnum, 0)
            arcpy.CalculateField_management(OW + outName, pnum1, 2)


        # Merge presence and absence point files together
        def merge():
            ext = checkGDB()

            outName = OW + speciesName + "_RandomAbsence" + ext
            pointFC_proj = ""
            Final_shp = OW + speciesName + "_PA" + ext

            if coordSys != None:
                pointFC_proj = OW + speciesName + "_Presence_proj" + ext

            elif coordSys == None and presenceInFileFL != None:
                pointFC_proj = presenceInFileFL

            else:
                pointFC_proj = OW + speciesName + "_Presence_latlon" + ext

            arcpy.Merge_management([outName, pointFC_proj], Final_shp, "")

            # Delete undesired fields which were automatically created by Arc
            dropFields = ["CID", "Id"]
            arcpy.DeleteField_management (Final_shp, dropFields)

            spatial_ref = arcpy.Describe(Final_shp).spatialReference
            finalShp_temp = OW + speciesName + "_PA_temp" + ext

            if spatial_ref != coordSys and coordSys != None:
                arcpy.Project_management(Final_shp, finalShp_temp, coordSys, "", "", "", "", "")

                arcpy.Delete_management(Final_shp)

                arcpy.Rename_management(finalShp_temp, Final_shp)

            else:
                pass


        initialize()

        messages.addMessage("Completed!")

        return





import arcpy

# set workspace
arcpy.env.workspace = arcpy.GetParameterAsText(0)
outPath = arcpy.GetParameterAsText(1)
outName = arcpy.GetParameterAsText(2)

# Create random points
def RandomPointGen():
    # Create random points in the features of a constraining feature class
    # Number of points for each feature determined by the value in the field specified
    conFC = "SHP_FILE_HERE"                       # Shp file from option 2
    numField = arcpy.GetParameterAsText(3)
    minAllowedDist = arcpy.GetParameterAsText(4)
    arcpy.CreateRandomPoints_management(outPath, outName, conFC, "", numField, 
        minAllowedDist)


# Add text feilds
def addTextField():
    RandomPointGen()

    # Create fields
    presence = "Presence"
    pum = "Pnum"
    pnum1 = "Pnum1"
    arcpy.AddField_management(outName, presence, "TEXT")  # add text field
    arcpy.AddField_management(outName, pnum, "SHORT") # add short field
    arcpy.AddField_management(outName, pnum1, "SHORT") # add short field
        

    # Fill in given value for every record
    arcpy.CalculateField_management(outName, presence, "A")
    arcpy.CalculateField_management(outName, pum, 0)
    arcpy.CalculateField_management(outName, pnum1, 2)


# Merge shp files together
def merge():
    addTextField()

    presenceData = "SHP_FILE_HERE"           # Shp file from phase 1
    absenceDAta = "SHP_FILE_HERE"            # Shp file from option 2
    outPath = arcpy.GetParameterAsText(5)
    arcpy.Merge_management([presenceData, absenceDAta], outPath)

def main ():
    merge()
    print("DONE!")


if __name__ == "__main__":
    main()

"""
Name: Marc Healy
Date: April 21, 2018
Description: Option 2 for the project
"""
#Imort modules used for this project
import arcpy

#Set script argument to get data from user
Workspace_or_Feature_Dataset = arcpy.GetParameterAsText(0)
Input_Features = arcpy.GetParameterAsText(1)
Distance__value_or_field_ = arcpy.GetParameterAsText(2)
Clip_Features = arcpy.GetParameterAsText(3)

# Local variables tied to workspace designated by user

if Workspace_or_Feature_Dataset.endswith('.gdb'):
    Buffer_Dist_FromPresence = Workspace_or_Feature_Dataset+"\\Buffer_Dist_FromPresence"
else:
    Buffer_Dist_FromPresence = Workspace_or_Feature_Dataset+"\\Buffer_Dist_FromPresence.shp"

if Workspace_or_Feature_Dataset.endswith('.gdb'):
    Excluded_Buffer_Zone = Workspace_or_Feature_Dataset+"\\Excluded_Buffer_Zone"
else:
    Excluded_Buffer_Zone = Workspace_or_Feature_Dataset+"\\Excluded_Buffer_Zone.shp"

# Process: Buffer
arcpy.Buffer_analysis(Input_Features, Buffer_Dist_FromPresence, Distance__value_or_field_, "FULL", "ROUND", "ALL", "", "PLANAR")

# Process: Clip
arcpy.Clip_analysis(Buffer_Dist_FromPresence, Clip_Features, Excluded_Buffer_Zone, "")

print "Done"
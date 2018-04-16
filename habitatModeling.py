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
        params = None
        return params

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
        
        # Set up workspaces
        try:  
            arcpy.env.workspace = r'TEMP'
        except Exception:
            print "This path cannot be found. Please try another."

        # set up workspaces
        arcpy.env.workspace = "TEMP"
        arcpy.env.overwriteOutput = True
    
        # send outputs to a different folder
        out_dir = "TEMP" 

        '''
        TODO: 
            1. The tool could take either a points shapefile or CSV file with the lat/lon 
                of species presence as the input
            2. User can set the destination workspace
            3. User can output random points file name
            4. User can customize parameters (ex. number of points, spacing of random points, 
                input a boundaries shapefile with which to constrain the placement of random 
                points, etc.)
            5. The tool will output the merged presence/absence points shapefile
        '''
        return









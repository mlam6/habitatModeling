# Creating psuedo-absence points for habitat modeling

This tool can be used to create species pseudo-absence points and to merge them with species presence points into a single point feature. The merged Presence-Absence (PA) point feature is often a required input in presence-absence species distribution models (ex. Logistic regression, artifical neural networks).

## Getting Started

From a GUI, the user may either input (1) a .CSV file with species presence points in decimal degree coordinates (WGS 1984) or (2) a point features Shapefile (.shp) or File Geodatabase Feature Class.

Users are required to specify: (1) a species name (2) an output workspace (3) the number of randomly-placed absence points, and (4) the polygon feature in which to constrain random point placement. 

Optional parameters include: (1) a buffer distance from presence points to exclude absence points, (2) the minimum distance that absence points must be placed from other random points, and (3) a projected coordinate system. 

### Software Requirements

ESRI ArcMap or ESRI ArcGIS Pro (If using ArcGIS Pro, the code will need to be updated to support Python 3)

### Installing & Running

Download the zip folder and connect extracted folder to ArcCatalog where the python toolbox will become visible. 

This code for creating pseudo-absence points incorporates:
  - Encapsulation of each major step into methods
  - Conditional if statements allow for optional parameter fields
  - Messages included to give the user feedback in ArcMap GUI as the tool runs
  - General tool and input field descriptions to help the user


### Outputs

1. Projected, presence-only points

2. Projected & merged, presence-absence points
	 - attribute field to denote “P” (Presence) vs. “A” (Absence)
	 - two integer fields used in habitat modeling (P = 1; A = 0 or 2)
	 
## Built With

Python and Arcpy in a Python Toolbox

## For More Information 

Please read ....

Barbet‐Massin, M., Jiguet, F., Albert, C.H. and Thuiller, W., 2012. Selecting pseudo‐absences for species distribution models: how, 
	where and how many?. Methods in ecology and evolution, 3(2), pp.327-338.

Senay, S.D., Worner, S.P. and Ikeda, T., 2013. Novel three-step pseudo-absence selection technique for improved species distribution 
	modelling. PLoS One, 8(8), p.e71218.

West, A.M., Evangelista, P.H., Jarnevich, C.S., Young, N.E., Stohlgren, T.J., Talbert, C., Talbert, M., Morisette, J. and Anderson, R., 
	2016. Integrating remote sensing with species distribution models; mapping tamarisk invasions using the software for 
	assisted habitat modeling (SAHM). Journal of visualized experiments: JoVE, (116).

## Authors

Michelle Lam, Marc Healy & Carson Hauck

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

Clark University, Arthur Elmes, and a habitat modeling course that provided inspiration!

# Creating psuedo-absence points for habitat modeling

This tool can be used to create species pseudo-absence points and to merge them with species presence points into a single point feature. The merged Presence-Absence (PA) point feature is often a required input in presence-absence species distribution models (ex. Logistic regression, artifical neural networks).

## Getting Started

The user may either input (1) a .CSV file with species presence points in decimal degree coordinates (WGS 1984) or (2) a point features Shapefile (.SHP) or File Geodatabase Feature Class.

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
	 - attribute field to denote “P” vs. “A”
	 - two integer fields used in modeling (P = 1; A = 0 or 2)

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* 

## Contributing

Please read ....

## Versioning

We use ...

## Authors

Michelle Lam, Marc Healy, & Carson Hauck

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* 

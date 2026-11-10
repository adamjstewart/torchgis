"Install a Packaged TorchGIS release from inside ArcGIS Pro."

"""
Target:

Add this .pyt through Catalog > Toolboxes > Add Toolbox, then run the
Install or Update TorchGIS tool. Select the bundled ZIP or enter a direct
GitHub release asset URL.

The installer runs with ArcPy and the Python standard library, so it can
open before the training dependencies are installed. It stores release files
and virtual environments under %LOCALAPPDATA%/TorchGIS. The installed
training toolbox launches a separate Python process using the interpreter
recorded in python-runtime.txt.

(python-runtime.txt will be a small file the installer creates. It contains the 
path to that environment’s python.exe, so the training tool knows which Python 
to start. User don’t need to open or edit the file. When training finishes, 
ArcGIS Pro adds the resulting GeoTIFF to user's map.)

"""

import hashlib, io, msvcrt, os, re, subprocess, tempfile, arcpy;
from pathlib import Path;

ASSET_NAME = "TorchGIS-ArcGISPro.zip"
DEFAULT_RELEASE_URL = "" # Set this to the release asset's HTTPS download URL to select GitHub by default.
TOOLBOX_NAME = "TorchGeo_ArcGISPro.pyt"
RELEASE_FILES = (TOOLBOX_NAME, "torchgis_worker.py", "requirements.txt", "LICENSE")

"""
torchgis_worker.py will contains the training and prediction code adapted from the
original toolbox. It preprocesses the training mask, trains the land cover 
model with TorchGeo, and writes the prediction as a GeoTIFF.

"""
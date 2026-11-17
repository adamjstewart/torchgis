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

torchgis_worker.py will contains the training and prediction code adapted from the
original toolbox. It preprocesses the training mask, trains the land cover 
model with TorchGeo, and writes the prediction as a GeoTIFF.

"""

import hashlib, io, msvcrt, os, re, subprocess, tempfile, arcpy;
from pathlib import Path;

ASSET_NAME = "TorchGIS-ArcGISPro.zip"
DEFAULT_RELEASE_URL = f"https://github.com/adamjstewart/torchgis/releases/latest/download/{ASSET_NAME}"
TOOLBOX_NAME = "TorchGeo_ArcGISPro.pyt"
RELEASE_FILES = (TOOLBOX_NAME, "torchgis_worker.py", "requirements.txt", "LICENSE")

"""Python toolbox in the ArcGIS Pro Catalog."""

class Toolbox:

    def __init__(self):
        self.label = "TorchGIS Installer"
        self.alias = "torchgis_installer"
        self.tools = [InstallOrUpdateTorchGIS]

class InstallOrUpdateTorchGIS:

    def __init__(self):
        self.label = "Install or Update TorchGIS"
        self.description = "Install a TorchGIS release and add it to the current project."
        self.canRunInBackground = False

    def getParameterInfo(self):
        return []

    def execute(self, parameters, messages):
        install_torchgis(parameters, messages)

"""
Run the installation

Args:
    parameters (list): Tool parameters forwarded by execute().
    messages: ArcGIS Pro message interface used to report the project
    path and download progress.

Returns:
    None.
"""

def install_torchgis(parameters, messages):
    project = arcpy.mp.ArcGISProject("CURRENT")

    if project.isReadOnly:
        raise RuntimeError("Open a writable ArcGIS Pro project before installing.")

    messages.addMessage(f"Current project is {project.filePath}")
    messages.addMessage("Downloading the TorchGIS release...")
    data = read_release()
    messages.addMessage(f"Downloaded {len(data):,} bytes.")

"""
Download the release ZIP and return its bytes.

Args:
    None. The URL comes from DEFAULT_RELEASE_URL.

Returns:
    bytes: The downloaded archive contents.

"""
def read_release():
    with urlopen(DEFAULT_RELEASE_URL, timeout=60) as response:
        return response.read()

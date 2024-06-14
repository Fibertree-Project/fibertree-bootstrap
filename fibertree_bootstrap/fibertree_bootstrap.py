"""IPython fibertree bootstrap code

This module will bootstrap an environment for running fibertree code
in a Jupyter notebook, including downloading and installing the
fibertree Python package if it is now available, e.g., in a Google
Colab environment.  It also impoorts a number of useful packages for
that environment and defines some methods that will bootstrap the
enviroment and also download some data files used by various fibertree
notebooks.

If the module needs to install the fibertree module, it checks for the
existence of the environment variable FIBERTREE_URL and installs from
there, otherwise it uses a default URL.

One of the variables this package creates is `FTD`, which is a
`DisplayTensor()` object. It also creates some aliases to method calls
on the `FTD` object, specifically `displayTensor()`, `displayGraph()`,
`createCanvas()` and `displayCanvas()`. See the documentation for
`DisplayTensor()` for more information.

"""

#
# Startup...
#
print("Running bootstrap")

#
# System imports
#
import os
import sys
import requests
import string
import random
import warnings
import argparse

from functools import *
from pathlib import Path

#
# Import display classes/utilities
#
from IPython.display import display
from IPython.display import Image
from IPython.display import HTML
from IPython.display import Javascript

from tqdm.notebook import tqdm, trange

#
# Math imports
#
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow
from matplotlib import rc

#
# Import ipywidgets
#
import ipywidgets as widgets
from ipywidgets import interact, interactive, fixed, interact_manual

#
# Try to import networkx
#
have_networkx = True
try:
    import networkx as nx
except ImportError:
    have_networkx = False

#
# Use rc to configure animation for HTML5
#
rc('animation', html='jshtml')

#
# Import tensor class
#
import importlib
import subprocess

#
# Import fibertree package (optionally installing it from github)
#
try:
    module_name = 'fibertree'
    importlib.import_module(module_name)
    print(f"The {module_name} module is already installed and available to import")
except ImportError:
    print(f"The {module_name} module is not available. Installing...")

    # Check enviroment variable for repo URL
    if 'FIBERREE_URL' in os.environ:
        url = os.environ['FIBERTREE_URL']
    else:
        url = 'git+https://github.com/Fibertree-Project/fibertree',

    # Define the pip command to execute
    pip_command = ['pip',
                   'install',
                   url,
                   '--quiet']
    # Execute the pip command
    subprocess.call(pip_command)


from fibertree import Payload, Fiber, CoordPayload, Tensor
from fibertree import TensorImage, TensorCanvas, CycleManager
from fibertree import NotebookUtils, TensorMaker, TensorDisplay

#
# Pick up some old utility functions (their use  should be deprecated)
#
from fibertree.notebook.notebook_utils import *

#
# Instantiate the Notebook Utilities class
#
NB = NotebookUtils()

#
# Instantiate the Tensor Display class
#
# This object holds the current styles for displaying and animating the tensors.
#
FTD = TensorDisplay(style="tree",
                    animation="movie",
                    have_ipywidgets=True,
                    create_dialog=False)


#
# Convenience functions that just call the class methods on the FTD
# object created above. 
#
displayTensor = FTD.displayTensor
displayGraph = FTD.displayGraph
createCanvas = FTD.createCanvas
displayCanvas = FTD.displayCanvas


def fibertree_bootstrap(style="tree",
                        animation="movie",
                        logger=False):
    """A public method to bootstrap a fibertree environment in a
    Jupyter notebook.

    This method will initialize some standard data structures
    primarily for displaying fibertrees and fibertree-based
    animations.

    It also creates a dialog to select the global default for display
    and animation styles. Those styles can be overwritten in
    individual calls to `displayTensor()` and `createCanvas()`.

    Parameters
    ----------

    style: string, default="tree"
        A display style. One of: tree, uncompressed or tree+uncompressed

    animation: string, default="movie"
        A animation sytle. One of: movie, spacetime or none

    logger: bool, default=False
        Enable diaglog to control log levels in the fibertree code

    Notes
    -----

    None.

    """

    global NB
    global FTD

    FTD.setupWidgets()
    FTD.setStyle(style)
    FTD.setAnimation(animation)

    if logger:
        NB.showLogging()

    #
    # Create a runall button (but not in colab)
    #
    if 'COLAB_JUPYTER_IP' not in os.environ:
        NB.createRunallButton()


#
# Utility function to download data for use in the notebook environment
#
def download_github_directory(user, repo, directory, verbose=False):
    """ Download files from a github repo's directory

    Parameters
    ----------

    user: string
        The name of a github user or project

    repo: string
        The name of a github repo

    directory: string
        The path name of a directory in the repo

    verbose: Bool, default=False
        Print more progress information

    Notes
    -----

    None.


    """

    api_url = f"https://api.github.com/repos/{user}/{repo}/contents/{directory}"
    response = requests.get(api_url)
    if response.status_code == 200:
        contents = response.json()
        if not os.path.exists(directory):
            os.makedirs(directory)
        for item in contents:
            download_url = item["download_url"]
            file_name = item["name"]
            response = requests.get(download_url)
            if response.status_code == 200:
                with open(os.path.join(directory, file_name), "wb") as file:
                    file.write(response.content)
                    if verbose:
                        print(f"Downloaded: {file_name}")
            else:
                print(f"Failed to download: {file_name}")
    else:
        print("Failed to fetch directory contents.")


def download_data(verbose=True):
    """Download fibertree data files from the fibertree-notebooks repo

    Put the data files in `./data', but skips the download if the
    directory `data/` exists somewhere nearby.

    Parameters
    ----------

    verbose: Bool, default=False
        Print more progress information

    Returns
    -------

    path: Path
        The path to the data directory

    Notes
    -----

    None.

    """

    for data_dir in ["../../data", "../data", "./data"]:
        if os.path.exists(data_dir):
            if verbose:
                print(f"Data directory exists at: {data_dir}")
            return Path(data_dir)

    download_github_directory("Fibertree-Project",
                              "fibertree-notebooks",
                              "data",
                              verbose=verbose)

    data_dir = "./data"
    print(f"Data directory downloaded to: {data_dir}")
    return Path(data_dir)


#
# Create datafile name (for backwards compatibility)
#
def datafileName(filename):
    """ Construct fibertree data filename including directory

    Parameters
    ----------

    filename, string
        The name of a fibertree data file (without full path)

    Returns
    -------

    path: Path
        The full path to the data file

    Notes
    -----

    Exists for backwards compatibility.

    """

    data_dir = download_data(verbose=False)

    return data_dir / filename

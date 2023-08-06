#!/usr/bin/env python3

"""
The grassgis module contains functions for using GRASS GIS
as data warehouse for data from geonorge.no

This module is incomplete!

Use the module like this:

.. code-block:: python

   import os
   # Import downloader class from module
   from osgeonorge.grassgis import GRASSGISAdapter
   # Initialize class
   ogng = GRASSGISAdapter(grassdata="/data/grassdata", cores=5)

"""


import subprocess
from osgeonorge.utils import norwegian_to_ascii, compile_ogr_cmd, ogr_casts
import re


class GRASSGISAdapter:
    """
    Basic class for importing data from geonorge.no into GRASS GIS

    """

    def __init__(
        self,
        grassdata="./",
        cores=1,
        verbose=True,
    ):
        #: Attribute containg the path to the GRASS GIS database
        self.grassdata = grassdata
        #: Attribute containg the path to the GRASS GIS database
        self.cores = cores


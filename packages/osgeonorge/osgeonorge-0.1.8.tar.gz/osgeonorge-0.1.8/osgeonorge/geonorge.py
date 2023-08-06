#!/usr/bin/env python3

"""
The geonorge module contains functions and global variables for
interaction with ATOM feeds and download API of geonorge.no

Use the module like this:

.. code-block:: python

   # Import module
   from osgeonorge.geonorge import GeonorgeAdapter
   # Initialize class
   gn_download = GeonorgeAdapter()
   # List available feeds in a pretty table format
   gn_download.print_feeds()

This returns something like this:

.. code-block:: python

   AdminstrativeEnheter GML   30-Oct-2019 05:27 1677 https://nedlasting.geonorge.no/geonorge/ATOM-Feeds/AdminstrativeEn...

Next pick a dataset and format to parse and download:

.. code-block:: python

   # Parse feed of dataset 'Sprstrandsoner' in 'FGDB' format
   gn_download.parse_feed('Sprstrandsoner', 'FGDB')
   # Get a list of datasets that cover the whole country
   gn_download.get_data_list(coverage="Landsdekkende", crs=(3045, 5973, 25833))


Finally, download the currently selected dataset(s):

.. code-block:: python

   gn_download.download_datasets()
   gn_download.extract_datasets()
   gn_download.get_files()
   gn_download.get_metadata()

Now you are ready to e.g. import data to PostgreSQL using the
:obj:`~osgeonorge.postgres.PostGISImporter`

"""

import os
import urllib.request
from xml.etree import ElementTree as ET
from html.parser import HTMLParser
from multiprocessing import Pool

# import sys
import re
import warnings

import requests
from osgeonorge.utils import extract_zip, slice_dict, extract_metadata, remove_suffixes


class GeonorgeAdapter:
    """
    Basic class for listing, downloading, extracting and parsing  data from
    ATOM feeds in geonorge.no

    :todo: a) add option to store logs
           b) option to only update if needed and also clean in future
           Globbing the download_dir could help
           c) add option to remove zip files
    """

    #: Attribute containg a dict with supported formats and suffix keys for extracting data from zip archives
    ogr_supported_formats = {
        "CSV": (".csv"),
        "FGDB": (".gdb/gdb"),
        "GEOJSON": (".json"),
        "GML": (".gml"),
        "GPX": (".gpx"),
        "GeoJSON": (".json"),
        "POSTGIS": (".backup"),
        "PostGIS": (".backup"),
        "SOSI": (".sos"),
        "Shape": (".shp"),
        "SpatiaLite": (".sqlite"),
        "XYZ": ("xyz"),
    }
    #: Attribute containg a dict with supported formats and suffix keys for extracting data from zip archives
    gdal_supported_formats = {
        "BIN": ".bil",
        "CSV": ".csv",
        "DEM": ".dem",
        "GeoTIFF": (".tif", ".tiff", ".gtif", ".gtiff"),
        "IMG": (".img"),
        "JPEG": (".jpg", ".jpeg"),
        "MrSID": (".mr", ".sid"),
        "SpatiaLite": None,
        "TIFF": (".tif", ".tiff", ".gtif", ".gtiff"),
        "XYZ": (".xyz"),
    }
    #: Attribute containg a tuple with (currently) unsupported or non-spatial formats
    currently_unsupported_formats = (
        "AI",
        "DAT",
        "DLL",
        "EMF",
        "ENH",
        "JSON",
        "NED",
        "PDF",
        "PPTX",
        "S57",
        "XLSX",
    )
    #: Attribute containg a tuple with (currently) tested formats
    currently_tested_formats = "FGDB"
    #: Arrtibute containg a tuple of target EPSG codes (defaults to country wide valid EPSG codes)
    target_crs = (32633, 25833, 3045, 5973)

    def __init__(
        self,
        atom_url="https://nedlasting.geonorge.no/geonorge/ATOM-Feeds",
        download_dir="./",
        work_dir="./",
        credits_file=None,
        cores=1,
        verbose=True,
    ):
        #: Attribute containg the URL to the website listing available ATOM feeds from geonorge.no
        self.atom_url = atom_url
        #: Attribute containg aictionary with parsed list of ATOM feeds
        self.feeds = {}
        self.get_feeds()
        #: Attribute containg a set of all available formats in geonorge feeds
        self.available_formats = {k for val in self.feeds.values() for k in val.keys()}
        #: Attribute containg directory to which data is downloaded or written to
        self.download_dir = download_dir
        #: Attribute containg the working directory where zip files are extracted to
        self.work_dir = work_dir
        #: Attribute containg dictionary with metadata of the current, parsed dataset feed
        self.current_feed_dict = {}
        #: Attribute containg dictionary the format of the current, parsed dataset feed
        self.current_feed_format = None
        #: Attribute containg dictionary with metadata of the current, parsed dataset of a selected format
        self.current_data_dict = {}
        #: Attribute containg a list of dictionaries with members of the zip files downloaded and extracted from the current_data_dict
        self.current_zip_content = None
        #: Attribute containg a list of OGR readable files in the zip files downloaded and extracted from the current_data_dict
        self.current_ogr_files = None
        #: Attribute containg geonorge credits as tuple (username, password)
        self.user_credits = (None, None)
        self.get_geonorge_credits(credits_file)
        #: Number of cores to use for parallel download (if relevant)
        self.cores = cores
        #: Attribute to define if verbose messages should be given
        self.verbose = verbose
        # Check if download directory is writable
        self.__check_permissions(self.download_dir, "Download")
        # Check if working directory is writable
        self.__check_permissions(self.work_dir, "Extraction of zip files")

    def __check_permissions(self, directory, mode, log_level="warning"):
        """"""
        if not os.access(directory, os.W_OK):
            user_message = "Cannot write to directory {directory}. {mode} will fail."
            if log_level == "warning":
                warnings.Warning(user_message)
            else:
                raise OSError(user_message)

    def get_feed(self, dataset, ogr_format):
        """
        Extract dataset information from ATOM feed and stores the meatadata
        parsed into a dictionary in the
        :attr:`~osgeonorge.geonorge.GeonorgeAdapter.current_feed_dict` attribute.

        Currently parsing is mostly tailored at "kommuneplan" feed

        Basic elements handled so far are:

        - '{http://www.w3.org/2005/Atom}subtitle'
        - '{http://www.w3.org/2005/Atom}link'
        - '{http://www.w3.org/2005/Atom}updated'
        - '{http://www.w3.org/2005/Atom}generator'
        - '{http://www.w3.org/2005/Atom}rights'
        - '{http://www.w3.org/2005/Atom}entry'
        - '{http://www.w3.org/2005/Atom}title'
        - '{http://www.w3.org/2005/Atom}id'

        Datasets are listed as entries

        :param dataset: Dataset of which the ATOM feed XML document should be parsed
        :type dataset: str
        :param ogr_format: OGR readable format to fetch ATOM feed for
                           (see :attr:`~osgeonorge.geonorge.GeonorgeAdapter.available_formats`).
        :type ogr_format: str

        """
        if ogr_format not in self.ogr_supported_formats:
            raise ValueError(f"Requested format is currently not supported.")
        if ogr_format not in self.available_formats:
            raise ValueError(f"Requested format is currently not available at geonorge.no.")
        if dataset not in self.feeds:
            raise ValueError(f"No ATOM feed found for dataset {dataset} on geonorge.")
        if ogr_format not in self.feeds[dataset]:
            raise ValueError(
                f"Format {ogr_format} not found for dataset {dataset} on geonorge."
            )

        feed_dict = {}
        feed = requests.get(self.feeds[dataset][ogr_format]["url"])
        root = ET.fromstring(feed.text)
        for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
            updated = entry.find("{http://www.w3.org/2005/Atom}updated").text
            title = [
                e.strip()
                for e in entry.find("{http://www.w3.org/2005/Atom}title").text.split(
                    ","
                )
            ]
            url = entry.find("{http://www.w3.org/2005/Atom}id").text.replace(
                f"_{updated}", ""
            )
            crs = [
                e.attrib["term"]
                for e in entry.findall("{http://www.w3.org/2005/Atom}category")
                if "scheme" in e.attrib
                and e.attrib["scheme"] == "http://www.opengis.net/def/crs/"
            ][0]
            feed_dict[url.split("/")[-1]] = {
                "updated": updated,
                "title": title,
                "url": url,
                "crs": crs,
            }

        self.current_feed_dict = feed_dict
        self.current_feed_format = ogr_format

    def get_feeds(self):
        """
        Method to fetch available ATOM feeds and store the results as a dict
        in the :attr:`~osgeonorge.geonorge.GeonorgeAdapter.feeds` attribute.

        :param atom_url: URL to ATOM feed XML document to parse
        :type atom_url: str
        """
        atom_list_dict = {}
        parse_atom = ParseATOMList()
        with urllib.request.urlopen(self.atom_url) as response:
            parse_atom.feed(response.read().decode())
        for key, val in parse_atom.feed_dict.items():
            key_elements = key.replace(".xml", "").split("_AtomFeed")
            if len(key_elements) != 2:
                continue
            if key_elements[0] in atom_list_dict:
                atom_list_dict[key_elements[0]][key_elements[1]] = {
                    "url": f"{self.atom_url}/{key}",
                    "updated": val[1][0],
                    "size": val[1][1],
                }
            else:
                atom_list_dict[key_elements[0]] = {
                    key_elements[1]: {
                        "url": f"{self.atom_url}/{key}",
                        "updated": val[1][0],
                        "size": val[1][1],
                    }
                }

        self.feeds = atom_list_dict

    def get_geonorge_credits(self, credits_file=None):
        """
        Method to fetch user credits for Geonorge.no and store it in the
        :attr:`~osgeonorge.geonorge.GeonorgeAdapter.user_credits` attribute.
        Credentials for authentication to geonorge API can be either given
        using a credtis_file (see .geonorge.example) or by defining
        environment variables:

        :envvar:`GEONORGE_USER`
        :envvar:`GEONORGE_PASSWORD`

        The user's :envvar:`HOME` directoy is allways searched for a .geonorge
        credits file.

        Username and password need to represent BAAT authentication (and not GeoID)

        :param credits_file: Path to credis file to read
        :type credits_file: str
        """
        # Get authentication
        user = os.environ.get("GEONORGE_USER")
        password = os.environ.get("GEONORGE_PASSWORD")

        credits_file = credits_file or os.path.expanduser("~/.geonorge")
        if os.path.exists(credits_file):
            try:
                with open(credits_file, "r") as geonorge_credits:
                    user, password = geonorge_credits.read().split("\n")[0:2]
            except OSError as e:
                raise e
        if not all((user, password)):
            warnings.Warning(
                "No authentication provided. Downloading data is thus not possible.\n"
                "Please provide authentication information"
            )
        self.user_credits = (user, password)

    def print_feeds(self):
        """
        Method to print available ATOM feeds in table like style
        """
        for key, val in self.feeds.items():
            for k, v in val.items():
                print(f"{key:<75} {k:<7} {v['updated']:<17} {v['size']:<8} {v['url']}")

    def print_datasets(self):
        """
        Method to print a list of available datasets from ATOM feeds
        """
        print("\n".join(self.feeds.keys()))

    def print_all_formats(self):
        """
        Method to print a list of all available formats from ATOM feeds
        """
        print("\n".join(self.available_formats))

    def print_currect_feed(self):
        """
        Method to print content of an ATOM feed in table like style
        """
        if not self.current_feed_dict:
            warnings.Warning("No feed initialized. Run 'get_feed' method first.")
        else:
            for key, val in self.current_feed_dict:
                print(
                    f"{key:<75} {val['updated']:<20} {val['crs'].replace('EPSG:', ''):<5} {val['title'][-1]:<15}"
                )

    def get_data_dict(self, coverage=None, crs=(3045, 5973, 25833)):
        """
        Method to store metadata of a selected coverage and crs from the
        :attr:`~osgeonorge.geonorge.GeonorgeAdapter.current_feed_dict`
        in the :attr:`~osgeonorge.geonorge.GeonorgeAdapter.current_data_dict`
        attribute. A current feed has to be fetched beforehand with the
        :func:`~osgeonorge.geonorge.GeonorgeAdapter.get_feed` method.

        :param coverage: Dataset whos feed(s) to parse
        :type coverage: str
        :param crs: Coordinate reference system of feed(s) to parse
        :type crs: tuple of int
        """
        if coverage and crs:
            self.current_data_dict = {
                key: val
                for key, val in self.current_feed_dict.items()
                if val["crs"] in (f"EPSG:{c}" for c in crs)
                and coverage in val["title"][-1]
            }
        elif coverage:
            self.current_data_dict = {
                key: val
                for key, val in self.current_feed_dict.items()
                if coverage in val["title"][-1]
            }
        elif crs:
            self.current_data_dict = {
                key: val
                for key, val in self.current_feed_dict.items()
                if val["crs"] in (f"EPSG:{c}" for c in crs)
            }

    def download_current_datasets(self):
        """
        Method to download data from the
        :attr:`~osgeonorge.geonorge.GeonorgeAdapter.current_feed_dict` attribute
        """
        self.__check_permissions(self.download_dir, "Download", log_level="error")
        if len(self.current_data_dict) == 1 or self.cores == 1:
            [
                self.__download_geonorge({key: val})
                for key, val in self.current_data_dict.items()
            ]
        elif len(self.current_data_dict) > 1 and self.cores > 1:
            with Pool(self.cores) as p:
                p.map(
                    self.__download_geonorge,
                    [dict_chunk for dict_chunk in slice_dict(self.current_data_dict)],
                )
        else:
            warnings.Warning("Nothing to download in current datasets")

    def __download_geonorge(self, atom_dict):
        """
        Private method to download all data in the the atom_dict from geonorge nedlasting API

        :todo: Should only update if needed and also clean in future
               Globbing the download_dir could help

        """
        # Setup http session
        s = requests.Session()

        # Check provided authentication
        if (
            len(self.user_credits) != 2
            or type(self.user_credits) != tuple
            or not all(
                [type(auth_element) == str for auth_element in self.user_credits]
            )
        ):
            raise ValueError("No or invalid authentication provided.")

        # Authenticate with basic http authentication by adding header to session
        s.auth = self.user_credits

        # Download dict content
        for file_id, file_dict in atom_dict.items():
            if self.verbose:
                print(f"Downloading {file_dict['url']}...")
            zip_file = s.get(file_dict["url"], allow_redirects=True)
            if not zip_file.ok:
                zip_file.raise_for_status()
            with open(os.path.join(self.download_dir, file_id), "wb") as f:
                f.write(zip_file.content)

    def extract_current_datasets(self):
        """
        Method to extract data from downloaded zip file(s) from the
        :attr:`~osgeonorge.geonorge.GeonorgeAdapter.current_feed_dict` attribute.
        Datasets have to be downloaded beforehand with the
        :func:`~osgeonorge.geonorge.GeonorgeAdapter.download_datasets` method.
        A list of extracted files is stored in the
        :attr:`~osgeonorge.geonorge.GeonorgeAdapter.current_zip_content` attribute.
        """
        self.__check_permissions(
            self.work_dir, "Extraction of zip files", log_level="error"
        )
        if len(self.current_data_dict) == 1 or self.cores == 1:
            self.current_zip_content = [
                extract_zip(
                    os.path.join(self.download_dir, f"{dataset_id}.zip"),
                    workdir=self.work_dir,
                )
                for dataset_id in self.current_data_dict
            ]
        elif len(self.current_data_dict) > 1 and self.cores > 1:
            with Pool(self.cores) as p:
                self.current_zip_content = p.starmap(
                    extract_zip,
                    [
                        (
                            os.path.join(self.download_dir, f"{dataset_id}.zip"),
                            self.work_dir,
                        )
                        for dataset_id in self.current_feed_dict.keys()
                    ],
                )
        else:
            warnings.Warning("Nothing to extract")

    def get_current_ogr_files(self):
        """
        Method to extract OGR readable file data from downloaded zip files from the
        :attr:`~osgeonorge.geonorge.GeonorgeAdapter.current_feed_dict` attribute.
        Datasets have to be extracted beforehand with the
        :func:`~osgeonorge.geonorge.GeonorgeAdapter.extract_datasets` method.
        """
        ogr_files_in_zips = {}
        print(self.ogr_supported_formats[self.current_feed_format])
        for zip_file, zip_content in self.current_zip_content:
            for member in zip_content:
                if member.endswith(self.ogr_supported_formats[self.current_feed_format]):
                    print(member)
            ogr_files_in_zips[zip_file] = [
                remove_suffixes(member, (f"{os.sep}gdb"))
                for member in zip_content
                if any([member.endswith(suffix) for suffix in self.ogr_supported_formats[self.current_feed_format]])
            ]
        self.current_ogr_files = ogr_files_in_zips

    def get_current_metadata(self, split_by_objtype=False, layer=None):
        """
        Method to extract metadata from ogr readable files in the downloaded data from the
        :attr:`~osgeonorge.geonorge.GeonorgeAdapter.current_members` attribute.
        Datasets have to be extracted beforehand with the
        :func:`~osgeonorge.geonorge.GeonorgeAdapter.extract_datasets` method
        and ogr readable files listed with the
        :func:`~osgeonorge.geonorge.GeonorgeAdapter.get_ogr_files` method.
        Results are stored in the
        :attr:`~osgeonorge.geonorge.GeonorgeAdapter.current_members_metadata` attribute.
        """
        self.current_ogr_files_metadata = {
            member: extract_metadata(
                os.path.join(self.work_dir, member),
                target_srs=GeonorgeAdapter.target_crs,
                split_by_objtype=False,
                layer_name=layer,
            )
            for member in self.current_members
        }


class ParseATOMList(HTMLParser):
    """
    A simple, basic html parser class to extract links to ATOM feeds in geonorge.no
    together with attributes (time of last update, size)
    """

    def __init__(self):
        super().__init__()
        self.reset()
        self.count = 0
        self.tag = None
        self.href = None
        self.feed_dict = {}

    def handle_starttag(self, tag, attrs):
        """
        Extract href tags and stor info a class attribute
        """
        self.tag = tag
        self.count += 1

        if tag == "a":
            self.href = attrs[0][1]
            self.feed_dict[attrs[0][1]] = []

    def handle_data(self, data):
        """
        Get data stored with href tags
        """
        if self.tag == "a":
            self.feed_dict[self.href].append(re.split(r"\s{2,}", data.strip()))

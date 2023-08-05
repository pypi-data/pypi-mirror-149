#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 16:50:58 2022

@author: bouwman
"""
import os
import shutil
from urllib.parse import urlencode
from urllib.parse import urlparse
from pathlib import Path
import requests
import zipfile
import io
import time

from cascade_filtering import __path__
from cascade_filtering import __version__ as __CASCADE_FILTERING_VERSION

__all__ = ['check_cascade_version', 'setup_examples', 'get_zip_data_from_git',
           'copy_data_from_git', 'copy_data_from_distribution',
           'CASCADE_FILTERING_EXAMPLE_DIR']

_CASCADE_FILTERING_DIST_EXAMPLE_PATH = Path(os.path.dirname(__path__[0])) / \
    'examples/'

CASCADE_FILTERING_EXAMPLE_DIR = \
    Path(os.environ.get('CASCADE_STORAGE_PATH',
                        str(Path.home() / 'CASCADeSTORAGE/'))) / \
        'examples_filtering/'

__DATA_DIRS = ['data/', 'notebooks/', 'config_files/']


def check_cascade_version(version: str) -> str:
    """
    Check if a release version of the cascade package excists on Gitlab.

    Parameters
    ----------
    version : 'str'
        Version of the cascade package.

    Returns
    -------
    used_version: 'str'
        Online CASCADe-filtering version from which the data will be downloaded.

    """
    __check_url = f"https://gitlab.com/jbouwman/CASCADe-filtering/-/releases/{version}/"
    response = requests.get(__check_url)
    if response.status_code == 200:
        used_version = version
    else:
        # warnings.warn(f'No releases found for cascade version {version}')
        used_version = 'main'
    return used_version


def setup_examples(overwrite=False) -> None:
    """
    Setup directory structure and data files needed by CASCAde. 

    Parameters
    ----------
    overwrite : 'bool', optional
        Default value is False    

    Returns
    -------
    None

    """

    if _CASCADE_FILTERING_DIST_EXAMPLE_PATH.is_dir():
        
        print("Copying example data from distribution to user defined directory.")

        copy_data_from_distribution(overwrite=overwrite)

    else:
 
        print("Copying example data from git repository to user defined directory. " 
              "This can take a moment depending on the connection speed.")

        copy_data_from_git(overwrite=overwrite)

def copy_data_from_distribution(overwrite=False) -> None:
    """
    Copy the data needed by CASCADe to the user defined directory.

    Parameters
    ----------
    overwrite : 'bool', optional
        Default value is False

    Returns
    -------
    None

    """
    if CASCADE_FILTERING_EXAMPLE_DIR.is_dir() & (not overwrite):
        shutil.rmtree(CASCADE_FILTERING_EXAMPLE_DIR)   
    
    dest = shutil.copytree(_CASCADE_FILTERING_DIST_EXAMPLE_PATH,
                           CASCADE_FILTERING_EXAMPLE_DIR,
                           dirs_exist_ok=True)
    print("Copied CASCADe-filtering examples to directory: {}".format(dest))


def copy_data_from_git(overwrite=False) -> None:
    """
    Reset the local CASCAde data with the data from the git repository.

    Parameters
    ----------
    overwrite : 'bool'    

    Returns
    -------
    None

    """
    online_version = check_cascade_version(__CASCADE_FILTERING_VERSION)
    git_url = (f"https://gitlab.com/jbouwman/CASCADe-filtering/-/archive/"
               f"{online_version}/"
               f"cascade-filtering-{online_version}.zip?")

    query_list = [{'path': f'examples/{section}'}
                  for section in __DATA_DIRS]   
    for query in query_list:
        get_zip_data_from_git(CASCADE_FILTERING_EXAMPLE_DIR, git_url,
                              query, overwrite=overwrite)
        time.sleep(1)

def get_zip_data_from_git(data_path_archive: Path,
                          url_distribution: str,
                          query: dict,
                          overwrite=False) -> None:
    """
    Copy the data needed by CASCADe to the user defined directory from git.

    Parameters
    ----------
    data_path_archive : 'pathlib.Path'
        Path to the user defined data repository for CACADe.
    url_distribution : 'str'
        URL of the git repository from which data is copied to user
        defined location.
    query : 'dict'
        Dictionary used to constuct query to git repository to download zip file
        containing the data to be copied. The dictionary key is always 'path'
        with the value pointing to a subdirectory in the git repository.
    overwrite : 'bool', optional
        If true, excisting directories are not deleted first before copying.
        The default is False.

    Returns
    -------
    None

    """

    new_path = data_path_archive / Path(*Path(query['path']).parts[1:])
    if new_path.is_dir() & (not overwrite):
        shutil.rmtree(new_path)    
    
    # some header info just to make sure it works.
    header = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
               "(KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
    url_repository = url_distribution + urlencode(query)
    req = requests.get(url_repository, headers=header, allow_redirects=False)

    with zipfile.ZipFile(io.BytesIO(req.content)) as archive:
         for file in archive.namelist():
             if file.endswith('/'):
                 continue
             p = Path(file)
             sub_index = p.parts.index(new_path.stem)
             sub_path = Path(*p.parts[sub_index:])
             new_destintion = data_path_archive / sub_path
             zipInfo = archive.getinfo(file)
             zipInfo.filename = p.name
             new_destintion.parent.mkdir(parents=True, exist_ok=True)
             archive.extract(zipInfo, new_destintion.parent)

    # clean up temperory zip directory. Not present if version is master?
    base = Path(urlparse(url_distribution).path).stem + '-'
    temp_zip_dir = base +'-'.join(Path(query['path']).parts)
    shutil.rmtree(data_path_archive / temp_zip_dir, ignore_errors=True)

    print("Updated cascade data in directory: {}".
          format(str(Path(*Path(query['path']).parts[1:]))))

if __name__ == '__main__':
    setup_examples()
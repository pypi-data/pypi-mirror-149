import setuptools
import os
import pathlib

def package_files(directory):
    exclude = ['data', 'examples']
    paths = []
    for (path, directories, filenames) in os.walk(directory, topdown=True):
        directories[:] = [d for d in directories if d not in exclude]
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

# The directory containing this file, MUST be RELATIVE
HERE = pathlib.Path(__file__)
HERE = HERE.relative_to(HERE.parent).parent

# The text of the README file
README = (HERE / "README.md").read_text()

extra_files = package_files((HERE/'configuration_files/').as_posix())

scripts =  [(HERE / 'scripts/setup_cascade-filtering.py').as_posix(),]

config = {
    'name': 'CASCADe-filtering',
    'description': 'CASCADe filtering: Calibration of trAnsit Spectroscopy using CAusal Data filtering module.',
    'long_description': README,
    'long_description_content_type': "text/markdown",
    'author': 'Jeroen Bouwman',
    'url': 'https://jbouwman.gitlab.io/CASCADe-filtering/',
    'download_url': 'https://gitlab.com/jbouwman/CASCADe-filtering',
    'author_email': 'bouwman@mpia.de',
    'version': '1.0.0',
    'python_requires': '>=3.7, <3.10',
    'license': 'GNU General Public License v3 (GPLv3)',
    'classifiers': ["Programming Language :: Python :: 3",
                    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
                    "Operating System :: OS Independent",
                    'Intended Audience :: Science/Research',
                    'Topic :: Scientific/Engineering :: Astronomy',
                    ],
    'packages': setuptools.find_packages(exclude=("tests_private", "docs", "examples",)),
    'include_package_data': True,
    'package_data': {"": extra_files},
    'install_requires': ['astropy', 'scipy',
                         'numpy==1.21.5', 'configparser', 'jupyter',
                         'matplotlib', 'tqdm', 'seaborn',
                         'pytest', 'scikit-image', 'sphinx', 'alabaster',
                         'pyfiglet', 'six', 'colorama', 'termcolor',
                         'cython', 'numba==0.55.1','ray[default]'
                         ],
    'scripts': scripts,
    'data_files': [('', [(HERE / 'README.md').as_posix(),
                         (HERE / 'LICENSE.txt').as_posix()])]
}

setuptools.setup(**config)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gloria']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.4.3,<4.0.0', 'netCDF4>=1.5.2,<2.0.0', 'numpy>=1.17.2,<2.0.0']

entry_points = \
{'console_scripts': ['gloria_to_nc = gloria.gloria_to_nc:main',
                     'gloria_to_txt = gloria.gloria_to_txt:main',
                     'plot_gloria = gloria.plot_gloria:main',
                     'read_gloria = gloria.read_gloria:main',
                     'write_gloria = gloria.write_gloria:main']}

setup_kwargs = {
    'name': 'bas-gloria',
    'version': '0.2.0',
    'description': 'Package for working with GLORIA side-scan sonar files',
    'long_description': "# gloria\n\nThis project enables GLORIA .dat files to be read, rewritten, and converted.\n\n## The gloria package\n\nThe `GLORIAFile` class is a context manager for GLORIA files.  The class contains methods for reading the scan header and data in the .dat file, rewriting the scan header and subsetting the data, and converting the file to netCDF4.\n\n## Install\n\nThe package can be installed from PyPI (note the package distribution name):\n\n```bash\n$ pip install bas-gloria\n```\n\n## Simple utility scripts\n\nThe package contains a number of scripts for converting from/to netCDF, plotting the data etc.  When installing the package (e.g., via `pip install`) then these scripts are available as commands and added to the `PATH`.  So for instance, you can just call `gloria_to_nc`.  If running the scripts from a `clone` of the source code repository, then they need to be run as modules, e.g. `python -m gloria.gloria_to_nc`.\n\n### gloria_to_nc.py\n\nThis script converts a GLORIA .dat file to netCDF4.  The default output netCDF filename has the same name as the input .dat file, but with a .nc file suffix.  Optionally an alternative output netCDF filename can be explicitly given.\n\n```bash\npython3 -m gloria.gloria_to_nc infile.dat [outfile.nc]\n```\n\nEach scan (header and data) appears as a netCDF4 group in the output file.  The group is named `scan<n>`, where `<n>` is the scan number.  The scan header items become attributes of the group in the netCDF file, and the data are stored as a `sonar_samples`-long 1D data array.\n\n### gloria_to_txt.py\n\nThis script converts a GLORIA .dat file to a simple ASCII text file.  The output text filename has the same name as the input .dat file, but with a .txt file suffix.  Optionally an alternative output text filename can be explicitly given.\n\n```bash\npython3 -m gloria.gloria_to_txt infile.dat [outfile.txt]\n```\n\nThe format of the text file is a straightforward rendering of the binary .dat format to text, i.e. for each scan, the header items are output followed by the data.\n\n### plot_gloria.py\n\nThis script will plot the scans from the given file as a sonargram, in its default mode (`--sonargram`).  In its other mode (`--scans`), it will plot samples from the first `nrows` x `ncols` scans, in an `nrows` by `ncols` grid of plots.  By default `nrows` = `ncols` = 1, hence only the first scan is plotted.  The file can be either a GLORIA .dat file, or a converted netCDF file.\n\n```bash\npython3 -m gloria.plot_gloria [-h] [-r | -s] [-g NROWS NCOLS] [-c CONTRAST] [-m CMAP] [-o out_file.{png,tiff,pdf}] in_file.{dat,nc} [out_file.{png,tiff,pdf}]\n```\n\nAlternatively, instead of displaying the plot, the script can save the plot to an output file.  This can be speficied by *either* the `--output-file` option, *or* simply as a second, optional positional argument, for example to save as a PNG:\n\n```bash\npython3 -m gloria.plot_gloria in_file.dat out_file.png\n```\n\nWhen saving the plot, any of the formats supported by matplotlib can be specified by using the appropriate file suffix.  For example, an output file named `out_file.tiff` will save as a TIFF file, `out_file.pdf` will save as a PDF etc.\n\n### read_gloria.py\n\nThis script will read the given GLORIA .dat file, and print the number of scans in the file, and a summary of the first scan.  This summary contains the length of the sonar samples array, the scan header, and the *head* of the data array (by default the first 10 samples), to give an initial simple look at the data.\n\nThe script's primary purpose is as a simple example of how to use the `GLORIAFile` class to read a GLORIA .dat data file.\n\n```bash\npython3 -m gloria.read_gloria filename.dat\n```\n\n### write_gloria.py\n\nThis script will read the given input GLORIA .dat file, and write the scans (header and data) to the given output GLORIA .dat file.  Optionally a subset of the input data can be written out, specified as the first `scans` scans, and the first `samples` samples of these scans.  If `scans` and `samples` are not specified, then the output file is identical to the input file.  Note that as the GLORIA record format is fixed-width, when subsetting samples the unwanted samples are actually set to zero, to preserve the correct record length.\n\nThe script's primary purpose is as a simple example of how to use the `GLORIAFile` class to rewrite a GLORIA .dat data file.\n\n```bash\npython3 -m gloria.write_gloria [-s SCANS] [-a SAMPLES] infile.dat outfile.dat\n```\n\n",
    'author': 'Paul Breen',
    'author_email': 'pbree@bas.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/antarctica/bas-gloria',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

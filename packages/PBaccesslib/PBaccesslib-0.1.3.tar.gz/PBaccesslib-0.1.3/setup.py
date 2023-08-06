__author__ = 'Jordi Arellano'
__copyright__ = 'Copyleft 2021'
__date__ = '05/04/22'
__credits__ = ['Jordi Arellano', ]
__license__ = 'CC0 1.0 Universal'
__version__ = '0.1.3'
__maintainer__ = 'Jordi Arellano'
__email__ = 'jarellan@ifae.es'

from setuptools import setup
import os

here = os.path.abspath(os.path.dirname(__file__))
requirementPath = os.path.join(here, 'requirements.txt')
install_requires = []  # Here we'll get: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

# Read README and CHANGES files for the long description

with open(os.path.join(here, 'README.md')) as fh:
    long_description = fh.read()

setup(name="PBaccesslib",
      include_package_data=True,
      version=__version__,
      description="This lib controls Probecard.",
      long_description_content_type="text/markdown",
      long_description=long_description,
      python_requires='>=3',
      packages=["PBaccesslib", "PBaccesslib.characteritzation", "PBaccesslib.characteritzation.logic",
                "PBaccesslib.wafer_test"],
      package_data={'': [f"{os.path.join(here, 'PBaccesslib/data/*.npy')}", ]},
      license="CC0 1.0 Universal",
      zip_safe=False,
      classifiers=[
          "Development Status :: 4 - Beta",
          "Programming Language :: Python :: 3",
      ],
      setup_requires=['wheel'],
      install_requires=["pandas==1.4.1", "numpy==1.22.3", "python-dateutil==2.8.2", "pytz==2022.1", "six==1.16.0",
                        "typing-extensions==4.1.1", "Excelacceslib==0.0.4", "K2600acceslib==0.0.3",
                        "Commacceslib==0.0.5", "Bconvertacceslib==0.0.1"],
      )

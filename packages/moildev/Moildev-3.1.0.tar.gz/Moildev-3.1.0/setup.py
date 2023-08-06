import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '3.1.0'
PACKAGE_NAME = 'Moildev'
AUTHOR = 'Haryanto'
AUTHOR_EMAIL = 'haryanto@o365.mcut.edu.tw'
URL = 'https://github.com/MoilOrg/moildev'

LICENSE = 'MIT License '
DESCRIPTION = 'Moildev is a sophisticated fisheye image processing library'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      'opencv-python>=4.2.0.32',
      'numpy>=1.18.1',
      'setuptools>56.0.0'
]

setup(name=PACKAGE_NAME,
      version=VERSION,
      include_package_data=True,
      package_data={"": ['MoilCV.cpython-36m-x86_64-linux-gnu.so','MoilCV.cpython-37m-x86_64-linux-gnu.so', 'MoilCV.cpython-38-x86_64-linux-gnu.so', 'MoilCV.cpython-39-x86_64-linux-gnu.so','MoilCV.cpython-310-x86_64-linux-gnu.so', 'MoilCV.cp36-win_amd64.pyd', 'MoilCV.cp37-win_amd64.pyd', 'MoilCV.cp38-win_amd64.pyd', 'MoilCV.cp39-win_amd64.pyd','MoilCV.cp310-win_amd64.pyd']},
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages(),
      python_requires='>=3.6',
      )

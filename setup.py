from distutils.core import setup

import undoredo

with open("README.md", "r") as fp:
    long_description = fp.read()

setup(name="undoredo",
      version=undoredo.__version__,
      author="Ross Anderson",
      author_email="ross.anderson@ualberta.ca",
      url="https://github.com/rosshamish/undoredo/",
      download_url = 'https://github.com/rosshamish/undoredo/tarball/' + undoredo.__version__,
      description="undo/redo functionality for arbitrary python classes",
      long_description=long_description,
      keywords=[],
      classifiers=[],
      license="GPLv3",

      py_modules=["undoredo"],
	)

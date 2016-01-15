from distutils.core import setup

import six

with open("README.md", "r") as fp:
    long_description = fp.read()

setup(name="undoredo",
      version=undoredo.__version__,
      author="Ross Anderson",
      author_email="ross.anderson@ualberta.ca",
      url="http://pypi.python.org/pypi/undoredo/",
      py_modules=["undoredo"],
      description="undo/redo functionality for arbitrary python classes",
      long_description=long_description,
      license="GPLv3",
      classifiers=[]
	)

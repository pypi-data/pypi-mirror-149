import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tolip",                     # This is the name of the package
    version="0.0.1",                        # The initial release version
    author="Suyash Bhattarai",                     # Full name of the author
    description="Tools Library in Python",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/x-rst",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    py_modules=["tolip"],             # Name of the python package
    package_dir={'':'tolip'},     # Directory of the source code of the package
    url = 'https://github.com/Su-yes/tolip',
    project_urls = {
        "Documentation" : "https://tolip.readthedocs.io/en/latest/",
    
    }
)
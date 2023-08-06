
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="EZ2",                             # This is the name of the package
    version="0.0.5",                        # The initial release version
    author="Raoul P. P. P. Grasman",        # Full name of the author
    author_email="R.P.P.P.Grasman@uva.nl",  # Author email
    description="Fit a simple drift diffusion model to observed sample moments",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',                # Minimum version requirement of the package
    py_modules=["EZ2"],                     # Name of the python package
    package_dir={'':'EZ2/src'},             # Directory of the source code of the package
    install_requires=[],                    # Install other dependencies if any
    url="https://github.com/raoelg/EZ2"
)

#!/usr/bin/env python3
import setuptools

#######
def get_require_modules(given_file):
    """
    Get main python requirements modules
    """
    with open(given_file, 'r') as f:
        myModules = [line.strip().split(',')[0] for line in f]
    
    return myModules

#######
def get_version(version_file):
    """
    Original code: PhiSpy setup.py 
    https://github.com/linsalrob/PhiSpy/blob/master/setup.py
    """
    with open(version_file, 'r') as f:
        v = f.readline().strip()

    return v




long_description_text = ""
with open("README.md", "r") as fh:
    long_description_text = fh.read()

setuptools.setup(
    name="HCGB",
    version=get_version("./VERSION"),

    author="Jose F. Sanchez-Herrero",
    description="Useful python functions",

    author_email="jfbioinformatics@gmail.com",

    long_description_content_type="text/markdown",
    long_description=long_description_text,

    url="https://github.com/HCGB-IGTP/HCGB_python_functions/",

    packages=setuptools.find_packages(),
    license='MIT License',

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    install_requires=get_require_modules("./HCGB/config/python_requirements.txt"),
)

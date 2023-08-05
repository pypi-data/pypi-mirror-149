import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "drona", # package name
    version = "6.0.0",
    author = "Prabir Debnath",
    author_email = "prabirdeb@gmail.com",
    description = "This is a data science related question asnwering model for the beginners",
    license = "MIT",
    url = "",
    packages= find_packages(), # searches the folder containing __init__.py file
    package_data= {'drona': ['*.csv']},  # This is used for packaging data file in the final distribution (data files must be kept in the package folder)
    install_requires= ['numpy==1.21.5','pandas==1.3.5', 'nltk==3.2.5', 'scikit-learn==1.0.2'], # 'sklearn==0.0', 'transformers==4.17.0'('re', 'string', 'io', 'pkgutil') may not be required as these are built in functions
    keywords = ["data science", "datascience", "machine learning", "deep learning"],
    long_description= read("README.txt")  # for project description readme.txt file shall be referred
    # classifiers=[
    #     "Development Status :: 3 - Alpha",
    #     "Topic :: Utilities",
    #     "License :: OSI Approved :: BSD License",
    # ],
)
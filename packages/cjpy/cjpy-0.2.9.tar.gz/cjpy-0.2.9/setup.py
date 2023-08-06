import setuptools
import re

with open("README.txt", "r") as fh:
    long_description = fh.read()

mat=re.search('Ver ([0-9.]+) by', long_description)
if not bool(mat): exit()
else: 
	version = mat.group(1)

author = "Jaesub Hong"

with open("cjpy/__init__.py", "w") as fi:
	fi.write('__version__ = "'+version+'"\n')
	fi.write('__author__  = "'+author+'"')

setuptools.setup(
    name		= "cjpy", 
    version		= version,
    author		= author, 
    author_email	= "jhong@cfa.harvard.edu",
    packages	= ['cjpy'],
    url		= "https://pypi.org/project/cjpy/"+version,

    description	   = "Command liner with JSON based input file",
    long_description = long_description,
    long_description_content_type="text/markdown",

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    install_requires=[
		'textwrap3'
	    ]
)

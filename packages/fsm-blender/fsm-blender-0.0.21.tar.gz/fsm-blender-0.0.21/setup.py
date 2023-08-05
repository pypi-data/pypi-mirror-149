import pathlib
from setuptools import setup, find_packages

VERSION = '0.0.21'
DESCRIPTION = 'Data Driven Content Creation in Blender'
LONG_DESCRIPTION = ''

with open('requirements.txt') as f:
    required = f.read().splitlines()

# Setting up
setup(
        name="fsm-blender",
        version=VERSION,
        author="Philip Paprotny",
        author_email="<philip.paprotny@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        # packages=["nlpp"],
        include_package_data=True,
        install_requires=required,
        keywords=['python', 'blender', 'datavis'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.9",
        ]
)

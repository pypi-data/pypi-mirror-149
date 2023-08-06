from setuptools import setup, find_packages

VERSION = '0.0.11'
DESCRIPTION = 'A package for matrix operations.'
LONG_DESCRIPTION = 'A package for basic linear algebra operations.'

setup(
    name="matrixmodule",
    version=VERSION,
    author="Elliott Walker",
    author_email="<22walkerelliott@gmail.com>",
    url="https://pypi.org/manage/project/matrixmodule/release/0.0.10/",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'linear algebra', 'matrices'],
    classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
    ]
)

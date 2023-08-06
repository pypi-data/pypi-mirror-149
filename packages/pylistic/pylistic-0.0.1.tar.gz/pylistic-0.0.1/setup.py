from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'A python package to handle lists'
LONG_DESCRIPTION = 'A python package to handle lists of non primitive data types, like dictionaries and lists'

# Setting up
setup(
        name="pylistic", 
        version=VERSION,
        author="Gabriel Caldas",
        author_email="gabrielgcbs97@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(exclude=['tests']),
        install_requires=[],
        setup_requires=['wheel'],
        
        keywords=['python', 'list', 'data structure'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX :: Linux",
        ]
)
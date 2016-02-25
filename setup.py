from setuptools import setup, find_packages
setup(
    name = "fontsquirrel-dl",
    version = "0.1",
    packages = find_packages(),
    py_modules = ['fontsquirrel'],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
#    install_requires = ['docutils>=0.3'],

    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        'hello': ['*.msg'],
    },

    # metadata for upload to PyPI
    author = "Víctor Fernández Rico",
    author_email = "vfrico@gmail.com",
    description = "A library to easy download fonts from Font Squirrel",
    license = "GPLv3",
    keywords = "font web fonts fontsquirrel squirrel ttf otf",
    url = "https://github.com/vfrico/fontsquirrel_dl/",   # project home page, if any

    # could also include long_description, download_url, classifiers, etc.
)

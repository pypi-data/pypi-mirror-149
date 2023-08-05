"""
A package that allows easy-to-read conversion
of a dictionary to a string and pretty printing.

VARIABLES

    __version__
        Contains the package version.

FUNCTONS

    convert(dictionary)
        Returns a dictionary with flattened elements.

    get(dictionary)
        Returns a string from the whole dictionary.

    pprint(dictionary)
        Flattens the dictionary and pretty prints.

"""

from dictppr.dictppr import get, pprint, convert

# Block access to submodule and it other functions
del locals()["dictppr"]

__version__ = "1.0.0"

'''
Module containing utility functions supporting the DLPOLY Python Workflow
'''

import math
import itertools
from abc import ABC
import shutil
import re
import glob
import numpy as np

COMMENT_CHAR = '#'


def copy_file(inpf, outd):
    """ Copy a file in a folder, avoiding same file error

    :param inpf: input file to copy
    :param outd: output directory to copy to
    """
    try:
        shutil.copy(inpf, outd)
    except shutil.SameFileError:
        pass


def next_file(filename):
    """ Get the name of the next available file

    :param filename: filename to check
    :returns: New output file name
    :rtype: str
    """
    files = glob.glob(f"{filename}*")
    if files:
        # Get last dir number
        idx = (int(re.search('([0-9]+)$', file).group(0)) for file in files
               if re.search('([0-9]+)$', file))

        new_num = max(idx, default=1) + 1

        outfile = f"{filename}{new_num}"
    else:
        outfile = f"{filename}"

    return outfile


def peek(iterable):
    """ Test generator without modifying (creates new generator)

    :param iterable: Generator to test
    :returns: Original generator
    :rtype: Generator

    """
    try:
        first = next(iterable)
    except StopIteration:
        return None
    return itertools.chain([first], iterable)


def parse_line(line):
    """ Handle comment chars and whitespace

    :param line: line to parse

    """
    return line.split(COMMENT_CHAR)[0].strip()


def read_line(in_file):
    """ Read a line, stripping comments and blank lines

    :param in_file: File to read

    """
    line = None
    for line in in_file:
        line = parse_line(line)
        if line:
            break
    else:
        line = None
    return line


def build_3d_rotation_matrix(alpha=0., beta=0., gamma=0., units="rad"):
    """ Build a rotation matrix in degrees or radians

    :param alpha: Angle XY
    :param beta:  Angle XZ
    :param gamma: Angle YZ
    :param units: Angle units "deg" or "rad"

    """
    if units == "deg":
        alpha, beta, gamma = map(lambda x: x*math.pi/180, (alpha, beta, gamma))
    salp, sbet, sgam = map(np.sin, (alpha, beta, gamma))
    calp, cbet, cgam = map(np.cos, (alpha, beta, gamma))
    matrix = np.asarray([[cbet*cgam, cgam*salp*sbet - calp*sgam, calp*cgam*sbet + salp*sgam],
                         [cbet*sgam, calp*cgam+salp*sbet*sgam, calp*sbet*sgam-cgam*salp],
                         [-1.*sbet, cbet*salp, calp*cbet]], dtype=float)
    return matrix


class DLPData(ABC):
    """ Abstract datatype for handling automatic casting and restricted assignment

     :param datatypes: Datatypes to handle as dict of "element name : dataype"
     :param strict: Whether fuzzy matching will be applied

     """

    def __init__(self, datatypes: dict, strict: bool = False):
        self._datatypes = datatypes
        self._strict = strict

    datatypes = property(lambda self: self._datatypes)
    keys = property(lambda self: [key for key in self.datatypes
                                  if key not in ("keysHandled", "_strict")])
    set_keys = property(lambda self: (key for key in self.keys if self.is_set(key)))
    className = property(lambda self: type(self).__name__)

    def dump(self):
        """ Dump keys to screen """
        for key in self.keys:
            print(key, self[key])

    @property
    def strict(self):
        """ Whether should throw if bad keys supplied """
        return self._strict

    def __setattr__(self, key, val):
        if key == "_datatypes":  # Protect datatypes

            if not hasattr(self, "_datatypes"):
                self.__dict__[key] = {**val, "keysHandled": tuple, "_strict": bool}
            else:
                raise KeyError("Cannot alter datatypes")
            return

        if key == "_strict":
            if not hasattr(self, "_strict"):
                self.__dict__[key] = val
            else:
                raise KeyError("Cannot alter strict")
            return

        if key == "source":  # source is not really a keyword
            return

        if key == "ensemble" and val is None:
            raise KeyError("Ensemble cannot be empty")

        if self.strict and key not in self.datatypes:
            raise KeyError(f"Param {key} not allowed in {self.className.lower()} definition")

        val = self._map_types(key, val)
        self.__dict__[key] = val

    def __getitem__(self, key):
        """ Fuzzy matching on get/set item """
        key = check_arg(key, *self.keys)
        return getattr(self, str(key))

    def __setitem__(self, key_in, val):
        """ Fuzzy matching on get/set item """
        if not self.strict:
            key = check_arg(key_in, *self.keys)
            if not key:
                raise KeyError(f"'{key_in}' is not a member of {type(self).__name__}")
        else:
            key = key_in
        setattr(self, key, val)

    def is_set(self, key):
        """ Check if key is set in this object

        :param key: Key to check
        """
        return key in self.__dict__

    def __iter__(self):
        return ((key, self[key]) for key in self.set_keys)

    def __add__(self, other):
        for key, val in other:
            if not self.is_set(key):
                self[key] = val

    def _map_types(self, key, vals):
        """ Map argument types to their respective types according to datatypes.

        :param key: Key to set
        :param vals: Value to convert

        """
        datatype = self._datatypes[key]
        if isinstance(vals, (tuple, list)) and \
           not isinstance(datatype, (tuple, bool)) and \
           datatype is not tuple:

            if not vals:
                pass
            elif len(vals) == 1:
                vals = vals[0]
            else:
                for arg in vals:
                    try:
                        vals = arg
                        break
                    except TypeError:
                        pass
                else:
                    raise TypeError(f"No arg of {vals} ({[type(x).__name__ for x in vals]}) "
                                    f"for key {key} valid, must be castable to {datatype.__name__}")

        if isinstance(datatype, tuple):

            if isinstance(vals, (int, float, str)):
                vals = (vals,)

            try:
                if ... in datatype:
                    loc = datatype.index(...)
                    if loc != len(datatype)-1:
                        pre, ellided, post = datatype[:loc], datatype[loc-1], datatype[loc+1:]
                        val = ([target_type(item) for item, target_type in zip(vals[:loc], pre)] +
                               [ellided(item) for item in vals[loc:-len(post)]] +
                               [target_type(item)
                                for item, target_type in zip(vals[-len(post):], post)])
                    else:
                        pre, ellided = datatype[:loc], datatype[loc-1]
                        val = ([target_type(item) for item, target_type in zip(vals[:loc], pre)] +
                               [ellided(item) for item in vals[loc:]])

                else:
                    val = [target_type(item) for item, target_type in zip(vals, datatype)]
            except TypeError as err:
                message = (f"Type of {vals} ({[type(x).__name__ for x in vals]}) not valid, "
                           f"must be castable to {[x.__name__ for x in datatype]}")

                if not self.strict:
                    print(message)
                    return None

                raise TypeError(message) from err

        elif isinstance(vals, datatype):  # Already right type
            val = vals
        elif datatype is bool:  # If present true unless explicitly false
            val = vals not in (0, False)

        else:
            try:
                val = self._datatypes[key](vals)
            except TypeError as err:
                message = (f"Type of {vals} ({type(vals).__name__}) not valid, "
                           f"must be castable to {datatype.__name__}")

                if not self.strict:
                    print(err)
                    print(message)
                    return None

                raise TypeError(message) from err

        return val


def check_arg(key, *args):
    """ Perform fuzzy match against potential arguments

    :param key: Key supplied
    :param args: Potential matching fuzzies in order of priority
    :returns: Matching key or False if not found
    """

    for arg in args:
        if key.startswith(arg):
            return arg
    return False
